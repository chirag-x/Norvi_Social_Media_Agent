import os
import json
import logging
from datetime import datetime, timezone
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from src.storage.database.database import DatabaseManager

logger = logging.getLogger(__name__)

SCOPES = ['https://www.googleapis.com/auth/youtube.upload']


class YouTubeAPI:
    def __init__(self):
        self.db = DatabaseManager.get_instance()
        self.platform = "youtube"

    def authenticate(self):
        with self.db.get_connection() as conn:
            cursor = conn.execute(
                "SELECT client_id, client_secret FROM api_keys WHERE platform = ?",
                (self.platform,)
            )
            row = cursor.fetchone()
        if not row or not row['client_id'] or not row['client_secret']:
            raise ValueError("YouTube Client ID or Client Secret not found in the database.")
        client_id = row['client_id']
        client_secret = row['client_secret']
        client_config = {
            "installed": {
                "client_id": client_id,
                "client_secret": client_secret,
                "project_id": "nexus",
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
                "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
                "redirect_uris": ["http://localhost"]
            }
        }
        flow = InstalledAppFlow.from_client_config(client_config, SCOPES)
        creds = flow.run_local_server(port=0)
        creds_json = creds.to_json()
        with self.db.get_connection() as conn:
            conn.execute(
                "UPDATE api_keys SET refresh_token = ? WHERE platform = ?",
                (creds_json, self.platform)
            )
            conn.commit()
        return "Successfully authenticated with YouTube!"

    def upload_video(
        self,
        video_path: str,
        title: str,
        description: str,
        tags: list,
        schedule_time: datetime = None,
    ) -> str:
        """Upload a video to YouTube.

        Args:
            video_path: Local path to the video file.
            title: Video title.
            description: Video description.
            tags: List of tag strings.
            schedule_time: Optional datetime (timezone-aware or naive UTC) for
                scheduled publishing. When provided and in the future the video
                is kept private and ``publishAt`` is set. When ``None`` the
                video is uploaded immediately as private.

        Returns:
            The YouTube video ID of the uploaded video.

        Raises:
            ValueError: If the account is not authenticated or credentials are
                missing.
        """
        from googleapiclient.http import MediaFileUpload

        # ------------------------------------------------------------------
        # 1. Load stored credentials
        # ------------------------------------------------------------------
        with self.db.get_connection() as conn:
            cursor = conn.execute(
                "SELECT refresh_token FROM api_keys WHERE platform = ?",
                (self.platform,)
            )
            row = cursor.fetchone()

        if not row or not row['refresh_token']:
            raise ValueError("YouTube account is not authenticated.")

        creds = Credentials.from_authorized_user_info(
            json.loads(row['refresh_token']), SCOPES
        )

        # ------------------------------------------------------------------
        # 2. Refresh the access token if it has expired
        # ------------------------------------------------------------------
        if creds.expired and creds.refresh_token:
            logger.info("YouTube access token expired — refreshing...")
            creds.refresh(Request())
            # Persist the refreshed credentials so future calls don't need to
            # re-authenticate.
            with self.db.get_connection() as conn:
                conn.execute(
                    "UPDATE api_keys SET refresh_token = ? WHERE platform = ?",
                    (creds.to_json(), self.platform)
                )
                conn.commit()
            logger.info("YouTube access token refreshed and saved.")

        # ------------------------------------------------------------------
        # 3. Build the request body
        # ------------------------------------------------------------------
        status_body = {
            'privacyStatus': 'private',
            'selfDeclaredMadeForKids': False,
        }

        if schedule_time is not None:
            # Normalise to UTC-aware datetime
            if schedule_time.tzinfo is None:
                schedule_time = schedule_time.replace(tzinfo=timezone.utc)

            now_utc = datetime.now(timezone.utc)
            if schedule_time > now_utc:
                publish_at = schedule_time.astimezone(timezone.utc).strftime(
                    '%Y-%m-%dT%H:%M:%SZ'
                )
                status_body['publishAt'] = publish_at
                logger.info("Video scheduled for publication at %s (UTC).", publish_at)
            else:
                logger.warning(
                    "Provided schedule_time %s is not in the future — "
                    "uploading immediately as private.",
                    schedule_time,
                )

        body = {
            'snippet': {
                'title': title,
                'description': description,
                'tags': tags,
                'categoryId': '24',
            },
            'status': status_body,
        }

        # ------------------------------------------------------------------
        # 4. Build YouTube client and initiate resumable upload
        # ------------------------------------------------------------------
        youtube = build('youtube', 'v3', credentials=creds)

        media = MediaFileUpload(video_path, chunksize=256 * 1024, resumable=True)
        request = youtube.videos().insert(
            part=",".join(body.keys()),
            body=body,
            media_body=media,
        )

        # ------------------------------------------------------------------
        # 5. Execute chunked upload with progress logging
        # ------------------------------------------------------------------
        logger.info("Starting YouTube upload: '%s'", title)
        response = None
        while response is None:
            status, response = request.next_chunk()
            if status:
                progress = int(status.progress() * 100)
                logger.info("Upload progress: %d%%", progress)

        video_id = response.get("id")
        logger.info("Upload complete. YouTube video ID: %s", video_id)
        return video_id
