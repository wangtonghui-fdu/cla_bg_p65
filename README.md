# P65 CLA BG Local Flow

This folder runs the P65 CLA BG dual-version test with local build and remote simulation only.

## Usage

```powershell
cd G:\new\auto_random_cla\auto_random_cla\cla_bg_p65_v4.0
python .\run_p65_bg.py --instr 1000
```

Common options:

```powershell
python .\run_p65_bg.py --instr 10 --no-remote-run
python .\run_p65_bg.py --skip-generate --source path\to\random.s
python .\run_p65_bg.py --instr 1000 --sim-timeout 300
python .\run_p65_bg.py --instr 1000 --no-reference-sim
```

## Flow

1. Generate `random.s` with the bundled `random_test` generator, or use `--source`.
2. Wrap it into `task8.s` using the BG wrapper.
3. Copy cached P65 `Release_wo` and `Release_w` templates into a timestamped work directory.
4. Assemble `task8.s` locally with the bundled P65 Linux `as.bin`.
5. Link both releases locally with the bundled P65 Linux `ld.bin`, P65 `ldscript`, and P65 `libv2`.
6. Generate RAM images locally with bundled `gen_ram_image.py`.
7. Run the bundled `reference_sim` instruction simulator on `random.s` and extract `reference_sim.gr` from `simulator.log`.
8. Upload image `.dat` files to the configured remote VCS directory.
9. Run remote `simv`, download BG traces, compare WO/W first three whitespace-separated columns, and optionally compare reference simulator GR/value against WO.

The remote side only runs `simv`; this flow does not invoke remote `cla_autotest_p65_bg.py`.

## Local Inputs

The P65 template is expected under:

```text
cache/p65_bg_template/
  Release_wo/
  Release_w/
  ldscript/
  libv2/
```

`Release_wo` comes from `no_int_Release\Release`.
`Release_w` comes from `with_int_Release\Release`.
The P65 build tools are expected under:

```text
p65_linux_tools/
  bin/as.bin
  bin/ld.bin
  bin/objcopy.bin
  bin/objdump.bin
  bin/gen_ram_image.py
```

The local reference simulator is expected under:

```text
reference_sim/
  simulator/simulator_step13
  toolchains/bin/as.bin
  toolchains/bin/ld.bin
  toolchains/lib/qx320f/
  toolchains/test/scripts/trobjdat_8slot.py
  toolchains/tools/objcopy.bin
```

## Output

Each run writes a timestamped folder under `output/`:

```text
output/<timestamp>_<case>/
  random.s
  task8.s
  work/
    Release_wo/
    Release_w/
  Release_wo/
  Release_w/
  random_wo.gr
  random_w.gr
  reference_sim.gr
  reference_simulator.log
  reference_vs_wo_compare.log
  sim_wo.log
  sim_w.log
  compare.log
  summary.json
```
