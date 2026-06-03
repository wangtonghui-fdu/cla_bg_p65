P65 CLA BG portable executable package
======================================

Default start:
1. Double-click Start_P65_BG_UI.bat
2. Or double-click P65_BG_UI.exe

V3 features:
- "指定random.s仿真": put a file at custom_random/random.s, then click this
  button to run that exact source once.
- Failed result rows have a "重跑" button. It reruns the archived random.s from
  that failed output directory.
- Flow errors are shown in the UI log/status as short actionable messages
  instead of a PyInstaller unhandled-exception popup.

Important:
- Send/extract the whole cla_bg_p65_v3.0 folder. Do not copy only
  P65_BG_UI.exe.
- The package already includes the P65 Linux tools under p65_linux_tools/bin:
  as.bin, ld.bin, objcopy.bin, objdump.bin, and gen_ram_image.py.
- WSL itself is a Windows system dependency and is not included in this
  package. A blank PC still needs WSL installed and initialized.

This package keeps P65_BG_UI.exe as the default entry, and also keeps Python
scripts for debugging, command-line runs, and rebuilding the exe.

Important files:
- P65_BG_UI.exe
- Start_P65_BG_UI.bat
- p65_bg_ui.py
- run_p65_bg.py
- analyze_bg_mismatch.py
- config_p65.json
- ui_settings.json
- random_test/instr_generate/
- p65_linux_tools/bin/as.bin
- p65_linux_tools/bin/ld.bin
- p65_linux_tools/bin/objcopy.bin
- p65_linux_tools/bin/objdump.bin
- p65_linux_tools/bin/gen_ram_image.py
- cache/p65_bg_template/

Runtime requirements on another PC:
- WSL must be available.
- If WSL was just installed, run `wsl` once in PowerShell and finish Linux
  initialization before clicking the UI environment check.
- The UI uses non-login `bash -c` for WSL commands to avoid hanging on custom
  `.profile` or `.bashrc` startup prompts.
- If Linux `python3` is missing, install it manually inside WSL:
  `sudo apt update && sudo apt install -y python3`.
- Network/SSH must be able to reach the configured server.
- Remote sim directory must already have a runnable simv and BG trace enabled.
- PySide6 is not required when launching P65_BG_UI.exe.

Generated output:
- output/<timestamp>_random/
- output/ can be deleted before sharing the package.
