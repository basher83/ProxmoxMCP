"""Security tests for VM command execution."""

import pytest

from proxmox_mcp.utils.command_security import CommandSecurityConfig, CommandValidator


class TestCommandSecurity:
    def test_command_length_validation(self):
        """Test command length limits."""
        config = CommandSecurityConfig(max_command_length=10)
        validator = CommandValidator(config)

        with pytest.raises(ValueError, match="exceeds maximum length"):
            validator.validate_command("this is a very long command")

    def test_dangerous_pattern_blocking(self):
        """Test blocking of dangerous command patterns."""
        validator = CommandValidator()

        dangerous_commands = [
            "rm -rf /",
            "dd if=/dev/zero of=/dev/sda",
            "sudo rm -rf /home",
            "chmod 777 /etc/passwd",
        ]

        for cmd in dangerous_commands:
            with pytest.raises(ValueError, match="blocked pattern"):
                validator.validate_command(cmd)

    def test_shell_operator_blocking(self):
        """Test blocking of shell operators."""
        validator = CommandValidator()

        dangerous_operators = [
            "ls | rm",
            "cat file && rm file",
            "ls; rm file",
            "$(malicious command)",
            "ls > /etc/shadow",
        ]

        for cmd in dangerous_operators:
            with pytest.raises(ValueError, match="not allowed"):
                validator.validate_command(cmd)

    def test_command_whitelist(self):
        """Test command whitelist functionality."""
        config = CommandSecurityConfig(allowed_commands={"ls", "cat"})
        validator = CommandValidator(config)

        assert validator.validate_command("ls -la") == "ls -la"
        assert validator.validate_command("cat /etc/hostname") == "cat /etc/hostname"

        with pytest.raises(ValueError, match="not in allowed list"):
            validator.validate_command("rm file.txt")

    def test_command_sanitization(self):
        """Test proper command sanitization."""
        validator = CommandValidator()

        result = validator.validate_command('echo "hello world"')
        assert result == "echo 'hello world'"

        result = validator.validate_command("ls -la")
        assert result == "ls -la"

    def test_safe_commands_pass_validation(self):
        """Test that safe commands pass validation."""
        validator = CommandValidator()

        safe_commands = [
            "ls -la",
            "cat /etc/hostname",
            "ps aux",
            "df -h",
            "free -m",
            "uname -a",
            "date",
            "uptime",
        ]

        for cmd in safe_commands:
            result = validator.validate_command(cmd)
            assert isinstance(result, str)
            assert len(result) > 0

    def test_empty_command_handling(self):
        """Test handling of empty commands."""
        validator = CommandValidator()

        result = validator.validate_command("")
        assert result == ""

    def test_custom_blocked_patterns(self):
        """Test custom blocked patterns configuration."""
        config = CommandSecurityConfig(
            blocked_patterns=[r"custom_dangerous_cmd", r"another_bad_cmd"]
        )
        validator = CommandValidator(config)

        with pytest.raises(ValueError, match="blocked pattern"):
            validator.validate_command("custom_dangerous_cmd --option")

        with pytest.raises(ValueError, match="blocked pattern"):
            validator.validate_command("another_bad_cmd")
