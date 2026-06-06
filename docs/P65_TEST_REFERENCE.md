# P65 CLA BG 测试技术说明（原理 / 模块 / 流程 / 结果分析）

本文是 P65 CLA 后台任务（Background Task，BG）随机指令测试的**技术参考**：测试在测什么、
怎么测、每个模块干什么、流程与原理、输出含义，以及失败后如何定位根因。

> 面向需要理解内部机制、排查 RTL 缺陷的人。只想点界面跑测试，看
> [README.md](../README.md) 和 [P65_CLA_BG_OPERATION_GUIDE.md](P65_CLA_BG_OPERATION_GUIDE.md)。

---

## 1. 测试在测什么（目标）

CLA（Control Law Accelerator）支持**后台任务**：一段低优先级任务（task8 / background）在
空闲时持续运行，可被高优先级**前台任务**（Task1..7，由中断/`iack` 触发）**抢占**。抢占时
硬件负责保存后台现场，前台跑完后硬件恢复现场、后台从断点继续。

本测试要验证的核心命题：

> **同一段后台程序，在“无中断”和“有中断抢占”两种情况下，执行结果必须完全一致。**

把同一份随机指令流编译成两套镜像：

- **WO**（With-Out interrupt）：后台不被抢占，作为**黄金参考**。
- **W**（With interrupt）：后台运行中反复被前台 Task1 抢占。

比较两者的 GR（通用寄存器）写回轨迹。**只要 W ≠ WO，就说明中断抢占破坏了后台执行**——
即 CLA 流水线/中断现场保存恢复存在缺陷。这是一个**差分测试（differential testing）**。

可选第三路 **reference simulator（指令级模拟器）**：用本地模拟器跑同一份 `random.s`，
与 RTL 的 WO 对比，用来判断 **RTL 与 ISA 语义**是否一致（与中断无关）。

---

## 2. 三方对比与三类 Bug

```
            随机 random.s
        ┌────────┼─────────┐
        ▼        ▼         ▼
   RTL 无中断  RTL 有中断  指令级模拟器
    (WO.gr)    (W.gr)     (reference_sim.gr)
        │        │         │
        ├── W vs WO ───────┤   → 中断现场缺陷 (Bug A / Bug B)
        └── 模拟器 vs WO ───┘   → RTL/ISA 语义差异 (Bug C)
```

| 类别 | 对比 | 现象 | 含义 |
|---|---|---|---|
| **Bug A** | W vs WO | W 比 WO **少行**（写回被丢），值被污染、级联，严重时 PC 跑飞、后台提前终止 | 中断恢复点丢失某条指令的 GR 写回（含 FPU/自增的延迟扩展写回 `wenx`）。**真实缺陷** |
| **Bug B** | W vs WO | 行数相等，某条 `movc2g` 读到的 **CR 值差 bit4（CON）**，标记“CR误差” | 中断没保存/恢复控制寄存器 CR；前台比较指令的 CON 标志泄漏给后台。CON 又写不回（只能由比较指令置位）。**真实缺陷** |
| **Bug C** | 模拟器 vs WO | 同周期写回顺序不同（可忽略）；`fcvtus` 等 1-ULP 舍入差异（真实） | RTL 截断 vs 模拟器就近舍入等语义细节。与中断无关 |

> 区分关键：**Bug A 会改变行数（掉写回）；Bug B 行数不变只值差且发生在 `movc2g`；Bug C 只在
> 模拟器/WO 一路出现。** 详见各自的 `docs/bugs/` 写作（039 侧有完整案例，机理对 P65 通用）。

---

## 3. 项目各模块的作用

### 3.1 顶层（编排 / 界面）

| 文件/目录 | 作用 |
|---|---|
| `run_p65_bg.py` | **核心编排脚本**。完成：生成→编译 WO/W→上传→远端 simv→下载 trace→对比→出 `summary.json`。命令行与 UI 都调它 |
| `p65_bg_ui.py` | PySide6 图形界面：参数设置、单次/多次/指定 `random.s` 仿真、结果表、对比简报。打包成 `P65_BG_UI.exe` |
| `analyze_bg_mismatch.py` | 失败后自动生成 `analysis_report.md`：把首个分歧点、上下文 trace、对应反汇编、抢占点拼到一起 |
| `config_p65.json` | 全部配置：SSH、远端目录、本地工具链、`project_out`、参数、窗口状态。**含明文密码，禁止提交公开仓库** |
| `Build_P65_BG_UI_EXE.bat` | 用 PyInstaller 把 UI 打包成单文件 exe |
| `bootstrap_ui_env.py` | 首次运行准备 UI 运行环境 |

### 3.2 资源 / 缓存

| 目录 | 作用 |
|---|---|
| `cache/` | P65 `qx_c2000` 工程模板、两套 `.o`、链接脚本、库。本地编译镜像的底座，**不能删** |
| `p65_linux_tools/` | 本地编译用的 Linux 工具（P65 走 **WSL** + `.bin` 工具链；039 走 Windows `.exe`），**不能删** |
| `reference_sim/` | 本地指令级模拟器 + 工具链，用于“模拟器/WO 对比”，**不能删** |
| `custom_random/` | 放指定的 `random.s` 用于复现 |
| `output/` | 每次测试的结果目录 `output/<时间>_random/` |
| `bootloader/` | 上传到远端的 bootloader 镜像 |

### 3.3 指令生成器 `random_test/instr_generate/`

把随机指令、依赖、打包逻辑分模块管理：

| 模块 | 作用 |
|---|---|
| `main.py` | 入口：`python main.py <case> <number>`。`random` = 全指令随机并按 3 槽打包 |
| `config/config.py` | 全局开关：`PACKED_INSTR`(打包)、`DISABLE_CLA_ADDR_REGS`(禁用特殊/间接寄存器)、各指令是否支持、槽位约束 |
| `config/weight_model.py` | 各指令出现权重 |
| `slot1/` | slot1 指令：`mov.py`(movigh/movigl/movg2c/movc2g…)、`alu_calculate.py`(加减等)、`alu_compare.py`(gt/lt/eq/neqi… **置 CON**) |
| `fpu/fpu.py` | CLA 浮点：fsmul/fsdiv/fsmac/fsadd/fssqrt/fcvt*/fseq… |
| `load_store/` | 访存：`load_function.py`/`store_function.py`/`load_store.py`。区分 `load/store`(普通)、`loadu/storeu`(**GR+立即数自增**，走扩展写回)、`loado/storeo`(**OFF/BAR/MR 间接寻址**)、`loadi/storei`(立即) |
| `jmp/` | 跳转与除法 `jmp.py`/`devide.py` |
| `tmu/` `vcu/` `fintdiv/` | 三角运算单元、向量比较单元、整数除法 |
| `peripheral/` `global_state/` | 外设(I2C)、全局状态相关指令 |
| `tool/` | `tool.py`(寄存器/依赖管理、打包、enqueue)、`ram.py`(内存地址/数据准备) |

**两个关键开关（环境变量注入）**：

- `QX_PACKED_INSTR=1/0`：打包/不打包。打包=一条 bundle 多槽并行；不打包=每条单独占槽。
- `QX_DISABLE_CLA_ADDR_REGS=1`：禁用“特殊寄存器”。会从随机池排除 `loado/storeo`（用 OFF/BAR/MR）
  以及 `loadu/storeu`（GR 自增，走扩展端口 `wenx`），使指令流不含间接寻址与自增写回。

> `run_p65_bg.py` 的 `generate_random()` 用 `os.environ.copy()` 起子进程，所以可在调用前用
> 环境变量注入，或在 `config_p65.json.local.disable_cla_addr_regs` 配置。

---

## 4. 测试流程与原理

```
Windows 本地                                         lx4 服务器 (10.18.30.199)
────────────────────────────────────────────       ──────────────────────────
1. generate_random()  生成器→ random.s
2. prepare_task8()    包装成 BG task8.s（+尾部 mstop）
3. build_dual()       本地 WSL 编译两套镜像：
      Release_wo  (无中断 bootloader)
      Release_w   (有中断 bootloader: iack 触发 Task1)
4. simulate_dual():
      upload images ─────────────────────────────►  写入 qx_c2000/vcs
      run_remote_sim() ───────────────────────────►  ./simv  (跑 WO 一次、W 一次)
      download_trace() ◄───────────────────────────  cla_bgtask_sprs_trace.dat 等
5. compare_files()    WO/W GR trace 逐行对比
6. (可选) reference simulator：本地跑 random.s → reference_sim.gr
   compare_reference_to_rtl()  模拟器 vs WO（按周期分组，过滤可忽略重排）
7. 写 summary.json / compare.log / analysis_report.md
```

**中断从哪来**：有中断的 bootloader（`others/bgtask_interrupt.c` 对应逻辑）在后台运行期间，
循环执行 `iack 0x1`（约 11 次），每次触发前台 CLA Task1，抢占后台 task8。抢占与现场
保存/恢复**由硬件完成**，不是软件保存。这正是被测对象。

**GR trace 怎么来**：服务器 TB（`fpga/c2000_tb.v`）在后台运行窗口内，把每拍提交到 GR 寄存器堆
的写回（寄存器号、值、PC、时间）打印成 `cla_bgtask_sprs_trace.dat`，下载后存为
`random_wo.gr` / `random_w.gr`。每行格式：`<reg> <value> <pc> [<time> ns]`。

> P65 与 039 的差异：P65 用 WSL `.bin` 工具链、工程 `p6/qx_c2000`、`project_out=F28P6x_driver_core0`；
> 039 用 Windows `.exe`、工程 `T55_039_NTO/qx_c2000`、`F280039_driver_core0`。
> 两仓库共享文件用 `check_bg_sync.py` 跟踪漂移。

---

## 5. 输出文件与含义

每次测试在 `output/<时间>_random/`：

| 文件 | 含义 |
|---|---|
| `summary.json` | **结果总览**（见下表字段）。UI 和分析都读它 |
| `compare.log` | WO/W 逐行对比详情：结果、行数、各类 mismatch 计数、首个分歧、对齐诊断、逐条差异 |
| `analysis_report.md` | 自动分析报告：首分歧上下文 trace + 反汇编 + 抢占点 |
| `random.s` | 本次随机源（打包形态） |
| `task8.s` | 实际编译进后台任务的汇编 |
| `random_wo.gr` / `random_w.gr` | WO / W 的 GR 写回轨迹（核心证据） |
| `random_w.pc.trace` 等 | （若服务器 TB 装了完整 trace）PC/中断/状态/时间线轨迹，用于看跑飞与抢占点 |
| `reference_sim.gr` | 指令级模拟器轨迹 |
| `reference_vs_wo_compare.log` | 模拟器 vs WO 分类对比 |
| `sim_wo.log` / `sim_w.log` | 远端 simv 日志 |
| `Release_wo/` `Release_w/` `work/` | 编译产物与 `.dis` 反汇编、`.map`（PASS 时自动清理，`--keep-scratch` 保留） |

### `summary.json` 关键字段

| 字段 | 含义 |
|---|---|
| `status` / `pass` | pass / fail |
| `wo_rows` / `w_rows` | WO / W 写回行数。**`w_rows < wo_rows` = 掉行 = Bug A** |
| `mismatches` | 逐行对比的总分歧数 |
| `pc_only_mismatches` | 仅 PC 不同（reg+value 相同）——通常 trace 口径问题，多为良性 |
| `reg_value_mismatches` | reg 或 value 不同的“真差异” |
| `cr_mismatches` | 其中属于 **CR误差（movc2g 读 CR）** 的条数——Bug B（注：此字段在 039 已加，P65 同步后生效） |
| `failure_reason` | 如 `cr_flag_only`(全是 CR误差)、`single_extra_or_missing_trace_row`(单行错位) |
| `alignment_issue` | 删哪一行能让后续对齐，残余多少——判断是“单点掉行+级联”还是多点错 |
| `reference_sim.compare_to_wo.real_mismatches` | 模拟器/WO 的**不可忽略**差异（Bug C，如 1-ULP）；`ignorable_reorder_cycles` 为可忽略重排 |

---

## 6. 怎么分析结果、定位根因

### 步骤 0：先看 `summary.json`
- `pass=true` → 通过。
- `w_rows < wo_rows` → **掉行，走 Bug A 分析**。
- 行数相等但 `cr_mismatches>0` / `failure_reason=cr_flag_only` → **Bug B（CR误差）**。
- `reference_sim...real_mismatches>0` → **Bug C（看模拟器/WO 日志）**。

### 步骤 1：找真正被丢的写回（Bug A，不要只信 compare.log 首行）
compare.log 的“首个分歧”在级联里**会误指**。可靠做法是**原始对齐 WO/W**：

```bash
# 在某个 PC 邻域对齐 WO/W（reg value pc）
awk '$3>="0x00001000" && $3<="0x00001040"' random_wo.gr
awk '$3>="0x00001000" && $3<="0x00001040"' random_w.gr
```

找出 WO 有、W 没有的那一行，就是被丢的写回。再用反汇编看那条指令：

```bash
# 反汇编（PASS 清理了 work/，失败会保留；或用 --keep-scratch）
grep -E "^\s*1014:" work/Release_wo/F28P6x_driver_core0.dis
```

### 步骤 2：对上抢占点
被丢的写回几乎都在**中断恢复点附近**。看抢占 `prev_pc`：

```bash
grep -oE "prev_pc=0x[0-9a-f]+" random_w.irq.trace | tr '\n' ' '
```

若某次 `prev_pc` 紧邻被丢指令的前一两拍，即“抢占→恢复→该指令写回丢失”。
**结论性认知（本项目实测）**：被丢的可以是任意端口的写回（普通 mov/ALU、FPU 延迟写回、
load/store 自增 `wenx`），所以**靠生成器禁某类指令无法根治**，根因在 RTL 中断恢复的写回保持。

### 步骤 3：看是否级联成“跑飞”
若被污染的寄存器随后被当作**地址基址或跳转目标**，会野访存甚至 PC 跳进前台代码区：

```bash
tail -25 random_w.pc.trace          # 看 PC 是否跳到低地址(前台区)、run 状态何时变 0
grep "run=1" random_w.pc.trace | tail -5
```

后台撞进前台代码并执行到前台 `mstop` → 后台提前终止 → `w_rows` 远小于 `wo_rows`。

### 步骤 4：Bug B（CR误差）确认
若分歧落在 `movc2g`：

```bash
# 该 PC 是不是 movc2g；差异是否仅 bit4(0x10=CON)
grep -E "^\s*<pc>:" work/Release_wo/*.dis
```

CR 位定义（手册 §2.2）：bit14=EALLOW、[13:8]=OVC、bit7=OF、bit5=OVM、**bit4=CON（标量比较结果，
粘滞，只能由比较指令置位）**、bit2=LVF、bit1=LUF、bit0=CF。前台 Task1 的比较指令把 CON 改了，
返回后台没恢复（`movg2c` 也写不回 CON）→ 后台 `movc2g` 读到前台的 CON。

### 步骤 5：Bug C（模拟器/WO）
看 `reference_vs_wo_compare.log`：
- `ignorable_reorder_cycles`：同周期写回顺序不同 → **可忽略**。
- `real_mismatches`：如 `fcvtus` 的 1-ULP（RTL 截断 vs 模拟器就近舍入）→ **真实语义差异**，与中断无关。

---

## 7. 命令行速查

```powershell
# 标准：1000 指令、打包、含模拟器对比
python run_p65_bg.py --instr 1000 --sim-timeout 400

# 禁用特殊寄存器（间接寻址+自增）+ 对比模拟器
#   （或在 config_p65.json.local.disable_cla_addr_regs=true）
$env:QX_DISABLE_CLA_ADDR_REGS=1; python run_p65_bg.py --instr 1000 --sim-timeout 400 --reference-sim

# 不打包（每条单槽，槽位忠实）
python run_p65_bg.py --instr 1000 --no-pack

# 复现指定例子（不重新随机）
python run_p65_bg.py --skip-generate --source custom_random\random.s --sim-timeout 400 --keep-scratch

# 跳过模拟器
python run_p65_bg.py --instr 1000 --no-reference-sim
```

---

## 8. 小结

- 本测试是 **WO/W 差分 + 模拟器/WO 语义** 三方对比。
- **Bug A**（掉写回，会级联到跑飞）和 **Bug B**（CR/CON 未跨中断保护）是两处**独立**的中断现场
  缺陷；**Bug C** 是 RTL/ISA 语义差异（多为 1-ULP）。
- 定位根因的关键纪律：**用原始 WO/W 对齐找真正被丢的行**（别信 compare.log 首行），对上抢占点，
  再看是否级联到地址/PC 跑飞；CR 类差异看是不是 `movc2g` 的 CON 泄漏。
