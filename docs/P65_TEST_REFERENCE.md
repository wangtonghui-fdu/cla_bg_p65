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

## 2. 三方对比

一份随机 `random.s` 会被跑出三条 GR 写回轨迹，做两组对比：

```
            随机 random.s
        ┌────────┼──────────┐
        ▼        ▼          ▼
   RTL 无中断   RTL 有中断   指令级模拟器
   (WO.gr)     (W.gr)      (reference_sim.gr)
        │        │          │
        └─ ① W vs WO ───────┤   后台中断一致性
                            │
        └─ ② 模拟器 vs WO ───┘   RTL/ISA 语义一致性
```

### 2.1 三条轨迹分别是什么

| 轨迹 | 怎么来 | 代表什么 |
|---|---|---|
| `random_wo.gr` | RTL 跑**无中断** bootloader 的后台任务，TB 打印后台 GR 写回 | 后台“正确”基准（没人打扰） |
| `random_w.gr` | RTL 跑**有中断** bootloader（后台运行中反复 `iack` 触发前台 Task1 抢占） | 后台在被抢占情况下的实际结果 |
| `reference_sim.gr` | 本地**指令级模拟器**按 ISA 语义跑同一份 `random.s` | 指令集语义上的“应得结果” |

每行格式统一为 `<reg> <value> <pc> [<time> ns]`，前三列（寄存器号、写回值、PC）是对比依据。

### 2.2 对比 ①：W vs WO（后台中断一致性）

- **比什么**：同一段后台程序，有中断版 `random_w.gr` 与无中断版 `random_wo.gr` 的 GR 写回序列。
- **作用**：验证“**中断抢占不改变后台执行结果**”。两者必须逐行一致；任何不一致都说明中断的
  现场保存/恢复影响了后台。这是测试的主目标。
- **怎么实现**（`run_p65_bg.py::compare_files`）：
  1. `parse_trace_line` 把每行解析成 `(reg, value, pc)`；
  2. 取两侧前三列**逐行比较**，统计 `mismatches`；其中 reg+value 相同只 PC 不同的计入
     `pc_only_mismatches`，reg 或 value 不同的计入 `reg_value_mismatches`；
  3. 若两侧**总行数不同**，记 `row count differs`（说明有一侧多/少写回行）；
  4. `find_single_extra_trace_row` 做**对齐诊断**：尝试删掉某一行后看残余分歧数，判断这是
     “单点多/少一行 + 后续错位级联”还是“多点独立差异”，结果写进 `alignment_issue`。

### 2.3 对比 ②：reference_sim vs WO（RTL/ISA 语义一致性）

- **比什么**：指令级模拟器 `reference_sim.gr` 与 RTL 无中断 `random_wo.gr`。
- **作用**：与中断**无关**，用来判断 **RTL 实现是否符合指令集语义**（即使 WO/W 一致，RTL 也可能
  和模拟器在某些指令上有语义差异）。
- **怎么实现**（`run_p65_bg.py::compare_reference_to_rtl`）：
  1. 两侧都按 `(reg, value, pc)` 解析；
  2. 按 **RTL 的周期/时间戳分组**：把同一拍提交的多个写回归为一组，比较的是“每拍写了哪些
     寄存器=什么值”的集合，而非严格行顺序；
  3. `find_reference_start` 先对齐两侧起点（跳过模拟器启动阶段多出的行）；
  4. 分类差异：**同一拍内写回顺序不同**记为可忽略（`ignorable_reorder_cycles`，因为模拟器与
     RTL 对同周期多写回的打印顺序本就可能不同）；**真正值不同**记为 `real_mismatches`。

> 一句话：**对比 ① 看“有没有被中断搞坏”，对比 ② 看“RTL 是否照 ISA 算对”。** 两者目的不同、
> 实现不同（① 逐行、② 按拍分组并过滤同拍重排）。

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
  以及 `loadu/storeu`（GR 基址自增），使指令流不含间接寻址与自增写回。

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
| `random_w.pc.trace` 等 | （若服务器 TB 装了完整 trace）PC/中断/状态/时间线轨迹，用于看 PC 走向与抢占点 |
| `reference_sim.gr` | 指令级模拟器轨迹 |
| `reference_vs_wo_compare.log` | 模拟器 vs WO 分类对比 |
| `sim_wo.log` / `sim_w.log` | 远端 simv 日志 |
| `Release_wo/` `Release_w/` `work/` | 编译产物与 `.dis` 反汇编、`.map`（PASS 时自动清理，`--keep-scratch` 保留） |

### `summary.json` 关键字段

| 字段 | 含义 |
|---|---|
| `status` / `pass` | pass / fail |
| `wo_rows` / `w_rows` | WO / W 写回行数。两者不相等说明有一侧多/少写回行 |
| `mismatches` | 逐行对比的总分歧数 |
| `pc_only_mismatches` | 仅 PC 不同（reg+value 相同）——通常 trace 口径问题，多为良性 |
| `reg_value_mismatches` | reg 或 value 不同的“真差异” |
| `cr_mismatches` | 其中属于 **CR误差**（差异发生在 `movc2g` 读 CR 的行）的条数（此字段在 039 已加，P65 同步后生效） |
| `failure_reason` | 如 `cr_flag_only`(全部差异都是 CR误差)、`single_extra_or_missing_trace_row`(单行错位) |
| `alignment_issue` | 删哪一行能让后续对齐，残余多少——判断是“单点掉行+级联”还是多点错 |
| `reference_sim.compare_to_wo.real_mismatches` | 模拟器/WO 的**不可忽略**差异条数；`ignorable_reorder_cycles` 为可忽略的同拍重排 |

---

## 6. 怎么分析结果（定位到出错的写回与对应汇编）

本章的目标只到：**找出哪些行没对上、是哪个 GR、什么值不对、对应到 `random.s`/`task8.s` 的
哪条汇编指令、在哪一块**。再往下的成因判断不在测试人员职责内。

先看 `summary.json` 判断是哪一路出问题：
- `mismatches>0` 或 `wo_rows≠w_rows` → 走 **6.1 bgtask 对比（WO/W）**。
- `reference_sim.compare_to_wo.real_mismatches>0` → 走 **6.2 模拟器对比（sim/WO）**。

### 6.1 bgtask 对比（W vs WO）

**第 1 步：看不配对的行数。** 在 `summary.json` / `compare.log` 看：

```text
WO rows: 724        W rows: 486        → 两侧差 238 行（有一侧少写回）
Number of mismatches / Reg/value mismatches
```

- 行数相等：是“同位置写回值不同”的差异。
- 行数不等：有一侧多/少写回行；`alignment_issue` 会提示“删掉某一行后能否对齐、残余多少”，
  帮你判断是单点错位级联还是多点差异。

**第 2 步：找出具体哪个 GR、什么值不对。** `compare.log` 的“Detailed Mismatch Information”
逐条列出 `line N: WO=<reg> <value> <pc> | W=<reg> <value> <pc>`。
注意：行数不等时，首条分歧往往是**错位的起点而非真正缺失的那一行**。要确认到底哪一行没配上，
直接在出问题 PC 邻域**原始对齐两侧 trace**：

```bash
# 把 WO 和 W 在同一段 PC 范围列出来，肉眼找“WO 有、W 没有”（或反之）的那一行
awk '$3>="0x00001000" && $3<="0x00001040"' random_wo.gr
awk '$3>="0x00001000" && $3<="0x00001040"' random_w.gr
```

对齐后即可读出：**缺失/多出的那一行写的是哪个寄存器（如 `0x05`=GR5）、值应是多少、PC 是多少**；
对“值不同”的行，能读出同一 PC 同一寄存器 WO 与 W 各是什么值。

**第 3 步：把 PC 映射回汇编。** 用该行的 PC 到反汇编里查指令（失败的 run 会保留 `work/`，
或加 `--keep-scratch`）：

```bash
# 假设上一步定位到 PC=0x1014
grep -E "^\s*1014:" work/Release_wo/F28P6x_driver_core0.dis
# 看上下文一段
awk '/^\s*1010:/{f=1} f{print} /^\s*1030:/{exit}' work/Release_wo/F28P6x_driver_core0.dis
```

得到那条汇编（例如 `1014: ... movigh gr5 ...`）后，再回到 `task8.s` / `random.s` 找它属于
**哪一块**（按指令顺序/bundle 定位）。到此就完成“出错写回 → 具体 GR 与值 → 对应汇编指令与位置”
的定位。

> 辅助：`analysis_report.md` 已自动把首个分歧的上下文 trace + 反汇编拼好，可先看它再用上面的
> 原始对齐核实真正缺失的行。

### 6.2 模拟器对比（reference_sim vs WO）

**第 1 步：看 `reference_vs_wo_compare.log` / `summary.json`** 里的两个计数：
- `ignorable_reorder_cycles`：同一拍内写回顺序不同 → **可忽略**，不用追。
- `real_mismatches` 与 `first_real_cycle`：真正值不同的条数与第一处所在周期 → 要追这些。

**第 2 步：找出具体哪个 GR、什么值不对。** 在 `reference_vs_wo_compare.log` 里定位到
`first_real_cycle` 那一拍，日志会列出该拍模拟器侧与 WO 侧各写了哪些寄存器=什么值，读出
**是哪个 GR、模拟器值 vs RTL(WO) 值各是多少、对应 PC**。

**第 3 步：把 PC 映射回汇编**（同 6.1 第 3 步）：

```bash
grep -E "^\s*<pc>:" work/Release_wo/F28P6x_driver_core0.dis
```

读出该 PC 的汇编指令，再到 `random.s`/`task8.s` 找到它所在的块。到此完成模拟器侧
“不一致写回 → 具体 GR 与值 → 对应汇编指令与位置”的定位。

> 提示：模拟器对比是 RTL vs 模拟器，与中断无关；它和 bgtask(WO/W) 对比是两套独立的差异，
> 分别按上面两节各自定位即可。

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

- 本测试是 **WO/W 差分（后台中断一致性）+ 模拟器/WO（RTL/ISA 语义一致性）** 的三方对比。
- 两组对比目的与实现都不同：① 逐行比有无被中断改变；② 按拍分组并过滤同拍重排，比 RTL 是否
  照 ISA 算对。
- 测试人员的分析到此为止即可：**看不配对的行数 → 用原始对齐找出是哪个 GR、什么值不对 →
  用 PC 在反汇编里查到对应汇编指令、回到 `random.s`/`task8.s` 定位它在哪一块**。
  （compare.log 首行在行数不等时常是错位起点，务必用原始对齐核实真正缺失/多出的行。）
