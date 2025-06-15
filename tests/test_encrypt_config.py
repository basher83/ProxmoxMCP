"""
Tests for encrypt_config utility.

This module tests the encrypt_config command-line utility including:
- Secure master key generation
- Key display security
- Interactive prompts and warnings
- Configuration encryption workflows
"""

import json
import os
from pathlib import Path
import tempfile
from unittest.mock import MagicMock, patch

import pytest

from proxmox_mcp.utils.encrypt_config import (
    clear_terminal_if_requested,
    create_backup,
    generate_master_key,
    rotate_master_key,
    rotate_master_key_all,
    verify_config_decryption,
)
from proxmox_mcp.utils.encryption import TokenEncryption


class TestSecureKeyGeneration:
    """Test cases for secure master key generation."""

    @patch("pathlib.Path.write_text")
    @patch("pathlib.Path.chmod")
    @patch("pathlib.Path.home")
    @patch("builtins.print")
    def test_generate_master_key_secure_workflow(
        self,
        mock_print: MagicMock,
        mock_home: MagicMock,
        mock_chmod: MagicMock,
        mock_write_text: MagicMock,
    ) -> None:
        """Test that master key generation follows secure workflow."""
        # Mock home directory
        mock_home.return_value = Path("/home/test")

        # Call the function
        generate_master_key()

        # Verify key was written to secure file
        mock_write_text.assert_called_once()
        written_key = mock_write_text.call_args[0][0]
        # Key should be base64 encoded string, not prefixed with PROXMOX_MCP_MASTER_KEY=
        assert len(written_key) > 0, "Key should be written"
        assert not written_key.startswith(
            "PROXMOX_MCP_MASTER_KEY="
        ), "Key should be stored without prefix"

        # Verify file permissions were set to 600 (owner read/write only)
        mock_chmod.assert_called_once_with(0o600)

        # Verify secure workflow messages were displayed
        printed_calls = [str(call) for call in mock_print.call_args_list]
        all_output = " ".join(printed_calls)

        assert "Master key generated securely" in all_output
        assert "Key saved to:" in all_output
        assert "export PROXMOX_MCP_MASTER_KEY=$(cat ~/.proxmox_mcp_key)" in all_output

        # Verify NO raw key is displayed in output
        key_displays = [
            call
            for call in printed_calls
            if "PROXMOX_MCP_MASTER_KEY=" in call and "$(cat" not in call
        ]
        assert (
            len(key_displays) == 0
        ), "Raw key should NOT be displayed in console output"

    @patch("pathlib.Path.write_text")
    @patch("pathlib.Path.chmod")
    @patch("pathlib.Path.home")
    @patch("builtins.print")
    def test_generate_master_key_file_error_handling(
        self,
        mock_print: MagicMock,
        mock_home: MagicMock,
        mock_chmod: MagicMock,
        mock_write_text: MagicMock,
    ) -> None:
        """Test error handling when key file cannot be written."""
        # Mock home directory
        mock_home.return_value = Path("/home/test")

        # Mock file write error
        mock_write_text.side_effect = OSError("Permission denied")

        # Should exit with error
        with pytest.raises(SystemExit) as exc_info:
            generate_master_key()

        assert exc_info.value.code == 1

        # Verify error message was displayed
        printed_calls = [str(call) for call in mock_print.call_args_list]
        error_messages = [
            call for call in printed_calls if "Error saving key file" in call
        ]
        assert len(error_messages) > 0

    @patch("pathlib.Path.write_text")
    @patch("pathlib.Path.chmod")
    @patch("pathlib.Path.home")
    @patch("builtins.print")
    def test_no_key_exposure_in_output(
        self,
        mock_print: MagicMock,
        mock_home: MagicMock,
        mock_chmod: MagicMock,
        mock_write_text: MagicMock,
    ) -> None:
        """Test that master key is never exposed in console output."""
        # Mock home directory
        mock_home.return_value = Path("/home/test")

        # Call the function
        generate_master_key()

        # Get all printed output
        printed_calls = [str(call) for call in mock_print.call_args_list]
        all_output = " ".join(printed_calls)

        # Verify that no actual key value appears in the output
        # The key should only be written to file, not displayed
        assert (
            "PROXMOX_MCP_MASTER_KEY=AAAA" not in all_output
        ), "Actual key values should not appear in output"

        # The only reference should be in the export command template
        export_commands = [
            call
            for call in printed_calls
            if "export PROXMOX_MCP_MASTER_KEY=$(cat" in call
        ]
        assert len(export_commands) == 1, "Should show export command template"

    @patch("pathlib.Path.write_text")
    @patch("pathlib.Path.chmod")
    @patch("pathlib.Path.home")
    @patch("builtins.print")
    def test_security_reminders_displayed(
        self,
        mock_print: MagicMock,
        mock_home: MagicMock,
        mock_chmod: MagicMock,
        mock_write_text: MagicMock,
    ) -> None:
        """Test that appropriate security reminders are displayed."""
        # Mock home directory
        mock_home.return_value = Path("/home/test")

        generate_master_key()

        printed_calls = [str(call) for call in mock_print.call_args_list]
        all_output = " ".join(printed_calls)

        # Check for key security reminders
        assert "Store this file securely" in all_output
        assert "Key file permissions set to 600" in all_output
        assert "Losing this key means losing access" in all_output


class TestKeyRotation:
    """Test cases for master key rotation functionality."""

    def test_create_backup(self) -> None:
        """Test that backup creation works correctly."""
        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".json") as f:
            test_config = {"test": "data"}
            json.dump(test_config, f)
            f.flush()

            try:
                backup_path = create_backup(f.name)

                # Verify backup exists
                assert os.path.exists(backup_path)

                # Verify backup contains same data
                with open(backup_path) as backup_f:
                    backup_data = json.load(backup_f)
                assert backup_data == test_config

                # Verify backup path format
                assert backup_path.startswith(f.name + ".backup.")

                # Clean up
                os.unlink(backup_path)
            finally:
                os.unlink(f.name)

    def test_verify_config_decryption_with_encrypted_token(self) -> None:
        """Test config decryption verification with encrypted token."""
        # Create test config with encrypted token
        master_key = TokenEncryption.generate_master_key()
        encryptor = TokenEncryption(master_key=master_key)
        encrypted_token = encryptor.encrypt_token("test-token")

        test_config = {"auth": {"token_value": encrypted_token}}

        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".json") as f:
            json.dump(test_config, f)
            f.flush()

            try:
                # Should verify successfully with correct key
                assert verify_config_decryption(f.name, master_key)

                # Should fail with wrong key
                wrong_key = TokenEncryption.generate_master_key()
                assert not verify_config_decryption(f.name, wrong_key)
            finally:
                os.unlink(f.name)

    def test_verify_config_decryption_with_plain_token(self) -> None:
        """Test config decryption verification with plain text token."""
        test_config = {"auth": {"token_value": "plain-text-token"}}

        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".json") as f:
            json.dump(test_config, f)
            f.flush()

            try:
                # Should pass verification even with random key since token is plain text
                random_key = TokenEncryption.generate_master_key()
                assert verify_config_decryption(f.name, random_key)
            finally:
                os.unlink(f.name)

    def test_verify_config_decryption_no_token(self) -> None:
        """Test config decryption verification with no token."""
        test_config = {"other": "data"}

        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".json") as f:
            json.dump(test_config, f)
            f.flush()

            try:
                # Should pass verification when no encrypted tokens exist
                random_key = TokenEncryption.generate_master_key()
                assert verify_config_decryption(f.name, random_key)
            finally:
                os.unlink(f.name)

    @patch.dict(os.environ, {}, clear=True)
    def test_rotate_master_key_no_env_key(self) -> None:
        """Test key rotation fails when no environment key is set."""
        test_config = {"auth": {"token_value": "enc:test"}}

        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".json") as f:
            json.dump(test_config, f)
            f.flush()

            try:
                with pytest.raises(SystemExit):
                    rotate_master_key(f.name)
            finally:
                os.unlink(f.name)

    @patch.dict(os.environ, {"PROXMOX_MCP_MASTER_KEY": "invalid_key"})
    def test_rotate_master_key_invalid_env_key(self) -> None:
        """Test key rotation fails when environment key can't decrypt config."""
        # Create config with token encrypted with different key
        actual_key = TokenEncryption.generate_master_key()
        encryptor = TokenEncryption(master_key=actual_key)
        encrypted_token = encryptor.encrypt_token("test-token")

        test_config = {"auth": {"token_value": encrypted_token}}

        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".json") as f:
            json.dump(test_config, f)
            f.flush()

            try:
                with pytest.raises(SystemExit):
                    rotate_master_key(f.name)
            finally:
                os.unlink(f.name)

    def test_rotate_master_key_successful(self) -> None:
        """Test successful key rotation."""
        # Create original key and encrypted config
        old_key = TokenEncryption.generate_master_key()
        old_encryptor = TokenEncryption(master_key=old_key)
        encrypted_token = old_encryptor.encrypt_token("test-token-value")

        test_config = {"auth": {"token_value": encrypted_token}, "other": "data"}

        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".json") as f:
            json.dump(test_config, f)
            f.flush()

            try:
                # Set old key in environment
                with patch.dict(os.environ, {"PROXMOX_MCP_MASTER_KEY": old_key}):
                    # Generate new key for rotation
                    new_key = TokenEncryption.generate_master_key()

                    # Perform rotation
                    rotate_master_key(f.name, new_key)

                    # Verify config was updated
                    with open(f.name) as config_f:
                        rotated_config = json.load(config_f)

                    # Should have different encrypted token
                    new_encrypted_token = rotated_config["auth"]["token_value"]
                    assert new_encrypted_token != encrypted_token
                    assert new_encrypted_token.startswith("enc:")

                    # Should decrypt to same value with new key
                    new_encryptor = TokenEncryption(master_key=new_key)
                    decrypted_token = new_encryptor.decrypt_token(new_encrypted_token)
                    assert decrypted_token == "test-token-value"

                    # Other data should be unchanged
                    assert rotated_config["other"] == "data"

                    # Backup should exist
                    backup_files = [
                        file
                        for file in os.listdir(os.path.dirname(f.name))
                        if file.startswith(os.path.basename(f.name) + ".backup.")
                    ]
                    assert len(backup_files) == 1

                    # Clean up backup
                    backup_path = os.path.join(os.path.dirname(f.name), backup_files[0])
                    os.unlink(backup_path)

            finally:
                os.unlink(f.name)

    def test_rotate_master_key_all_successful(self) -> None:
        """Test successful bulk key rotation."""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create test keys
            old_key = TokenEncryption.generate_master_key()
            old_encryptor = TokenEncryption(master_key=old_key)

            # Create multiple config files
            config1_path = os.path.join(temp_dir, "config1.json")
            config2_path = os.path.join(temp_dir, "config2.json")
            config3_path = os.path.join(temp_dir, "config_plain.json")

            # Config 1: encrypted token
            config1 = {
                "auth": {"token_value": old_encryptor.encrypt_token("token1")},
                "name": "config1",
            }

            # Config 2: encrypted token
            config2 = {
                "auth": {"token_value": old_encryptor.encrypt_token("token2")},
                "name": "config2",
            }

            # Config 3: plain token (should be skipped)
            config3 = {"auth": {"token_value": "plain-token"}, "name": "config3"}

            # Write configs
            with open(config1_path, "w") as f:
                json.dump(config1, f)
            with open(config2_path, "w") as f:
                json.dump(config2, f)
            with open(config3_path, "w") as f:
                json.dump(config3, f)

            # Set old key in environment and perform bulk rotation
            with patch.dict(os.environ, {"PROXMOX_MCP_MASTER_KEY": old_key}):
                new_key = TokenEncryption.generate_master_key()
                rotate_master_key_all(temp_dir, new_key)

                # Verify encrypted configs were rotated
                new_encryptor = TokenEncryption(master_key=new_key)

                # Check config1
                with open(config1_path) as f:
                    rotated_config1 = json.load(f)
                decrypted_token1 = new_encryptor.decrypt_token(
                    rotated_config1["auth"]["token_value"]
                )
                assert decrypted_token1 == "token1"
                assert rotated_config1["name"] == "config1"

                # Check config2
                with open(config2_path) as f:
                    rotated_config2 = json.load(f)
                decrypted_token2 = new_encryptor.decrypt_token(
                    rotated_config2["auth"]["token_value"]
                )
                assert decrypted_token2 == "token2"
                assert rotated_config2["name"] == "config2"

                # Check config3 (should be unchanged)
                with open(config3_path) as f:
                    unchanged_config3 = json.load(f)
                assert unchanged_config3["auth"]["token_value"] == "plain-token"
                assert unchanged_config3["name"] == "config3"

                # Verify backups were created for rotated configs
                backup_files = [f for f in os.listdir(temp_dir) if ".backup." in f]
                assert (
                    len(backup_files) == 2
                )  # Only encrypted configs should have backups

    def test_rotate_master_key_all_no_configs(self) -> None:
        """Test bulk rotation with no configuration files."""
        with tempfile.TemporaryDirectory() as temp_dir:
            with pytest.raises(SystemExit):
                rotate_master_key_all(temp_dir)

    def test_rotate_master_key_all_invalid_directory(self) -> None:
        """Test bulk rotation with invalid directory."""
        with pytest.raises(SystemExit):
            rotate_master_key_all("/nonexistent/directory")


class TestTerminalClearing:
    """Test cases for terminal clearing functionality."""

    @patch("subprocess.run")
    @patch("platform.system")
    @patch("builtins.input")
    @patch("builtins.print")
    def test_clear_terminal_if_requested_yes_linux(
        self,
        mock_print: MagicMock,
        mock_input: MagicMock,
        mock_system: MagicMock,
        mock_subprocess: MagicMock,
    ) -> None:
        """Test terminal clearing when user agrees on Linux/macOS."""
        # Mock user saying yes and platform being Linux
        mock_input.return_value = "y"
        mock_system.return_value = "Linux"
        mock_subprocess.return_value = MagicMock()

        clear_terminal_if_requested()

        # Verify correct command was called with secure parameters
        mock_subprocess.assert_called_once_with(["clear"], check=True, timeout=5)

        # Verify success message was printed
        printed_calls = [str(call) for call in mock_print.call_args_list]
        success_messages = [
            call for call in printed_calls if "Terminal cleared for security" in call
        ]
        assert len(success_messages) > 0

    @patch("subprocess.run")
    @patch("platform.system")
    @patch("builtins.input")
    @patch("builtins.print")
    def test_clear_terminal_if_requested_yes_windows(
        self,
        mock_print: MagicMock,
        mock_input: MagicMock,
        mock_system: MagicMock,
        mock_subprocess: MagicMock,
    ) -> None:
        """Test terminal clearing when user agrees on Windows."""
        # Mock user saying yes and platform being Windows
        mock_input.return_value = "yes"
        mock_system.return_value = "Windows"
        mock_subprocess.return_value = MagicMock()

        clear_terminal_if_requested()

        # Verify correct command was called with secure parameters
        mock_subprocess.assert_called_once_with(["cls"], check=True, timeout=5)

        # Verify success message was printed
        printed_calls = [str(call) for call in mock_print.call_args_list]
        success_messages = [
            call for call in printed_calls if "Terminal cleared for security" in call
        ]
        assert len(success_messages) > 0

    @patch("subprocess.run")
    @patch("platform.system")
    @patch("builtins.input")
    @patch("builtins.print")
    def test_clear_terminal_if_requested_no(
        self,
        mock_print: MagicMock,
        mock_input: MagicMock,
        mock_system: MagicMock,
        mock_subprocess: MagicMock,
    ) -> None:
        """Test when user declines terminal clearing."""
        # Mock user saying no
        mock_input.return_value = "n"
        mock_system.return_value = "Linux"

        clear_terminal_if_requested()

        # Verify no subprocess was called
        mock_subprocess.assert_not_called()

        # Verify manual instruction was printed
        printed_calls = [str(call) for call in mock_print.call_args_list]
        manual_instructions = [
            call for call in printed_calls if "clear terminal manually" in call
        ]
        assert len(manual_instructions) > 0

    @patch("subprocess.run")
    @patch("platform.system")
    @patch("builtins.input")
    @patch("builtins.print")
    def test_clear_terminal_if_requested_keyboard_interrupt(
        self,
        mock_print: MagicMock,
        mock_input: MagicMock,
        mock_system: MagicMock,
        mock_subprocess: MagicMock,
    ) -> None:
        """Test handling of keyboard interrupt during terminal clearing."""
        # Mock user pressing Ctrl+C
        mock_input.side_effect = KeyboardInterrupt()
        mock_system.return_value = "Linux"

        # Should not raise exception
        clear_terminal_if_requested()

        # Verify no subprocess was called
        mock_subprocess.assert_not_called()

        # Verify manual instruction was printed - look for the specific message from
        # KeyboardInterrupt handler
        printed_calls = [str(call) for call in mock_print.call_args_list]
        interrupt_instructions = [
            call
            for call in printed_calls
            if "Consider clearing terminal manually for security" in call
        ]
        assert len(interrupt_instructions) > 0

    @patch("subprocess.run")
    @patch("platform.system")
    @patch("builtins.input")
    @patch("builtins.print")
    def test_clear_terminal_if_requested_eof_error(
        self,
        mock_print: MagicMock,
        mock_input: MagicMock,
        mock_system: MagicMock,
        mock_subprocess: MagicMock,
    ) -> None:
        """Test handling of EOF error during terminal clearing."""
        # Mock EOF error
        mock_input.side_effect = EOFError()
        mock_system.return_value = "Linux"

        # Should not raise exception
        clear_terminal_if_requested()

        # Verify no subprocess was called
        mock_subprocess.assert_not_called()

        # Verify manual instruction was printed - look for the specific message from
        # EOFError handler
        printed_calls = [str(call) for call in mock_print.call_args_list]
        eof_instructions = [
            call
            for call in printed_calls
            if "Consider clearing terminal manually for security" in call
        ]
        assert len(eof_instructions) > 0

    @patch("subprocess.run")
    @patch("platform.system")
    @patch("builtins.input")
    @patch("builtins.print")
    def test_clear_terminal_if_requested_subprocess_error(
        self,
        mock_print: MagicMock,
        mock_input: MagicMock,
        mock_system: MagicMock,
        mock_subprocess: MagicMock,
    ) -> None:
        """Test handling of subprocess error during terminal clearing."""
        # Mock user saying yes but subprocess failing
        mock_input.return_value = "y"
        mock_system.return_value = "Linux"
        mock_subprocess.side_effect = Exception("Command failed")

        # Should not raise exception
        clear_terminal_if_requested()

        # Verify error message was printed
        printed_calls = [str(call) for call in mock_print.call_args_list]
        error_messages = [
            call for call in printed_calls if "Could not clear terminal" in call
        ]
        assert len(error_messages) > 0

        # Verify manual instruction was printed
        manual_instructions = [
            call for call in printed_calls if "clear terminal manually" in call
        ]
        assert len(manual_instructions) > 0

    @patch("proxmox_mcp.utils.encrypt_config.clear_terminal_if_requested")
    @patch("builtins.input")
    @patch("builtins.print")
    def test_generate_master_key_calls_terminal_clearing(
        self, mock_print: MagicMock, mock_input: MagicMock, mock_clear: MagicMock
    ) -> None:
        """Test that master key generation calls terminal clearing."""
        # Mock user pressing Enter twice (to confirm and after storing)
        mock_input.side_effect = ["", ""]

        generate_master_key()

        # Verify terminal clearing was called
        mock_clear.assert_called_once()

    @patch("platform.system")
    @patch("builtins.input")
    @patch("builtins.print")
    def test_clear_terminal_case_insensitive_responses(
        self, mock_print: MagicMock, mock_input: MagicMock, mock_system: MagicMock
    ) -> None:
        """Test that terminal clearing accepts case-insensitive responses."""
        mock_system.return_value = "Linux"

        # Test various positive responses
        positive_responses = ["Y", "YES", "Yes", "y", "yes"]

        for response in positive_responses:
            mock_input.return_value = response
            with patch("subprocess.run") as mock_subprocess:
                mock_subprocess.return_value = MagicMock()

                clear_terminal_if_requested()

                # Should call subprocess for all positive responses with secure parameters
                mock_subprocess.assert_called_once_with(
                    ["clear"], check=True, timeout=5
                )
                mock_subprocess.reset_mock()

    @patch("platform.system")
    @patch("builtins.input")
    @patch("builtins.print")
    def test_clear_terminal_whitespace_handling(
        self, mock_print: MagicMock, mock_input: MagicMock, mock_system: MagicMock
    ) -> None:
        """Test that terminal clearing handles whitespace in responses."""
        mock_system.return_value = "Linux"

        # Test responses with whitespace
        responses_with_whitespace = ["  y  ", "\ty\t", "\n yes \n"]

        for response in responses_with_whitespace:
            mock_input.return_value = response
            with patch("subprocess.run") as mock_subprocess:
                mock_subprocess.return_value = MagicMock()

                clear_terminal_if_requested()

                # Should call subprocess after stripping whitespace with secure parameters
                mock_subprocess.assert_called_once_with(
                    ["clear"], check=True, timeout=5
                )
                mock_subprocess.reset_mock()
