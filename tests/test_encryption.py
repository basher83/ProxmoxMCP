"""
Tests for token encryption utilities.

This module tests the TokenEncryption class functionality including:
- Token encryption and decryption
- Unique salt generation per encryption
- Backward compatibility with old format
- Error handling and validation
- Master key generation and management
"""

import base64
import os
from unittest.mock import patch

import pytest

from proxmox_mcp.utils.encryption import (
    TokenEncryption,
    decrypt_sensitive_value,
    encrypt_sensitive_value,
)


class TestTokenEncryption:
    """Test cases for TokenEncryption class."""

    def test_init_with_master_key(self):
        """Test initialization with provided master key."""
        master_key = TokenEncryption.generate_master_key()
        encryptor = TokenEncryption(master_key=master_key)
        assert encryptor._master_key == master_key

    @patch.dict(
        os.environ,
        {"PROXMOX_MCP_MASTER_KEY": "dGVzdF9rZXlfZnJvbV9lbnYxMjM0NTY3ODkwMTIzNDU2"},
    )
    def test_init_with_env_key(self):
        """Test initialization with key from environment variable."""
        encryptor = TokenEncryption()
        assert encryptor._master_key == "dGVzdF9rZXlfZnJvbV9lbnYxMjM0NTY3ODkwMTIzNDU2"

    @patch.dict(os.environ, {}, clear=True)
    @patch("builtins.print")
    def test_init_generates_new_key_when_no_env(self, mock_print):
        """Test that a new key is generated when no environment variable is set."""
        encryptor = TokenEncryption()
        assert encryptor._master_key is not None
        assert len(encryptor._master_key) > 0
        # Verify warning was printed but key was NOT exposed
        assert mock_print.called

        # Check that no call to print contains the actual master key
        for call_args in mock_print.call_args_list:
            printed_text = str(call_args[0][0]) if call_args[0] else ""
            # The master key should not appear in any print statement
            assert encryptor._master_key not in printed_text

        # Verify security messaging is included
        printed_messages = [
            str(call[0][0]) for call in mock_print.call_args_list if call[0]
        ]
        security_message_found = any(
            "SECURITY" in msg or "security" in msg for msg in printed_messages
        )
        assert security_message_found, "Security warning should be displayed"

        # Verify that the key itself is NOT printed to console
        printed_calls = [str(call) for call in mock_print.call_args_list]
        for call in printed_calls:
            # Make sure the actual key value is not in any print statement
            assert encryptor._master_key not in call

    @patch.dict(os.environ, {}, clear=True)
    @patch("builtins.print")
    def test_key_not_exposed_in_auto_generation(self, mock_print):
        """Test that auto-generated keys are not exposed in console output."""
        encryptor = TokenEncryption()

        # Get all the printed messages
        printed_messages = []
        for call_args in mock_print.call_args_list:
            if call_args[0]:  # If there are positional arguments
                printed_messages.append(call_args[0][0])  # First positional argument

        # Join all messages and verify the key is not exposed
        all_output = " ".join(printed_messages)
        assert encryptor._master_key not in all_output

        # Verify appropriate security warnings are shown
        assert any("WARNING" in msg for msg in printed_messages)
        assert any("temporary key" in msg for msg in printed_messages)
        assert any("encrypt_config" in msg for msg in printed_messages)

    def test_encrypt_decrypt_roundtrip_new_format(self):
        """Test that encryption and decryption work correctly with new format."""
        master_key = TokenEncryption.generate_master_key()
        encryptor = TokenEncryption(master_key=master_key)

        original_token = "test-api-token-12345"
        encrypted_token = encryptor.encrypt_token(original_token)
        decrypted_token = encryptor.decrypt_token(encrypted_token)

        assert decrypted_token == original_token
        assert encrypted_token.startswith("enc:")
        # New format should have salt and encrypted data separated by colons
        assert encrypted_token.count(":") == 2

    def test_unique_salts_for_same_token(self):
        """Test that encrypting the same token twice generates different salts."""
        master_key = TokenEncryption.generate_master_key()
        encryptor = TokenEncryption(master_key=master_key)

        token = "test-token"
        encrypted1 = encryptor.encrypt_token(token)
        encrypted2 = encryptor.encrypt_token(token)

        # Both should decrypt to the same value
        assert encryptor.decrypt_token(encrypted1) == token
        assert encryptor.decrypt_token(encrypted2) == token

        # But should have different encrypted representations (due to unique salts)
        assert encrypted1 != encrypted2

        # Extract salts and verify they're different
        salt1 = encrypted1.split(":")[1]
        salt2 = encrypted2.split(":")[1]
        assert salt1 != salt2

    def test_backward_compatibility_old_format(self):
        """Test that old format tokens (without salt) can still be decrypted."""
        master_key = TokenEncryption.generate_master_key()
        encryptor = TokenEncryption(master_key=master_key)

        # Simulate an old format encrypted token (using static salt)
        original_token = "legacy-token"

        # Create cipher with static salt (old behavior)
        cipher = encryptor._create_cipher()  # No salt provided, uses static salt
        encrypted_bytes = cipher.encrypt(original_token.encode())
        encrypted_b64 = base64.urlsafe_b64encode(encrypted_bytes).decode()
        old_format_token = f"enc:{encrypted_b64}"

        # Should be able to decrypt old format
        decrypted_token = encryptor.decrypt_token(old_format_token)
        assert decrypted_token == original_token

    def test_decrypt_plain_text_token(self):
        """Test that plain text tokens (without enc: prefix) are returned as-is."""
        encryptor = TokenEncryption()
        plain_token = "plain-text-token"
        result = encryptor.decrypt_token(plain_token)
        assert result == plain_token

    def test_is_encrypted(self):
        """Test the is_encrypted method."""
        encryptor = TokenEncryption()

        # Test plain text token
        assert not encryptor.is_encrypted("plain-token")

        # Test encrypted token
        encrypted = encryptor.encrypt_token("test-token")
        assert encryptor.is_encrypted(encrypted)

    def test_migrate_plain_token(self):
        """Test migrating plain text token to encrypted format."""
        encryptor = TokenEncryption()

        plain_token = "plain-token"
        migrated_token = encryptor.migrate_plain_token(plain_token)

        # Should be encrypted
        assert migrated_token.startswith("enc:")
        assert encryptor.is_encrypted(migrated_token)

        # Should decrypt to original value
        assert encryptor.decrypt_token(migrated_token) == plain_token

        # Migrating already encrypted token should return it unchanged
        migrated_again = encryptor.migrate_plain_token(migrated_token)
        assert migrated_again == migrated_token

    def test_invalid_master_key(self):
        """Test that invalid master keys raise appropriate errors."""
        with pytest.raises(ValueError, match="Invalid master key"):
            TokenEncryption(master_key="invalid-key")

    def test_invalid_encrypted_token_format(self):
        """Test that invalid encrypted token formats raise appropriate errors."""
        encryptor = TokenEncryption()

        # Invalid format (too many colons)
        with pytest.raises(ValueError, match="Failed to decrypt token"):
            encryptor.decrypt_token("enc:part1:part2:part3:extra")

        # Invalid base64
        with pytest.raises(ValueError, match="Failed to decrypt token"):
            encryptor.decrypt_token("enc:invalid_base64:invalid_base64")

    def test_generate_master_key(self):
        """Test master key generation."""
        key1 = TokenEncryption.generate_master_key()
        key2 = TokenEncryption.generate_master_key()

        # Keys should be different
        assert key1 != key2

        # Keys should be valid base64
        assert base64.urlsafe_b64decode(key1.encode())
        assert base64.urlsafe_b64decode(key2.encode())

    def test_different_encryptors_same_master_key(self):
        """Test that different encryptor instances with same master key can decrypt each
        other's tokens.
        """
        master_key = TokenEncryption.generate_master_key()

        encryptor1 = TokenEncryption(master_key=master_key)
        encryptor2 = TokenEncryption(master_key=master_key)

        token = "shared-token"
        encrypted_by_1 = encryptor1.encrypt_token(token)
        decrypted_by_2 = encryptor2.decrypt_token(encrypted_by_1)

        assert decrypted_by_2 == token


class TestConvenienceFunctions:
    """Test cases for convenience functions."""

    def test_encrypt_sensitive_value(self):
        """Test encrypt_sensitive_value convenience function."""
        value = "sensitive-value"
        encrypted = encrypt_sensitive_value(value)

        assert encrypted.startswith("enc:")
        assert encrypted.count(":") == 2  # New format

    @patch.dict(
        os.environ,
        {"PROXMOX_MCP_MASTER_KEY": "dGVzdF9rZXlfZnJvbV9lbnYxMjM0NTY3ODkwMTIzNDU2"},
    )
    def test_decrypt_sensitive_value(self):
        """Test decrypt_sensitive_value convenience function."""
        value = "sensitive-value"
        encrypted = encrypt_sensitive_value(value)
        decrypted = decrypt_sensitive_value(encrypted)

        assert decrypted == value

    def test_convenience_functions_with_custom_encryptor(self):
        """Test convenience functions with custom encryptor."""
        master_key = TokenEncryption.generate_master_key()
        encryptor = TokenEncryption(master_key=master_key)

        value = "test-value"
        encrypted = encrypt_sensitive_value(value, encryptor)
        decrypted = decrypt_sensitive_value(encrypted, encryptor)

        assert decrypted == value
