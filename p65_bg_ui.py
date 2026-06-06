#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Minimal PySide6 launcher for the P65 CLA BG local flow."""

from __future__ import annotations

import json
import math
import os
import re
import runpy
import subprocess
import sys
import time
import importlib.util
from difflib import SequenceMatcher
from pathlib import Path
from typing import Any

from PySide6.QtCore import QByteArray, QObject, QThread, Qt, QUrl, Signal, Slot
from PySide6.QtGui import QDesktopServices, QFont, QTextCursor
from PySide6.QtWidgets import (
    QApplication,
    QCheckBox,
    QFormLayout,
    QGridLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QProgressBar,
    QPushButton,
    QSpinBox,
    QTableWidget,
    QTableWidgetItem,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

APP_TITLE = "P65 CLA BG 仿真工具"
def app_dir() -> Path:
    if getattr(sys, "frozen", False):
        return Path(sys.executable).resolve().parent
    return Path(__file__).resolve().parent


SCRIPT_DIR = app_dir()
CONFIG_PATH = SCRIPT_DIR / "config_p65.json"
RUN_SCRIPT = SCRIPT_DIR / "run_p65_bg.py"
OUTPUT_DIR = SCRIPT_DIR / "output"
CUSTOM_RANDOM_DIR = SCRIPT_DIR / "custom_random"
CUSTOM_RANDOM_FILE = CUSTOM_RANDOM_DIR / "random.s"
MAX_LOG_BLOCKS = 20000


def run_packaged_python_script(argv: list[str]) -> int:
    if not argv:
        print("ERROR: missing script path", file=sys.stderr, flush=True)
        return 1
    script = Path(argv[0]).resolve()
    if not script.exists():
        print(f"ERROR: script does not exist: {script}", file=sys.stderr, flush=True)
        return 1
    sys.argv = [str(script), *argv[1:]]
    sys.path.insert(0, str(script.parent))
    runpy.run_path(str(script), run_name="__main__")
    return 0


def dispatch_cli_subcommand() -> int | None:
    if len(sys.argv) < 2:
        return None
    command = sys.argv[1]
    try:
        if command == "--run-p65-bg":
            import run_p65_bg

            return run_p65_bg.main(sys.argv[2:])
        if command == "--run-python-script":
            return run_packaged_python_script(sys.argv[2:])
    except Exception as exc:
        print(f"ERROR: {friendly_process_error(str(exc))}", file=sys.stderr, flush=True)
        return 1
    return None


def clamp(value: int, low: int, high: int) -> int:
    return max(low, min(high, value))


def auto_timeout(instr_count: int) -> int:
    return clamp(120 + math.ceil(instr_count * 0.08), 120, 600)


def decode_process_output(data: bytes | str | None) -> str:
    if data is None:
        return ""
    if isinstance(data, str):
        return data
    if not data:
        return ""
    if data.startswith(b"\xff\xfe") or data.startswith(b"\xfe\xff") or b"\x00" in data[:128]:
        return data.decode("utf-16", errors="replace")
    for encoding in ("utf-8", "gbk", "mbcs"):
        try:
            return data.decode(encoding)
        except Exception:
            continue
    return data.decode("utf-8", errors="replace")


def friendly_process_error(text: str) -> str:
    compact = " ".join(str(text).strip().split())
    if not compact:
        return "流程异常结束，未返回具体错误。"
    if "No non-empty remote trace found" in compact:
        return (
            "远端仿真完成后没有找到非空 BG trace。"
            "请检查仿真目录是否正确、c2000_tb.v 是否打开 BG trace、"
            "以及 cla_bgtask_sprs_trace.dat/cla_gr_trace.dat 是否生成且非空。"
        )
    if "Source has neither '.=1024' nor a 'main:' label" in compact:
        return "指定 random.s 格式不符合要求：文件中需要包含 '.=1024' 或 main: 标签。"
    if "Source .s does not exist" in compact:
        return "指定 random.s 文件不存在。"
    if "Remote sim failed" in compact:
        return "远端 simv 执行失败，请检查远端仿真目录、simv 是否可运行以及 remote_sim 日志。"
    if "timed out" in compact.lower():
        return "流程超时，请检查 WSL/SSH/远端仿真是否卡住，或调大仿真时间。"
    if "Unhandled exception" in compact:
        return "流程异常结束，请查看日志中的 ERROR 行定位原因。"
    return compact[-600:]


def load_json(path: Path, default: dict[str, Any]) -> dict[str, Any]:
    if not path.exists():
        return default.copy()
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return default.copy()


def save_json(path: Path, data: dict[str, Any]) -> None:
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def default_config() -> dict[str, Any]:
    return {
        "ssh": {"host": "", "port": 22, "user": "", "password": "", "connect_timeout": 30},
        "remote": {"sim_dir": ""},
        "local": {
            "unpack_pipes": False,
            "append_task8_trailer": True,
            "reference_sim": {
                "enabled": False,
                "dir": "reference_sim",
                "sim_config": "-c qx320f034 --cla",
                "exclude_regs": [0, 30, 31],
                "compare_to_wo": True,
            },
        },
    }


def default_settings() -> dict[str, Any]:
    return {
        "instr": 1000,
        "run_count": 3,
        "sim_timeout": auto_timeout(1000),
        "last_output_dir": "",
        "geometry": "",
    }


def config_ui_section(cfg: dict[str, Any]) -> dict[str, Any]:
    ui = cfg.setdefault("ui", {})
    defaults = default_settings()
    for key, value in defaults.items():
        ui.setdefault(key, value)
    return ui


def save_config_with_ui(cfg: dict[str, Any], settings: dict[str, Any]) -> None:
    cfg["ui"] = settings
    save_json(CONFIG_PATH, cfg)


def latest_output_dir(start_time: float) -> Path | None:
    if not OUTPUT_DIR.exists():
        return None
    candidates = [p for p in OUTPUT_DIR.iterdir() if p.is_dir() and p.stat().st_mtime >= start_time - 1]
    if not candidates:
        return None
    return max(candidates, key=lambda p: p.stat().st_mtime)


def _trace_keys(path: Path) -> list[tuple[str, str, str]]:
    if not path.exists():
        return []
    rows: list[tuple[str, str, str]] = []
    for raw in path.read_text(encoding="utf-8", errors="replace").splitlines():
        parts = raw.strip().split()
        if len(parts) >= 3:
            rows.append((parts[0].lower(), parts[1].lower(), parts[2].lower()))
    return rows


def failure_reason_for_run(run_dir: str, summary: dict[str, Any]) -> str:
    if not summary:
        return "未完成对比"
    if summary.get("pass"):
        return "PASS"
    if summary.get("failure_reason") == "cr_flag_only":
        n = summary.get("cr_mismatches", "")
        return f"CR误差：movc2g 读 CR 标志位差异（CON/CR[4] 未跨中断保护，Bug B）{n} 条，非掉写回/数据损坏"
    alignment_issue = summary.get("alignment_issue") or {}
    if alignment_issue.get("residual_mismatches") == 0:
        side = alignment_issue.get("side", "?")
        line = alignment_issue.get("line", "?")
        row = alignment_issue.get("row") or {}
        return f"{side} 多/少一条trace导致错位，line {line}: {row.get('reg', '')} {row.get('value', '')} pc={row.get('pc', '')}"
    if not run_dir:
        return "缺少输出目录"

    base = Path(run_dir)
    wo_rows = _trace_keys(base / "random_wo.gr")
    w_rows = _trace_keys(base / "random_w.gr")
    if not wo_rows or not w_rows:
        return "缺少 trace"

    matcher = SequenceMatcher(None, wo_rows, w_rows, autojunk=False)
    insert_count = 0
    delete_count = 0
    value_diff_count = 0
    different_write_count = 0
    first_pos = ""
    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        if tag == "equal":
            continue
        if not first_pos:
            first_pos = f"，起点 WO#{i1 + 1}/W#{j1 + 1}"
        if tag == "insert":
            insert_count += j2 - j1
        elif tag == "delete":
            delete_count += i2 - i1
        elif tag == "replace":
            wo_len = i2 - i1
            w_len = j2 - j1
            for offset in range(min(wo_len, w_len)):
                wo_row = wo_rows[i1 + offset]
                w_row = w_rows[j1 + offset]
                if wo_row[0] == w_row[0] and wo_row[2] == w_row[2]:
                    value_diff_count += 1
                else:
                    different_write_count += 1
            if w_len > wo_len:
                insert_count += w_len - wo_len
            elif wo_len > w_len:
                delete_count += wo_len - w_len

    parts: list[str] = []
    if insert_count:
        parts.append(f"W 多 {insert_count} 条")
    if delete_count:
        parts.append(f"W 少 {delete_count} 条")
    extra_parts: list[str] = []
    if value_diff_count:
        extra_parts.append(f"同PC同寄存器值差异 {value_diff_count} 条")
    if different_write_count:
        extra_parts.append(f"不同写回 {different_write_count} 条")
    if parts and not extra_parts:
        return "，".join(parts) + "导致错误" + first_pos
    if parts:
        return "，".join(parts) + "，另有" + "，".join(extra_parts) + first_pos
    return "，".join(extra_parts) + first_pos


def format_compare_brief(result: dict[str, Any]) -> str:
    summary = result.get("summary", {})
    run_dir = str(result.get("run_dir", ""))
    failure_reason = failure_reason_for_run(run_dir, summary)
    if not summary:
        return (
            "\n[对比简报]\n"
            f"状态: {result.get('status')} - {result.get('message')}\n"
            f"输出目录: {run_dir or '无'}\n"
            "summary.json 未生成，未完成对比。\n"
        )
    return (
        "\n[对比简报]\n"
        f"状态: {summary.get('status', result.get('status'))}\n"
        f"结果: {'PASS' if summary.get('pass') else 'FAIL'}\n"
        f"比较行数: {summary.get('lines_compared', '')}\n"
        f"WO/W 行数: {summary.get('wo_rows', '')}/{summary.get('w_rows', '')}\n"
        f"Mismatch: {summary.get('mismatches', '')}\n"
        f"失败原因: {failure_reason}\n"
        f"Reg/value: {summary.get('reg_value_mismatches', '')}\n"
        f"输出目录: {run_dir}\n"
    )


def format_reference_compare_cell(summary: dict[str, Any]) -> str:
    reference_sim = summary.get("reference_sim") or {}
    ref_compare = reference_sim.get("compare_to_wo") or {}
    if reference_sim.get("status") == "pass" and ref_compare:
        return (
            f"{'PASS' if ref_compare.get('pass') else 'FAIL'} "
            f"real={ref_compare.get('real_mismatches', '')} "
            f"ign={ref_compare.get('ignorable_reorder_cycles', '')}"
        )
    if reference_sim.get("status") in {"disabled", "skipped"} or not reference_sim:
        return "未开启"
    if reference_sim.get("status"):
        return str(reference_sim.get("status"))
    return "未开启"


def format_compare_brief(result: dict[str, Any]) -> str:
    summary = result.get("summary", {})
    run_dir = str(result.get("run_dir", ""))
    failure_reason = failure_reason_for_run(run_dir, summary)
    if not summary:
        return (
            "\n[对比简报]\n"
            f"状态: {result.get('status')} - {result.get('message')}\n"
            f"输出目录: {run_dir or '无'}\n"
            "summary.json 未生成，未完成对比。\n"
        )
    reference_sim = summary.get("reference_sim") or {}
    ref_compare = reference_sim.get("compare_to_wo") or {}
    if reference_sim.get("status") == "pass" and ref_compare:
        ref_line = (
            f"模拟器/WO: {'PASS' if ref_compare.get('pass') else 'FAIL'} "
            f"writebacks={ref_compare.get('reference_writebacks', '')}/{ref_compare.get('rtl_writebacks', '')} "
            f"real={ref_compare.get('real_mismatches', '')} ignore={ref_compare.get('ignorable_reorder_cycles', '')}\n"
        )
    elif reference_sim.get("status") in {"disabled", "skipped"} or not reference_sim:
        ref_line = "模拟器/WO: 未开启\n"
    elif reference_sim.get("status"):
        ref_line = f"模拟器/WO: {reference_sim.get('status')} {reference_sim.get('error', '')}\n"
    else:
        ref_line = "模拟器/WO: 未开启\n"
    return (
        "\n[对比简报]\n"
        f"状态: {summary.get('status', result.get('status'))}\n"
        f"结果: {'PASS' if summary.get('pass') else 'FAIL'}\n"
        f"比较行数: {summary.get('lines_compared', '')}\n"
        f"WO/W 行数: {summary.get('wo_rows', '')}/{summary.get('w_rows', '')}\n"
        f"Mismatch: {summary.get('mismatches', '')}\n"
        f"{ref_line}"
        f"失败原因: {failure_reason}\n"
        f"Reg/value: {summary.get('reg_value_mismatches', '')}（其中 CR误差: {summary.get('cr_mismatches', 0)}）\n"
        f"输出目录: {run_dir}\n"
    )


class RunWorker(QObject):
    log = Signal(str)
    run_started = Signal(int, int, int)
    run_result = Signal(dict)
    finished = Signal()

    def __init__(
        self,
        instr_count: int,
        total_runs: int,
        timeout_s: int,
        source_s: Path | None = None,
        label: str = "random",
        reference_compare: bool = False,
        no_pack: bool = False,
    ) -> None:
        super().__init__()
        self.instr_count = instr_count
        self.total_runs = total_runs
        self.timeout_s = timeout_s
        self.source_s = source_s
        self.label = label
        self.reference_compare = reference_compare
        self.no_pack = no_pack
        self._stop_requested = False
        self._process: subprocess.Popen[str] | None = None

    @Slot()
    def run(self) -> None:
        timeout_s = self.timeout_s
        try:
            for index in range(1, self.total_runs + 1):
                if self._stop_requested:
                    self._emit_stopped(index, timeout_s)
                    break
                self.run_started.emit(index, self.total_runs, timeout_s)
                result = self._run_once(index, timeout_s)
                self.log.emit(format_compare_brief(result))
                self.run_result.emit(result)
                if result["status"] in {"ERROR", "STOPPED"}:
                    break
        finally:
            self.finished.emit()

    def stop(self) -> None:
        self._stop_requested = True
        proc = self._process
        if proc is not None and proc.poll() is None:
            self.log.emit("正在停止当前本地仿真进程...\n")
            try:
                proc.terminate()
            except Exception as exc:
                self.log.emit(f"停止进程失败: {exc}\n")

    def _emit_stopped(self, index: int, timeout_s: int) -> None:
        self.run_result.emit(
            {
                "index": index,
                "status": "STOPPED",
                "instr": self.instr_count,
                "timeout": timeout_s,
                "summary": {},
                "run_dir": "",
                "message": "用户停止",
                "returncode": None,
                "source_s": str(self.source_s) if self.source_s else "",
            }
        )

    def _run_once(self, index: int, timeout_s: int) -> dict[str, Any]:
        start_time = time.time()
        run_dir: Path | None = None
        env = os.environ.copy()
        env["PYTHONIOENCODING"] = "utf-8"
        if getattr(sys, "frozen", False):
            cmd = [sys.executable, "--run-p65-bg", "--instr", str(self.instr_count), "--sim-timeout", str(timeout_s)]
        else:
            cmd = [sys.executable, str(RUN_SCRIPT), "--instr", str(self.instr_count), "--sim-timeout", str(timeout_s)]
        if self.source_s is not None:
            cmd.extend(["--skip-generate", "--source", str(self.source_s)])
        if self.reference_compare:
            cmd.append("--reference-sim")
        else:
            cmd.append("--no-reference-sim")
        if self.no_pack:
            cmd.append("--no-pack")
        self.log.emit(f"\n===== 第 {index}/{self.total_runs} 次仿真 =====\n")
        if self.source_s is not None:
            self.log.emit(f"使用指定 random.s: {self.source_s}\n")
        self.log.emit(f"命令: {' '.join(cmd)}\n")

        try:
            creationflags = subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0
            self._process = subprocess.Popen(
                cmd,
                cwd=str(SCRIPT_DIR),
                env=env,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                encoding="utf-8",
                errors="replace",
                bufsize=1,
                creationflags=creationflags,
            )
        except Exception as exc:
            return self._result(index, timeout_s, "ERROR", None, None, f"启动失败: {exc}")

        assert self._process.stdout is not None
        output_re = re.compile(r"^Run output:\s*(.+)\s*$")
        error_lines: list[str] = []
        for line in self._process.stdout:
            self.log.emit(line)
            match = output_re.match(line.strip())
            if match:
                run_dir = Path(match.group(1).strip())
            if line.startswith("ERROR:") or "No non-empty remote trace found" in line or "Unhandled exception" in line:
                error_lines.append(line.strip())
            if self._stop_requested and self._process.poll() is None:
                self.stop()

        returncode = self._process.wait()
        self._process = None

        if run_dir is None:
            run_dir = latest_output_dir(start_time)
        if self._stop_requested:
            return self._result(index, timeout_s, "STOPPED", returncode, run_dir, "用户停止")

        summary = self._load_summary(run_dir)
        if returncode == 0:
            status = "PASS"
            message = "流程通过"
        elif returncode == 2:
            status = "COMPARE FAIL"
            message = "流程完成，compare 失败"
        else:
            status = "ERROR"
            detail = "\n".join(error_lines) if error_lines else f"脚本返回码 {returncode}"
            message = friendly_process_error(detail)
        return self._result(index, timeout_s, status, returncode, run_dir, message, summary)

    def _load_summary(self, run_dir: Path | None) -> dict[str, Any]:
        if run_dir is None:
            return {}
        summary_path = run_dir / "summary.json"
        if not summary_path.exists():
            return {}
        try:
            return json.loads(summary_path.read_text(encoding="utf-8"))
        except Exception as exc:
            self.log.emit(f"读取 summary.json 失败: {exc}\n")
            return {}

    def _result(
        self,
        index: int,
        timeout_s: int,
        status: str,
        returncode: int | None,
        run_dir: Path | None,
        message: str,
        summary: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        return {
            "index": index,
            "status": status,
            "instr": self.instr_count,
            "timeout": timeout_s,
            "summary": summary or {},
            "run_dir": str(run_dir) if run_dir else "",
            "message": message,
            "returncode": returncode,
            "source_s": str(self.source_s) if self.source_s else "",
        }


class LocalEnvWorker(QObject):
    log = Signal(str)
    finished = Signal(bool, str)

    def __init__(self, cfg: dict[str, Any]) -> None:
        super().__init__()
        self.cfg = cfg

    @Slot()
    def run(self) -> None:
        try:
            self.log.emit("\n===== 一键补齐程序运行环境 =====\n")
            self._ensure_python_packages()
            self._check_local_files()
            self._check_wsl()
            self._check_ssh_remote()
            self.log.emit("程序运行环境检测通过。\n")
            self.finished.emit(True, "程序运行环境检测通过")
        except Exception as exc:
            self.log.emit(f"程序运行环境检测失败: {exc}\n")
            self.finished.emit(False, str(exc))

    def _ensure_python_packages(self) -> None:
        packages = [("paramiko", "paramiko"), ("PySide6-Essentials", "PySide6")]
        missing = [package for package, module in packages if importlib.util.find_spec(module) is None]
        if not missing:
            self.log.emit("Python 依赖已满足: paramiko, PySide6\n")
            return
        self.log.emit(f"安装 Python 依赖: {', '.join(missing)}\n")
        if getattr(sys, "frozen", False):
            raise RuntimeError("Packaged EXE is missing embedded Python modules: " + ", ".join(missing))
        cmd = [sys.executable, "-m", "pip", "install", "--no-cache-dir", *missing]
        result = subprocess.run(
            cmd,
            cwd=str(SCRIPT_DIR),
            text=True,
            encoding="utf-8",
            errors="replace",
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )
        self.log.emit(result.stdout)
        if result.returncode != 0:
            raise RuntimeError(f"pip install failed, return code {result.returncode}")

    def _check_local_files(self) -> None:
        required_files = [
            SCRIPT_DIR / "config_p65.json",
            SCRIPT_DIR / "random_test" / "instr_generate" / "main.py",
            SCRIPT_DIR / "p65_linux_tools" / "bin" / "as.bin",
            SCRIPT_DIR / "p65_linux_tools" / "bin" / "ld.bin",
            SCRIPT_DIR / "p65_linux_tools" / "bin" / "objcopy.bin",
            SCRIPT_DIR / "p65_linux_tools" / "bin" / "objdump.bin",
            SCRIPT_DIR / "p65_linux_tools" / "bin" / "gen_ram_image.py",
            SCRIPT_DIR / "reference_sim" / "simulator" / "simulator_step13",
            SCRIPT_DIR / "reference_sim" / "toolchains" / "bin" / "as.bin",
            SCRIPT_DIR / "reference_sim" / "toolchains" / "bin" / "ld.bin",
            SCRIPT_DIR / "reference_sim" / "toolchains" / "test" / "scripts" / "trobjdat_8slot.py",
            SCRIPT_DIR / "reference_sim" / "toolchains" / "tools" / "objcopy.bin",
        ]
        if not getattr(sys, "frozen", False):
            required_files.insert(0, RUN_SCRIPT)
        required_dirs = [
            SCRIPT_DIR / "cache" / "p65_bg_template" / "Release_w",
            SCRIPT_DIR / "cache" / "p65_bg_template" / "Release_wo",
            SCRIPT_DIR / "cache" / "p65_bg_template" / "ldscript",
            SCRIPT_DIR / "cache" / "p65_bg_template" / "libv2",
            SCRIPT_DIR / "reference_sim" / "toolchains" / "lib" / "qx320f",
        ]
        missing = [str(path) for path in required_files if not path.is_file()]
        missing += [str(path) for path in required_dirs if not path.is_dir()]
        OUTPUT_DIR.mkdir(exist_ok=True)
        if missing:
            raise RuntimeError("缺少本地运行资源:\n" + "\n".join(missing))
        self.log.emit("本地脚本、随机生成器、P65 Linux 工具和模板 cache 已满足。\n")

    def _check_wsl(self) -> None:
        bash_path = self._windows_to_wsl_path(SCRIPT_DIR)
        self.log.emit("检查 WSL 可用性...\n")
        status = subprocess.run(
            ["wsl", "--status"],
            cwd=str(SCRIPT_DIR),
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            timeout=30,
        )
        status_output = decode_process_output(status.stdout)
        if status_output.strip():
            self.log.emit(status_output)
        if status.returncode != 0:
            raise RuntimeError("WSL 不可用。请先安装 WSL，并确认在 PowerShell 中执行 wsl 能正常进入 Linux。")

        command = (
            f"cd {self._shell_quote(bash_path)} || {{ echo CANNOT_CD; exit 20; }}; "
            "echo WSL_PWD=$(pwd); "
            "echo WSL_TOOL_LIST; "
            "ls -l p65_linux_tools/bin 2>&1 || true; "
            "missing=0; "
            "for f in as.bin ld.bin objcopy.bin objdump.bin gen_ram_image.py; do "
            "if [ ! -f p65_linux_tools/bin/$f ]; then echo MISSING:p65_linux_tools/bin/$f; missing=1; fi; "
            "done; "
            "for f in simulator/simulator_step13 toolchains/bin/as.bin toolchains/bin/ld.bin toolchains/test/scripts/trobjdat_8slot.py toolchains/tools/objcopy.bin; do "
            "if [ ! -f reference_sim/$f ]; then echo MISSING:reference_sim/$f; missing=1; fi; "
            "done; "
            "if [ ! -d reference_sim/toolchains/lib/qx320f ]; then echo MISSING:reference_sim/toolchains/lib/qx320f; missing=1; fi; "
            "if [ $missing -ne 0 ]; then exit 21; fi; "
            "chmod +x p65_linux_tools/bin/*.bin 2>&1 || true; "
            "chmod +x reference_sim/toolchains/bin/*.bin reference_sim/toolchains/tools/*.bin reference_sim/simulator/simulator_step13 2>&1 || true; "
            "if ! command -v python3 >/dev/null 2>&1; then echo MISSING:python3; exit 22; fi; "
            "echo PYTHON3=$(python3 --version 2>&1); "
            "echo WSL_OK"
        )
        try:
            result = subprocess.run(
                ["wsl", "-e", "bash", "-c", command],
                cwd=str(SCRIPT_DIR),
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                timeout=120,
            )
        except subprocess.TimeoutExpired as exc:
            output = decode_process_output(exc.stdout)
            self.log.emit(output)
            raise RuntimeError(
                "WSL 启动或访问当前目录超过 120 秒。\n"
                "请先在 PowerShell 手动执行一次 wsl，确认 Linux 能正常启动；"
                "如果是首次安装 WSL，请完成初始化后再重新点击环境检测。"
            ) from exc
        result_output = decode_process_output(result.stdout)
        self.log.emit(result_output)
        if result.returncode != 0 or "WSL_OK" not in result_output:
            if "MISSING:python3" in result_output:
                raise RuntimeError(
                    "WSL 可用，但 Linux 里缺少 python3。\n"
                    "请让对方先打开 PowerShell 执行 wsl，然后在 Linux 里手动执行：\n"
                    "sudo apt update\n"
                    "sudo apt install -y python3\n"
                    "这一步可能需要输入 WSL 密码；安装完成后重新点击环境检测。"
                )
            raise RuntimeError(
                "WSL 可启动，但无法访问当前程序目录或缺少 P65 Linux 工具。\n"
                f"WSL 路径: {bash_path}\n"
                "请确认该目录位于 Windows 本地磁盘，并且 p65_linux_tools/bin 下有 as.bin、ld.bin、objcopy.bin、objdump.bin。"
            )
        self.log.emit("WSL 可用，且能访问当前程序目录和 P65 Linux 工具。\n")

    def _check_ssh_remote(self) -> None:
        ssh = self.cfg.get("ssh", {})
        remote = self.cfg.get("remote", {})
        host = str(ssh.get("host", "")).strip()
        user = str(ssh.get("user", "")).strip()
        password = str(ssh.get("password", ""))
        sim_dir = str(remote.get("sim_dir", "")).strip().rstrip("/")
        if not host or not user or not password or not sim_dir:
            raise RuntimeError("SSH 地址、用户名、密码和仿真目录必须先配置完整")

        import paramiko

        self.log.emit(f"检查 SSH 和远端目录: {user}@{host}:{sim_dir}\n")
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            client.connect(
                hostname=host,
                port=int(ssh.get("port", 22)),
                username=user,
                password=password,
                look_for_keys=False,
                allow_agent=False,
                timeout=30,
                banner_timeout=60,
                auth_timeout=30,
            )
            code, output = self._run_remote(client, f'test -d "{sim_dir}" && test -x "{sim_dir}/simv" && echo REMOTE_OK')
            self.log.emit(output)
            if code != 0 or "REMOTE_OK" not in output:
                raise RuntimeError("远端仿真目录不存在，或 simv 不可执行")
        finally:
            client.close()
        self.log.emit("SSH 连接和远端仿真目录检查通过。\n")

    def _run_remote(self, client, command: str) -> tuple[int, str]:
        stdin, stdout, stderr = client.exec_command(command, get_pty=True)
        stdin.close()
        out = stdout.read().decode("utf-8", errors="replace")
        err = stderr.read().decode("utf-8", errors="replace")
        return stdout.channel.recv_exit_status(), out + err

    def _windows_to_wsl_path(self, path: Path) -> str:
        resolved = path.resolve()
        drive = resolved.drive.rstrip(":").lower()
        rest = resolved.as_posix()[3:] if resolved.as_posix()[1:3] == ":/" else resolved.as_posix()
        return f"/mnt/{drive}/{rest}" if drive else rest

    def _shell_quote(self, value: str) -> str:
        return "'" + value.replace("'", "'\"'\"'") + "'"


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle(APP_TITLE)
        self.cfg = load_json(CONFIG_PATH, default_config())
        self.settings = config_ui_section(self.cfg)
        self.last_output_dir = str(self.settings.get("last_output_dir", ""))
        self.row_output_dirs: dict[int, str] = {}
        self.row_rerun_sources: dict[int, str] = {}
        self.worker: RunWorker | None = None
        self.thread: QThread | None = None
        self.local_env_worker: LocalEnvWorker | None = None
        self.local_env_thread: QThread | None = None
        self._build_ui()
        self._load_fields()
        self._restore_geometry()

    def _build_ui(self) -> None:
        root = QWidget(self)
        layout = QVBoxLayout(root)
        top_layout = QHBoxLayout()
        top_layout.addWidget(self._build_config_group(), 1)
        top_layout.addWidget(self._build_run_group(), 1)
        layout.addLayout(top_layout)
        layout.addWidget(self._build_result_group())
        layout.addWidget(self._build_log_group(), 1)
        self.setCentralWidget(root)
        self.resize(1120, 760)

    def _build_config_group(self) -> QGroupBox:
        group = QGroupBox("连接配置")
        group.setMaximumHeight(140)
        group.setMaximumWidth(1040)
        grid = QGridLayout(group)

        self.host_edit = QLineEdit()
        self.port_spin = QSpinBox()
        self.port_spin.setRange(1, 65535)
        self.user_edit = QLineEdit()
        self.password_edit = QLineEdit()
        self.password_edit.setEchoMode(QLineEdit.Password)
        self.sim_dir_edit = QLineEdit()

        grid.addWidget(QLabel("SSH 地址"), 0, 0)
        grid.addWidget(self.host_edit, 0, 1)
        grid.addWidget(QLabel("端口"), 0, 2)
        grid.addWidget(self.port_spin, 0, 3)
        grid.addWidget(QLabel("用户名"), 1, 0)
        grid.addWidget(self.user_edit, 1, 1)
        grid.addWidget(QLabel("密码"), 1, 2)
        grid.addWidget(self.password_edit, 1, 3)
        grid.addWidget(QLabel("仿真目录"), 2, 0)
        grid.addWidget(self.sim_dir_edit, 2, 1, 1, 3)
        grid.setColumnStretch(1, 1)
        grid.setColumnStretch(3, 1)
        return group

    def _build_run_group(self) -> QGroupBox:
        group = QGroupBox("仿真参数")
        group.setMaximumHeight(170)
        layout = QGridLayout(group)

        self.instr_spin = QSpinBox()
        self.instr_spin.setRange(1, 200000)
        self.instr_spin.valueChanged.connect(self._update_timeout_label)
        self.run_count_spin = QSpinBox()
        self.run_count_spin.setRange(1, 999)
        self.sim_timeout_spin = QSpinBox()
        self.sim_timeout_spin.setRange(10, 3600)
        self.sim_timeout_spin.setSuffix(" s")
        self.unpack_pipes_check = QCheckBox("拆包运行")
        self.unpack_pipes_check.setToolTip("开启后让随机生成器不打包(QX_PACKED_INSTR=0),每个 bundle 只放一条真实指令、保持其原始槽位;关闭则正常打包。")
        self.disable_addr_regs_check = QCheckBox("禁用间接寄存器")
        self.disable_addr_regs_check.setToolTip(
            "开启后 CLA 随机生成不选择 OFF/BAR/MR，并排除 GR30，避免间接取址/取指相关寄存器写入。"
        )

        self.reference_compare_check = QCheckBox("模拟器/WO对比")
        self.reference_compare_check.setToolTip("开启后额外运行本地模拟器，生成 reference_sim.gr，并和无中断 WO trace 做 GR/value 对比。")

        self.timeout_label = QLabel()
        self.auto_timeout_button = QPushButton("自动时间")
        self.save_button = QPushButton("保存配置")
        self.local_env_button = QPushButton("一键补齐检测环境")
        self.single_button = QPushButton("单次仿真")
        self.multi_button = QPushButton("多次仿真")
        self.source_button = QPushButton("指定random.s仿真")
        self.stop_button = QPushButton("停止当前仿真")
        self.open_button = QPushButton("打开输出目录")
        self.stop_button.setEnabled(False)

        self.save_button.clicked.connect(self.save_all)
        self.local_env_button.clicked.connect(self.start_local_env_check)
        self.single_button.clicked.connect(lambda: self.start_runs(1))
        self.multi_button.clicked.connect(lambda: self.start_runs(self.run_count_spin.value()))
        self.source_button.clicked.connect(self.start_custom_random_run)
        self.stop_button.clicked.connect(self.stop_current_run)
        self.open_button.clicked.connect(self.open_output_dir)
        self.auto_timeout_button.clicked.connect(self.apply_auto_timeout)

        form = QFormLayout()
        form.addRow("指令数", self.instr_spin)
        form.addRow("仿真次数", self.run_count_spin)
        form.addRow("仿真时间", self.sim_timeout_spin)
        form.addRow("指令打包", self.unpack_pipes_check)
        form.addRow("寄存器限制", self.disable_addr_regs_check)
        form.addRow("推荐时间", self.timeout_label)
        form.addRow("模拟对比", self.reference_compare_check)
        layout.addLayout(form, 0, 0, 5, 1)
        layout.addWidget(self.auto_timeout_button, 0, 1)
        layout.addWidget(self.save_button, 0, 2)
        layout.addWidget(self.local_env_button, 1, 1, 1, 2)
        layout.addWidget(self.single_button, 2, 1)
        layout.addWidget(self.multi_button, 2, 2)
        layout.addWidget(self.source_button, 3, 1, 1, 2)
        layout.addWidget(self.stop_button, 4, 1)
        layout.addWidget(self.open_button, 4, 2)
        layout.setColumnStretch(0, 2)
        layout.setColumnStretch(1, 1)
        layout.setColumnStretch(2, 1)
        return group

    def _build_result_group(self) -> QGroupBox:
        group = QGroupBox("结果")
        layout = QVBoxLayout(group)
        self.status_label = QLabel("未运行")
        self.status_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.result_table = QTableWidget(0, 11)
        self.result_table.setHorizontalHeaderLabels(
            ["#", "状态", "指令数", "timeout", "WO 行", "W 行", "Mismatch", "失败原因", "重跑"]
        )
        self.result_table.setHorizontalHeaderLabels(
            ["#", "状态", "指令数", "timeout", "WO行", "W行", "Mismatch", "模拟行", "模拟/WO", "失败原因", "重跑"]
        )
        self.result_table.horizontalHeader().setStretchLastSection(True)
        self.result_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.result_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.result_table.cellDoubleClicked.connect(self._open_table_row)
        status_row = QHBoxLayout()
        status_row.addWidget(self.status_label, 1)
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 1)
        self.progress_bar.setValue(0)
        self.progress_bar.setTextVisible(True)
        status_row.addWidget(self.progress_bar)
        layout.addLayout(status_row)
        layout.addWidget(self.result_table)
        return group

    def _build_log_group(self) -> QGroupBox:
        group = QGroupBox("日志")
        layout = QVBoxLayout(group)
        self.log_edit = QTextEdit()
        self.log_edit.setReadOnly(True)
        self.log_edit.setLineWrapMode(QTextEdit.NoWrap)
        font = QFont("Consolas")
        font.setStyleHint(QFont.Monospace)
        self.log_edit.setFont(font)
        layout.addWidget(self.log_edit)
        return group

    def _load_fields(self) -> None:
        ssh = self.cfg.get("ssh", {})
        remote = self.cfg.get("remote", {})
        local = self.cfg.get("local", {})
        self.host_edit.setText(str(ssh.get("host", "")))
        self.port_spin.setValue(int(ssh.get("port", 22) or 22))
        self.user_edit.setText(str(ssh.get("user", "")))
        self.password_edit.setText(str(ssh.get("password", "")))
        self.sim_dir_edit.setText(str(remote.get("sim_dir", "")))
        self.instr_spin.setValue(int(self.settings.get("instr", 1000) or 1000))
        self.run_count_spin.setValue(int(self.settings.get("run_count", 3) or 3))
        timeout_value = int(self.settings.get("sim_timeout", auto_timeout(self.instr_spin.value())) or auto_timeout(self.instr_spin.value()))
        self.sim_timeout_spin.setValue(timeout_value)
        self.unpack_pipes_check.setChecked(bool(local.get("unpack_pipes", False)))
        self.disable_addr_regs_check.setChecked(bool(local.get("disable_cla_addr_regs", True)))
        reference_sim = local.get("reference_sim") or {}
        self.reference_compare_check.setChecked(bool(reference_sim.get("enabled", False)))
        self._update_timeout_label()

    def _restore_geometry(self) -> None:
        raw = str(self.settings.get("geometry", ""))
        if raw:
            self.restoreGeometry(QByteArray.fromBase64(raw.encode("ascii")))

    def _append_log(self, text: str) -> None:
        self.log_edit.moveCursor(QTextCursor.End)
        self.log_edit.insertPlainText(text)
        self._trim_log()
        self.log_edit.moveCursor(QTextCursor.End)

    def _trim_log(self) -> None:
        document = self.log_edit.document()
        extra_blocks = document.blockCount() - MAX_LOG_BLOCKS
        if extra_blocks <= 0:
            return
        cursor = QTextCursor(document)
        cursor.movePosition(QTextCursor.Start)
        for _ in range(extra_blocks):
            cursor.select(QTextCursor.BlockUnderCursor)
            cursor.removeSelectedText()
            cursor.deleteChar()

    def _update_timeout_label(self) -> None:
        self.timeout_label.setText(f"{auto_timeout(self.instr_spin.value())} 秒")

    def apply_auto_timeout(self) -> None:
        self.sim_timeout_spin.setValue(auto_timeout(self.instr_spin.value()))

    def validate_fields(self) -> bool:
        if not self.host_edit.text().strip():
            QMessageBox.warning(self, "配置错误", "SSH 地址不能为空。")
            return False
        if not self.user_edit.text().strip():
            QMessageBox.warning(self, "配置错误", "用户名不能为空。")
            return False
        if not self.password_edit.text():
            QMessageBox.warning(self, "配置错误", "密码不能为空。")
            return False
        if not self.sim_dir_edit.text().strip():
            QMessageBox.warning(self, "配置错误", "仿真目录不能为空。")
            return False
        if not RUN_SCRIPT.exists():
            QMessageBox.critical(self, "缺少脚本", f"找不到 {RUN_SCRIPT}")
            return False
        return True

    @Slot()
    def save_all(self) -> bool:
        if not self.validate_fields():
            return False
        # Reload the current config before saving UI fields so hidden options
        # changed on disk are not overwritten by an old in-memory copy.
        self.cfg = load_json(CONFIG_PATH, self.cfg if isinstance(self.cfg, dict) else default_config())
        self.cfg.setdefault("ssh", {})
        self.cfg.setdefault("remote", {})
        self.cfg.setdefault("local", {})
        self.cfg["ssh"]["host"] = self.host_edit.text().strip()
        self.cfg["ssh"]["port"] = self.port_spin.value()
        self.cfg["ssh"]["user"] = self.user_edit.text().strip()
        self.cfg["ssh"]["password"] = self.password_edit.text()
        self.cfg["remote"]["sim_dir"] = self.sim_dir_edit.text().strip().rstrip("/")
        self.cfg["local"]["unpack_pipes"] = self.unpack_pipes_check.isChecked()
        self.cfg["local"]["disable_cla_addr_regs"] = self.disable_addr_regs_check.isChecked()
        self.cfg["local"].setdefault("reference_sim", {})
        self.cfg["local"]["reference_sim"]["enabled"] = self.reference_compare_check.isChecked()
        self.cfg["local"]["reference_sim"].setdefault("dir", "reference_sim")
        self.cfg["local"]["reference_sim"].setdefault("sim_config", "-c qx320f034 --cla")
        self.cfg["local"]["reference_sim"].setdefault("exclude_regs", [0, 30, 31])
        self.cfg["local"]["reference_sim"].setdefault("compare_to_wo", True)
        self.settings["instr"] = self.instr_spin.value()
        self.settings["run_count"] = self.run_count_spin.value()
        self.settings["sim_timeout"] = self.sim_timeout_spin.value()
        self.settings["last_output_dir"] = self.last_output_dir
        self.settings["geometry"] = bytes(self.saveGeometry().toBase64()).decode("ascii")
        save_config_with_ui(self.cfg, self.settings)
        self._append_log(f"配置已保存: {CONFIG_PATH}\n")
        return True

    def start_runs(
        self,
        count: int,
        source_s: Path | None = None,
        clear_results: bool = True,
        label: str = "random",
    ) -> None:
        if self.thread is not None:
            return
        if not self.save_all():
            return

        if clear_results:
            self.result_table.setRowCount(0)
            self.row_output_dirs.clear()
            self.row_rerun_sources.clear()
        self.status_label.setText("运行中")
        self.progress_bar.setRange(0, count)
        self.progress_bar.setValue(0)
        self.progress_bar.setFormat("0/%m")
        self._set_running(True)

        self.worker = RunWorker(
            self.instr_spin.value(),
            count,
            self.sim_timeout_spin.value(),
            source_s,
            label,
            self.reference_compare_check.isChecked(),
            self.unpack_pipes_check.isChecked(),
        )
        self.thread = QThread(self)
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.run)
        self.worker.log.connect(self._append_log)
        self.worker.run_started.connect(self._on_run_started)
        self.worker.run_result.connect(self._on_run_result)
        self.worker.finished.connect(self._on_worker_finished)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.thread.finished.connect(self._clear_thread)
        self.thread.start()

    def start_custom_random_run(self) -> None:
        CUSTOM_RANDOM_DIR.mkdir(parents=True, exist_ok=True)
        if not CUSTOM_RANDOM_FILE.exists():
            QMessageBox.information(
                self,
                "指定random.s",
                f"请先把要仿真的文件放到:\n{CUSTOM_RANDOM_FILE}\n\n"
                "文件名必须是 random.s。目录已自动创建。",
            )
            QDesktopServices.openUrl(QUrl.fromLocalFile(str(CUSTOM_RANDOM_DIR)))
            return
        self.start_runs(1, source_s=CUSTOM_RANDOM_FILE, clear_results=True, label="指定random.s")

    def start_local_env_check(self) -> None:
        if self.thread is not None or self.local_env_thread is not None:
            return
        if not self.save_all():
            return

        self.local_env_button.setText("检测中...")
        self.local_env_button.setStyleSheet("")
        self._set_running(True)
        self.stop_button.setEnabled(False)

        self.local_env_worker = LocalEnvWorker(json.loads(json.dumps(self.cfg)))
        self.local_env_thread = QThread(self)
        self.local_env_worker.moveToThread(self.local_env_thread)
        self.local_env_thread.started.connect(self.local_env_worker.run)
        self.local_env_worker.log.connect(self._append_log)
        self.local_env_worker.finished.connect(self._on_local_env_finished)
        self.local_env_worker.finished.connect(self.local_env_thread.quit)
        self.local_env_worker.finished.connect(self.local_env_worker.deleteLater)
        self.local_env_thread.finished.connect(self.local_env_thread.deleteLater)
        self.local_env_thread.finished.connect(self._clear_local_env_thread)
        self.local_env_thread.start()

    @Slot(int, int, int)
    def _on_run_started(self, index: int, total: int, timeout_s: int) -> None:
        self.status_label.setText(f"第 {index}/{total} 次运行中，timeout={timeout_s} 秒")
        self.progress_bar.setRange(0, total)
        self.progress_bar.setValue(index - 1)
        self.progress_bar.setFormat(f"{index - 1}/{total}")

    @Slot(dict)
    def _on_run_result(self, result: dict[str, Any]) -> None:
        summary = result.get("summary", {})
        run_dir = str(result.get("run_dir", ""))
        row = self.result_table.rowCount()
        if run_dir:
            self.last_output_dir = run_dir
            self.row_output_dirs[row] = run_dir
            rerun_source = Path(run_dir) / "random.s"
            if rerun_source.exists():
                self.row_rerun_sources[row] = str(rerun_source)
        failure_reason = failure_reason_for_run(run_dir, summary)
        reference_sim = summary.get("reference_sim") or {}
        self.result_table.insertRow(row)
        values = [
            result.get("index", ""),
            result.get("status", ""),
            result.get("instr", ""),
            result.get("timeout", ""),
            summary.get("wo_rows", ""),
            summary.get("w_rows", ""),
            summary.get("mismatches", ""),
            reference_sim.get("rows", ""),
            format_reference_compare_cell(summary),
            failure_reason,
        ]
        for col, value in enumerate(values):
            item = QTableWidgetItem(str(value))
            self.result_table.setItem(row, col, item)
        rerun_button = QPushButton("重跑")
        rerun_button.setEnabled(row in self.row_rerun_sources and result.get("status") != "PASS")
        rerun_button.clicked.connect(lambda _checked=False, r=row: self.rerun_table_row(r))
        self.result_table.setCellWidget(row, 10, rerun_button)
        self.result_table.resizeColumnsToContents()
        self.status_label.setText(f"{result.get('status')} - {result.get('message')}")
        index = int(result.get("index", row + 1) or row + 1)
        total = max(self.progress_bar.maximum(), index)
        self.progress_bar.setRange(0, total)
        self.progress_bar.setValue(index)
        self.progress_bar.setFormat(f"{index}/{total}")
        self.settings["last_output_dir"] = self.last_output_dir
        save_config_with_ui(self.cfg, self.settings)

    def rerun_table_row(self, row: int) -> None:
        source = self.row_rerun_sources.get(row, "")
        if not source or not Path(source).exists():
            QMessageBox.warning(self, "无法重跑", "找不到该次运行归档中的 random.s。")
            return
        self.start_runs(1, source_s=Path(source), clear_results=False, label="重跑失败样例")

    @Slot()
    def _on_worker_finished(self) -> None:
        self._set_running(False)
        self._append_log("\n批次结束。\n")

    @Slot()
    def _clear_thread(self) -> None:
        self.thread = None
        self.worker = None

    @Slot(bool, str)
    def _on_local_env_finished(self, ok: bool, message: str) -> None:
        self._set_running(False)
        if ok:
            self.local_env_button.setText("环境已就绪")
            self.local_env_button.setStyleSheet(
                "QPushButton { background-color: #1f9d55; color: white; font-weight: 600; }"
            )
            self.status_label.setText("程序运行环境已就绪")
        else:
            self.local_env_button.setText("一键补齐检测环境")
            self.local_env_button.setStyleSheet(
                "QPushButton { background-color: #b91c1c; color: white; font-weight: 600; }"
            )
            self.status_label.setText(f"程序运行环境异常: {message}")

    @Slot()
    def _clear_local_env_thread(self) -> None:
        self.local_env_thread = None
        self.local_env_worker = None

    def stop_current_run(self) -> None:
        if self.worker is not None:
            self.worker.stop()
        self.stop_button.setEnabled(False)

    def open_output_dir(self) -> None:
        target = self.last_output_dir or str(OUTPUT_DIR)
        path = Path(target)
        if path.exists():
            QDesktopServices.openUrl(QUrl.fromLocalFile(str(path)))
        else:
            QMessageBox.information(self, "输出目录", f"目录不存在: {path}")

    def _open_table_row(self, row: int, _column: int) -> None:
        run_dir = self.row_output_dirs.get(row, "")
        if run_dir:
            path = Path(run_dir)
            if path.exists():
                QDesktopServices.openUrl(QUrl.fromLocalFile(str(path)))

    def _set_running(self, running: bool) -> None:
        self.save_button.setEnabled(not running)
        self.local_env_button.setEnabled(not running)
        self.single_button.setEnabled(not running)
        self.multi_button.setEnabled(not running)
        self.source_button.setEnabled(not running)
        self.stop_button.setEnabled(running)
        self.instr_spin.setEnabled(not running)
        self.run_count_spin.setEnabled(not running)
        self.sim_timeout_spin.setEnabled(not running)
        self.unpack_pipes_check.setEnabled(not running)
        self.reference_compare_check.setEnabled(not running)
        self.auto_timeout_button.setEnabled(not running)

    def closeEvent(self, event) -> None:  # type: ignore[override]
        if self.thread is not None or self.local_env_thread is not None:
            choice = QMessageBox.question(self, "退出", "任务仍在运行，是否停止并退出？")
            if choice != QMessageBox.Yes:
                event.ignore()
                return
            if self.worker is not None:
                self.worker.stop()
        self.settings["geometry"] = bytes(self.saveGeometry().toBase64()).decode("ascii")
        self.settings["instr"] = self.instr_spin.value()
        self.settings["run_count"] = self.run_count_spin.value()
        self.settings["sim_timeout"] = self.sim_timeout_spin.value()
        self.settings["last_output_dir"] = self.last_output_dir
        save_config_with_ui(self.cfg, self.settings)
        event.accept()


def main() -> int:
    subcommand_status = dispatch_cli_subcommand()
    if subcommand_status is not None:
        return subcommand_status
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
