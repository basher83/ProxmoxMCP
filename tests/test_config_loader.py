"""
Tests for configuration loader with enhanced error handling.

This module tests the enhanced decryption error handling functionality including:
- Field-specific error messages
- Distinction between format errors and decryption errors
- Actionable error messages with suggestions
- Security considerations (no sensitive data exposure)
"""

import json
import os
import tempfile
from unittest.mock import MagicMock, patch

import pytest

from proxmox_mcp.config.loader import (
    _decrypt_config_tokens,
    _handle_decryption_error,
    load_config,
)


class TestEnhancedDecryptionErrors:
    """Test cases for enhanced decryption error handling."""

    def test_handle_decryption_error_invalid_format(self):
        """Test error handling for invalid encryption format."""
        with pytest.raises(ValueError) as exc_info:
            _handle_decryption_error("auth.token_value", "not_encrypted", Exception("test"))

        error_msg = str(exc_info.value)
        assert "auth.token_value" in error_msg
        assert "invalid encrypted token format" in error_msg
        assert "enc:" in error_msg
        assert "encrypt_config utility" in error_msg

    def test_handle_decryption_error_corrupted_format(self):
        """Test error handling for corrupted encryption format."""
        original_error = Exception("invalid encrypted token format")
        with pytest.raises(ValueError) as exc_info:
            _handle_decryption_error("auth.token_value", "enc:corrupted", original_error)

        error_msg = str(exc_info.value)
        assert "auth.token_value" in error_msg
        assert "Invalid encryption format" in error_msg
        assert "corrupted or use an unsupported format" in error_msg
        assert "encrypt_config" in error_msg

    def test_handle_decryption_error_key_mismatch(self):
        """Test error handling for master key mismatch."""
        original_error = Exception("Failed to decrypt token")
        with pytest.raises(ValueError) as exc_info:
            _handle_decryption_error("auth.token_value", "enc:valid_format", original_error)

        error_msg = str(exc_info.value)
        assert "auth.token_value" in error_msg
        assert "Decryption key mismatch" in error_msg
        assert "PROXMOX_MCP_MASTER_KEY" in error_msg
        assert "tokens must be re-encrypted" in error_msg

    def test_handle_decryption_error_base64_corruption(self):
        """Test error handling for base64 decoding errors."""
        original_error = Exception("Invalid base64 padding")
        with pytest.raises(ValueError) as exc_info:
            _handle_decryption_error("auth.token_value", "enc:invalid_base64", original_error)

        error_msg = str(exc_info.value)
        assert "auth.token_value" in error_msg
        assert "Token data is corrupted" in error_msg
        assert "invalid characters" in error_msg
        assert "re-encrypt the original token" in error_msg

    def test_handle_decryption_error_generic(self):
        """Test error handling for generic decryption failures."""
        original_error = Exception("Unknown encryption error")
        with pytest.raises(ValueError) as exc_info:
            _handle_decryption_error("auth.token_value", "enc:some_token", original_error)

        error_msg = str(exc_info.value)
        assert "auth.token_value" in error_msg
        assert "Unknown encryption error" in error_msg
        assert "Verify the token format and master key" in error_msg

    def test_different_field_names_in_errors(self):
        """Test that different field names appear correctly in error messages."""
        test_cases = [
            "auth.token_value",
            "auth.username",
            "database.password",
            "api.secret_key",
        ]

        for field_name in test_cases:
            with pytest.raises(ValueError) as exc_info:
                _handle_decryption_error(field_name, "not_encrypted", Exception("test"))

            error_msg = str(exc_info.value)
            assert field_name in error_msg

    @patch("proxmox_mcp.config.loader.TokenEncryption")
    def test_decrypt_config_tokens_field_context_in_error(self, mock_encryption_class):
        """Test that field context is preserved when decryption fails."""
        # Setup mock to raise an exception
        mock_encryptor = MagicMock()
        mock_encryptor.decrypt_token.side_effect = Exception("Decryption failed")
        mock_encryption_class.return_value = mock_encryptor

        config_data = {"auth": {"token_value": "enc:fake_encrypted_token"}}

        with pytest.raises(ValueError) as exc_info:
            _decrypt_config_tokens(config_data)

        error_msg = str(exc_info.value)
        assert "auth.token_value" in error_msg
        assert "Decryption key mismatch" in error_msg

    def test_decrypt_config_tokens_skips_plain_text(self):
        """Test that plain text tokens are not processed and don't cause errors."""
        config_data = {"auth": {"token_value": "plain_text_token"}}

        # Should not raise any errors
        result = _decrypt_config_tokens(config_data)
        assert result["auth"]["token_value"] == "plain_text_token"

    def test_decrypt_config_tokens_skips_non_string_values(self):
        """Test that non-string values are skipped without errors."""
        config_data = {"auth": {"token_value": 12345}}  # Non-string value

        # Should not raise any errors
        result = _decrypt_config_tokens(config_data)
        assert result["auth"]["token_value"] == 12345

    def test_decrypt_config_tokens_missing_auth_section(self):
        """Test that missing auth section is handled gracefully."""
        config_data = {"proxmox": {"host": "test-host"}}

        # Should not raise any errors
        result = _decrypt_config_tokens(config_data)
        assert "auth" not in result

    def test_no_sensitive_data_in_error_messages(self):
        """Test that error messages don't expose sensitive token data."""
        sensitive_token = "enc:very_sensitive_secret_token_data"

        with pytest.raises(ValueError) as exc_info:
            _handle_decryption_error("auth.token_value", sensitive_token, Exception("test"))

        error_msg = str(exc_info.value)

        # The field name should be present
        assert "auth.token_value" in error_msg

        # But the actual token content should NOT be present
        assert "very_sensitive_secret_token_data" not in error_msg
        assert sensitive_token not in error_msg

        # Should have helpful guidance but not expose sensitive data
        assert "Verify the token format and master key" in error_msg


class TestConfigLoaderIntegration:
    """Integration tests for config loader with enhanced error handling."""

    @patch("proxmox_mcp.config.loader.TokenEncryption")
    def test_load_config_with_decryption_error_provides_context(self, mock_encryption_class):
        """Test that load_config provides enhanced error context when decryption fails."""
        # Setup mock to raise an exception during decryption
        mock_encryptor = MagicMock()
        mock_encryptor.decrypt_token.side_effect = Exception("Mock decryption failure")
        mock_encryption_class.return_value = mock_encryptor

        # Create a temporary config file with encrypted token that will fail to decrypt
        config_data = {
            "proxmox": {"host": "test-host"},
            "auth": {
                "user": "test@pam",
                "token_name": "test-token",
                "token_value": "enc:encrypted_token_that_will_fail",  # Valid format, will fail
            },
            "logging": {"level": "INFO"},
        }

        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            json.dump(config_data, f)
            temp_path = f.name

        try:
            with pytest.raises(ValueError) as exc_info:
                load_config(temp_path)

            error_msg = str(exc_info.value)
            # Should get enhanced error from our error handler
            assert "auth.token_value" in error_msg
            assert "Decryption key mismatch" in error_msg

        finally:
            os.unlink(temp_path)

    @patch("proxmox_mcp.config.loader.TokenEncryption")
    def test_load_config_with_encryption_library_error(self, mock_encryption_class):
        """Test load_config handling when encryption library itself fails."""
        # Setup mock to raise an exception during initialization
        mock_encryption_class.side_effect = Exception("Encryption library error")

        config_data = {
            "proxmox": {"host": "test-host"},
            "auth": {
                "user": "test@pam",
                "token_name": "test-token",
                "token_value": "enc:fake_token",
            },
            "logging": {"level": "INFO"},
        }

        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            json.dump(config_data, f)
            temp_path = f.name

        try:
            with pytest.raises(ValueError) as exc_info:
                load_config(temp_path)

            error_msg = str(exc_info.value)
            # Should still get enhanced error context
            assert "auth.token_value" in error_msg

        finally:
            os.unlink(temp_path)
