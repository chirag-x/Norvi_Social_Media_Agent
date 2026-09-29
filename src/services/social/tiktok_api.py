import os
import time
import math
import requests
import json
from src.storage.database.database import DatabaseManager
from src.utils.logger import logger

class TikTokAPI:
    def __init__(self):
        self.db = DatabaseManager.get_instance()
        self.platform = "tiktok"

    def _get_access_token(self) -> str:
        with self.db.get_connection() as conn:
            cursor = conn.execute(
                "SELECT access_token FROM api_keys WHERE platform = ?",
                (self.platform,)
            )
            row = cursor.fetchone()
            
        if not row or not row['access_token']:
            raise ValueError("TikTok account not authenticated. Please authenticate in Settings.")
        return row['access_token']

    def upload_video(self, video_path: str, title: str, description: str, schedule_time=None) -> str:
        access_token = self._get_access_token()
        
        file_size = os.path.getsize(video_path)
        CHUNK_SIZE = 10 * 1024 * 1024  # 10MB
        total_chunks = math.ceil(file_size / CHUNK_SIZE)
        
        # Max title length is 2200
        full_title = f"{title}\n{description}"
        if len(full_title) > 2200:
            full_title = full_title[:2197] + "..."
            
        logger.info("Initializing TikTok upload...")
        init_url = "https://open.tiktokapis.com/v2/post/publish/video/init/"
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json; charset=UTF-8"
        }
        body = {
            "post_info": {
                "title": full_title,
                "privacy_level": "SELF_ONLY",
                "disable_duet": False,
                "disable_stitch": False,
                "disable_comment": False
            },
            "source_info": {
                "source": "FILE_UPLOAD",
                "video_size": file_size,
                "chunk_size": CHUNK_SIZE,
                "total_chunk_count": total_chunks
            }
        }
        
        resp = requests.post(init_url, headers=headers, json=body)
        
        # Check for permission errors
        if resp.status_code == 403 or resp.json().get("error", {}).get("code") == "permission_denied":
            raise ValueError("TikTok Content Posting API access not approved. Please apply at developers.tiktok.com.")
            
        try:
            resp.raise_for_status()
        except requests.exceptions.HTTPError as e:
            err = resp.json().get("error", {}).get("message", str(e))
            raise ValueError(f"Failed to initialize TikTok upload: {err}")
            
        data = resp.json().get("data", {})
        publish_id = data.get("publish_id")
        upload_url = data.get("upload_url")
        
        if not publish_id or not upload_url:
            raise ValueError("Failed to get publish_id or upload_url from TikTok API.")
            
        logger.info(f"Uploading {total_chunks} chunks to TikTok...")
        with open(video_path, 'rb') as f:
            for i in range(total_chunks):
                chunk = f.read(CHUNK_SIZE)
                start = i * CHUNK_SIZE
                end = start + len(chunk)
                
                chunk_headers = {
                    "Content-Range": f"bytes {start}-{end-1}/{file_size}",
                    "Content-Length": str(len(chunk)),
                    "Content-Type": "video/mp4"
                }
                
                logger.info(f"Uploading TikTok chunk {i+1}/{total_chunks}")
                put_resp = requests.put(upload_url, headers=chunk_headers, data=chunk)
                
                try:
                    put_resp.raise_for_status()
                except requests.exceptions.HTTPError as e:
                    raise ValueError(f"Failed to upload chunk {i+1}: {e}")
                    
        logger.info("TikTok upload complete. Polling for processing status...")
        
        status_url = "https://open.tiktokapis.com/v2/post/publish/status/fetch/"
        status_headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
        
        for _ in range(24):
            status_resp = requests.post(status_url, headers=status_headers, json={"publish_id": publish_id})
            status_resp.raise_for_status()
            
            status_data = status_resp.json().get("data", {})
            status = status_data.get("status")
            
            if status == "PUBLISH_COMPLETE":
                logger.info(f"TikTok publish successful: {publish_id}")
                return publish_id
            elif status == "FAILED":
                fail_reason = status_data.get("fail_reason", "Unknown failure")
                raise ValueError(f"TikTok publish failed: {fail_reason}")
                
            logger.info(f"TikTok processing status: {status}. Waiting 5s...")
            time.sleep(5)
            
        raise ValueError("TikTok media processing timed out.")
