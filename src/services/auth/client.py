import os
import json
import base64
import time
import httpx
from typing import Tuple, Optional
from src.utils.logger import logger
from src.services.auth.hwid import get_hardware_id

# Product slug identifies Nexus in the NORVI backend — must match what
# is registered on the server side (e.g. when the license key was created).
PRODUCT_SLUG = "nexus"

# Agency backend URL — reads from env var NORVI_API_URL, falling back to the
# production API server. This is the same variable used by norvi_gatekeeper.py.
API_BASE_URL = os.getenv("NORVI_API_URL", "https://nor-vi.in")


class AuthClient:
    """
    Handles communication with the NORVI Agency backend for authentication
    and licensing. Implements the same 2-step flow as norvi_gatekeeper.py:

    Step 1 — Login:   POST /api/agent-auth/login
                      Body: { email, password }
                      Returns: { access_token }

    Step 2 — Activate: POST /api/agent-auth/activate
                        Body: { licenseKey, deviceId, productSlug }
                        Header: Authorization: Bearer <access_token>
                        Returns: { lease }  (a signed JWT with an exp claim)
    """

    # ── Step 1: Login ─────────────────────────────────────────────────────────
    async def _api_login(self, email: str, password: str) -> str:
        """
        Authenticates the user's NORVI account credentials.
        Returns the short-lived access_token on success.
        Raises an Exception with a user-friendly message on failure.
        """
        payload = {"email": email, "password": password}
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{API_BASE_URL}/api/agent-auth/login",
                    json=payload,
                    timeout=10.0,
                )
            if response.status_code == 200:
                data = response.json()
                token = data.get("access_token")
                if not token:
                    raise Exception("Server returned no access token. Please try again.")
                return token
            else:
                # Try to read a structured error from the backend
                try:
                    error_msg = response.json().get("error", "Login failed.")
                except Exception:
                    error_msg = "Login failed."
                raise Exception(error_msg)

        except httpx.RequestError as e:
            logger.error(f"Network error during login: {e}")
            raise Exception("Could not connect to the NORVI server. Check your internet connection.")

    # ── Step 2: Activate ──────────────────────────────────────────────────────
    async def _api_activate(self, access_token: str, license_key: str, hwid: str) -> Tuple[str, float]:
        """
        Activates the license key for this machine.
        Returns (lease_jwt, expires_at_timestamp) on success.
        Raises an Exception with a user-friendly message on failure.
        """
        payload = {
            "licenseKey": license_key,
            "deviceId": hwid,
            "productSlug": PRODUCT_SLUG,
        }
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{API_BASE_URL}/api/agent-auth/activate",
                    json=payload,
                    headers={
                        "Content-Type": "application/json",
                        "Authorization": f"Bearer {access_token}",
                    },
                    timeout=10.0,
                )
            if response.status_code == 200:
                data = response.json()
                lease = data.get("lease")
                if not lease:
                    raise Exception("Server returned no lease token. Please try again.")
                # Decode the JWT payload to extract the expiration timestamp
                expires_at = self._decode_jwt_exp(lease)
                return lease, expires_at
            else:
                try:
                    error_msg = response.json().get("error", "Activation failed.")
                except Exception:
                    error_msg = "Activation failed."
                raise Exception(error_msg)

        except httpx.RequestError as e:
            logger.error(f"Network error during activation: {e}")
            raise Exception("Could not connect to the NORVI server. Check your internet connection.")

    # ── JWT helper ────────────────────────────────────────────────────────────
    @staticmethod
    def _decode_jwt_exp(jwt_token: str) -> float:
        """
        Decodes the payload section of a JWT to read the 'exp' claim.
        Returns the expiration timestamp. Falls back to 7 days from now
        if the claim is missing or the token is malformed.
        """
        try:
            parts = jwt_token.split(".")
            if len(parts) >= 2:
                # Add padding so base64 doesn't choke on short payloads
                payload_b64 = parts[1] + "=" * (-len(parts[1]) % 4)
                decoded = json.loads(base64.b64decode(payload_b64).decode())
                exp = decoded.get("exp")
                if exp:
                    return float(exp)
        except Exception as e:
            logger.warning(f"Could not decode JWT exp claim: {e}")
        # Safe fallback: treat lease as valid for 7 days
        return time.time() + (7 * 24 * 60 * 60)

    # ── Public entry point ────────────────────────────────────────────────────
    async def login(
        self, email: str, password: str, activation_key: str
    ) -> Tuple[bool, str, Optional[str], Optional[float]]:
        """
        Executes the full 2-step NORVI authentication flow.

        Returns:
            (success: bool, message: str, lease_token: str|None, expires_at: float|None)
        """
        hwid = get_hardware_id()
        logger.info(f"Attempting NORVI login for {email} — HWID prefix: {hwid[:16]}...")

        try:
            # Step 1 — Verify email & password
            access_token = await self._api_login(email, password)
            logger.info("Step 1 (login) succeeded.")

            # Step 2 — Verify license key and bind this machine
            lease, expires_at = await self._api_activate(access_token, activation_key, hwid)
            logger.info("Step 2 (activation) succeeded. Lease obtained.")

            return True, "Authentication successful.", lease, expires_at

        except Exception as e:
            logger.error(f"Authentication failed: {e}")
            return False, str(e), None, None
