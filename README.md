# P65 CLA BG 测试工具使用说明

这个目录是 P65 CLA BG 测试工具。别人拉下仓库后，不需要开发、不需要重新打包 exe，按下面步骤配置后就可以直接跑测试。

## 1. 目录不要拆开

请保留整个目录，不要只复制 `P65_BG_UI.exe`。

必须一起存在的内容：

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

其中：

- `P65_BG_UI.exe` 是主界面，普通测试人员直接点它。
- `config_p65.json` 保存 SSH、远端仿真目录和测试参数。
- `cache/` 保存 P65 工程模板、两套 `.o`、链接脚本和库，不能删。
- `p65_linux_tools/` 保存本地编译用的 Linux 工具，不能删。
- `random_test/` 保存随机指令生成器，不能删。
- `reference_sim/` 保存本地模拟器，用于“模拟器/WO 对比”功能。
- `custom_random/` 用于放指定的 `random.s`。
- `output/` 保存每次测试结果。

## 2. 电脑需要什么环境

Windows 电脑需要：

1. 能访问远端仿真服务器。
2. 已安装并初始化 WSL。
3. WSL 里能运行 `bash` 和 `python3`。

如果 WSL 是新装的，先在 PowerShell 里手动运行一次：

```powershell
wsl
```

如果进入 WSL 后发现没有 `python3`，在 WSL 里执行：

```bash
sudo apt update
sudo apt install -y python3
```

使用 `P65_BG_UI.exe` 启动时，不需要额外安装 PySide6。

## 3. 启动方式

推荐直接双击：

```text
P65_BG_UI.exe
```

如果 exe 双击没有反应，可以双击：

```text
Start_P65_BG_UI.bat
```

## 4. 首次配置

打开界面后，先检查连接配置：

- SSH Host：服务器 IP。
- Port：通常是 `22`。
- User：服务器用户名。
- Password：服务器密码。
- 仿真目录：远端 VCS 仿真目录，例如 `.../qx_c2000/vcs`。

填好后点击“保存配置”。

注意：密码会保存到本地 `config_p65.json`，只适合内部测试环境使用。

## 5. 单次随机测试

常用流程：

1. 设置“指令数”，例如 `1000`。
2. 设置“仿真时间”，例如 `400` 秒。
3. 点击“单次仿真”。
4. 等待日志打印完成。

程序会自动完成：

```text
生成 random.s
生成 task8.s
本地编译 WO/W 两套镜像
上传到远端仿真目录
远端运行 simv
下载 trace
对比 WO/W
生成 summary.json 和 compare.log
```

## 6. 多次随机测试

如果要连续跑多次：

1. 设置“指令数”。
2. 设置“多次仿真次数”。
3. 点击“多次仿真”。

多次测试会串行执行，每次都会生成独立的输出目录。

## 7. 跑指定 random.s

如果想复现某个固定例子：

1. 把文件放到：

```text
custom_random/random.s
```

2. 点击界面里的“指定 random.s 仿真”。

程序会直接使用这个 `random.s` 跑一次测试，不重新随机生成。

## 8. 模拟器/WO 对比

界面里有“模拟器/WO 对比”选项。

打开后会额外做一件事：

```text
用本地 reference_sim 跑 random.s，生成 reference_sim.gr，
再把 reference_sim.gr 和 RTL 无中断版本 random_wo.gr 做对比。
```

这个功能用于辅助判断 RTL 和模拟器语义是否一致。

注意：模拟器和 RTL 在同周期多写回的打印顺序可能不同，所以如果只看到同一组写回顺序不同，不一定是 RTL 错。

## 9. 测试结果在哪里

每次测试结果都在：

```text
output/<时间>_random/
```

常看这些文件：

```text
summary.json                  总结结果
compare.log                   WO/W 对比日志
analysis_report.md            自动分析报告
random.s                      本次随机源文件
task8.s                       实际编译进 BG task 的汇编
random_wo.gr                  无中断版本 GR trace
random_w.gr                   中断版本 GR trace
reference_sim.gr              模拟器 trace
reference_vs_wo_compare.log   模拟器和 WO 对比日志
sim_wo.log                    远端 WO 仿真日志
sim_w.log                     远端 W 仿真日志
```

## 10. 怎么看结果

如果界面显示 WO/W 对比 PASS，说明：

```text
无中断版本 WO 和中断版本 W 的 BG 执行结果一致。
```

如果 WO/W FAIL，重点看：

```text
analysis_report.md
compare.log
random_wo.gr
random_w.gr
```

常见失败类型：

- W 比 WO 少一行：可能是中断返回后某条写回丢失。
- W 比 WO 多一行：可能是中断返回点或 trace 对齐异常。
- value mismatch：同一个 GR 写回值不一样，需要重点分析。
- 只有 PC 不同：可能是 trace PC 口径问题，要结合上下文判断。

## 11. 常见问题

### 提示 WSL 超时

先手动打开 PowerShell 执行：

```powershell
wsl
```

确认 WSL 能正常进入，不会卡在密码、初始化或 `.bashrc` 输入提示。

### 提示找不到 trace

通常是远端仿真没跑到 BG trace 输出，检查：

- 远端仿真目录是否填对。
- `simv` 是否能运行。
- 远端 TB 是否打开 BG trace。
- 仿真时间是否太短。

### 提示 SSH 失败

检查：

- IP 是否正确。
- 用户名密码是否正确。
- 本机是否能连服务器。
- 服务器是否允许当前网络访问。

### output 可以删除吗

可以。`output/` 只是测试结果目录，删除后下次测试会重新生成。

仓库里只保留 `output/.gitkeep`，用于让空目录存在。

## 12. 命令行测试

普通测试人员建议用 UI。如果需要命令行，可以在当前目录执行：

```powershell
python run_p65_bg.py --instr 1000 --sim-timeout 400
```

使用已有 `random.s`：

```powershell
python run_p65_bg.py --skip-generate --source custom_random\random.s --sim-timeout 400
```

不做模拟器对比：

```powershell
python run_p65_bg.py --instr 1000 --sim-timeout 400 --no-reference-sim
```
