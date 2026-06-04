#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass
from pathlib import Path


TRACE_RE = re.compile(r"^\s*(0x[0-9a-fA-F]+)\s+(0x[0-9a-fA-F]+)\s+(0x[0-9a-fA-F]+)(.*)$")
DIS_RE = re.compile(r"^\s*([0-9a-fA-F]+):\s+[0-9a-fA-F ]+\s+(.+?)\s*$")
MAP_TASK8_RE = re.compile(r"^\s*(0x[0-9a-fA-F]+)\s+task8\s*$")
PC_COMMENT_RE = re.compile(r"#\s*pc\s*=\s*(0x[0-9a-fA-F]+)")


@dataclass(frozen=True)
class TraceRow:
    line_no: int
    reg: str
    value: str
    pc: str
    raw: str


@dataclass(frozen=True)
class Mismatch:
    line_no: int
    wo: TraceRow | None
    w: TraceRow | None


def normalize_hex(raw: str, width: int = 8) -> str:
    return f"0x{int(raw, 16):0{width}x}"


def reg_name(raw: str) -> str:
    return f"GR{int(raw, 16)}"


def parse_trace(path: Path) -> list[TraceRow]:
    rows: list[TraceRow] = []
    if not path.exists():
        return rows
    for idx, line in enumerate(path.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
        match = TRACE_RE.match(line)
        if not match:
            continue
        reg, value, pc, _rest = match.groups()
        rows.append(TraceRow(idx, normalize_hex(reg, 2), normalize_hex(value), normalize_hex(pc), line))
    return rows


def first_mismatch(wo_rows: list[TraceRow], w_rows: list[TraceRow]) -> Mismatch | None:
    count = min(len(wo_rows), len(w_rows))
    for idx in range(count):
        if row_key(wo_rows[idx]) != row_key(w_rows[idx]):
            return Mismatch(idx + 1, wo_rows[idx], w_rows[idx])
    if len(wo_rows) != len(w_rows):
        if len(wo_rows) > len(w_rows):
            return Mismatch(count + 1, wo_rows[count], None)
        return Mismatch(count + 1, None, w_rows[count])
    return None


def row_key(row: TraceRow) -> tuple[str, str, str]:
    return row.reg, row.value, row.pc


def mismatch_count(wo_rows: list[TraceRow], w_rows: list[TraceRow]) -> int:
    count = min(len(wo_rows), len(w_rows))
    mismatches = sum(1 for i in range(count) if row_key(wo_rows[i]) != row_key(w_rows[i]))
    return mismatches + abs(len(wo_rows) - len(w_rows))


def find_single_extra_row(wo_rows: list[TraceRow], w_rows: list[TraceRow], around: int) -> tuple[str, int, TraceRow, int] | None:
    """Return side, 1-based line, extra row, residual mismatches after removing it."""
    best: tuple[str, int, TraceRow, int] | None = None
    start = max(1, around - 8)
    end = around + 8
    candidates: list[tuple[str, int, TraceRow, int]] = []
    if len(w_rows) >= len(wo_rows):
        for line_no in range(start, min(end, len(w_rows)) + 1):
            idx = line_no - 1
            residual = mismatch_count(wo_rows, w_rows[:idx] + w_rows[idx + 1 :])
            candidates.append(("W", line_no, w_rows[idx], residual))
    if len(wo_rows) >= len(w_rows):
        for line_no in range(start, min(end, len(wo_rows)) + 1):
            idx = line_no - 1
            residual = mismatch_count(wo_rows[:idx] + wo_rows[idx + 1 :], w_rows)
            candidates.append(("WO", line_no, wo_rows[idx], residual))
    if candidates:
        best = min(candidates, key=lambda item: item[3])
    return best


def parse_task8_address(run_dir: Path) -> int | None:
    for release in ("Release_w", "Release_wo"):
        for base in (run_dir / "work" / release, run_dir / release):
            map_path = base / "F28P6x_driver_core0.map"
            if not map_path.exists():
                continue
            for line in map_path.read_text(encoding="utf-8", errors="replace").splitlines():
                if " task8" not in line:
                    continue
                match = MAP_TASK8_RE.search(line)
                if match:
                    return int(match.group(1), 16)
    return None


def instruction_slots(line: str) -> list[str]:
    code = line.split("#", 1)[0].strip()
    if not code or code.startswith((".", "//")) or code.endswith(":"):
        return []
    normalized = code.replace("||", "|")
    return [part.strip() for part in normalized.split("|") if part.strip()]


def build_task8_pc_map(task8: Path, task8_addr: int | None) -> tuple[dict[int, tuple[int, str, int | None]], list[str]]:
    lines = task8.read_text(encoding="utf-8", errors="replace").splitlines() if task8.exists() else []
    if task8_addr is None:
        return {}, lines
    pc_map: dict[int, tuple[int, str, int | None]] = {}
    linked_pc = task8_addr
    current_comment_pc: int | None = None
    for line_no, line in enumerate(lines, 1):
        match = PC_COMMENT_RE.search(line)
        if match:
            current_comment_pc = int(match.group(1), 16)
            continue
        for slot in instruction_slots(line):
            pc_map[linked_pc] = (line_no, slot, current_comment_pc)
            linked_pc += 4
    return pc_map, lines


def parse_disassembly(run_dir: Path) -> dict[int, str]:
    for release in ("Release_w", "Release_wo"):
        for base in (run_dir / "work" / release, run_dir / release):
            dis_path = base / "F28P6x_driver_core0.S.dis"
            if not dis_path.exists():
                dis_path = base / "F28P6x_driver_core0.dis"
            if not dis_path.exists():
                continue
            dis: dict[int, str] = {}
            for line in dis_path.read_text(encoding="utf-8", errors="replace").splitlines():
                match = DIS_RE.match(line)
                if not match:
                    continue
                dis[int(match.group(1), 16)] = match.group(2).strip()
            return dis
    return {}


def context_rows(rows: list[TraceRow], line_no: int, radius: int = 7) -> list[TraceRow]:
    start = max(1, line_no - radius)
    end = min(len(rows), line_no + radius)
    return rows[start - 1 : end]


def trace_table(title: str, rows: list[TraceRow], highlight: int | None = None) -> list[str]:
    out = [f"### {title}", "", "| line | reg | value | pc | raw |", "|---:|---|---|---|---|"]
    for row in rows:
        mark = " **<--**" if highlight == row.line_no else ""
        out.append(f"| {row.line_no} | {reg_name(row.reg)} | `{row.value}` | `{row.pc}` | `{row.raw}`{mark} |")
    out.append("")
    return out


def dis_context(dis: dict[int, str], pc: int, radius: int = 6) -> list[str]:
    pcs = [addr for addr in sorted(dis) if pc - radius * 4 <= addr <= pc + radius * 4]
    if not pcs:
        return []
    out = ["### Disassembly Context", "", "```asm"]
    for addr in pcs:
        mark = "  <-- first mismatch PC" if addr == pc else ""
        out.append(f"{addr:04x}: {dis[addr]}{mark}")
    out.extend(["```", ""])
    return out


def source_context(pc_map: dict[int, tuple[int, str, int | None]], task8_lines: list[str], pc: int, radius: int = 7) -> list[str]:
    item = pc_map.get(pc)
    if item is None:
        return []
    line_no, _slot, _comment_pc = item
    start = max(1, line_no - radius)
    end = min(len(task8_lines), line_no + radius)
    out = ["### task8.s Context", "", "```asm"]
    for idx in range(start, end + 1):
        mark = "  <-- first mismatch PC" if idx == line_no else ""
        out.append(f"{idx:04d}: {task8_lines[idx - 1]}{mark}")
    out.extend(["```", ""])
    return out


def gr_state(rows: list[TraceRow], until_line_exclusive: int) -> dict[str, str]:
    state: dict[str, str] = {}
    for row in rows:
        if row.line_no >= until_line_exclusive:
            break
        state[reg_name(row.reg)] = row.value
    return state


def state_table(wo_rows: list[TraceRow], w_rows: list[TraceRow], line_no: int, regs: list[str]) -> list[str]:
    wo_state = gr_state(wo_rows, line_no)
    w_state = gr_state(w_rows, line_no)
    out = ["### GR State Before First Mismatch", "", "| reg | WO last value | W last value |", "|---|---|---|"]
    for reg in regs:
        out.append(f"| {reg} | `{wo_state.get(reg, '-')}` | `{w_state.get(reg, '-')}` |")
    out.append("")
    return out


def load_summary(run_dir: Path) -> dict:
    path = run_dir / "summary.json"
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8", errors="replace"))


def generate_report(run_dir: Path, output: Path | None = None) -> Path:
    output = output or run_dir / "analysis_report.md"
    summary = load_summary(run_dir)
    wo_rows = parse_trace(run_dir / "random_wo.gr")
    w_rows = parse_trace(run_dir / "random_w.gr")
    task8_addr = parse_task8_address(run_dir)
    pc_map, task8_lines = build_task8_pc_map(run_dir / "task8.s", task8_addr)
    dis = parse_disassembly(run_dir)
    mismatch = first_mismatch(wo_rows, w_rows)

    lines: list[str] = [
        "# CLA BG Mismatch Analysis",
        "",
        f"- Run directory: `{run_dir}`",
        f"- Status: `{summary.get('status', 'unknown')}`",
        f"- WO rows: `{len(wo_rows)}`",
        f"- W rows: `{len(w_rows)}`",
        f"- Summary mismatches: `{summary.get('mismatches', 'unknown')}`",
        "",
    ]

    if mismatch is None:
        lines.extend(["## Result", "", "No mismatch found in WO/W GR traces.", ""])
        output.write_text("\n".join(lines), encoding="utf-8")
        return output

    wo = mismatch.wo
    w = mismatch.w
    first_pc = int((w or wo).pc, 16)
    extra = find_single_extra_row(wo_rows, w_rows, mismatch.line_no)

    lines.extend(
        [
            "## First Mismatch",
            "",
            f"- First mismatch line: `{mismatch.line_no}`",
            f"- WO: `{format_row(wo)}`",
            f"- W : `{format_row(w)}`",
            "",
        ]
    )

    if extra:
        side, line_no, row, residual = extra
        lines.extend(
            [
                "## Alignment Diagnosis",
                "",
                f"- Best single-row removal: remove `{side}` line `{line_no}`",
                f"- Removed row: `{format_row(row)}`",
                f"- Residual mismatches after removal: `{residual}`",
                "",
            ]
        )
        if residual == 0:
            lines.extend(
                [
                    "Conclusion: this run is dominated by one extra/missing trace row, not a long sequence of independent value errors.",
                    "",
                ]
            )
        if side == "W" and reg_name(row.reg) == "GR30":
            lines.extend(
                [
                    "Likely cause: W interrupt flow captured an extra GR30 context/SP write in the BG GR trace.",
                    "The task instruction at the same PC is not a GR30 write, so this is trace pollution or interrupt context writeback visibility.",
                    "",
                ]
            )

    item = pc_map.get(first_pc)
    if item:
        line_no, slot, comment_pc = item
        lines.extend(
            [
                "## Instruction At Mismatch PC",
                "",
                f"- Linked/task trace PC: `{first_pc:#06x}`",
                f"- task8.s line: `{line_no}`",
                f"- task8.s slot: `{slot}`",
                f"- Nearest generator `#pc`: `{comment_pc:#010x}`" if comment_pc is not None else "- Nearest generator `#pc`: `unknown`",
                f"- Disassembly: `{dis.get(first_pc, 'unknown')}`",
                "",
            ]
        )
    else:
        lines.extend(
            [
                "## Instruction At Mismatch PC",
                "",
                f"- Linked/task trace PC: `{first_pc:#06x}`",
                "- Could not map this PC back to task8.s.",
                f"- Disassembly: `{dis.get(first_pc, 'unknown')}`",
                "",
            ]
        )

    regs: list[str] = []
    for row in [wo, w, extra[2] if extra else None]:
        if row is None:
            continue
        name = reg_name(row.reg)
        if name not in regs:
            regs.append(name)
    for name in ("GR30", "GR5", "GR11", "GR16"):
        if name not in regs:
            regs.append(name)

    lines.extend(state_table(wo_rows, w_rows, mismatch.line_no, regs))
    lines.extend(trace_table("WO Trace Context", context_rows(wo_rows, mismatch.line_no), wo.line_no if wo else None))
    lines.extend(trace_table("W Trace Context", context_rows(w_rows, mismatch.line_no), w.line_no if w else None))
    lines.extend(dis_context(dis, first_pc))
    lines.extend(source_context(pc_map, task8_lines, first_pc))

    output.write_text("\n".join(lines), encoding="utf-8")
    return output


def format_row(row: TraceRow | None) -> str:
    if row is None:
        return "<missing>"
    return f"{reg_name(row.reg)} {row.value} {row.pc}"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate CLA BG mismatch analysis report for one output directory.")
    parser.add_argument("run_dir", type=Path)
    parser.add_argument("--output", type=Path, default=None)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    path = generate_report(args.run_dir.resolve(), args.output)
    print(f"Analysis report: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
