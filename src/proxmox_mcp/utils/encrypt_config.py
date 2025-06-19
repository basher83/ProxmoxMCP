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
import subprocess
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
            # Security fix: Use safer subprocess call without shell=True
            # and validate the command to prevent injection
            if platform.system() == "Windows":
                clear_cmd = ["cls"]
            else:
                clear_cmd = ["clear"]

            try:
                # Use subprocess.run without shell=True for security
                # This prevents command injection vulnerabilities
                subprocess.run(clear_cmd, check=True, timeout=5)
                print("✅ Terminal cleared for security")
                print("💡 Consider also clearing your shell history if needed")
            except subprocess.TimeoutExpired:
                print("⚠️  Terminal clear command timed out")
                print("💡 Please clear terminal manually for security")
            except subprocess.CalledProcessError as e:
                print(f"⚠️  Could not clear terminal (exit code {e.returncode})")
                print("💡 Please clear terminal manually for security")
            except FileNotFoundError:
                print("⚠️  Terminal clear command not found")
                print("💡 Please clear terminal manually for security")
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


def rotate_master_key(config_path: str, new_key: Optional[str] = None) -> None:
    """Rotate master key for a single encrypted configuration file.

    Args:
        config_path: Path to the configuration file to rotate
        new_key: Optional new master key. If not provided, will generate one.
    """
    try:
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

        print(f"🔄 Starting key rotation for: {config_path}")
        print()

        # Verify old key works with current config
        print("🔍 Verifying current master key...")
        if not verify_config_decryption(config_path, old_key):
            print("❌ Error: Current master key cannot decrypt the configuration")
            print("   Please ensure PROXMOX_MCP_MASTER_KEY is set correctly")
            sys.exit(1)
        print("✅ Current master key verified")

        # Create backup
        print("💾 Creating backup...")
        backup_path = create_backup(config_path)
        print(f"✅ Backup created: {backup_path}")

        # Generate or use provided new key
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

        # Offer to clear terminal for security
        clear_terminal_if_requested()

    except Exception as e:
        print(f"❌ Error during key rotation: {e}")
        sys.exit(1)


def rotate_master_key_all(directory: str, new_key: Optional[str] = None) -> None:
    """Rotate master key for all encrypted configuration files in a directory.

    Args:
        directory: Path to directory containing configuration files
        new_key: Optional new master key. If not provided, will generate one.
    """
    try:
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
        print(f"🔄 Starting bulk key rotation in: {directory}")
        print(f"   Found {len(config_files)} configuration files")
        print()

        successful_rotations: List[str] = []
        failed_rotations: List[tuple[str, str]] = []

        # Rotate each file
        for config_file in config_files:
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
                    continue

                # Perform rotation
                rotate_master_key(config_file, new_key)
                successful_rotations.append(config_file)
                print("   ✅ Rotated successfully")

            except Exception as e:
                print(f"   ❌ Failed: {e}")
                failed_rotations.append((config_file, str(e)))

            print()

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

            # Offer to clear terminal for security
            clear_terminal_if_requested()

    except Exception as e:
        print(f"❌ Error during bulk key rotation: {e}")
        sys.exit(1)


def main() -> None:
    """Main command-line interface."""
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

    args = parser.parse_args()

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


if __name__ == "__main__":
    main()
