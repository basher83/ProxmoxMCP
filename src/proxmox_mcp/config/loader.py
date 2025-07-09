"""
Configuration loading utilities for the Proxmox MCP server.

This module handles loading and validation of server configuration:
- JSON configuration file loading
- Environment variable handling
- Configuration validation using Pydantic models
- Token encryption/decryption for secure storage
- Error handling for invalid configurations

The module ensures that all required configuration is present
and valid before the server starts operation. Sensitive values
like API tokens can be stored encrypted in the configuration file.
"""

import json
import os
from typing import Any, Dict, Optional

from ..utils.encryption import TokenEncryption
from .models import Config


def load_config(config_path: Optional[str] = None) -> Config:
    """Load and validate configuration from a JSON file.

    Steps performed:
    1. Resolve config path (parameter > env variable)
    2. Load and parse the JSON file
    3. Decrypt encrypted tokens (if prefixed with 'enc:')
    4. Validate presence of required fields
    5. Return typed Config object (via Pydantic)

    Expected keys:
    - proxmox: host, port, etc.
    - auth: user, token_name, token_value (supports decryption)
    - logging: level, format, etc.

    Master key for decryption must be in the PROXMOX_MCP_MASTER_KEY env variable.

    Args:
        config_path: Optional path to the config JSON file.
                     Defaults to PROXMOX_MCP_CONFIG env variable.

    Returns:
        A validated and decrypted Config object.

    Raises:
        ValueError: If the path is missing, JSON is invalid,
                    required fields are absent, or decryption fails.
    """
    path = _resolve_config_path(config_path)
    config_data = _load_json_config(path)
    _validate_required_fields(config_data)
    config_data = _decrypt_config_tokens(config_data)
    return _build_config(config_data)


def _resolve_config_path(config_path: Optional[str]) -> str:
    """Resolve config path from argument or environment."""
    if config_path:
        return config_path
    env_path = os.environ.get("PROXMOX_MCP_CONFIG")
    if not env_path:
        raise ValueError("Config path must be provided or set via PROXMOX_MCP_CONFIG.")
    return env_path


def _load_json_config(path: str) -> Any:
    """Load and parse JSON configuration from file."""
    try:
        with open(path) as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON in config file: {e}") from e
    except Exception as e:
        raise ValueError(f"Failed to read config file: {e}") from e


def _validate_required_fields(config: Dict[str, Any]) -> None:
    """Ensure required fields are present in the configuration."""
    if not config.get("proxmox", {}).get("host"):
        raise ValueError("Proxmox host cannot be empty")


def _build_config(config_data: Dict[str, Any]) -> Config:
    """Create and return the validated Config object."""
    try:
        return Config(**config_data)
    except Exception as e:
        raise ValueError(f"Invalid configuration structure: {e}") from e


def _decrypt_config_tokens(config_data: dict) -> dict:
    """Decrypt encrypted tokens in configuration data.

    Searches for encrypted values (prefixed with 'enc:') and decrypts them
    using the TokenEncryption utility. Handles backward compatibility
    with plain text tokens.

    Args:
        config_data: Raw configuration dictionary from JSON

    Returns:
        Configuration dictionary with decrypted tokens

    Raises:
        ValueError: If token decryption fails with detailed context
    """
    # Only initialize encryption if we find encrypted values
    encryptor = None

    # Check and decrypt auth.token_value if encrypted
    if "auth" in config_data and "token_value" in config_data["auth"]:
        token_value = config_data["auth"]["token_value"]
        if isinstance(token_value, str) and token_value.startswith("enc:"):
            try:
                if encryptor is None:
                    encryptor = TokenEncryption()
                config_data["auth"]["token_value"] = encryptor.decrypt_token(token_value)
            except Exception as e:
                _handle_decryption_error("auth.token_value", token_value, e)

    # Future: Add support for other encrypted fields here
    # e.g., database passwords, API keys, etc.

    return config_data


def _handle_decryption_error(
    field_name: str, encrypted_value: str, original_error: Exception
) -> None:
    """Handle decryption errors with enhanced context and actionable messages.

    Args:
        field_name: The configuration field that failed to decrypt
        encrypted_value: The encrypted value that failed (for format validation)
        original_error: The original exception that occurred

    Raises:
        ValueError: With enhanced error message containing field context and suggestions
    """
    # Analyze the type of error and provide specific guidance
    error_msg = str(original_error).lower()

    # Check for format errors
    if not encrypted_value.startswith("enc:"):
        raise ValueError(
            f"Configuration field '{field_name}' contains invalid encrypted token format. "
            f"Encrypted tokens must start with 'enc:' prefix. "
            f"Use the encrypt_config utility to properly encrypt tokens."
        )

    # Check for invalid encryption format
    if "invalid encrypted token format" in error_msg:
        raise ValueError(
            f"Failed to decrypt token for field '{field_name}': Invalid encryption format. "
            f"The token may be corrupted or use an unsupported format. "
            f"Re-encrypt the token using: python -m proxmox_mcp.utils.encrypt_config"
        )

    # Check for decryption key issues
    if "invalid master key" in error_msg or "decrypt" in error_msg:
        raise ValueError(
            f"Failed to decrypt token for field '{field_name}': Decryption key mismatch. "
            f"Ensure PROXMOX_MCP_MASTER_KEY environment variable is set correctly. "
            f"If the master key was changed, tokens must be re-encrypted."
        )

    # Check for base64 decoding errors
    if "base64" in error_msg or "invalid" in error_msg:
        raise ValueError(
            f"Failed to decrypt token for field '{field_name}': Token data is corrupted. "
            f"The encrypted token contains invalid characters. "
            f"Please re-encrypt the original token value."
        )

    # Generic decryption failure with context
    raise ValueError(
        f"Failed to decrypt token for field '{field_name}': {original_error}. "
        f"Verify the token format and master key are correct."
    )


def encrypt_config_file(config_path: str, output_path: Optional[str] = None) -> str:
    """Encrypt sensitive values in a configuration file.

    Utility function to migrate existing plain-text configuration files
    to use encrypted tokens. Creates a new configuration file with
    encrypted sensitive values.

    Args:
        config_path: Path to existing configuration file
        output_path: Optional path for encrypted config. If not provided,
                    creates a .encrypted version of the original file

    Returns:
        Path to the encrypted configuration file

    Raises:
        ValueError: If encryption fails or config is invalid
    """
    if output_path is None:
        base_path = config_path.rsplit(".", 1)[0]
        output_path = f"{base_path}.encrypted.json"

    try:
        # Load the original config
        with open(config_path) as f:
            config_data = json.load(f)

        # Initialize encryptor
        encryptor = TokenEncryption()

        # Encrypt sensitive values
        if "auth" in config_data and "token_value" in config_data["auth"]:
            token_value = config_data["auth"]["token_value"]
            if isinstance(token_value, str) and not encryptor.is_encrypted(token_value):
                config_data["auth"]["token_value"] = encryptor.encrypt_token(token_value)

        # Write encrypted config
        with open(output_path, "w") as f:
            json.dump(config_data, f, indent=4)

        print(f"✅ Encrypted configuration saved to: {output_path}")
        print("🔑 Make sure to set PROXMOX_MCP_MASTER_KEY environment variable")

        return output_path
    except Exception as e:
        raise ValueError(f"Failed to encrypt configuration file: {e}") from e
