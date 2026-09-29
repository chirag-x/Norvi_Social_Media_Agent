import os
import json
import requests
from datetime import datetime

from src.storage.database.database import DatabaseManager
from src.utils.logger import logger

GRAPH_API_BASE = "https://graph.facebook.com/v19.0"
CHUNK_SIZE = 10 * 1024 * 1024  # 10 MB


class FacebookAPI:
    """Handles Facebook video / Reels uploads via the Graph API."""

    def __init__(self):
        self.db = DatabaseManager()

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _get_credentials(self) -> dict:
        """Fetch Facebook credentials from the api_keys table.

        Returns a dict with keys: client_id, client_secret, access_token,
        refresh_token (page_id, may be None).

        Raises:
            ValueError: If the access_token (Page Access Token) is missing.
        """
        creds = self.db.get_api_keys("facebook")
        if not creds:
            raise ValueError(
                "No Facebook credentials found in the database. "
                "Please add them via Settings."
            )
        if not creds.get("access_token"):
            raise ValueError(
                "Facebook Page Access Token is missing. "
                "Please provide it in Settings."
            )
        return creds

    def _get_page_id(self, access_token: str) -> str:
        """Retrieve the Facebook Page ID for the given access token.

        Makes a GET request to /me?fields=id to obtain the page/user ID,
        then caches it in the refresh_token column of api_keys.

        Args:
            access_token: A valid Facebook Page Access Token.

        Returns:
            The page/user ID as a string.

        Raises:
            ValueError: If the API returns an error response.
        """
        url = f"{GRAPH_API_BASE}/me"
        params = {"fields": "id", "access_token": access_token}

        logger.info("Fetching Facebook Page ID from Graph API...")
        response = requests.get(url, params=params, timeout=30)
        data = response.json()

        if "error" in data:
            error = data["error"]
            raise ValueError(
                f"Facebook API error while fetching page ID: "
                f"[{error.get('code')}] {error.get('message')}"
            )

        page_id: str = data["id"]
        logger.info(f"Fetched Facebook Page ID: {page_id}")

        # Cache page_id in the refresh_token column
        self.db.update_api_keys(
            platform="facebook",
            refresh_token=page_id,
        )
        logger.debug("Cached Facebook Page ID to database (refresh_token column).")

        return page_id

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def upload_video(
        self,
        video_path: str,
        title: str,
        description: str,
        schedule_time: datetime = None,
    ) -> str:
        """Upload a video to a Facebook Page using the Resumable Upload API.

        The upload consists of three phases:
          1. **start**    – Initialise the upload session and get upload_session_id.
          2. **transfer** – Send the video in 10 MB chunks.
          3. **finish**   – Commit the upload with metadata and publish settings.

        Args:
            video_path:    Absolute or relative path to the local video file.
            title:         Title of the video post.
            description:   Description / caption of the video post.
            schedule_time: Optional future datetime to schedule the post.
                           If None or in the past, the video is published immediately.

        Returns:
            The video ID string returned by Facebook on a successful finish.

        Raises:
            FileNotFoundError: If video_path does not exist.
            ValueError:        On any Facebook API error response.
        """
        if not os.path.exists(video_path):
            raise FileNotFoundError(f"Video file not found: {video_path}")

        # ── Credentials ────────────────────────────────────────────────
        creds = self._get_credentials()
        access_token: str = creds["access_token"]

        # ── Page ID ────────────────────────────────────────────────────
        page_id: str = creds.get("refresh_token") or self._get_page_id(access_token)
        logger.info(f"Using Facebook Page ID: {page_id}")

        file_size = os.path.getsize(video_path)
        endpoint = f"{GRAPH_API_BASE}/{page_id}/videos"

        # ── Phase 1: Start ─────────────────────────────────────────────
        logger.info(
            f"[Facebook Upload] Phase 1 – Initialising upload session "
            f"(file size: {file_size} bytes)..."
        )
        start_response = requests.post(
            endpoint,
            params={
                "access_token": access_token,
                "upload_phase": "start",
                "file_size": file_size,
            },
            timeout=60,
        )
        start_data = start_response.json()

        if "error" in start_data:
            error = start_data["error"]
            raise ValueError(
                f"Facebook API error (start phase): "
                f"[{error.get('code')}] {error.get('message')}"
            )

        upload_session_id: str = start_data["upload_session_id"]
        start_offset: int = int(start_data["start_offset"])
        logger.info(
            f"[Facebook Upload] Session ID: {upload_session_id}, "
            f"start_offset: {start_offset}"
        )

        # ── Phase 2: Transfer (chunked) ────────────────────────────────
        logger.info("[Facebook Upload] Phase 2 – Transferring video chunks...")
        with open(video_path, "rb") as video_file:
            chunk_number = 0
            while True:
                video_file.seek(start_offset)
                chunk = video_file.read(CHUNK_SIZE)
                if not chunk:
                    break

                chunk_number += 1
                end_offset_expected = start_offset + len(chunk)
                logger.debug(
                    f"[Facebook Upload] Sending chunk {chunk_number}: "
                    f"bytes {start_offset}–{end_offset_expected - 1}"
                )

                transfer_response = requests.post(
                    endpoint,
                    params={
                        "access_token": access_token,
                        "upload_phase": "transfer",
                        "upload_session_id": upload_session_id,
                        "start_offset": start_offset,
                    },
                    files={"video_file_chunk": chunk},
                    timeout=120,
                )
                transfer_data = transfer_response.json()

                if "error" in transfer_data:
                    error = transfer_data["error"]
                    raise ValueError(
                        f"Facebook API error (transfer phase, chunk {chunk_number}): "
                        f"[{error.get('code')}] {error.get('message')}"
                    )

                end_offset = int(transfer_data["end_offset"])
                logger.debug(
                    f"[Facebook Upload] Chunk {chunk_number} accepted. "
                    f"Next start_offset: {end_offset}"
                )

                if end_offset >= file_size:
                    logger.info(
                        "[Facebook Upload] All chunks transferred successfully."
                    )
                    break

                start_offset = end_offset

        # ── Phase 3: Finish ────────────────────────────────────────────
        logger.info("[Facebook Upload] Phase 3 – Finishing upload and setting metadata...")

        finish_data = {
            "title": title,
            "description": description,
        }

        now = datetime.now()
        if schedule_time and isinstance(schedule_time, datetime) and schedule_time > now:
            finish_data["scheduled_publish_time"] = int(schedule_time.timestamp())
            finish_data["published"] = "false"
            logger.info(
                f"[Facebook Upload] Scheduling post for: {schedule_time.isoformat()}"
            )
        else:
            finish_data["published"] = "true"
            logger.info("[Facebook Upload] Publishing immediately.")

        finish_response = requests.post(
            endpoint,
            params={
                "access_token": access_token,
                "upload_phase": "finish",
                "upload_session_id": upload_session_id,
            },
            data=finish_data,
            timeout=60,
        )
        finish_result = finish_response.json()

        if "error" in finish_result:
            error = finish_result["error"]
            raise ValueError(
                f"Facebook API error (finish phase): "
                f"[{error.get('code')}] {error.get('message')}"
            )

        video_id: str = finish_result.get("video_id") or finish_result.get("id", "")
        logger.info(
            f"[Facebook Upload] Video uploaded successfully! Video ID: {video_id}"
        )
        return video_id
