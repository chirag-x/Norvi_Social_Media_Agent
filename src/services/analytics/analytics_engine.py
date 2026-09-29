import json
import logging
from typing import Dict

from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

from src.storage.database.database import DatabaseManager

logger = logging.getLogger(__name__)

class AnalyticsEngine:
    def __init__(self):
        self.db = DatabaseManager.get_instance()
        self.platform = "youtube"
        self.scopes = ['https://www.googleapis.com/auth/youtube.upload']

    def _get_youtube_client(self):
        row = self.db.get_api_keys(self.platform)
        
        if not row or not row.get('refresh_token'):
            raise ValueError("YouTube account is not authenticated.")

        creds = Credentials.from_authorized_user_info(
            json.loads(row['refresh_token']), self.scopes
        )

        if creds.expired and creds.refresh_token:
            creds.refresh(Request())
            self.db.update_api_keys(self.platform, creds.to_json())

        return build('youtube', 'v3', credentials=creds)

    def fetch_youtube_stats(self) -> dict:
        """Fetch real stats for YouTube from the database and API."""
        try:
            with self.db.get_connection() as conn:
                cursor = conn.execute(
                    "SELECT external_post_id FROM scheduled_posts WHERE platform = 'youtube' AND external_post_id IS NOT NULL"
                )
                rows = cursor.fetchall()
            
            video_ids = [row['external_post_id'] for row in rows if row['external_post_id']]
            
            if not video_ids:
                return {'views': 0, 'likes': 0}

            youtube = self._get_youtube_client()
            total_views = 0
            total_likes = 0

            # Batch them into 50s as YouTube API has a max limit of 50 ids per request
            for i in range(0, len(video_ids), 50):
                batch_ids = video_ids[i:i+50]
                request = youtube.videos().list(
                    part="statistics",
                    id=",".join(batch_ids)
                )
                response = request.execute()

                for item in response.get('items', []):
                    stats = item.get('statistics', {})
                    total_views += int(stats.get('viewCount', 0))
                    total_likes += int(stats.get('likeCount', 0))

            return {'views': total_views, 'likes': total_likes}
        except Exception as e:
            logger.error(f"Error fetching YouTube stats: {e}")
            return {'views': 0, 'likes': 0}

    def fetch_all_stats(self) -> Dict[str, Dict[str, int]]:
        """Fetch stats for all platforms."""
        return {
            'youtube': self.fetch_youtube_stats(),
            'tiktok': {'views': 0, 'likes': 0},
            'instagram': {'views': 0, 'likes': 0},
            'facebook': {'views': 0, 'likes': 0},
            'twitter': {'views': 0, 'likes': 0},
        }
