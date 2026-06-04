# P65 CLA BG 测试完整操作指南

本文面向第一次拿到 P65 CLA BG 测试工具的人，按顺序说明：本地如何拉仓库、服务器如何准备 `qx_c2000` 仿真工程、如何打开 TB trace、如何编译 `simv`、如何启动 UI 跑测试，以及测试失败后怎么看结果。

## 1. 整体流程

P65 CLA BG 测试分成两部分：

```text
Windows 本地机器：
  生成 random.s
  生成 task8.s
  本地编译 WO/W 两套 image
  上传 image 到服务器
  下载 trace 和日志
  做 WO/W 对比、生成分析报告

lx4 服务器：
  保存 qx_c2000 仿真工程
  编译 simv
  接收本地上传的 image dat
  运行 ./simv
  输出 BG trace 文件
```

本地工具不会在服务器上跑旧的 `cla_autotest_p65_bg.py`。服务器只负责运行 `simv`。

## 2. Windows 本地拉下测试工具

先安装 Git。然后在 PowerShell 里执行：

```powershell
cd <本地工作目录>
git clone https://github.com/wangtonghui-fdu/cla_bg_p65.git
cd cla_bg_p65
```

如果已经拉过，更新到最新版本：

```powershell
cd <本地工作目录>\cla_bg_p65
git pull
```

目录必须整体保留，不要只复制 `P65_BG_UI.exe`。至少需要这些内容：

```text
P65_BG_UI.exe
Start_P65_BG_UI.bat
config_p65.json
run_p65_bg.py
analyze_bg_mismatch.py

cache/
custom_random/
output/
p65_linux_tools/
random_test/
reference_sim/
```

## 3. Windows 本地环境要求

必须有：

```text
Git
WSL
WSL 里的 bash
WSL 里的 python3
能通过网络 SSH 访问 lx4 服务器
```

第一次使用 WSL 时，在 PowerShell 里先手动打开一次：

```powershell
wsl
```

如果 WSL 里没有 `python3`，进入 WSL 后执行：

```bash
sudo apt update
sudo apt install -y python3
```

UI 本身是打包好的 exe，正常情况下不需要安装 PySide6。  
如果双击 exe 没反应，可以双击：

```text
Start_P65_BG_UI.bat
```

## 4. 在 lx4 服务器拉下 qx_c2000 工程

登录服务器：

```bash
ssh <用户名>@10.18.30.199
```

创建固定工程目录：

```bash
mkdir -p /lx4data/$USER/cla/p65_new
cd /lx4data/$USER/cla/p65_new
```

拉取 P65 `qx_c2000` 工程：

```bash
git clone -b cla-p659 git@10.18.30.198:qx_dsp/qx_c2000.git qx_c2000
```

拉完后目录结构是：

```text
/lx4data/<user>/cla/p65_new/qx_c2000/
  sourceme
  fpga/
  vcs/
  ...
```

如果你已经有工程，只需要更新：

```bash
cd /lx4data/<user>/cla/p65_new/qx_c2000
git pull
```

后面 UI 里的“远端仿真目录”固定填写：

```text
/lx4data/<user>/cla/p65_new/qx_c2000/vcs
```

## 5. 替换服务器仿真目录里的 TB

BG 测试依赖 TB 输出 trace。不要手工在 TB 里一点点插代码，容易漏改或重复定义。统一做法是：进入你的服务器仿真工程目录，备份原来的 `c2000_tb.v`，然后拉取已经打开 BG trace 的 TB 文件，直接替换原文件。

没有正确替换 TB 时，UI 常见报错是：

```text
No non-empty remote trace found
```

### 5.1 进入 qx_c2000 工程目录

```bash
cd /lx4data/<user>/cla/p65_new/qx_c2000
```

确认当前目录下能看到 `fpga/c2000_tb.v` 和 `vcs`：

```bash
ls fpga/c2000_tb.v vcs
```

### 5.2 备份原 TB

替换前必须先备份：

```bash
cp fpga/c2000_tb.v fpga/c2000_tb.v.bak_$(date +%Y%m%d_%H%M%S)
```

### 5.3 拉取已经打开 BG trace 的 TB

把我的 TB 文件拉到服务器当前工程目录下。例如你提供的 TB 放在 Git 仓库、共享目录或服务器固定目录时，按实际位置执行下面其中一种。

如果 TB 在 Git 仓库里：

```bash
git clone <你的TB仓库地址> /tmp/p65_bg_tb
cp /tmp/p65_bg_tb/c2000_tb.v fpga/c2000_tb.v
```

如果 TB 已经在服务器某个固定目录里：

```bash
cp <你的c2000_tb.v实际路径> fpga/c2000_tb.v
```

如果 TB 文件名不是 `c2000_tb.v`，复制时也要改名成目标文件：

```bash
cp <你的TB文件路径> fpga/c2000_tb.v
```

替换完成后检查：

```bash
ls -lh fpga/c2000_tb.v
grep -n "cla_bgtask_sprs_trace.dat\\|cla_bgtask_timeline_trace.dat\\|task8_run" fpga/c2000_tb.v
```

至少应能搜到 `cla_bgtask_sprs_trace.dat`。如果搜不到，说明替换的不是 BG trace 版本 TB。

### 5.4 这个 TB 需要输出哪些 trace

主对比至少需要：

```text
cla_bgtask_sprs_trace.dat
```

辅助定位建议同时输出：

```text
cla_bgtask_pc_trace.dat
cla_bgtask_state_trace.dat
cla_bgtask_irq_trace.dat
cla_bgtask_timeline_trace.dat
```

`cla_bgtask_sprs_trace.dat` 是 WO/W 对比的主输入。其他 trace 主要用于定位“什么时候进入 BG task、什么时候退出、中断什么时候发生、PC 是否跑飞”。

替换 TB 后必须重新编译 `simv`。只替换文件但不重新编译，仿真仍然会用旧 TB。

## 6. 在服务器编译 simv

进入 `qx_c2000` 工程根目录，先 source 环境：

```bash
cd /lx4data/<user>/cla/p65_new/qx_c2000
source sourceme
```

进入 `vcs` 目录编译：

```bash
cd vcs
make comp_fullchip
```

编译成功后，`vcs` 目录下应该有：

```text
simv
simv.daidir/
```

手动检查 `simv` 能否启动：

```bash
./simv +avdd +dvdd
```

如果报动态库缺失，例如：

```text
error while loading shared libraries: libvcspc__...
```

通常是没有在工程根目录执行 `source sourceme`，或者 `make comp_fullchip` 没重新编译完整。重新执行：

```bash
cd /lx4data/<user>/cla/p65_new/qx_c2000
source sourceme
cd vcs
make comp_fullchip
```

`source sourceme` 和 `make comp_fullchip` 一般只需要在工程更新、TB 修改或第一次准备环境时做。后面 UI 直接调用 `simv`。

## 7. 打开 P65 BG UI

Windows 本地双击：

```text
P65_BG_UI.exe
```

第一次打开后填写连接配置：

```text
SSH Host: 10.18.30.199
Port: 22
User: 服务器用户名
Password: 服务器密码
仿真目录: /lx4data/<user>/cla/p65_new/qx_c2000/vcs
```

填完点击“保存配置”。

## 8. 环境检测

UI 里如果有“检测环境”按钮，建议先点一次。它主要检查：

```text
本地脚本是否存在
random_test 是否存在
p65_linux_tools 是否存在
reference_sim 是否存在
WSL 是否能启动
WSL 是否能访问当前 Windows 目录
```

如果提示 WSL 超时，先手动在 PowerShell 里执行：

```powershell
wsl
```

确认不会卡在首次初始化、密码输入、`.bashrc` 交互提示或 sudo 提示。

注意：本工具无法自动安装 WSL。WSL 必须由使用者提前装好并初始化。

## 9. 做一次单次随机测试

推荐先跑小指令数 smoke test：

```text
指令数: 20
仿真时间: 200 秒
```

点击：

```text
单次仿真
```

确认流程能完整跑完后，再跑正常测试：

```text
指令数: 1000
仿真时间: 300 到 500 秒
```

程序会自动完成：

```text
生成 random.s
包装 task8.s
本地生成 task8.o
链接 Release_wo / Release_w
生成 image dat
上传到远端 vcs 目录
远端运行 simv
下载 trace
WO/W 对比
生成 compare.log、summary.json、analysis_report.md
```

## 10. 跑多次随机测试

设置：

```text
指令数: 1000
仿真次数: 例如 10
仿真时间: 300 到 500 秒
```

点击：

```text
多次仿真
```

每次都会生成独立目录：

```text
output/<时间>_random/
```

## 11. 跑指定 random.s

把要复现的文件放到：

```text
custom_random/random.s
```

然后点击：

```text
指定 random.s 仿真
```

如果 UI 里勾选了“拆包运行”，指定 `random.s` 也会按当前配置走拆包逻辑。  
默认不拆包。

## 12. 是否打开“模拟器/WO 对比”

普通 BG 测试建议先关闭。

打开后会额外做：

```text
本地 reference_sim 跑 random.s
生成 reference_sim.gr
把 reference_sim.gr 和 random_wo.gr 对比
```

这个功能用于判断 RTL WO 版本和本地模拟器语义是否一致，不是 BG 中断主流程的必要条件。

如果报：

```text
模拟器/WO: error reference link failed with exit code 1
```

先拉最新仓库：

```powershell
git pull
```

新版已经修复了 reference simulator 链接脚本硬编码 `/mnt/g/QX/.../_main_sim.o` 的问题。  
如果仍失败，看：

```text
output/<时间>_random/reference_sim_error.log
```

## 13. 测试结果在哪里

每次运行都会生成：

```text
output/<时间>_random/
```

重点文件：

```text
summary.json                  总结
compare.log                   WO/W 对比详情
analysis_report.md            自动分析报告
random.s                      本次随机源文件
task8.s                       实际编进 BG task 的汇编
random_wo.gr                  无中断版本 BG GR trace
random_w.gr                   中断版本 BG GR trace
random_wo.pc.trace            WO PC 辅助 trace
random_w.pc.trace             W PC 辅助 trace
random_w.irq.trace            中断/BG 辅助 trace
random_w.timeline.trace       时序辅助 trace
sim_wo.log                    WO 远端仿真日志
sim_w.log                     W 远端仿真日志
reference_sim.gr              本地模拟器 trace
reference_vs_wo_compare.log   模拟器/WO 对比
```

## 14. 怎么判断 PASS / FAIL

### PASS

如果 UI 显示 WO/W PASS，说明：

```text
无中断版本 WO 和中断版本 W 的 BG task 写回结果一致。
```

### FAIL

如果 FAIL，先看：

```text
analysis_report.md
compare.log
```

常见类型：

```text
W 少一行:
  中断版本少了一次 GR 写回，可能是中断返回后某条指令写回丢失。

W 多一行:
  中断版本多了一次 GR 写回，可能是返回点、trace 采样或现场恢复写回过滤问题。

value mismatch:
  同一个 GR 写回值不一致，通常比单纯 PC mismatch 更严重。

PC-only:
  GR和值一致，只有 PC 不同。通常优先怀疑 trace PC 采样口径，也可能是同一写回被不同流水级 PC 标记。
```

## 15. 如何从结果定位到错误指令

优先看 `analysis_report.md`。它会给出：

```text
第一处 mismatch
WO 上下文
W 上下文
附近 random.s 指令
附近 GR trace
可能原因
```

如果要手动看：

1. 打开 `compare.log`，找到第一处 mismatch。
2. 记录 mismatch 附近的 PC。
3. 打开 `task8.s` 或反汇编文件，按 PC 找到对应指令。
4. 对照 `random_wo.gr` 和 `random_w.gr`，看是哪一个 GR 写回多了、少了或值不同。
5. 如果是 W 版本异常，再看：

```text
random_w.irq.trace
random_w.timeline.trace
random_w.pc.trace
sim_w.log
```

判断 mismatch 是否发生在：

```text
刚进入中断附近
中断返回附近
BG task 刚恢复执行附近
三槽指令打包/拆包附近
CR/OFF/BAR/MR 地址寄存器操作附近
```

## 16. 服务器 trace 文件检查

如果 UI 报找不到 trace，登录服务器检查 `vcs` 目录：

```bash
cd /lx4data/<user>/cla/p65_new/qx_c2000/vcs
ls -lh cla_bgtask_sprs_trace.dat cla_gr_trace.dat
```

至少要有一个非空：

```text
cla_bgtask_sprs_trace.dat
cla_gr_trace.dat
```

如果两个都没有或都是 0 字节：

```text
TB 没打开 BG trace
simv 没真正跑起来
仿真时间太短
上传 image 没生效
远端仿真目录填错
```

## 17. 常见报错

### No non-empty remote trace found

含义：远端没有生成非空 BG trace。

检查：

```text
远端仿真目录是否填到 vcs
TB 是否已经替换为 BG trace 版 c2000_tb.v
simv 是否重新编译
仿真时间是否太短
sim_w.log / sim_wo.log 是否有异常
```

### remote sim reached timeout

含义：仿真超过 UI 设置时间，被脚本停止。

如果 trace 已经生成，这不一定是失败；脚本会继续下载 trace 并对比。  
如果 trace 没生成，调大仿真时间或检查 simv 是否卡住。

### WSL path timeout

含义：本地 WSL 无法访问当前 Windows 目录。

检查：

```powershell
wsl
ls /mnt
ls /mnt/<盘符小写>
```

如果仓库放在网络盘或特殊同步目录，建议移到普通本地磁盘，例如：

```text
<本地普通磁盘目录>\cla_bg_p65
```

### reference link failed

含义：本地模拟器链接失败，不是远端 simv 失败。

先更新仓库：

```powershell
git pull
```

再看：

```text
output/<时间>_random/reference_sim_error.log
```

## 18. 命令行方式

UI 是推荐方式。命令行也可以：

```powershell
python run_p65_bg.py --instr 1000 --sim-timeout 400
```

只本地构建，不跑远端：

```powershell
python run_p65_bg.py --instr 20 --no-remote-run
```

跑指定 random.s：

```powershell
python run_p65_bg.py --skip-generate --source custom_random\random.s --sim-timeout 400
```

开启模拟器/WO 对比：

```powershell
python run_p65_bg.py --instr 1000 --sim-timeout 400 --reference-sim
```

关闭模拟器/WO 对比：

```powershell
python run_p65_bg.py --instr 1000 --sim-timeout 400 --no-reference-sim
```

## 19. 推荐首次验证顺序

建议按这个顺序做：

```text
1. Windows 拉 cla_bg_p65 仓库
2. 服务器拉 qx_c2000 工程
3. 服务器修改 c2000_tb.v，打开 BG trace
4. 服务器 source sourceme
5. 服务器 make comp_fullchip
6. UI 填 SSH 和 vcs 目录
7. UI 跑 instr=20 单次仿真
8. PASS 后跑 instr=1000
9. 需要语义辅助判断时，再打开“模拟器/WO 对比”
10. FAIL 时看 analysis_report.md 和 compare.log
```
