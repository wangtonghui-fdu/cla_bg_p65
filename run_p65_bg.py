#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import re
import shlex
import shutil
import subprocess
import sys
import time
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any

try:
    import paramiko
except Exception:  # pragma: no cover - handled at runtime
    paramiko = None


def app_dir() -> Path:
    if getattr(sys, "frozen", False):
        return Path(sys.executable).resolve().parent
    return Path(__file__).resolve().parent


SCRIPT_DIR = app_dir()
REPO_ROOT = SCRIPT_DIR.parent
DEFAULT_CONFIG = SCRIPT_DIR / "config_p65.json"

for stream in (sys.stdout, sys.stderr):
    if hasattr(stream, "reconfigure"):
        stream.reconfigure(encoding="utf-8", errors="replace")


@dataclass(frozen=True)
class RemoteConfig:
    host: str
    port: int
    user: str
    password: str
    connect_timeout: int
    template_dir: str
    sim_dir: str
    sim_setup_command: str
    sim_command: str
    trace_candidates: list[str]
    clean_before_sim: list[str]


def log(msg: str) -> None:
    print(msg, flush=True)


def load_config(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def target_name(cfg: dict[str, Any]) -> str:
    return str(cfg.get("target", "P65"))


def resolve_local_path(raw: str, base: Path = SCRIPT_DIR) -> Path:
    path = Path(raw)
    if path.is_absolute():
        return path
    return (base / path).resolve()


def remote_from_config(cfg: dict[str, Any]) -> RemoteConfig:
    ssh = cfg["ssh"]
    remote = cfg["remote"]
    return RemoteConfig(
        host=str(ssh["host"]),
        port=int(ssh.get("port", 22)),
        user=str(ssh["user"]),
        password=str(ssh.get("password", "")),
        connect_timeout=int(ssh.get("connect_timeout", 10)),
        template_dir=str(remote["template_dir"]).rstrip("/"),
        sim_dir=str(remote["sim_dir"]).rstrip("/"),
        sim_setup_command=str(remote.get("sim_setup_command", "")),
        sim_command=str(remote["sim_command"]),
        trace_candidates=[str(item) for item in remote.get("trace_candidates", [])],
        clean_before_sim=[str(item) for item in remote.get("clean_before_sim", [])],
    )


def connect(remote: RemoteConfig):
    if paramiko is None:
        raise RuntimeError("paramiko is required for SSH/SFTP. Install it or run inside the existing packaged environment.")
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(
        hostname=remote.host,
        port=remote.port,
        username=remote.user,
        password=remote.password or None,
        look_for_keys=False if remote.password else True,
        allow_agent=False if remote.password else True,
        timeout=remote.connect_timeout,
        banner_timeout=max(remote.connect_timeout, 60),
        auth_timeout=max(remote.connect_timeout, 30),
    )
    return client


def run_remote(client, command: str, timeout: int | None = None, stream_label: str | None = None) -> tuple[int, str]:
    # Do not set a Paramiko channel timeout here. VCS can be silent for long
    # stretches, and the remote `timeout` wrapper is the authority for stopping
    # the simulator.
    stdin, stdout, stderr = client.exec_command(f"bash -lc {shell_quote(command)}", get_pty=True)
    stdin.close()
    chunks: list[str] = []
    for raw in iter(stdout.readline, ""):
        chunks.append(raw)
        if stream_label:
            log(f"[{stream_label}] {raw.rstrip()}")
    err = stderr.read().decode("utf-8", errors="replace")
    if err:
        chunks.append(err)
        if stream_label:
            for line in err.splitlines():
                log(f"[{stream_label}] {line}")
    code = stdout.channel.recv_exit_status()
    return code, "".join(chunks)


def shell_quote(text: str) -> str:
    return "'" + text.replace("'", "'\"'\"'") + "'"


def sftp_is_dir(sftp, remote_path: str) -> bool:
    try:
        return bool(sftp.stat(remote_path).st_mode & 0o040000)
    except OSError:
        return False


def sftp_download_dir(sftp, remote_dir: str, local_dir: Path) -> None:
    local_dir.mkdir(parents=True, exist_ok=True)
    for entry in sftp.listdir_attr(remote_dir):
        remote_child = f"{remote_dir.rstrip('/')}/{entry.filename}"
        local_child = local_dir / entry.filename
        if entry.st_mode & 0o040000:
            sftp_download_dir(sftp, remote_child, local_child)
        else:
            local_child.parent.mkdir(parents=True, exist_ok=True)
            sftp.get(remote_child, str(local_child))


def bootstrap_template(cfg: dict[str, Any], force: bool = False) -> Path:
    remote = remote_from_config(cfg)
    cache_dir = resolve_local_path(cfg["local"]["template_cache_dir"])
    marker = cache_dir / ".bootstrap_complete"
    staging_dir = cache_dir.parent / f"{cache_dir.name}_bootstrap_tmp"
    required_dirs = [str(item) for item in cfg["bootstrap"]["required_dirs"]]
    optional_dirs = [str(item) for item in cfg["bootstrap"].get("optional_dirs", [])]

    if staging_dir.exists():
        shutil.rmtree(staging_dir)
    if cache_dir.exists() and (force or not marker.exists()):
        shutil.rmtree(cache_dir)
    if cache_dir.exists() and marker.exists() and not force:
        validate_template(cache_dir, required_dirs)
        log(f"Template cache already exists: {cache_dir}")
        return cache_dir
    staging_dir.mkdir(parents=True, exist_ok=True)

    log(f"Bootstrap template from {remote.user}@{remote.host}:{remote.template_dir}")
    client = connect(remote)
    try:
        sftp = client.open_sftp()
        try:
            for name in required_dirs + optional_dirs:
                src = f"{remote.template_dir}/{name}"
                dst = cache_dir / name
                if not sftp_is_dir(sftp, src):
                    if name in required_dirs:
                        raise RuntimeError(f"Remote required template directory is missing: {src}")
                    log(f"Optional remote directory missing, skipped: {src}")
                    continue
                dst = staging_dir / name
                log(f"Downloading {src} -> {dst}")
                sftp_download_dir(sftp, src, dst)
        finally:
            sftp.close()
    finally:
        client.close()

    validate_template(staging_dir, required_dirs, require_marker=False)
    marker.parent.mkdir(parents=True, exist_ok=True)
    if cache_dir.exists():
        shutil.rmtree(cache_dir)
    staging_dir.rename(cache_dir)
    marker.write_text(datetime.now().isoformat(timespec="seconds") + "\n", encoding="utf-8")
    validate_template(cache_dir, required_dirs)
    return cache_dir


def validate_template(cache_dir: Path, required_dirs: list[str], require_marker: bool = True) -> None:
    marker = cache_dir / ".bootstrap_complete"
    if require_marker and cache_dir.exists() and not marker.exists():
        raise RuntimeError(
            f"Template cache looks incomplete: {cache_dir}\n"
            f"Run: python {SCRIPT_DIR / 'run_p65_bg.py'} --bootstrap"
        )
    missing = [name for name in required_dirs if not (cache_dir / name).is_dir()]
    if missing:
        raise RuntimeError(
            "Template cache is incomplete. Missing: "
            + ", ".join(missing)
            + f"\nRun: python {SCRIPT_DIR / 'run_p65_bg.py'} --bootstrap"
        )
    for release in ("Release_wo", "Release_w"):
        release_dir = cache_dir / release
        if not any(release_dir.rglob("*.o")):
            raise RuntimeError(f"No object files found in template release: {release_dir}")


def command_output_tail(text: str, max_lines: int = 20) -> str:
    lines = [line.rstrip() for line in text.splitlines() if line.strip()]
    if not lines:
        return ""
    return "\n".join(lines[-max_lines:])


def run_checked(cmd: list[str], cwd: Path | None = None, env: dict[str, str] | None = None, label: str = "command") -> None:
    log(f"[{label}] {subprocess.list2cmdline([str(part) for part in cmd])}")
    run_env = os.environ.copy()
    if env:
        run_env.update(env)
    run_env["PYTHONIOENCODING"] = "utf-8"
    proc = subprocess.run(
        [str(part) for part in cmd],
        cwd=str(cwd) if cwd else None,
        env=run_env,
        text=True,
        encoding="utf-8",
        errors="replace",
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    if proc.stdout:
        print(proc.stdout, end="" if proc.stdout.endswith("\n") else "\n")
    if proc.returncode != 0:
        tail = command_output_tail(proc.stdout or "")
        detail = f"\n{tail}" if tail else ""
        raise RuntimeError(f"{label} failed with exit code {proc.returncode}{detail}")


def python_script_command(script: Path | str) -> list[str]:
    if getattr(sys, "frozen", False):
        return [sys.executable, "--run-python-script", str(script)]
    return [sys.executable, str(script)]


def local_build_backend(cfg: dict[str, Any]) -> str:
    return str(cfg["local"].get("build_backend", "windows")).lower()


def windows_to_wsl_path(path: Path | str) -> str:
    resolved = Path(path).resolve()
    raw = str(resolved)
    if len(raw) >= 3 and raw[1] == ":" and raw[2] in ("\\", "/"):
        drive = raw[0].lower()
        rest = raw[3:].replace("\\", "/")
        return f"/mnt/{drive}/{rest}"
    return raw.replace("\\", "/")


def run_wsl_checked(cmd: list[str], cwd: Path | None = None, label: str = "wsl command") -> None:
    command = " ".join(shlex.quote(str(part)) for part in cmd)
    if cwd is not None:
        command = f"cd {shlex.quote(windows_to_wsl_path(cwd))} && {command}"
    log(f"[{label}] wsl -e bash -c {command}")
    proc = subprocess.run(
        ["wsl", "-e", "bash", "-c", command],
        text=True,
        encoding="utf-8",
        errors="replace",
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    if proc.stdout:
        print(proc.stdout, end="" if proc.stdout.endswith("\n") else "\n")
    if proc.returncode != 0:
        tail = command_output_tail(proc.stdout or "")
        detail = f"\n{tail}" if tail else ""
        raise RuntimeError(f"{label} failed with exit code {proc.returncode}{detail}")


def generate_random(cfg: dict[str, Any], case_name: str, instr_count: int, run_dir: Path) -> Path:
    random_test_dir = resolve_local_path(cfg["local"]["random_test_dir"])
    gen_dir = random_test_dir / "instr_generate"
    output_dir = run_dir / "generated"
    env = os.environ.copy()
    env["QX_TEST_CLA"] = "1"
    env["QX_DISABLE_CLA_ADDR_REGS"] = "1"
    env["QX_OUTPUT_DIR"] = str(output_dir)
    run_checked(
        [*python_script_command(gen_dir / "main.py"), case_name, str(instr_count)],
        cwd=gen_dir,
        env=env,
        label="generate random.s",
    )
    generated = output_dir / f"{case_name}.s"
    if not generated.exists():
        raise RuntimeError(f"Random generator did not produce: {generated}")
    return generated


def prepare_bg_source(cfg: dict[str, Any], source_s: Path, run_dir: Path, case_name: str) -> Path:
    """Create the BG upload-style source used by the original random_test flow."""
    random_copy = run_dir / f"{case_name}.s"
    text = source_s.read_text(encoding="utf-8", errors="replace")
    lines = text.splitlines()
    if any(".=1024" in line for line in lines):
        random_copy.write_text(text, encoding="utf-8", errors="replace")
        return random_copy

    body_start = None
    for i, line in enumerate(lines):
        if line.strip() == "main:":
            body_start = i + 1
            break
    if body_start is None:
        raise RuntimeError(f"Source has neither '.=1024' nor a 'main:' label: {source_s}")

    random_test_dir = resolve_local_path(cfg["local"]["random_test_dir"])
    start2 = random_test_dir / "instr_generate" / "txt" / "start2.s"
    if not start2.exists():
        raise RuntimeError(f"Missing start2 template: {start2}")
    body = "\n".join(lines[body_start:])
    random_copy.write_text(
        start2.read_text(encoding="utf-8", errors="replace").rstrip() + "\n\n" + body + "\n",
        encoding="utf-8",
    )
    return random_copy


def prepare_task8(cfg: dict[str, Any], source_s: Path, run_dir: Path, case_name: str) -> tuple[Path, Path]:
    random_copy = prepare_bg_source(cfg, source_s, run_dir, case_name)

    lines = random_copy.read_text(encoding="utf-8", errors="replace").splitlines()
    start_idx = 0
    for i, line in enumerate(lines):
        if ".=1024" in line:
            start_idx = i + 1
            break
    body_lines = lines[start_idx:]
    if cfg["local"].get("unpack_pipes", False):
        body_lines = unpack_parallel_instruction_lines(body_lines)
    body = "\n".join(body_lines)
    if body and not body.endswith("\n"):
        body += "\n"
    task8 = run_dir / "task8.s"
    trailer = "nop||\nnop||\nnop||\nmstop||\nnop||\n" if cfg["local"].get("append_task8_trailer", True) else ""
    task8.write_text(
        ".global task8\n"
        ".section .cla_text\n"
        "task8:\n"
        f"{body}"
        f"{trailer}",
        encoding="ascii",
        errors="ignore",
    )
    return random_copy, task8


def unpack_parallel_instruction_lines(lines: list[str]) -> list[str]:
    unpacked: list[str] = []
    for line in lines:
        stripped = line.strip()
        if not stripped or stripped.startswith(("#", ".", "//")) or stripped.endswith(":"):
            unpacked.append(line)
            continue
        code, sep, comment = line.partition("#")
        parts = [part.strip() for part in code.replace("||", "|").split("|") if part.strip()]
        suffix = f" #{comment}" if sep else ""
        if len(parts) <= 1:
            if parts:
                unpacked.append(f"{format_single_slot_line(parts[0])}{suffix}")
            else:
                unpacked.append(line)
            continue
        unpacked.extend(f"{format_single_slot_line(part)}{suffix if idx == len(parts) - 1 else ''}" for idx, part in enumerate(parts))
    return unpacked


def format_single_slot_line(instruction: str) -> str:
    mnemonic = instruction.split(None, 1)[0].lower() if instruction.split(None, 1) else ""
    if mnemonic.startswith("load"):
        return f"nop|{instruction}|nop"
    if mnemonic.startswith("store"):
        return f"nop||{instruction}"
    return f"{instruction}||"


def copy_template_to_work(cache_dir: Path, run_dir: Path) -> Path:
    work_dir = run_dir / "work"
    if work_dir.exists():
        shutil.rmtree(work_dir)
    work_dir.mkdir(parents=True)
    for name in ("ldscript", "libv2", "Release_wo", "Release_w"):
        shutil.copytree(cache_dir / name, work_dir / name)
    # The P65 linker script uses plain INCLUDE directives, and this linker
    # resolves those from the release cwd rather than the script directory.
    for release in ("Release_wo", "Release_w"):
        for script in (work_dir / "ldscript").glob("ldscript_*.ld"):
            shutil.copy2(script, work_dir / release / script.name)
    return work_dir


def assemble_task8(cfg: dict[str, Any], task8: Path, work_dir: Path) -> None:
    if local_build_backend(cfg) == "wsl":
        linux_tool_dir = resolve_local_path(cfg["local"]["linux_tool_dir"])
        assembler = linux_tool_dir / "bin" / str(cfg["local"].get("assembler", "as.bin"))
        if not assembler.exists():
            raise RuntimeError(f"Missing assembler: {assembler}")
        assembler_args = [str(item) for item in cfg["local"].get("assembler_args", ["-c"])]
        for release in ("Release_wo", "Release_w"):
            run_wsl_checked(
                [windows_to_wsl_path(assembler), windows_to_wsl_path(task8), *assembler_args, "-o", "task8.o"],
                cwd=work_dir / release,
                label=f"assemble {release}/task8.o",
            )
        return

    toolchain = resolve_local_path(cfg["local"]["toolchain_dir"])
    assembler = toolchain / "bin" / str(cfg["local"].get("assembler", "as.exe"))
    if not assembler.exists():
        raise RuntimeError(f"Missing assembler: {assembler}")
    assembler_args = [str(item) for item in cfg["local"].get("assembler_args", ["-c"])]
    for release in ("Release_wo", "Release_w"):
        run_checked(
            [assembler, task8, *assembler_args, "-o", work_dir / release / "task8.o"],
            label=f"assemble {release}/task8.o",
        )


def link_release(cfg: dict[str, Any], work_dir: Path, release: str) -> None:
    if local_build_backend(cfg) == "wsl":
        linux_tool_dir = resolve_local_path(cfg["local"]["linux_tool_dir"])
        linker = linux_tool_dir / "bin" / str(cfg["local"].get("linker", "ld.bin"))
        if not linker.exists():
            raise RuntimeError(f"Missing linker: {linker}")
        release_dir = work_dir / release
        object_files = sorted(path.relative_to(release_dir).as_posix() for path in release_dir.rglob("*.o"))
        if not object_files:
            raise RuntimeError(f"No object files found in {release_dir}")
        project_out = cfg["local"].get("project_out", "F28P6x_driver_core0.out")
        project_map = cfg["local"].get("project_map", "F28P6x_driver_core0.map")
        link_script = cfg["local"].get("link_script", "ldscript_DSPCore0.ld")
        link_libraries = [str(item) for item in cfg["local"].get("link_libraries", [
            "-lfastrt_fpu32v2",
            "-lqxboot",
            "-lprintf",
            "-lm",
            "-lc",
            "-lrt",
            "-ldspsim",
        ])]
        cmd = [
            windows_to_wsl_path(linker),
            "-L",
            "../ldscript",
            "-L",
            "../libv2",
            "-T",
            link_script,
            "-Map=linkMapFile",
            "--no-check-sections",
            "--gc-sections",
            f"-Map={project_map}",
            "--no-check-sections",
            "--gc-sections",
            "-o",
            project_out,
            *object_files,
            *link_libraries,
        ]
        run_wsl_checked(cmd, cwd=release_dir, label=f"link {release}")
        return

    toolchain = resolve_local_path(cfg["local"]["toolchain_dir"])
    linker = toolchain / "bin" / str(cfg["local"].get("linker", "ld.exe"))
    if not linker.exists():
        raise RuntimeError(f"Missing linker: {linker}")
    release_dir = work_dir / release
    object_files = sorted(str(path.relative_to(release_dir)) for path in release_dir.rglob("*.o"))
    if not object_files:
        raise RuntimeError(f"No object files found in {release_dir}")
    project_out = cfg["local"].get("project_out", "F28P6x_driver_core0.out")
    project_map = cfg["local"].get("project_map", "F28P6x_driver_core0.map")
    link_script = cfg["local"].get("link_script", "../ldscript/ldscript_DSPCore0.ld")
    link_libraries = [str(item) for item in cfg["local"].get("link_libraries", [
        "-lfastrt_fpu32v2",
        "-lqxboot",
        "-lprintf",
        "-lm",
        "-lc",
        "-lrt",
        "-ldspsim",
    ])]
    cmd = [
        linker,
        "-L",
        "../ldscript",
        "-L",
        "../libv2",
        "-T",
        link_script,
        "-Map=linkMapFile",
        "--no-check-sections",
        "--gc-sections",
        f"-Map={project_map}",
        "--no-check-sections",
        "--gc-sections",
        "-o",
        project_out,
        *object_files,
        *link_libraries,
    ]
    run_checked(cmd, cwd=release_dir, label=f"link {release}")


def generate_images(cfg: dict[str, Any], work_dir: Path, release: str) -> None:
    if local_build_backend(cfg) == "wsl":
        linux_tool_dir = resolve_local_path(cfg["local"]["linux_tool_dir"])
        gen_script = linux_tool_dir / "bin" / "gen_ram_image.py"
        if not gen_script.exists():
            raise RuntimeError(f"Missing gen_ram_image.py: {gen_script}")
        release_dir = work_dir / release
        project_out = cfg["local"].get("project_out", "F28P6x_driver_core0.out")
        run_wsl_checked(
            [
                "python3",
                windows_to_wsl_path(gen_script),
                "--coretype",
                "core0",
                "--inputexec",
                project_out,
                "--toolbinpath",
                windows_to_wsl_path(linux_tool_dir / "bin"),
                "--linux",
            ],
            cwd=release_dir,
            label=f"generate images {release}",
        )
        required = ["dram_image.core0.dat", "iram_image.core0.dat", "dram_image.cla0.dat", "iram_image.cla0.dat"]
        missing = [name for name in required if not (release_dir / name).exists()]
        if missing:
            raise RuntimeError(f"Image generation for {release} missed: {', '.join(missing)}")
        return

    toolchain = resolve_local_path(cfg["local"]["toolchain_dir"])
    gen_script = toolchain / "bin" / "gen_ram_image.py"
    if not gen_script.exists():
        raise RuntimeError(f"Missing gen_ram_image.py: {gen_script}")
    release_dir = work_dir / release
    project_out = cfg["local"].get("project_out", "F28P6x_driver_core0.out")
    run_checked(
        [
            *python_script_command(gen_script),
            "--coretype",
            "core0",
            "--inputexec",
            project_out,
            "--toolbinpath",
            str(toolchain / "bin"),
        ],
        cwd=release_dir,
        label=f"generate images {release}",
    )
    required = ["dram_image.core0.dat", "iram_image.core0.dat", "dram_image.cla0.dat", "iram_image.cla0.dat"]
    missing = [name for name in required if not (release_dir / name).exists()]
    if missing:
        raise RuntimeError(f"Image generation for {release} missed: {', '.join(missing)}")


def reference_sim_cfg(cfg: dict[str, Any]) -> dict[str, Any]:
    ref = cfg.get("local", {}).get("reference_sim", {})
    if not isinstance(ref, dict):
        ref = {}
    return {
        "enabled": bool(ref.get("enabled", False)),
        "dir": str(ref.get("dir", "reference_sim")),
        "sim_config": str(ref.get("sim_config", "-c qx320f034 --cla")),
        "exclude_regs": [int(item) for item in ref.get("exclude_regs", [0, 30, 31])],
        "compare_to_wo": bool(ref.get("compare_to_wo", True)),
    }


def validate_reference_sim_root(sim_root: Path) -> dict[str, Path]:
    paths = {
        "assembler": sim_root / "toolchains" / "bin" / "as.bin",
        "linker": sim_root / "toolchains" / "bin" / "ld.bin",
        "link_script": sim_root / "toolchains" / "lib" / "qx320f" / "link_8slots.ld",
        "main_sim": sim_root / "toolchains" / "lib" / "qx320f" / "_main_sim.o",
        "lib_dir": sim_root / "toolchains" / "lib" / "qx320f" / "fp64",
        "dat_script": sim_root / "toolchains" / "test" / "scripts" / "trobjdat_8slot.py",
        "tools_dir": sim_root / "toolchains" / "tools",
        "objcopy": sim_root / "toolchains" / "tools" / "objcopy.bin",
        "simulator": sim_root / "simulator" / "simulator_step13",
    }
    missing = [str(path) for path in paths.values() if not path.exists()]
    if missing:
        raise RuntimeError("Reference simulator files are missing:\n" + "\n".join(missing))
    return paths


def prepare_reference_link_script(paths: dict[str, Path], tmp_dir: Path) -> Path:
    raw = paths["link_script"].read_text(encoding="utf-8", errors="replace")
    main_sim = windows_to_wsl_path(paths["main_sim"])
    patched = re.sub(r"STARTUP\([^)]*_main_sim\.o\)", f"STARTUP({main_sim})", raw)
    if patched == raw and "_main_sim.o" not in raw:
        patched = raw.replace("ENTRY(_main)", f"STARTUP({main_sim})\nENTRY(_main)", 1)
    portable = tmp_dir / "link_8slots.portable.ld"
    portable.write_text(patched, encoding="utf-8", errors="replace")
    return portable


def extract_reference_gr_trace(sim_log: Path, gr_trace: Path, exclude_regs: list[int]) -> int:
    write_pattern = re.compile(r"^\s*write gr(\d+)\s*=\s*0x([0-9a-fA-F]+)")
    pc_pattern = re.compile(r"PC\s*=\s*0x([0-9a-fA-F]+)")
    lines = sim_log.read_text(encoding="utf-8", errors="replace").splitlines()
    rows: list[str] = []
    excluded = set(exclude_regs)

    for idx, line in enumerate(lines):
        match = write_pattern.match(line.strip())
        if not match:
            continue
        reg_num = int(match.group(1))
        if reg_num in excluded or not 0 <= reg_num <= 31:
            continue
        value = int(match.group(2), 16)
        pc_val: int | None = None
        for next_line in lines[idx + 1 :]:
            pc_match = pc_pattern.search(next_line)
            if pc_match:
                pc_val = int(pc_match.group(1), 16)
                break
        if pc_val is None:
            rows.append(f"0x{reg_num:02x}\t0x{value:08x}\t0x00000000")
        else:
            rows.append(f"0x{reg_num:02x}\t0x{value:08x}\t0x{pc_val:08x}")

    gr_trace.write_text("\n".join(rows) + ("\n" if rows else ""), encoding="utf-8")
    return len(rows)


def compare_reference_to_rtl(ref_path: Path, rtl_path: Path, compare_path: Path) -> dict[str, Any]:
    def parse_reg_value(path: Path) -> list[tuple[str, str]]:
        rows: list[tuple[str, str]] = []
        for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
            parts = line.strip().split()
            if len(parts) >= 2:
                try:
                    reg_num = int(parts[0], 16)
                except ValueError:
                    continue
                if reg_num in (0, 30, 31) or not 0 <= reg_num <= 31:
                    continue
                rows.append((f"0x{reg_num:02x}", parts[1].lower()))
        return rows

    def find_reference_start(ref_rows: list[tuple[str, str]], rtl_rows: list[tuple[str, str]]) -> tuple[int, int]:
        best_offset = 0
        best_match = 0
        for offset in range(len(ref_rows)):
            matched = 0
            while (
                matched < len(rtl_rows)
                and offset + matched < len(ref_rows)
                and ref_rows[offset + matched] == rtl_rows[matched]
            ):
                matched += 1
            if matched > best_match:
                best_offset = offset
                best_match = matched
        threshold = min(8, len(rtl_rows))
        if best_match >= threshold:
            return best_offset, best_match
        return 0, best_match

    ref_rows = parse_reg_value(ref_path)
    rtl_rows = parse_reg_value(rtl_path)
    ref_start, prefix_match = find_reference_start(ref_rows, rtl_rows)
    aligned_ref_rows = ref_rows[ref_start:]
    count = min(len(aligned_ref_rows), len(rtl_rows))
    mismatches: list[str] = []
    first_mismatch_line = 0
    for idx in range(count):
        if aligned_ref_rows[idx] == rtl_rows[idx]:
            continue
        if first_mismatch_line == 0:
            first_mismatch_line = idx + 1
        ref_line = ref_start + idx + 1
        mismatches.append(
            f"line {idx + 1} (ref line {ref_line}): "
            f"REF={aligned_ref_rows[idx][0]} {aligned_ref_rows[idx][1]} | "
            f"RTL={rtl_rows[idx][0]} {rtl_rows[idx][1]}"
        )
    if len(aligned_ref_rows) != len(rtl_rows):
        if first_mismatch_line == 0:
            first_mismatch_line = count + 1
        mismatches.append(f"row count differs after alignment: REF={len(aligned_ref_rows)} RTL={len(rtl_rows)}")

    lines = [
        "=" * 80,
        "Reference simulator vs RTL WO trace",
        "=" * 80,
        f"Reference trace: {ref_path}",
        f"RTL WO trace   : {rtl_path}",
        "Comparison method: first 2 whitespace-separated columns (GR index + value), after filtering GR0/GR30/GR31 and aligning reference startup rows",
        "",
        f"RESULT: {'PASS' if not mismatches else 'FAIL'}",
        f"Total lines compared: {count}",
        f"Reference rows: {len(ref_rows)}",
        f"Reference startup rows skipped: {ref_start}",
        f"Reference prefix match rows: {prefix_match}",
        f"Aligned reference rows: {len(aligned_ref_rows)}",
        f"RTL WO rows: {len(rtl_rows)}",
        f"Number of mismatches: {len(mismatches)}",
    ]
    if mismatches:
        lines.extend(["", "Detailed Mismatch Information:", "-" * 80])
        lines.extend(f"{i}. {msg}" for i, msg in enumerate(mismatches, 1))
    compare_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return {
        "pass": not mismatches,
        "lines_compared": count,
        "reference_rows": len(ref_rows),
        "reference_startup_rows_skipped": ref_start,
        "reference_prefix_match_rows": prefix_match,
        "aligned_reference_rows": len(aligned_ref_rows),
        "rtl_wo_rows": len(rtl_rows),
        "mismatches": len(mismatches),
        "first_mismatch_line": first_mismatch_line,
        "compare_log": str(compare_path),
    }


def run_reference_simulator(
    cfg: dict[str, Any],
    source_s: Path,
    run_dir: Path,
    case_name: str,
    strict: bool = False,
) -> dict[str, Any]:
    ref_cfg = reference_sim_cfg(cfg)
    if not ref_cfg["enabled"]:
        return {"status": "disabled"}

    sim_root = resolve_local_path(ref_cfg["dir"])
    result: dict[str, Any] = {
        "status": "pending",
        "root": str(sim_root),
    }
    try:
        paths = validate_reference_sim_root(sim_root)
        sim_work = run_dir / "reference_sim"
        test_dir = sim_work / "test"
        tmp_dir = sim_work / "tmp"
        test_dir.mkdir(parents=True, exist_ok=True)
        tmp_dir.mkdir(parents=True, exist_ok=True)

        sim_source = test_dir / f"{case_name}.s"
        shutil.copy2(source_s, sim_source)
        portable_link_script = prepare_reference_link_script(paths, tmp_dir)
        log(f"----- reference simulator ({case_name}) -----")
        log(f"reference source: {sim_source}")

        run_wsl_checked(
            [
                "chmod",
                "+x",
                windows_to_wsl_path(paths["assembler"]),
                windows_to_wsl_path(paths["linker"]),
                windows_to_wsl_path(paths["objcopy"]),
                windows_to_wsl_path(paths["simulator"]),
            ],
            label="prepare reference simulator tools",
        )
        run_wsl_checked(
            [
                windows_to_wsl_path(paths["assembler"]),
                "-c",
                f"./test/{case_name}.s",
                "-o",
                f"./tmp/{case_name}.o",
            ],
            cwd=sim_work,
            label="reference assemble",
        )
        run_wsl_checked(
            [
                windows_to_wsl_path(paths["linker"]),
                "-T",
                windows_to_wsl_path(portable_link_script),
                "-L",
                windows_to_wsl_path(paths["lib_dir"]),
                f"./tmp/{case_name}.o",
                "-o",
                f"./tmp/{case_name}.out",
                "-lm",
                "-lc",
                "-lrt",
                "-ldspsim",
                "-ldbgsim",
            ],
            cwd=sim_work,
            label="reference link",
        )
        run_wsl_checked(
            [
                "python3",
                windows_to_wsl_path(paths["dat_script"]),
                f"./tmp/{case_name}.out",
                windows_to_wsl_path(paths["tools_dir"]),
            ],
            cwd=sim_work,
            label="reference generate dat",
        )
        sim_args = shlex.split(str(ref_cfg["sim_config"]))
        run_wsl_checked(
            [
                windows_to_wsl_path(paths["simulator"]),
                *sim_args,
                f"./{case_name}.dat",
                "-l",
            ],
            cwd=tmp_dir,
            label="reference simulator",
        )

        sim_log = tmp_dir / "simulator.log"
        if not sim_log.exists():
            raise RuntimeError(f"Reference simulator did not generate {sim_log}")
        archived_log = run_dir / "reference_simulator.log"
        shutil.copy2(sim_log, archived_log)
        gr_trace = run_dir / "reference_sim.gr"
        rows = extract_reference_gr_trace(sim_log, gr_trace, list(ref_cfg["exclude_regs"]))
        result.update(
            {
                "status": "pass",
                "work_dir": str(sim_work),
                "source": str(sim_source),
                "log": str(archived_log),
                "trace": str(gr_trace),
                "rows": rows,
                "exclude_regs": ref_cfg["exclude_regs"],
                "sim_config": ref_cfg["sim_config"],
            }
        )
        log(f"reference simulator trace: {gr_trace} ({rows} rows)")
        return result
    except Exception as exc:
        result.update({"status": "error", "error": str(exc)})
        error_log = run_dir / "reference_sim_error.log"
        error_log.write_text(str(exc) + "\n", encoding="utf-8", errors="replace")
        log(f"WARNING: reference simulator failed: {exc}")
        if strict:
            raise
        return result


def build_dual(cfg: dict[str, Any], cache_dir: Path, task8: Path, run_dir: Path) -> Path:
    work_dir = copy_template_to_work(cache_dir, run_dir)
    assemble_task8(cfg, task8, work_dir)
    for release in ("Release_wo", "Release_w"):
        link_release(cfg, work_dir, release)
        generate_images(cfg, work_dir, release)
    return work_dir


def upload_release_images(client, cfg: dict[str, Any], remote: RemoteConfig, release_dir: Path) -> None:
    sftp = client.open_sftp()
    try:
        upload_bootloader_images(sftp, cfg, remote)
        for item in cfg["uploads"]:
            local_path = release_dir / item["local"]
            if not local_path.exists():
                raise RuntimeError(f"Upload source missing: {local_path}")
            remote_path = f"{remote.sim_dir}/{item['remote']}"
            log(f"upload {local_path.name} -> {remote_path}")
            sftp.put(str(local_path), remote_path)
    finally:
        sftp.close()


def default_bootloader_candidates(name: str) -> list[Path]:
    return [
        SCRIPT_DIR / "IDE" / "software_lib_driver_28P6x" / "software_lib_driver_28P6x" / "bootloader" / "Release" / name,
        SCRIPT_DIR / "software_lib_driver_28P6x" / "software_lib_driver_28P6x" / "bootloader" / "Release" / name,
        REPO_ROOT / "cla_bg_p65_local" / "software_lib_driver_28P6x" / "software_lib_driver_28P6x" / "bootloader" / "Release" / name,
    ]


def resolve_bootloader_uploads(cfg: dict[str, Any]) -> list[tuple[Path | None, str]]:
    configured = cfg.get("bootloader_uploads")
    if configured:
        uploads: list[tuple[Path | None, str]] = []
        for item in configured:
            local_path = resolve_local_path(str(item["local"]))
            uploads.append((local_path, str(item.get("remote", local_path.name))))
        return uploads

    name = "core0.iram_image.bootloader.dat"
    for candidate in default_bootloader_candidates(name):
        if candidate.exists():
            return [(candidate, name)]
    return [(None, name)]


def upload_bootloader_images(sftp, cfg: dict[str, Any], remote: RemoteConfig) -> None:
    for local_path, remote_name in resolve_bootloader_uploads(cfg):
        if local_path is None or not local_path.exists():
            log(f"warning: local bootloader missing, keep remote existing: {remote_name}")
            continue
        remote_path = f"{remote.sim_dir}/{remote_name}"
        log(f"upload {local_path.name} -> {remote_path}")
        sftp.put(str(local_path), remote_path)


def clean_remote_trace(client, remote: RemoteConfig) -> None:
    if not remote.clean_before_sim:
        return
    log(f"clean remote traces in {remote.sim_dir}")
    files = " ".join(shell_quote(f"{remote.sim_dir}/{name}") for name in remote.clean_before_sim)
    code, output = run_remote(client, f"rm -f {files}")
    if code != 0:
        raise RuntimeError(f"Remote trace cleanup failed:\n{output}")


def run_remote_sim(client, remote: RemoteConfig, timeout_s: int, log_path: Path) -> None:
    setup = f"{remote.sim_setup_command} && " if remote.sim_setup_command else ""
    progress_interval_s = 10
    stable_checks_to_stop = 3
    monitored_command = (
        "set +e; "
        f"sim_cmd={shell_quote(remote.sim_command)}; "
        "setsid bash -lc \"$sim_cmd\" & sim_pid=$!; "
        "last_bg_size=-1; stable_count=0; "
        "trap 'kill -TERM -\"$sim_pid\" 2>/dev/null; wait \"$sim_pid\" 2>/dev/null; exit 124' INT TERM; "
        "while kill -0 \"$sim_pid\" 2>/dev/null; do "
        f"sleep {progress_interval_s}; "
        "bg_size=0; "
        "if [ -e cla_bgtask_sprs_trace.dat ]; then bg_size=$(wc -c < cla_bgtask_sprs_trace.dat); fi; "
        "if [ \"$bg_size\" -gt 0 ] && [ \"$bg_size\" = \"$last_bg_size\" ]; then "
        "stable_count=$((stable_count + 1)); "
        "else "
        "stable_count=0; "
        "fi; "
        "last_bg_size=\"$bg_size\"; "
        f"if [ \"$stable_count\" -ge {stable_checks_to_stop} ]; then "
        "kill -TERM -\"$sim_pid\" 2>/dev/null; "
        "sleep 2; "
        "kill -KILL -\"$sim_pid\" 2>/dev/null; "
        "wait \"$sim_pid\" 2>/dev/null; "
        "exit 0; "
        "fi; "
        "done; "
        "wait \"$sim_pid\""
    )
    sim_command = (
        f"timeout -s 2 {int(timeout_s)}s bash -lc {shell_quote(monitored_command)}"
        if timeout_s > 0
        else monitored_command
    )
    command = f"cd {shell_quote(remote.sim_dir)} && {setup}{sim_command}"
    log(f"start remote sim: {remote.sim_dir}")
    log(f"remote sim timeout: {timeout_s}s")
    log(f"remote sim command: {remote.sim_command}")
    code, output = run_remote(
        client,
        command,
        timeout=timeout_s + 30 if timeout_s > 0 else None,
        stream_label="simv",
    )
    log_path.write_text(output, encoding="utf-8", errors="replace")
    if code == 124:
        log(f"remote sim reached timeout {timeout_s}s, continuing with generated trace")
    else:
        log(f"remote sim finished with exit code {code}")
    if code not in ({0, 124} if timeout_s > 0 else {0}):
        raise RuntimeError(f"Remote sim failed with exit code {code}. See {log_path}")


def download_trace(client, remote: RemoteConfig, dest: Path) -> str:
    sftp = client.open_sftp()
    try:
        for name in remote.trace_candidates:
            remote_path = f"{remote.sim_dir}/{name}"
            try:
                stat = sftp.stat(remote_path)
            except OSError:
                continue
            if stat.st_size <= 0:
                continue
            sftp.get(remote_path, str(dest))
            return name
    finally:
        sftp.close()
    raise RuntimeError(f"No non-empty remote trace found in {remote.sim_dir}: {remote.trace_candidates}")


def download_optional_trace(client, remote: RemoteConfig, remote_name: str, dest: Path) -> bool:
    sftp = client.open_sftp()
    try:
        remote_path = f"{remote.sim_dir}/{remote_name}"
        try:
            stat = sftp.stat(remote_path)
        except OSError:
            return False
        if stat.st_size <= 0:
            return False
        sftp.get(remote_path, str(dest))
        return True
    finally:
        sftp.close()


TRACE_EXCLUDED_GR_REGS = {"0x00", "0x1e", "0x1f"}


def filter_bg_context_trace(trace_path: Path) -> int:
    raw_path = trace_path.with_suffix(".raw.gr")
    raw_text = trace_path.read_text(encoding="utf-8", errors="replace")
    raw_path.write_text(raw_text, encoding="utf-8", errors="replace")

    kept: list[str] = []
    removed = 0
    for line in raw_text.splitlines():
        parts = line.strip().split()
        if len(parts) >= 3 and parts[0].lower() in TRACE_EXCLUDED_GR_REGS:
            removed += 1
            continue
        kept.append(line)
    trace_path.write_text("\n".join(kept) + ("\n" if kept else ""), encoding="utf-8")
    return removed


def simulate_dual(cfg: dict[str, Any], work_dir: Path, run_dir: Path, keep_remote_trace: bool, timeout_s: int) -> tuple[Path, Path]:
    remote = remote_from_config(cfg)
    client = connect(remote)
    try:
        outputs: dict[str, Path] = {}
        for release, suffix in (("Release_wo", "wo"), ("Release_w", "w")):
            log(f"----- simulate {suffix} ({release}) -----")
            if not keep_remote_trace:
                clean_remote_trace(client, remote)
            upload_release_images(client, cfg, remote, work_dir / release)
            log(f"uploaded {suffix} images, entering remote sim")
            sim_log = run_dir / f"sim_{suffix}.log"
            run_remote_sim(client, remote, timeout_s, sim_log)
            trace_path = run_dir / f"random_{suffix}.gr"
            trace_name = download_trace(client, remote, trace_path)
            log(f"downloaded {trace_name} -> {trace_path}")
            removed_rows = filter_bg_context_trace(trace_path)
            if removed_rows:
                log(f"filtered {removed_rows} GR0/GR30/GR31 context rows from {trace_path.name}; raw saved as {trace_path.with_suffix('.raw.gr').name}")
            for remote_name, local_ext in (
                ("cla_bgtask_pc_trace.dat", "pc"),
                ("cla_bgtask_state_trace.dat", "state"),
                ("cla_bgtask_irq_trace.dat", "irq"),
                ("cla_bgtask_timeline_trace.dat", "timeline"),
            ):
                debug_path = run_dir / f"random_{suffix}.{local_ext}.trace"
                if download_optional_trace(client, remote, remote_name, debug_path):
                    log(f"downloaded {remote_name} -> {debug_path}")
            outputs[suffix] = trace_path
        return outputs["wo"], outputs["w"]
    finally:
        client.close()


def parse_trace_line(line: str) -> tuple[str, str, str] | None:
    parts = line.strip().split()
    if len(parts) < 3:
        return None
    return parts[0], parts[1], parts[2]


def trace_row_key(row: tuple[str, str, str]) -> tuple[str, str, str]:
    return row[0].lower(), row[1].lower(), row[2].lower()


def trace_mismatch_count(left: list[tuple[str, str, str]], right: list[tuple[str, str, str]]) -> int:
    count = min(len(left), len(right))
    total = sum(1 for idx in range(count) if trace_row_key(left[idx]) != trace_row_key(right[idx]))
    return total + abs(len(left) - len(right))


def find_single_extra_trace_row(
    wo_rows: list[tuple[str, str, str]],
    w_rows: list[tuple[str, str, str]],
    first_mismatch_line: int,
) -> dict[str, Any] | None:
    start = max(1, first_mismatch_line - 8)
    end = first_mismatch_line + 8
    candidates: list[dict[str, Any]] = []

    if len(w_rows) >= len(wo_rows):
        for line_no in range(start, min(end, len(w_rows)) + 1):
            idx = line_no - 1
            residual = trace_mismatch_count(wo_rows, w_rows[:idx] + w_rows[idx + 1 :])
            candidates.append({"side": "W", "line": line_no, "row": w_rows[idx], "residual_mismatches": residual})

    if len(wo_rows) >= len(w_rows):
        for line_no in range(start, min(end, len(wo_rows)) + 1):
            idx = line_no - 1
            residual = trace_mismatch_count(wo_rows[:idx] + wo_rows[idx + 1 :], w_rows)
            candidates.append({"side": "WO", "line": line_no, "row": wo_rows[idx], "residual_mismatches": residual})

    if not candidates:
        return None
    best = min(candidates, key=lambda item: item["residual_mismatches"])
    row = best["row"]
    best["row"] = {"reg": row[0], "value": row[1], "pc": row[2]}
    return best


def compare_files(wo_path: Path, w_path: Path, compare_path: Path) -> dict[str, Any]:
    wo_rows = [row for row in (parse_trace_line(line) for line in wo_path.read_text(errors="replace").splitlines()) if row]
    w_rows = [row for row in (parse_trace_line(line) for line in w_path.read_text(errors="replace").splitlines()) if row]
    count = min(len(wo_rows), len(w_rows))
    mismatches: list[str] = []
    pc_only = 0
    regval = 0
    first_mismatch_line = 0
    for idx in range(count):
        wo = wo_rows[idx]
        w = w_rows[idx]
        if wo == w:
            continue
        if first_mismatch_line == 0:
            first_mismatch_line = idx + 1
        if wo[:2] == w[:2] and wo[2] != w[2]:
            pc_only += 1
        else:
            regval += 1
        mismatches.append(f"line {idx + 1}: WO={wo[0]} {wo[1]} {wo[2]} | W={w[0]} {w[1]} {w[2]}")
    if len(wo_rows) != len(w_rows):
        if first_mismatch_line == 0:
            first_mismatch_line = count + 1
        mismatches.append(f"row count differs: WO={len(wo_rows)} W={len(w_rows)}")

    alignment_issue = None
    if first_mismatch_line:
        alignment_issue = find_single_extra_trace_row(wo_rows, w_rows, first_mismatch_line)

    lines = [
        "=" * 80,
        "CLA BG local dual comparison",
        "=" * 80,
        f"WO trace: {wo_path}",
        f"W trace : {w_path}",
        "Comparison method: first 3 whitespace-separated columns",
        "",
        f"RESULT: {'PASS' if not mismatches else 'FAIL'}",
        f"Total lines compared: {count}",
        f"WO rows: {len(wo_rows)}",
        f"W rows: {len(w_rows)}",
        f"Number of mismatches: {len(mismatches)}",
        f"PC-only mismatches: {pc_only}",
        f"Reg/value mismatches: {regval}",
        "",
    ]
    if alignment_issue:
        row = alignment_issue["row"]
        lines.extend(
            [
                "Alignment diagnosis:",
                "-" * 80,
                f"Best single-row removal: remove {alignment_issue['side']} line {alignment_issue['line']}",
                f"Removed row: {row['reg']} {row['value']} {row['pc']}",
                f"Residual mismatches after removal: {alignment_issue['residual_mismatches']}",
                "",
            ]
        )
        if alignment_issue["residual_mismatches"] == 0:
            lines.extend(
                [
                    "Conclusion: all remaining mismatches are explained by one extra/missing trace row.",
                    "",
                ]
            )
    if mismatches:
        lines.extend(["Detailed Mismatch Information:", "-" * 80])
        lines.extend(f"{i}. {msg}" for i, msg in enumerate(mismatches, 1))
    compare_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    result = {
        "pass": not mismatches,
        "lines_compared": count,
        "wo_rows": len(wo_rows),
        "w_rows": len(w_rows),
        "mismatches": len(mismatches),
        "pc_only_mismatches": pc_only,
        "reg_value_mismatches": regval,
    }
    if alignment_issue:
        result["alignment_issue"] = alignment_issue
        if alignment_issue["residual_mismatches"] == 0:
            result["failure_reason"] = "single_extra_or_missing_trace_row"
    return result


def write_analysis_report(run_dir: Path) -> None:
    try:
        if str(SCRIPT_DIR) not in sys.path:
            sys.path.insert(0, str(SCRIPT_DIR))
        from analyze_bg_mismatch import generate_report

        report = generate_report(run_dir)
        log(f"Analysis report: {report}")
    except Exception as exc:
        log(f"WARNING: failed to generate analysis report: {exc}")


def copy_key_artifacts(cfg: dict[str, Any], work_dir: Path, run_dir: Path) -> None:
    patterns = [str(item) for item in cfg["local"].get("artifact_patterns", [
        "task8.o",
        cfg["local"].get("project_out", "F28P6x_driver_core0.out"),
        cfg["local"].get("project_map", "F28P6x_driver_core0.map"),
        "dram_image.core0.dat",
        "iram_image.core0.dat",
        "dram_image.cla0.dat",
        "iram_image.cla0.dat",
    ])]
    for release in ("Release_wo", "Release_w"):
        release_dir = work_dir / release
        archive_dir = run_dir / release
        archive_dir.mkdir(exist_ok=True)
        for pattern in patterns:
            src = release_dir / pattern
            if src.exists():
                shutil.copy2(src, archive_dir / src.name)


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run P65 CLA BG local build flow; remote only runs simv.")
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG)
    parser.add_argument("--instr", type=int, default=1000)
    parser.add_argument("--case", default="random")
    parser.add_argument("--skip-generate", action="store_true")
    parser.add_argument("--source", type=Path, default=None)
    parser.add_argument("--bootstrap", action="store_true")
    parser.add_argument("--force-bootstrap", action="store_true")
    parser.add_argument("--sim-timeout", type=int, default=300)
    parser.add_argument("--keep-remote-trace", action="store_true")
    parser.add_argument("--no-remote-run", action="store_true")
    parser.add_argument("--reference-sim", action="store_true", help="Run the local instruction reference simulator.")
    parser.add_argument("--no-reference-sim", action="store_true", help="Skip the local instruction reference simulator.")
    parser.add_argument("--reference-sim-strict", action="store_true", help="Fail the run if the local reference simulator fails.")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    cfg = load_config(args.config)
    required_dirs = [str(item) for item in cfg["bootstrap"]["required_dirs"]]
    cache_dir = resolve_local_path(cfg["local"]["template_cache_dir"])

    if args.bootstrap or args.force_bootstrap:
        bootstrap_template(cfg, force=args.force_bootstrap)
        if args.bootstrap:
            log("Bootstrap completed.")
            return 0

    if not cache_dir.exists() or not (cache_dir / ".bootstrap_complete").exists():
        log(f"Template cache missing or incomplete: {cache_dir}")
        bootstrap_template(cfg)
    validate_template(cache_dir, required_dirs)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_root = resolve_local_path(cfg["local"]["output_dir"])
    run_dir = output_root / f"{timestamp}_{args.case}"
    run_dir.mkdir(parents=True, exist_ok=False)
    log(f"Run output: {run_dir}")

    if args.skip_generate:
        if args.source is None:
            raise RuntimeError("--skip-generate requires --source")
        source_s = args.source.resolve()
        if not source_s.exists():
            raise RuntimeError(f"Source .s does not exist: {source_s}")
    else:
        source_s = generate_random(cfg, args.case, args.instr, run_dir)

    random_s, task8 = prepare_task8(cfg, source_s, run_dir, args.case)
    log(f"Prepared random source: {random_s}")
    log(f"Prepared task8 source : {task8}")

    work_dir = build_dual(cfg, cache_dir, task8, run_dir)
    copy_key_artifacts(cfg, work_dir, run_dir)
    reference_summary: dict[str, Any] = {"status": "skipped"}
    if args.reference_sim:
        cfg.setdefault("local", {}).setdefault("reference_sim", {})["enabled"] = True
    run_reference = bool(reference_sim_cfg(cfg).get("enabled", False)) and not args.no_reference_sim
    if run_reference:
        reference_summary = run_reference_simulator(cfg, source_s, run_dir, args.case, strict=args.reference_sim_strict)

    summary: dict[str, Any] = {
        "target": target_name(cfg),
        "case": args.case,
        "instr": args.instr,
        "run_dir": str(run_dir),
        "random_s": str(random_s),
        "task8_s": str(task8),
        "remote_run": not args.no_remote_run,
        "reference_sim": reference_summary,
    }

    if args.no_remote_run:
        summary["status"] = "build_only"
    else:
        wo_trace, w_trace = simulate_dual(cfg, work_dir, run_dir, args.keep_remote_trace, args.sim_timeout)
        if (
            reference_summary.get("status") == "pass"
            and reference_summary.get("trace")
            and reference_sim_cfg(cfg).get("compare_to_wo", True)
        ):
            ref_compare = compare_reference_to_rtl(
                Path(str(reference_summary["trace"])),
                wo_trace,
                run_dir / "reference_vs_wo_compare.log",
            )
            reference_summary["compare_to_wo"] = ref_compare
        compare_summary = compare_files(wo_trace, w_trace, run_dir / "compare.log")
        summary.update(compare_summary)
        summary["status"] = "pass" if compare_summary["pass"] else "fail"

    (run_dir / "summary.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")
    log(f"Summary: {run_dir / 'summary.json'}")
    if not args.no_remote_run:
        write_analysis_report(run_dir)
    return 0 if summary["status"] in ("pass", "build_only") else 2


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr, flush=True)
        raise SystemExit(1)
