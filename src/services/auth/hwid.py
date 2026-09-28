import subprocess
import hashlib
import uuid
import platform
from src.utils.logger import logger

def get_hardware_id() -> str:
    """
    Generates a stable, unique hardware identifier for the current machine.
    Primary method: Windows CSPRODUCT UUID.
    Fallback method: MAC address (uuid.getnode()).
    """
    hwid = ""
    
    if platform.system() == "Windows":
        try:
            # Run wmic to get the machine's UUID
            result = subprocess.run(
                ["wmic", "csproduct", "get", "uuid"],
                capture_output=True,
                text=True,
                check=True
            )
            # The output has a header "UUID", we want the second line
            lines = result.stdout.strip().split("\n")
            if len(lines) >= 2:
                hwid = lines[1].strip()
        except Exception as e:
            logger.warning(f"Failed to get Windows UUID via wmic: {e}")
            
    # Fallback if Windows method fails or we are not on Windows
    if not hwid:
        logger.info("Using MAC address fallback for hardware ID.")
        mac = uuid.getnode()
        hwid = str(mac)
        
    # Hash the resulting string to ensure a consistent, clean format
    hash_obj = hashlib.sha256(hwid.encode('utf-8'))
    final_hwid = hash_obj.hexdigest()
    
    logger.debug(f"Generated Hardware ID: {final_hwid}")
    return final_hwid
