param()

$ErrorActionPreference = "Stop"

$Root = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $Root

$Bootstrap = @'
import importlib.util
import subprocess
import sys

missing = []
for package, module in (("PySide6-Essentials", "PySide6"), ("paramiko", "paramiko")):
    if importlib.util.find_spec(module) is None:
        missing.append(package)

if missing:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "--no-cache-dir", *missing])
'@

$Bootstrap | python -
python .\p65_bg_ui.py
