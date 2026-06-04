"""Install Python packages required by the P65 BG UI before launching it."""

from __future__ import annotations

import importlib.util
import subprocess
import sys


REQUIRED_PACKAGES = [
    ("PySide6-Essentials", "PySide6"),
    ("paramiko", "paramiko"),
]


def run(command: list[str]) -> None:
    print(" ".join(command), flush=True)
    subprocess.check_call(command)


def ensure_pip() -> None:
    result = subprocess.run(
        [sys.executable, "-m", "pip", "--version"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    if result.returncode == 0:
        return
    print("pip not found, running ensurepip...", flush=True)
    run([sys.executable, "-m", "ensurepip", "--upgrade"])


def main() -> int:
    print(f"Python: {sys.executable}", flush=True)
    ensure_pip()

    missing = [package for package, module in REQUIRED_PACKAGES if importlib.util.find_spec(module) is None]
    if not missing:
        print("Python dependencies are ready: PySide6, paramiko", flush=True)
        return 0

    print("Installing missing Python packages: " + ", ".join(missing), flush=True)
    run([sys.executable, "-m", "pip", "install", "--no-cache-dir", *missing])

    still_missing = [module for _package, module in REQUIRED_PACKAGES if importlib.util.find_spec(module) is None]
    if still_missing:
        print("ERROR: packages still missing after install: " + ", ".join(still_missing), flush=True)
        return 1

    print("Python dependencies installed successfully.", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
