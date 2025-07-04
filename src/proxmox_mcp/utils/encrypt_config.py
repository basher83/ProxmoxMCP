#!/usr/bin/env python3
"""
Configuration encryption utility for Proxmox MCP.

This script provides a command-line interface for encrypting sensitive
values in Proxmox MCP configuration files. It helps users migrate from
plain-text tokens to encrypted tokens for enhanced security.

Usage:
    python -m proxmox_mcp.utils.encrypt_config [config_file] [options]

Examples:
    # Encrypt tokens in existing config
    python -m proxmox_mcp.utils.encrypt_config proxmox-config/config.json

    # Encrypt and save to specific file
    python -m proxmox_mcp.utils.encrypt_config config.json -o config.encrypted.json

    # Generate a new master key
    python -m proxmox_mcp.utils.encrypt_config --generate-key
"""

import argparse
from datetime import datetime
import json
import os
from pathlib import Path
import platform
import shutil
import sys
from typing import List, Optional

# Add the src directory to the path so we can import our modules
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from proxmox_mcp.config.loader import encrypt_config_file
from proxmox_mcp.utils.encryption import TokenEncryption


def clear_terminal_if_requested() -> None:
    """Offer to clear terminal for security after key operations."""
    try:
        response = input("🧹 Clear terminal for security? (y/n): ").strip().lower()
        if response in ["y", "yes"]:
            if platform.system() == "Windows":
                # Use Windows-specific clear method via ctypes
                try:
                    import ctypes

                    ctypes.windll.kernel32.SetConsoleTitleW("ProxmoxMCP")  # type: ignore
                    # Clear screen using ANSI escape sequences (works on modern Windows)
                    print("\033[2J\033[H", end="", flush=True)
                except Exception:
                    # Fallback: just print newlines to push content up
                    print("\n" * 50)
            else:
                # Use ANSI escape sequences directly
                print("\033[2J\033[H", end="", flush=True)
            print("✅ Terminal cleared for security")
            print("💡 Consider also clearing your shell history if needed")
        else:
            print("💡 Remember to clear terminal manually: clear (Linux/Mac) or cls (Windows)")
    except (KeyboardInterrupt, EOFError):
        print("\n💡 Consider clearing terminal manually for security")
    except Exception as e:
        print(f"⚠️  Could not clear terminal: {e}")
        print("💡 Please clear terminal manually for security")


def generate_master_key() -> None:
    """Generate and save a new master key securely."""
    key = TokenEncryption.generate_master_key()

    # Save to secure file instead of displaying
    key_file = Path.home() / ".proxmox_mcp_key"
    try:
        key_file.write_text(key)
        key_file.chmod(0o600)  # Owner read/write only
    except Exception as e:
        print(f"❌ Error saving key file: {e}")
        sys.exit(1)

    print("🔐 Master key generated securely!")
    print(f"📁 Key saved to: {key_file}")
    print()
    print("📋 Set environment variable:")
    print("   export PROXMOX_MCP_MASTER_KEY=$(cat ~/.proxmox_mcp_key)")
    print()
    print("🔒 Security notes:")
    print("   - Key file permissions set to 600 (owner read/write only)")
    print("   - Store this file securely - you'll need it to decrypt your config!")
    print("   - Consider backing up the key file to a secure location")
    print()
    print("⚠️  WARNING: Losing this key means losing access to encrypted tokens!")
    print("✅ Key generation complete.")
    print()

    # Offer to clear terminal for security
    clear_terminal_if_requested()


def encrypt_config(config_path: str, output_path: Optional[str] = None) -> None:
    """Encrypt sensitive values in a configuration file."""
    try:
        # Check if config file exists
        if not os.path.exists(config_path):
            print(f"❌ Error: Configuration file not found: {config_path}")
            sys.exit(1)

        # Encrypt the configuration
        encrypted_path = encrypt_config_file(config_path, output_path)

        print()
        print("🔒 Configuration encrypted successfully!")
        print(f"   Original: {config_path}")
        print(f"   Encrypted: {encrypted_path}")
        print()
        print("📝 Next steps:")
        print("   1. Verify the encrypted config works:")
        print(f"      PROXMOX_MCP_CONFIG={encrypted_path} python -m proxmox_mcp.server --test")
        print("   2. Update your environment to use the encrypted config")
        print("   3. Securely delete the original plain-text config if desired")

    except Exception as e:
        print(f"❌ Error encrypting configuration: {e}")
        sys.exit(1)


def show_encryption_status(config_path: str) -> None:
    """Show the encryption status of a configuration file."""
    try:
        if not os.path.exists(config_path):
            print(f"❌ Error: Configuration file not found: {config_path}")
            sys.exit(1)

        with open(config_path) as f:
            config_data = json.load(f)

        print(f"📄 Configuration file: {config_path}")
        print()

        # Check token encryption status
        if "auth" in config_data and "token_value" in config_data["auth"]:
            token_value = config_data["auth"]["token_value"]
            if isinstance(token_value, str) and token_value.startswith("enc:"):
                print("🔒 Token value: ENCRYPTED ✅")
            else:
                print("🔓 Token value: PLAIN TEXT ⚠️")
        else:
            print("❓ Token value: NOT FOUND")

        print()

        # Check for master key
        master_key = os.getenv("PROXMOX_MCP_MASTER_KEY")
        if master_key:
            print("🔑 Master key: SET ✅")
        else:
            print("🔑 Master key: NOT SET ⚠️")
            print("   Set PROXMOX_MCP_MASTER_KEY environment variable")

    except Exception as e:
        print(f"❌ Error reading configuration: {e}")
        sys.exit(1)


def create_backup(file_path: str) -> str:
    """Create a timestamped backup of a file before rotation.

    Args:
        file_path: Path to the file to backup

    Returns:
        Path to the backup file

    Raises:
        OSError: If backup creation fails
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = f"{file_path}.backup.{timestamp}"

    try:
        shutil.copy2(file_path, backup_path)
        return backup_path
    except Exception as e:
        raise OSError(f"Failed to create backup: {e}") from e


def verify_config_decryption(config_path: str, old_key: str) -> bool:
    """Verify that a configuration file can be decrypted with the old key.

    Args:
        config_path: Path to the configuration file
        old_key: The old master key to test

    Returns:
        True if the file can be decrypted, False otherwise
    """
    try:
        # Create encryptor with old key
        old_encryptor = TokenEncryption(master_key=old_key)

        # Load config file
        with open(config_path) as f:
            config_data = json.load(f)

        # Check if there are any encrypted tokens
        if "auth" in config_data and "token_value" in config_data["auth"]:
            token_value = config_data["auth"]["token_value"]
            if isinstance(token_value, str) and token_value.startswith("enc:"):
                # Try to decrypt the token
                try:
                    old_encryptor.decrypt_token(token_value)
                    return True
                except Exception:
                    return False

        # If no encrypted tokens found, assume verification passed
        return True

    except Exception:
        return False


def _validate_rotation_environment(config_path: str) -> str:
    """Validate environment for key rotation and return old key.

    Args:
        config_path: Path to the configuration file

    Returns:
        The current master key from environment

    Raises:
        SystemExit: If validation fails
    """
    # Check if config file exists
    if not os.path.exists(config_path):
        print(f"❌ Error: Configuration file not found: {config_path}")
        sys.exit(1)

    # Get current master key from environment
    old_key = os.getenv("PROXMOX_MCP_MASTER_KEY")
    if not old_key:
        print("❌ Error: No master key found in environment variable PROXMOX_MCP_MASTER_KEY")
        print("   Set the current master key before rotation")
        sys.exit(1)

    # Verify old key works with current config
    print("🔍 Verifying current master key...")
    if not verify_config_decryption(config_path, old_key):
        print("❌ Error: Current master key cannot decrypt the configuration")
        print("   Please ensure PROXMOX_MCP_MASTER_KEY is set correctly")
        sys.exit(1)
    print("✅ Current master key verified")

    return old_key


def _handle_new_key_generation(new_key: Optional[str]) -> str:
    """Handle new key generation or validation.

    Args:
        new_key: Optional new master key. If None, will generate one.

    Returns:
        The new master key to use
    """
    if new_key is None:
        print("🔑 Generating new master key...")
        new_key = TokenEncryption.generate_master_key()
        print("✅ New master key generated")

        # Save new key to secure file
        key_file = Path.home() / ".proxmox_mcp_key"
        try:
            key_file.write_text(new_key)
            key_file.chmod(0o600)  # Owner read/write only
            print(f"🔐 New key saved securely to: {key_file}")
        except Exception as e:
            print(f"⚠️  Warning: Could not save key file: {e}")
            print("   Please save the key manually after rotation")
    else:
        print("🔑 Using provided new master key...")

    return new_key


def _perform_token_rotation(config_path: str, old_key: str, new_key: str) -> List[str]:
    """Perform the actual token rotation in a configuration file.

    Args:
        config_path: Path to the configuration file
        old_key: Current master key for decryption
        new_key: New master key for encryption

    Returns:
        List of rotated field names
    """
    # Create encryptors
    old_encryptor = TokenEncryption(master_key=old_key)
    new_encryptor = TokenEncryption(master_key=new_key)

    # Load configuration
    with open(config_path) as f:
        config_data = json.load(f)

    # Track what was rotated
    rotated_fields: List[str] = []

    # Rotate token_value if encrypted
    if "auth" in config_data and "token_value" in config_data["auth"]:
        token_value = config_data["auth"]["token_value"]
        if isinstance(token_value, str) and token_value.startswith("enc:"):
            # Decrypt with old key and re-encrypt with new key
            decrypted_token = old_encryptor.decrypt_token(token_value)
            config_data["auth"]["token_value"] = new_encryptor.encrypt_token(decrypted_token)
            rotated_fields.append("auth.token_value")

    # Save rotated configuration
    with open(config_path, "w") as f:
        json.dump(config_data, f, indent=2)

    return rotated_fields


def _display_rotation_summary(
    config_path: str, backup_path: str, rotated_fields: List[str]
) -> None:
    """Display rotation summary and next steps.

    Args:
        config_path: Path to the configuration file that was rotated
        backup_path: Path to the backup file created
        rotated_fields: List of field names that were rotated
    """
    print()
    print("🔒 Key rotation completed successfully!")
    print(f"   Configuration: {config_path}")
    print(f"   Backup: {backup_path}")
    if rotated_fields:
        print(f"   Rotated fields: {', '.join(rotated_fields)}")
    else:
        print("   No encrypted fields found to rotate")
    print()
    print("📋 Next steps:")
    print("   1. Update your environment with the new master key:")
    print("      export PROXMOX_MCP_MASTER_KEY=$(cat ~/.proxmox_mcp_key)")
    print("   2. Test the configuration:")
    print(f"      PROXMOX_MCP_CONFIG={config_path} python -m proxmox_mcp.server --test")
    print("   3. If successful, you can safely delete the backup file")
    print("   4. Update any other systems using the old key")
    print()


def rotate_master_key(config_path: str, new_key: Optional[str] = None) -> None:
    """Rotate master key for a single encrypted configuration file.

    Args:
        config_path: Path to the configuration file to rotate
        new_key: Optional new master key. If not provided, will generate one.
    """
    try:
        print(f"🔄 Starting key rotation for: {config_path}")
        print()

        # Validate environment and get old key
        old_key = _validate_rotation_environment(config_path)

        # Create backup
        print("💾 Creating backup...")
        backup_path = create_backup(config_path)
        print(f"✅ Backup created: {backup_path}")

        # Handle new key generation or validation
        new_key = _handle_new_key_generation(new_key)

        # Perform the actual token rotation
        rotated_fields = _perform_token_rotation(config_path, old_key, new_key)

        # Display summary and next steps
        _display_rotation_summary(config_path, backup_path, rotated_fields)

        # Offer to clear terminal for security
        clear_terminal_if_requested()

    except Exception as e:
        print(f"❌ Error during key rotation: {e}")
        sys.exit(1)


def _find_config_files(directory: str) -> List[str]:
    """Find all configuration files in a directory.

    Args:
        directory: Path to directory to search

    Returns:
        List of configuration file paths

    Raises:
        SystemExit: If directory doesn't exist or no files found
    """
    if not os.path.exists(directory):
        print(f"❌ Error: Directory not found: {directory}")
        sys.exit(1)

    if not os.path.isdir(directory):
        print(f"❌ Error: Path is not a directory: {directory}")
        sys.exit(1)

    # Find all JSON files in directory
    config_files: List[str] = []
    for file_path in Path(directory).rglob("*.json"):
        if not file_path.name.startswith("config.example"):  # Skip example files
            config_files.append(str(file_path))

    if not config_files:
        print(f"❌ No configuration files found in: {directory}")
        sys.exit(1)

    return config_files


def _prepare_bulk_rotation(new_key: Optional[str]) -> str:
    """Prepare for bulk key rotation by generating or validating the new key.

    Args:
        new_key: Optional new master key. If None, will generate one.

    Returns:
        The new master key to use for all files
    """
    # Generate single new key for all files if not provided
    if new_key is None:
        print("🔑 Generating new master key for all configurations...")
        new_key = TokenEncryption.generate_master_key()
        print("✅ New master key generated")

        # Save new key to secure file
        key_file = Path.home() / ".proxmox_mcp_key"
        try:
            key_file.write_text(new_key)
            key_file.chmod(0o600)  # Owner read/write only
            print(f"🔐 New key saved securely to: {key_file}")
        except Exception as e:
            print(f"⚠️  Warning: Could not save key file: {e}")
            print("   Please save the key manually after rotation")

    return new_key


def _process_single_config(config_file: str, new_key: str) -> bool:
    """Process a single configuration file for bulk rotation.

    Args:
        config_file: Path to the configuration file
        new_key: New master key to use

    Returns:
        True if rotation was successful, False otherwise
    """
    try:
        print(f"📝 Processing: {os.path.basename(config_file)}")

        # Check if file has encrypted content
        with open(config_file) as f:
            config_data = json.load(f)

        has_encrypted_content = False
        if "auth" in config_data and "token_value" in config_data["auth"]:
            token_value = config_data["auth"]["token_value"]
            if isinstance(token_value, str) and token_value.startswith("enc:"):
                has_encrypted_content = True

        if not has_encrypted_content:
            print("   ⏭️  Skipping (no encrypted content)")
            return True  # Not an error, just nothing to do

        # Perform rotation
        rotate_master_key(config_file, new_key)
        print("   ✅ Rotated successfully")
        return True

    except Exception as e:
        print(f"   ❌ Failed: {e}")
        return False


def _display_bulk_summary(
    successful_rotations: List[str], failed_rotations: List[tuple[str, str]]
) -> None:
    """Display summary of bulk rotation results and next steps.

    Args:
        successful_rotations: List of successfully rotated file paths
        failed_rotations: List of tuples containing (file_path, error_message) for failed rotations
    """
    # Summary
    print("📊 Bulk rotation summary:")
    print(f"   ✅ Successful: {len(successful_rotations)}")
    print(f"   ❌ Failed: {len(failed_rotations)}")

    if successful_rotations:
        print("   Rotated files:")
        for rotated_file in successful_rotations:
            print(f"     • {rotated_file}")

    if failed_rotations:
        print("   Failed files:")
        for failed_file, error in failed_rotations:
            print(f"     • {failed_file}: {error}")

    if successful_rotations:
        print()
        print("📋 Next steps:")
        print("   1. Update your environment with the new master key:")
        print("      export PROXMOX_MCP_MASTER_KEY=$(cat ~/.proxmox_mcp_key)")
        print("   2. Test each rotated configuration")
        print("   3. If successful, delete backup files")
        print("   4. Update any other systems using the old key")
        print()


def rotate_master_key_all(directory: str, new_key: Optional[str] = None) -> None:
    """Rotate master key for all encrypted configuration files in a directory.

    Args:
        directory: Path to directory containing configuration files
        new_key: Optional new master key. If not provided, will generate one.
    """
    try:
        # Find all configuration files
        config_files = _find_config_files(directory)

        # Prepare for bulk rotation
        new_key = _prepare_bulk_rotation(new_key)

        print(f"🔄 Starting bulk key rotation in: {directory}")
        print(f"   Found {len(config_files)} configuration files")
        print()

        successful_rotations: List[str] = []
        failed_rotations: List[tuple[str, str]] = []

        # Process each file
        for config_file in config_files:
            if _process_single_config(config_file, new_key):
                successful_rotations.append(config_file)
            else:
                # Error details already printed by _process_single_config
                failed_rotations.append((config_file, "Processing failed"))
            print()

        # Display results summary
        _display_bulk_summary(successful_rotations, failed_rotations)

        # Offer to clear terminal for security if any files were rotated
        if successful_rotations:
            clear_terminal_if_requested()

    except Exception as e:
        print(f"❌ Error during bulk key rotation: {e}")
        sys.exit(1)


def _setup_argument_parser() -> argparse.ArgumentParser:
    """Set up and configure the command-line argument parser.

    Returns:
        Configured ArgumentParser instance
    """
    parser = argparse.ArgumentParser(
        description="Encrypt sensitive values in Proxmox MCP configuration files",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s config.json                    # Encrypt config.json
  %(prog)s config.json -o encrypted.json  # Encrypt to specific file
  %(prog)s --generate-key                 # Generate new master key
  %(prog)s config.json --status           # Show encryption status
  %(prog)s --rotate-key config.json       # Rotate master key for single config
  %(prog)s --rotate-key-all proxmox-config/  # Rotate master key for all configs in directory
        """,
    )

    parser.add_argument("config_file", nargs="?", help="Path to configuration file to encrypt")

    parser.add_argument(
        "-o",
        "--output",
        help="Output path for encrypted configuration (default: [config].encrypted.json)",
    )

    parser.add_argument(
        "--generate-key",
        action="store_true",
        help="Generate a new master key for encryption",
    )

    parser.add_argument(
        "--status",
        action="store_true",
        help="Show encryption status of configuration file",
    )

    parser.add_argument(
        "--rotate-key",
        action="store_true",
        help="Rotate master key for a single configuration file",
    )

    parser.add_argument(
        "--rotate-key-all",
        action="store_true",
        help="Rotate master key for all configuration files in a directory",
    )

    return parser


def _handle_command(args: argparse.Namespace, parser: argparse.ArgumentParser) -> None:
    """Handle the parsed command-line arguments and execute appropriate action.

    Args:
        args: Parsed command-line arguments
        parser: Argument parser instance for error reporting
    """
    # Handle generate key command
    if args.generate_key:
        generate_master_key()
        return

    # Handle key rotation commands
    if args.rotate_key_all:
        if not args.config_file:
            parser.error("Directory path required for --rotate-key-all")
        rotate_master_key_all(args.config_file)
        return

    if args.rotate_key:
        if not args.config_file:
            parser.error("Configuration file required for --rotate-key")
        rotate_master_key(args.config_file)
        return

    # Require config file for other operations
    if not args.config_file:
        parser.error("Configuration file required (or use --generate-key)")

    # Handle status command
    if args.status:
        show_encryption_status(args.config_file)
        return

    # Handle encryption
    encrypt_config(args.config_file, args.output)


def main() -> None:
    """Main command-line interface."""
    parser = _setup_argument_parser()
    args = parser.parse_args()
    _handle_command(args, parser)


if __name__ == "__main__":
    main()
