#!/usr/bin/env python3
"""
Complexity checking script for ProxmoxMCP
Checks code complexity using radon
"""

from pathlib import Path
import subprocess
import sys


def check_radon_installed():
    """Check if radon is installed"""
    try:
        subprocess.run(["radon", "--version"], capture_output=True, text=True, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def run_complexity_check():
    """Run complexity check on source code"""
    if not check_radon_installed():
        print("⚠️  Install radon for complexity checking: pip install radon")
        return 0

    src_path = Path("src")
    if not src_path.exists():
        print("ℹ️  No src/ directory found, skipping complexity check")
        return 0

    try:
        # Check complexity with minimum threshold B
        result = subprocess.run(
            ["radon", "cc", "src/", "--min", "B", "--show-complexity"],
            capture_output=True,
            text=True,
            check=False,
        )

        if result.stdout:
            print("📊 Complexity Analysis Results:")
            print(result.stdout)

            # Count high complexity functions
            lines = result.stdout.split("\n")
            high_complexity = [
                line
                for line in lines
                if any(grade in line for grade in ["C (", "D (", "E (", "F ("])
            ]

            if high_complexity:
                print(
                    f"\n⚠️  Found {len(high_complexity)} functions with high complexity (C or worse)"
                )
                print("Consider refactoring these functions to improve maintainability.")
                return 1
            else:
                print("\n✅ All functions have acceptable complexity (B or better)")
        else:
            print("✅ No complexity issues found")

        return 0

    except Exception as e:
        print(f"❌ Error running complexity check: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(run_complexity_check())
