import os
import time
import requests
from requests_oauthlib import OAuth1Session
from src.storage.database.database import DatabaseManager
from src.utils.logger import logger

class TwitterAPI:
    def __init__(self):
        self.db = DatabaseManager.get_instance()
        self.upload_url = 'https://upload.twitter.com/1.1/media/upload.json'
        self.tweet_url = 'https://api.twitter.com/2/tweets'
        self.platform = "twitter"

    def _get_session(self) -> OAuth1Session:
        with self.db.get_connection() as conn:
            cursor = conn.execute(
                "SELECT client_id, client_secret, access_token, refresh_token FROM api_keys WHERE platform = ?",
                (self.platform,)
            )
            row = cursor.fetchone()

        if not row or not row['client_id'] or not row['client_secret'] or not row['access_token'] or not row['refresh_token']:
            raise ValueError("X (Twitter) credentials missing. Please check API Key, API Secret, Access Token, and Access Secret in Settings.")
        
        return OAuth1Session(
            row['client_id'],
            client_secret=row['client_secret'],
            resource_owner_key=row['access_token'],
            resource_owner_secret=row['refresh_token']
        )

    def _init_upload(self, session: OAuth1Session, file_size: int, media_type: str = 'video/mp4') -> str:
        logger.info(f"Initializing Twitter upload for {file_size} bytes")
        resp = session.post(self.upload_url, data={
            'command': 'INIT',
            'total_bytes': file_size,
            'media_type': media_type,
            'media_category': 'tweet_video'
        })
        resp.raise_for_status()
        return resp.json()['media_id_string']

    def _append_chunk(self, session: OAuth1Session, media_id: str, chunk: bytes, segment_index: int):
        logger.info(f"Appending chunk {segment_index}")
        resp = session.post(self.upload_url, data={
            'command': 'APPEND',
            'media_id': media_id,
            'segment_index': segment_index
        }, files={'media': chunk})
        resp.raise_for_status()

    def _finalize_upload(self, session: OAuth1Session, media_id: str) -> dict:
        logger.info(f"Finalizing upload for media_id: {media_id}")
        resp = session.post(self.upload_url, data={
            'command': 'FINALIZE',
            'media_id': media_id
        })
        resp.raise_for_status()
        return resp.json()

    def _wait_for_processing(self, session: OAuth1Session, media_id: str):
        logger.info("Waiting for Twitter media processing...")
        for _ in range(30):
            resp = session.get(self.upload_url, params={'command': 'STATUS', 'media_id': media_id})
            resp.raise_for_status()
            info = resp.json().get('processing_info', {})
            state = info.get('state', 'succeeded')
            if state == 'succeeded':
                logger.info("Twitter media processing succeeded")
                return
            if state == 'failed':
                error_msg = info.get('error', {}).get('message', 'Unknown error')
                raise ValueError(f"Twitter media processing failed: {error_msg}")
            
            wait_secs = info.get('check_after_secs', 5)
            logger.info(f"Processing state: {state}. Waiting {wait_secs}s...")
            time.sleep(wait_secs)
            
        raise ValueError('Twitter media processing timed out.')

    def upload_video(self, video_path: str, title: str, description: str, schedule_time=None) -> str:
        if schedule_time:
            logger.warning("X (Twitter) API v2 does not support scheduled tweets. Publishing immediately.")

        session = self._get_session()
        file_size = os.path.getsize(video_path)
        
        media_id = self._init_upload(session, file_size)
        
        CHUNK_SIZE = 4 * 1024 * 1024  # 4MB
        segment_index = 0
        
        with open(video_path, 'rb') as f:
            while True:
                chunk = f.read(CHUNK_SIZE)
                if not chunk:
                    break
                self._append_chunk(session, media_id, chunk, segment_index)
                segment_index += 1
                
        self._finalize_upload(session, media_id)
        self._wait_for_processing(session, media_id)
        
        # Max tweet length is roughly 280 chars, let's truncate description to 270 safely
        tweet_text = description
        if len(tweet_text) > 270:
            tweet_text = tweet_text[:267] + "..."
            
        logger.info("Creating tweet...")
        resp = session.post(self.tweet_url, json={
            'text': tweet_text,
            'media': {'media_ids': [media_id]}
        })
        
        try:
            resp.raise_for_status()
        except requests.exceptions.HTTPError as e:
            error_msg = resp.json().get("detail", str(e))
            raise ValueError(f"Failed to post tweet: {error_msg}")
            
        tweet_id = resp.json()['data']['id']
        logger.info(f"Tweet successfully posted with ID: {tweet_id}")
        return tweet_id
