import asyncio
import threading
import time
from datetime import datetime
from src.storage.database.database import DatabaseManager
from src.utils.logger import logger

class PublishingDaemon:
    """
    Background worker that constantly scans the database for scheduled posts.
    Handles the 'Hybrid' scheduling logic:
    - YouTube/Facebook: Uploads immediately with a publishAt future timestamp.
    - TikTok/X/IG: Waits until the exact timestamp to upload.
    """
    _instance = None
    
    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = PublishingDaemon()
        return cls._instance

    def __init__(self):
        self.db = DatabaseManager.get_instance()
        self._is_running = False
        self._thread = None
        self.native_platforms = ["YouTube Shorts", "Facebook"]

    def start(self):
        if self._is_running:
            return
        self._is_running = True
        self._thread = threading.Thread(target=self._run_loop, daemon=True, name="PublishingDaemon")
        self._thread.start()
        logger.info("Auto-Publishing Hybrid Daemon started.")

    def stop(self):
        self._is_running = False
        if self._thread:
            self._thread.join(timeout=2.0)

    def _run_loop(self):
        while self._is_running:
            try:
                self._check_queue()
            except Exception as e:
                logger.error(f"Daemon Error: {e}")
            
            # Check queue every 30 seconds
            time.sleep(30)

    def _check_queue(self):
        with self.db.get_connection() as conn:
            cursor = conn.execute("SELECT * FROM scheduled_posts WHERE status = 'PENDING'")
            posts = cursor.fetchall()

        now = datetime.now()
        
        for post in posts:
            post_id = post["id"]
            platforms_str = post["platforms"]
            schedule_time_str = post["schedule_time"]
            video_path = post["video_path"]
            
            schedule_time = datetime.strptime(schedule_time_str, "%Y-%m-%d %H:%M:%S")
            platforms = [p.strip() for p in platforms_str.split(",")]
            
            # Check if this post requires immediate native upload or waiting
            for platform in platforms:
                if platform in self.native_platforms:
                    # Native scheduling: upload immediately with a future timestamp!
                    logger.info(f"Daemon: Found Native-Scheduled task {post_id} for {platform}.")
                    self._dispatch_upload(post, platform, schedule_time, is_native=True)
                else:
                    # Local scheduling: wait until the exact minute!
                    if now >= schedule_time:
                        logger.info(f"Daemon: Time reached for Local-Scheduled task {post_id} for {platform}.")
                        self._dispatch_upload(post, platform, schedule_time, is_native=False)
                        
    def _dispatch_upload(self, post, platform, schedule_time, is_native):
        # Update status to PUBLISHING...
        post_id = post["id"]
        with self.db.get_connection() as conn:
            conn.execute("UPDATE scheduled_posts SET status = 'PUBLISHING...' WHERE id = ?", (post_id,))
            conn.commit()
            
        logger.info(f"Daemon -> Dispatching {platform} upload for Video {post_id}")
        
        try:
            video_path = post["video_path"]
            title = post["title"]
            description = post["description"]
            
            external_id = None
            
            # Map platform strings to API classes
            if platform == "YouTube Shorts":
                from src.services.social.youtube_api import YouTubeAPI
                api = YouTubeAPI()
                tags = [] # Could extract hashtags from description here
                external_id = api.upload_video(video_path, title, description, tags, schedule_time if is_native else None)
                
            elif platform == "TikTok":
                from src.services.social.tiktok_api import TikTokAPI
                api = TikTokAPI()
                external_id = api.upload_video(video_path, title, description, None)
                
            elif platform == "Instagram Reels":
                from src.services.social.instagram_api import InstagramAPI
                api = InstagramAPI()
                external_id = api.upload_video(video_path, title, description, None)
                
            elif platform == "Facebook":
                from src.services.social.facebook_api import FacebookAPI
                api = FacebookAPI()
                external_id = api.upload_video(video_path, title, description, schedule_time if is_native else None)
                
            elif platform == "X (Twitter)":
                from src.services.social.twitter_api import TwitterAPI
                api = TwitterAPI()
                external_id = api.upload_video(video_path, title, description, None)
                
            else:
                raise ValueError(f"Unknown platform '{platform}'")
            
            # When successful
            new_status = "NATIVE_SCHEDULED" if is_native else "PUBLISHED"
            
            with self.db.get_connection() as conn:
                conn.execute(
                    "UPDATE scheduled_posts SET status = ?, external_post_id = ? WHERE id = ?",
                    (new_status, str(external_id) if external_id else None, post_id)
                )
                conn.commit()
                
            logger.info(f"Daemon -> Successfully processed task {post_id} ({new_status})")
            
        except Exception as e:
            logger.error(f"Upload failed for task {post_id} ({platform}): {e}")
            with self.db.get_connection() as conn:
                conn.execute("UPDATE scheduled_posts SET status = 'FAILED' WHERE id = ?", (post_id,))
                conn.commit()
