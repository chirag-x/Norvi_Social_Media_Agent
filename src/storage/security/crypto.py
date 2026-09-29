import keyring
from cryptography.fernet import Fernet
import logging

logger = logging.getLogger(__name__)

class CryptoManager:
    _master_key = None
    _fernet = None
    _SERVICE = "nexus"
    _KEY_NAME = "db_master_key"

    @classmethod
    def _init_crypto(cls):
        if cls._fernet is not None:
            return
            
        try:
            # Try to get the key from the OS secure keychain
            stored_key = keyring.get_password(cls._SERVICE, cls._KEY_NAME)
            
            if not stored_key:
                # First run, generate a new key and save it securely
                logger.info("Generating new master encryption key for local secure storage...")
                new_key = Fernet.generate_key().decode('utf-8')
                keyring.set_password(cls._SERVICE, cls._KEY_NAME, new_key)
                stored_key = new_key
                
            cls._master_key = stored_key.encode('utf-8')
            cls._fernet = Fernet(cls._master_key)
        except Exception as e:
            logger.error(f"Failed to initialize secure storage. Fallback to unencrypted (WARNING: Not recommended for production). Error: {e}")
            cls._fernet = None

    @classmethod
    def encrypt(cls, data: str) -> str:
        """Encrypt a string if cryptography is available, else return plain text."""
        if not data:
            return data
            
        cls._init_crypto()
        if cls._fernet:
            try:
                # Return string with a prefix to identify encrypted data
                return "ENC:" + cls._fernet.encrypt(data.encode('utf-8')).decode('utf-8')
            except Exception as e:
                logger.error(f"Encryption failed: {e}")
                return data
        return data

    @classmethod
    def decrypt(cls, data: str) -> str:
        """Decrypt a string if it's encrypted."""
        if not data or not str(data).startswith("ENC:"):
            return data
            
        cls._init_crypto()
        if cls._fernet:
            try:
                # Remove the ENC: prefix and decrypt
                encrypted_payload = data[4:]
                return cls._fernet.decrypt(encrypted_payload.encode('utf-8')).decode('utf-8')
            except Exception as e:
                logger.error(f"Decryption failed: {e}")
                return data
        return data
