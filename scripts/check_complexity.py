#!/usr/bin/env python3
"""
Complexity checking script for ProxmoxMCP
Checks code complexity using radon
"""

from pathlib import Path
import subprocess
import sys


def check_radon_installed() -> bool:
    """Check if radon is installed"""
    try:
        subprocess.run(["radon", "--version"], capture_output=True, text=True, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def _validate_prerequisites() -> bool:
    """Validate prerequisites for complexity checking"""
    if not check_radon_installed():
        print("⚠️  Install radon for complexity checking: pip install radon")
        return False

    src_path = Path("src")
    if not src_path.exists():
        print("ℹ️  No src/ directory found, skipping complexity check")
        return False

    return True


def _analyze_complexity_output(output: str) -> int:
    """Analyze complexity output and return result code"""
    if not output:
        print("✅ No complexity issues found")
        return 0

    print("📊 Complexity Analysis Results:")
    print(output)

    # Count high complexity functions
    lines = output.split("\n")
    high_complexity = [
        line for line in lines if any(grade in line for grade in ["C (", "D (", "E (", "F ("])
    ]

    if high_complexity:
        print(f"\n⚠️  Found {len(high_complexity)} functions with high complexity (C or worse)")
        print("Consider refactoring these functions to improve maintainability.")
        return 1

    print("\n✅ All functions have acceptable complexity (B or better)")
    return 0


def _run_radon_analysis() -> tuple[str | None, str | None]:
    """Run radon complexity analysis"""
    try:
        result = subprocess.run(
            ["radon", "cc", "src/", "--min", "B", "--show-complexity"],
            capture_output=True,
            text=True,
            check=False,
        )
        return result.stdout, None
    except Exception as e:
        return None, f"❌ Error running complexity check: {e}"


def run_complexity_check() -> int:
    """Run complexity check on source code"""
    if not _validate_prerequisites():
        return 0

    output, error = _run_radon_analysis()
    if error:
        print(error)
        return 1

    return _analyze_complexity_output(output or "")


if __name__ == "__main__":
    sys.exit(run_complexity_check())
