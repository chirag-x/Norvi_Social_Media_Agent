import os
import time
from pathlib import Path
from src.utils.logger import logger

def run_auto_cleanup(days: int = 15):
    """
    Deletes media files in 'sources' and 'outputs' that are older than `days`.
    """
    try:
        now = time.time()
        cutoff = now - (days * 86400)
        
        folders_to_clean = ["sources", "outputs"]
        deleted_count = 0
        freed_bytes = 0
        
        for folder_name in folders_to_clean:
            folder_path = Path(folder_name)
            if not folder_path.exists():
                continue
                
            for file_path in folder_path.iterdir():
                if file_path.is_file() and file_path.suffix.lower() in [".mp4", ".wav", ".mkv", ".webm"]:
                    # Check modification time
                    mtime = file_path.stat().st_mtime
                    if mtime < cutoff:
                        size = file_path.stat().st_size
                        try:
                            file_path.unlink()
                            deleted_count += 1
                            freed_bytes += size
                            logger.info(f"[Cleanup] Deleted old file: {file_path.name}")
                        except Exception as e:
                            logger.warning(f"[Cleanup] Could not delete {file_path.name}: {e}")
                            
        if deleted_count > 0:
            logger.info(f"[Cleanup] Auto-cleanup removed {deleted_count} files, freeing {freed_bytes / (1024*1024):.2f} MB.")
            
    except Exception as e:
        logger.error(f"[Cleanup] Error running auto-cleanup: {e}")
