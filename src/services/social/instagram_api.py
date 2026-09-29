import os
import time
import requests

from src.storage.database.database import DatabaseManager
from src.utils.logger import logger


class InstagramAPI:
    """Handles Instagram Reels uploads via the Instagram Graph API (resumable upload flow)."""

    def __init__(self):
        self.db = DatabaseManager()
        self.base_url = "https://graph.facebook.com/v19.0"

    # ------------------------------------------------------------------
    # Credentials
    # ------------------------------------------------------------------

    def _get_credentials(self) -> tuple[str, str | None]:
        """Fetch Instagram credentials from the database.

        Returns:
            (access_token, ig_account_id)  — ig_account_id may be None if not
            yet cached.

        Raises:
            ValueError: if no access_token is stored for Instagram.
        """
        row = self.db.fetch_one(
            "SELECT access_token, refresh_token FROM api_keys WHERE platform = 'instagram'"
        )
        if not row or not row[0]:
            raise ValueError(
                "Instagram access_token is missing. "
                "Please add it in Settings → API Keys."
            )
        access_token: str = row[0]
        ig_account_id: str | None = row[1] if row[1] else None
        return access_token, ig_account_id

    # ------------------------------------------------------------------
    # IG Business Account resolution
    # ------------------------------------------------------------------

    def _get_ig_account_id(self, access_token: str) -> str:
        """Resolve the Instagram Business Account ID linked to the user's
        Facebook Pages and cache it in the ``refresh_token`` column.

        Args:
            access_token: A long-lived User/Page Access Token.

        Returns:
            The Instagram Business Account ID (string).

        Raises:
            ValueError: if no Instagram Business Account is linked, or if the
            API returns an error.
        """
        logger.info("Fetching Facebook Pages to resolve Instagram Business Account…")

        # Step A – list pages accessible to the user
        pages_url = f"{self.base_url}/me/accounts"
        pages_resp = requests.get(pages_url, params={"access_token": access_token}, timeout=30)
        pages_data = pages_resp.json()

        if "error" in pages_data:
            raise ValueError(
                f"Failed to fetch Facebook Pages: {pages_data['error'].get('message', pages_data['error'])}"
            )

        pages = pages_data.get("data", [])
        if not pages:
            raise ValueError(
                "No Facebook Pages found for this access token. "
                "Make sure the token has the 'pages_show_list' permission."
            )

        # Step B – for each page, look for a linked IG Business Account
        for page in pages:
            page_id = page.get("id")
            page_token = page.get("access_token", access_token)

            ig_url = f"{self.base_url}/{page_id}"
            ig_resp = requests.get(
                ig_url,
                params={
                    "fields": "instagram_business_account",
                    "access_token": page_token,
                },
                timeout=30,
            )
            ig_data = ig_resp.json()

            if "error" in ig_data:
                logger.warning(
                    "Could not fetch IG account for page %s: %s",
                    page_id,
                    ig_data["error"].get("message", ig_data["error"]),
                )
                continue

            ig_account = ig_data.get("instagram_business_account")
            if ig_account and ig_account.get("id"):
                ig_account_id: str = ig_account["id"]
                logger.info("Found Instagram Business Account ID: %s", ig_account_id)

                # Cache in DB so we don't need to resolve again
                self.db.execute(
                    "UPDATE api_keys SET refresh_token = ? WHERE platform = 'instagram'",
                    (ig_account_id,),
                )
                logger.debug("Cached Instagram Business Account ID in database.")
                return ig_account_id

        raise ValueError(
            "No Instagram Business Account linked to this Facebook Page. "
            "Make sure your Instagram account is set to Business/Creator and "
            "connected to a Facebook Page."
        )

    # ------------------------------------------------------------------
    # Upload
    # ------------------------------------------------------------------

    def upload_video(
        self,
        video_path: str,
        title: str,
        description: str,
        schedule_time=None,  # noqa: ARG002  — scheduling not supported via API
    ) -> str:
        """Upload a video as an Instagram Reel using the resumable upload flow.

        Note:
            Instagram does **not** support native scheduling via the Graph API
            for Reels without Content Publishing API approval, so ``schedule_time``
            is accepted for interface compatibility but ignored — the Reel is
            always published immediately.

        Args:
            video_path:    Absolute (or relative) path to the local video file.
            title:         Reel title (used for logging; Instagram captions are
                           set via ``description``).
            description:   Caption for the Reel.
            schedule_time: Ignored (see note above).

        Returns:
            The published Instagram media ID (string).

        Raises:
            FileNotFoundError: if ``video_path`` does not exist.
            ValueError:        on any API-level error.
        """
        if not os.path.isfile(video_path):
            raise FileNotFoundError(f"Video file not found: {video_path}")

        file_size = os.path.getsize(video_path)
        logger.info(
            "Starting Instagram Reels upload — title=%r, file=%s (%d bytes)",
            title,
            video_path,
            file_size,
        )

        # ----------------------------------------------------------------
        # Resolve credentials
        # ----------------------------------------------------------------
        access_token, ig_account_id = self._get_credentials()

        if not ig_account_id:
            logger.info("Instagram Business Account ID not cached — fetching from API…")
            ig_account_id = self._get_ig_account_id(access_token)

        # ----------------------------------------------------------------
        # Step 1 – Initialize resumable upload session
        # ----------------------------------------------------------------
        logger.info("Step 1/4 — Initialising Instagram media container…")

        init_url = f"{self.base_url}/{ig_account_id}/media"
        init_resp = requests.post(
            init_url,
            params={"access_token": access_token},
            json={
                "media_type": "REELS",
                "upload_type": "resumable",
                "caption": description,
            },
            timeout=30,
        )
        init_data = init_resp.json()

        if "error" in init_data:
            raise ValueError(
                f"Failed to initialise upload session: {init_data['error'].get('message', init_data['error'])}"
            )

        container_id: str = init_data.get("id") or init_data.get("container_id")
        upload_url: str = init_data.get("upload_url", "")

        if not container_id:
            raise ValueError(
                f"Unexpected response from container creation — no 'id' found: {init_data}"
            )
        if not upload_url:
            raise ValueError(
                f"Unexpected response from container creation — no 'upload_url' found: {init_data}"
            )

        logger.info("Container created — id=%s", container_id)

        # ----------------------------------------------------------------
        # Step 2 – Upload video bytes (resumable PUT)
        # ----------------------------------------------------------------
        logger.info("Step 2/4 — Uploading video bytes to resumable endpoint…")

        with open(video_path, "rb") as video_file:
            video_bytes = video_file.read()

        upload_headers = {
            "Authorization": f"OAuth {access_token}",
            "offset": "0",
            "file_size": str(file_size),
        }
        upload_resp = requests.put(
            upload_url,
            headers=upload_headers,
            data=video_bytes,
            timeout=300,  # large file uploads may take a while
        )

        if not upload_resp.ok:
            try:
                err_msg = upload_resp.json().get("error", {}).get("message", upload_resp.text)
            except Exception:
                err_msg = upload_resp.text
            raise ValueError(f"Video upload failed (HTTP {upload_resp.status_code}): {err_msg}")

        logger.info("Video bytes uploaded successfully.")

        # ----------------------------------------------------------------
        # Step 3 – Poll until container status is FINISHED
        # ----------------------------------------------------------------
        logger.info("Step 3/4 — Waiting for media container to finish processing…")

        status_url = f"{self.base_url}/{container_id}"
        max_attempts = 30
        poll_interval = 2  # seconds

        for attempt in range(1, max_attempts + 1):
            status_resp = requests.get(
                status_url,
                params={"fields": "status_code", "access_token": access_token},
                timeout=30,
            )
            status_data = status_resp.json()

            if "error" in status_data:
                raise ValueError(
                    f"Error polling container status: {status_data['error'].get('message', status_data['error'])}"
                )

            status_code: str = status_data.get("status_code", "")
            logger.debug(
                "Container status poll %d/%d — status_code=%s",
                attempt,
                max_attempts,
                status_code,
            )

            if status_code == "FINISHED":
                logger.info("Container is ready (FINISHED).")
                break
            elif status_code == "ERROR":
                raise ValueError(
                    f"Instagram media container entered ERROR state for container_id={container_id}. "
                    "The video may be in an unsupported format or codec."
                )
            elif attempt == max_attempts:
                raise ValueError(
                    f"Timed out waiting for Instagram container to become FINISHED "
                    f"(last status_code={status_code!r}). "
                    "Try again later or check the video format."
                )

            time.sleep(poll_interval)

        # ----------------------------------------------------------------
        # Step 4 – Publish the Reel
        # ----------------------------------------------------------------
        logger.info("Step 4/4 — Publishing Reel…")

        publish_url = f"{self.base_url}/{ig_account_id}/media_publish"
        publish_resp = requests.post(
            publish_url,
            params={
                "creation_id": container_id,
                "access_token": access_token,
            },
            timeout=30,
        )
        publish_data = publish_resp.json()

        if "error" in publish_data:
            raise ValueError(
                f"Failed to publish Reel: {publish_data['error'].get('message', publish_data['error'])}"
            )

        media_id: str = publish_data.get("id", "")
        if not media_id:
            raise ValueError(
                f"Unexpected publish response — no media 'id' returned: {publish_data}"
            )

        logger.info(
            "Instagram Reel published successfully — media_id=%s, title=%r",
            media_id,
            title,
        )
        return media_id
