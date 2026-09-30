import os
import json
import time
from typing import Optional
from src.utils.logger import logger

# The lease file is stored in the user's home directory.
# Using a product-specific name ("nexus") prevents collisions with other
# NORVI agents (e.g. Voro uses ".norvi_voro_lease") installed on the same PC.
LEASE_FILE = os.path.join(os.path.expanduser("~"), ".norvi_nexus_lease")


class SessionManager:
    """
    Manages the user's active session using the NORVI Agency lease file system.

    The lease is a JSON file stored at ~/.norvi_nexus_lease containing:
        {
            "token":      "<JWT lease string>",
            "expires_at": <unix timestamp float>
        }

    This approach is consistent with norvi_gatekeeper.py used by Voro and
    all other NORVI agents, allowing the backend to manage lease lifecycles
    centrally.
    """

    # ── Save ──────────────────────────────────────────────────────────────────
    @staticmethod
    def save_token(token: str, expires_at: float) -> bool:
        """
        Writes the JWT lease and its expiration timestamp to the lease file.
        Returns True on success, False on failure.
        """
        try:
            with open(LEASE_FILE, "w") as f:
                json.dump({"token": token, "expires_at": expires_at}, f)
            logger.info(f"Nexus lease saved to {LEASE_FILE}.")
            return True
        except Exception as e:
            logger.error(f"Failed to save Nexus lease: {e}")
            return False

    # ── Load ──────────────────────────────────────────────────────────────────
    @staticmethod
    def load_lease() -> Optional[dict]:
        """
        Reads and validates the lease file.
        Returns the lease dict if the file exists and the lease has NOT expired.
        Returns None if the file is missing, unreadable, or the lease is expired.
        """
        if not os.path.exists(LEASE_FILE):
            return None
        try:
            with open(LEASE_FILE, "r") as f:
                data = json.load(f)
            expires_at = data.get("expires_at")
            if expires_at and time.time() > float(expires_at):
                logger.info("Nexus lease has expired.")
                return None
            return data
        except Exception as e:
            logger.warning(f"Could not read Nexus lease file: {e}")
            return None

    # ── Token retrieval ───────────────────────────────────────────────────────
    @staticmethod
    def get_token() -> Optional[str]:
        """Returns the raw JWT lease string if the session is still valid."""
        lease = SessionManager.load_lease()
        return lease.get("token") if lease else None

    # ── Authentication check ──────────────────────────────────────────────────
    @staticmethod
    def is_authenticated() -> bool:
        """
        Returns True if a valid, unexpired lease exists on disk.
        This is checked at app startup to skip the login screen entirely.
        """
        return SessionManager.load_lease() is not None

    # ── Logout / Clear ────────────────────────────────────────────────────────
    @staticmethod
    def clear_session() -> bool:
        """
        Deletes the lease file from disk (logout).
        Returns True even if the file didn't exist (idempotent).
        """
        try:
            if os.path.exists(LEASE_FILE):
                os.remove(LEASE_FILE)
                logger.info("Nexus lease file removed (logout).")
            return True
        except Exception as e:
            logger.error(f"Failed to clear Nexus lease: {e}")
            return False
