"""
Convenience development test runner.
"""

import subprocess
import sys


def main() -> int:
    return subprocess.call(
        [sys.executable, "-m", "pytest", "tests"]
    )


if __name__ == "__main__":
    raise SystemExit(main())
