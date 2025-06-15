"""
Token encryption utilities for secure storage of sensitive configuration data.

This module provides secure encryption and decryption of API tokens and other
sensitive configuration values using Fernet symmetric encryption. It includes:
- Key generation and management
- Token encryption/decryption
- Environment-based key storage
- Migration support for existing plain-text configurations

Security features:
- Uses Fernet (AES 128 in CBC mode with HMAC SHA256 for authentication)
- Key derivation from environment variables or auto-generation
- Constant-time operations for security
- Proper error handling for invalid encrypted data
"""

import base64
import os
from typing import Optional

from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


class TokenEncryption:
    """Handles encryption and decryption of sensitive tokens.

    This class provides a secure way to encrypt API tokens and other sensitive
    configuration data. It uses Fernet encryption with key derivation from
    a master key stored in environment variables.

    Usage:
        # Encrypt a token
        encryptor = TokenEncryption()
        encrypted_token = encryptor.encrypt_token("my-secret-token")

        # Decrypt a token
        decrypted_token = encryptor.decrypt_token(encrypted_token)
    """

    def __init__(self, master_key: Optional[str] = None):
        """Initialize the encryption handler.

        Args:
            master_key: Optional master key for encryption. If not provided,
                       will attempt to load from PROXMOX_MCP_MASTER_KEY
                       environment variable, or generate a new one.
        """
        self._master_key = master_key or self._get_or_generate_master_key()
        self._cipher = self._create_cipher()

    def _get_or_generate_master_key(self) -> str:
        """Get master key from environment or generate a new one.

        Returns:
            Base64-encoded master key

        Raises:
            RuntimeError: If key cannot be loaded or generated
        """
        # Try to load from environment variable
        env_key = os.getenv("PROXMOX_MCP_MASTER_KEY")
        if env_key:
            return env_key

        # Generate a new key for the session but do not display it
        new_key = base64.urlsafe_b64encode(os.urandom(32)).decode()

        print("⚠️  WARNING: No master key found in environment.")
        print("   A temporary key has been generated for this session only.")
        print("   To generate and set a permanent master key:")
        print("   1. Run: python -m proxmox_mcp.utils.encrypt_config --generate-key")
        print("   2. Copy the key to your environment: export PROXMOX_MCP_MASTER_KEY=<key>")
        print("   3. Any tokens encrypted with the temporary key will need re-encryption.")
        print("   ⚠️  WARNING: Terminal history may expose keys - use the utility for security!")

        # Return the generated key for this session but don't expose it in logs
        return new_key

    def _create_cipher(self, salt: Optional[bytes] = None) -> Fernet:
        """Create Fernet cipher from master key with optional salt.

        Args:
            salt: Optional salt for key derivation. If not provided, uses static salt
                  for backward compatibility.

        Returns:
            Fernet cipher instance

        Raises:
            ValueError: If master key is invalid
        """
        try:
            # Decode the master key and create cipher
            key_bytes = base64.urlsafe_b64decode(self._master_key.encode())

            # Use provided salt or fall back to static salt for backward compatibility
            if salt is None:
                salt = b"proxmox_mcp_salt"  # Static salt for backward compatibility

            # Use PBKDF2 to derive a proper Fernet key from the master key
            kdf = PBKDF2HMAC(
                algorithm=hashes.SHA256(),
                length=32,
                salt=salt,
                iterations=100000,
            )
            fernet_key = base64.urlsafe_b64encode(kdf.derive(key_bytes))

            return Fernet(fernet_key)
        except Exception as e:
            raise ValueError(f"Invalid master key: {e}") from e

    def encrypt_token(self, token: str) -> str:
        """Encrypt a token for secure storage with unique salt.

        Args:
            token: Plain text token to encrypt

        Returns:
            Base64-encoded encrypted token with format 'enc:{salt_b64}:{encrypted_data_b64}'

        Raises:
            ValueError: If token cannot be encrypted
        """
        try:
            # Generate a unique salt for this encryption
            unique_salt = os.urandom(16)  # 16 bytes = 128 bits of salt

            # Create cipher with unique salt
            cipher = self._create_cipher(unique_salt)

            # Encrypt the token
            encrypted_bytes = cipher.encrypt(token.encode())

            # Encode salt and encrypted data
            salt_b64 = base64.urlsafe_b64encode(unique_salt).decode()
            encrypted_b64 = base64.urlsafe_b64encode(encrypted_bytes).decode()

            return f"enc:{salt_b64}:{encrypted_b64}"
        except Exception as e:
            raise ValueError(f"Failed to encrypt token: {e}") from e

    def decrypt_token(self, encrypted_token: str) -> str:
        """Decrypt an encrypted token with backward compatibility.

        Supports both formats:
        - New format: 'enc:{salt_b64}:{encrypted_data_b64}' (unique salt per token)
        - Old format: 'enc:{encrypted_data_b64}' (static salt for backward compatibility)

        Args:
            encrypted_token: Encrypted token with 'enc:' prefix

        Returns:
            Decrypted plain text token

        Raises:
            ValueError: If token cannot be decrypted or is invalid format
        """
        try:
            # Check if token is encrypted (has 'enc:' prefix)
            if not encrypted_token.startswith("enc:"):
                # Token is not encrypted, return as-is (for backward compatibility)
                return encrypted_token

            # Remove 'enc:' prefix
            token_parts = encrypted_token[4:].split(":")

            if len(token_parts) == 2:
                # New format: enc:{salt_b64}:{encrypted_data_b64}
                salt_b64, encrypted_b64 = token_parts

                # Decode salt and encrypted data
                salt = base64.urlsafe_b64decode(salt_b64.encode())
                encrypted_bytes = base64.urlsafe_b64decode(encrypted_b64.encode())

                # Create cipher with the stored salt
                cipher = self._create_cipher(salt)

                # Decrypt and return
                decrypted_bytes = cipher.decrypt(encrypted_bytes)
                return decrypted_bytes.decode()

            elif len(token_parts) == 1:
                # Old format: enc:{encrypted_data_b64} (backward compatibility)
                encrypted_b64 = token_parts[0]
                encrypted_bytes = base64.urlsafe_b64decode(encrypted_b64.encode())

                # Use default cipher with static salt for backward compatibility
                decrypted_bytes = self._cipher.decrypt(encrypted_bytes)
                return decrypted_bytes.decode()

            else:
                raise ValueError("Invalid encrypted token format")

        except Exception as e:
            raise ValueError(f"Failed to decrypt token: {e}") from e

    def is_encrypted(self, token: str) -> bool:
        """Check if a token is encrypted.

        Args:
            token: Token to check

        Returns:
            True if token is encrypted (has 'enc:' prefix), False otherwise
        """
        return token.startswith("enc:")

    def migrate_plain_token(self, plain_token: str) -> str:
        """Migrate a plain text token to encrypted format.

        Args:
            plain_token: Plain text token to migrate

        Returns:
            Encrypted token with 'enc:' prefix
        """
        if self.is_encrypted(plain_token):
            # Already encrypted
            return plain_token

        # Encrypt the plain token
        return self.encrypt_token(plain_token)

    @staticmethod
    def generate_master_key() -> str:
        """Generate a new master key for encryption.

        Returns:
            Base64-encoded master key
        """
        return base64.urlsafe_b64encode(os.urandom(32)).decode()


def encrypt_sensitive_value(value: str, encryptor: Optional[TokenEncryption] = None) -> str:
    """Convenience function to encrypt a sensitive value.

    Args:
        value: Sensitive value to encrypt
        encryptor: Optional TokenEncryption instance. If not provided, creates new one.

    Returns:
        Encrypted value
    """
    if encryptor is None:
        encryptor = TokenEncryption()
    return encryptor.encrypt_token(value)


def decrypt_sensitive_value(
    encrypted_value: str, encryptor: Optional[TokenEncryption] = None
) -> str:
    """Convenience function to decrypt a sensitive value.

    Args:
        encrypted_value: Encrypted value to decrypt
        encryptor: Optional TokenEncryption instance. If not provided, creates new one.

    Returns:
        Decrypted value
    """
    if encryptor is None:
        encryptor = TokenEncryption()
    return encryptor.decrypt_token(encrypted_value)
