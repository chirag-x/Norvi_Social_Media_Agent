import os
import sys
import json
import httpx
import subprocess
import tempfile
import threading
from PySide6.QtCore import QObject, Signal

from src.config.version import APP_VERSION, UPDATE_CHECK_URL
from src.utils.logger import logger

class Updater(QObject):
    """
    Background service that checks GitHub for updates, downloads the latest
    installer, and launches it silently.
    """
    update_available = Signal(str, str, str) # version, notes, download_url
    download_progress = Signal(int)
    download_complete = Signal(str)
    download_error = Signal(str)
    check_error = Signal(str)
    no_update = Signal()

    _instance = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def __init__(self):
        super().__init__()
        self.is_downloading = False

    def check_for_updates(self):
        """Spawns a background thread to check the version JSON."""
        def _check():
            try:
                r = httpx.get(UPDATE_CHECK_URL, timeout=5.0)
                if r.status_code == 200:
                    data = r.json()
                    latest = data.get("latest_version")
                    url = data.get("download_url")
                    notes = data.get("release_notes", "")
                    
                    if latest and self._is_newer(latest, APP_VERSION):
                        logger.info(f"Update available: {latest}")
                        self.update_available.emit(latest, notes, url)
                    else:
                        self.no_update.emit()
                else:
                    self.check_error.emit(f"HTTP {r.status_code}")
            except Exception as e:
                logger.error(f"[updater] Check failed: {e}")
                self.check_error.emit(str(e))
                
        threading.Thread(target=_check, daemon=True).start()

    def _is_newer(self, remote: str, local: str) -> bool:
        """Parses version strings to determine if remote is newer."""
        def parse(v): 
            # Strip 'v' if present (e.g., v1.2.0 -> 1.2.0)
            return tuple(map(int, v.strip('v').split('.')))
        try:
            return parse(remote) > parse(local)
        except Exception as e:
            logger.warning(f"Version parse error: {e}")
            return False

    def download_and_install(self, download_url: str):
        """Downloads the installer to the temp folder and runs it silently."""
        if self.is_downloading: 
            return
            
        self.is_downloading = True
        
        def _download():
            try:
                temp_dir = tempfile.gettempdir()
                installer_path = os.path.join(temp_dir, "Nexus_Update.exe")
                
                with httpx.stream("GET", download_url, follow_redirects=True) as r:
                    r.raise_for_status()
                    total = int(r.headers.get("content-length", 0))
                    downloaded = 0
                    
                    with open(installer_path, "wb") as f:
                        for chunk in r.iter_bytes(chunk_size=8192):
                            f.write(chunk)
                            downloaded += len(chunk)
                            if total:
                                progress = int((downloaded / total) * 100)
                                self.download_progress.emit(progress)
                                
                self.download_complete.emit(installer_path)
                logger.info(f"Download complete. Launching installer: {installer_path}")
                
                # Launch installer silently and quit this application
                # /SILENT is standard for InnoSetup
                subprocess.Popen([installer_path, "/SILENT"])
                os._exit(0)
                
            except Exception as e:
                logger.error(f"[updater] Download failed: {e}")
                self.download_error.emit(str(e))
                self.is_downloading = False
                
        threading.Thread(target=_download, daemon=True).start()
