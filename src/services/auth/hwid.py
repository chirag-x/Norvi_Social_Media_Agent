import uuid
import platform
from src.utils.logger import logger


def get_hardware_id() -> str:
    """
    Generates a hardware identifier for the current machine that is compatible
    with the NORVI Agency authentication system (norvi_gatekeeper.py).

    Format: "{hostname}-{mac_address_integer}"
    This matches the exact format used across all NORVI agents so the backend
    can track hardware consistently regardless of which agent is installed.
    """
    mac = uuid.getnode()
    hwid = f"{platform.node()}-{mac}"
    logger.debug(f"Generated Hardware ID: {hwid[:16]}...")
    return hwid
