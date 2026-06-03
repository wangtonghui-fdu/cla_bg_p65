import os
import random
import sys


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)

from slot1.slot1 import handle_slot1_instr
from slot1.slot1 import alu_calculate_instr_map, alu_compare_instr_map, mov_instr_map
from load_store.load_store import handle_slot2_instr, handle_slot3_instr
from fpu.fpu import handle_fpu_instr
from jmp.devide import devide_instr
from jmp.jmp import check_jmp, START_SIGN, HIGH_ADDR, LOW_ADDR
from config.config import ClaConfig, Double_WB_instr
from global_state.global_state import MARK_SIGN, print_reg, slot1_queue, slot2_queue, slot3_queue
from global_state.global_state import return_instr_count
from tool.tool import format_imm
from tool.ram import calc_data_region, DATA_BLOCK
from config.config import BASE_PC
from config.config import TestConfig, JmpConfig


CLA_NOT_SUPPORT_ALU = ClaConfig.CLA_NOT_SUPPORT_ALU
CLA_NOT_SUPPORT_MOV = ClaConfig.CLA_NOT_SUPPORT_MOV
CLA_NOT_SUPPORT_SLOT1 = CLA_NOT_SUPPORT_MOV + CLA_NOT_SUPPORT_ALU

S1_DOUBLE_WB_INSTR = Double_WB_instr.S1_DOUBLE_WB_INSTR
FINTDIV_INSTR = Double_WB_instr.FINTDIV_INSTR
S2_DOUBLE_WB_INSTR = Double_WB_instr.S2_DOUBLE_WB_INSTR
S1_DELAY_SLOT = Double_WB_instr.S1_DELAY_SLOT

slot1_instr_map = {**mov_instr_map, **alu_compare_instr_map, **alu_calculate_instr_map}
cla_instr_map = [key for key in slot1_instr_map if key not in CLA_NOT_SUPPORT_SLOT1]
CLA_SUPPORT_SLOT3 = ClaConfig.CLA_SUPPORT_SLOT3

PACKED_INSTR = TestConfig.PACKED_INSTR
TEST_JMP_CALL = TestConfig.TEST_JMP_CALL
TEST_BACK_END = TestConfig.BACK_END_TEST
TEST_CLA = TestConfig.TEST_CLA
FPU_TEST = TestConfig.FPU_TEST
DOUBLE_WB_PACK = TestConfig.DOUBLE_WB_PACK

FUNCTION_NAMES = JmpConfig.FUNCTION_NAMES
START_PART = JmpConfig.START_PART
FINISH_PART = JmpConfig.FINISH_PART

OUTPUT_DIR = os.path.abspath(os.getenv("QX_OUTPUT_DIR", os.path.join(BASE_DIR, "generate")))
TEMPLATE_FILE = os.path.join(BASE_DIR, "txt", "start.s")
TEMPLATE_FILE_JMP = os.path.join(BASE_DIR, "txt", "start_jmp.s")
TEMPLATE_FILE_BACK_END = os.path.join(BASE_DIR, "txt", "start_backend.s")


def can_dequeue(entry, s1_head, s2_head, s3_head, slot, cla=False):
    d1, d2, d3 = entry["dep"]

    if slot == 1:
        if not cla:
            return (s2_head >= d2 or s2_head == 0) and (s3_head >= d3 or s3_head == 0)
        return (s1_head > d1 + 1) and (s2_head > d2 or s2_head == 0) and (s3_head > d3 or s3_head == 0)
    if slot == 2:
        return (s1_head >= d1) and (s3_head >= d3)
    if slot == 3:
        return (s1_head >= d1) and (s2_head >= d2)
    raise ValueError("slot must be 1, 2 or 3")


def run_generation(output_name: str, count: int) -> str:
    try:
        count = int(count)
    except ValueError as exc:
        raise ValueError("count must be an integer") from exc

    DATA_BLOCK["RAM"] = calc_data_region(count)
    if DATA_BLOCK["RAM"] != (0, 0):
        start_addr = hex(DATA_BLOCK["RAM"][0])
        end_addr = hex(DATA_BLOCK["RAM"][1])
        print(f"Data range: RAM[{start_addr} ~ {end_addr}]")
    else:
        start_addr = hex(DATA_BLOCK["FLASH"][0])
        end_addr = hex(DATA_BLOCK["FLASH"][1])
        print("RAM has no free range, data will use peripheral space.")
        print(f"Data range: FLASH[{start_addr} ~ {end_addr}]")

    if TEST_JMP_CALL:
        devide_instr(count)

    instr_count = 0
    while instr_count < count:
        for _ in range(random.randint(1, 4)):
            if check_jmp(TEST_JMP_CALL):
                continue
            handle_slot1_instr(output_name)
            instr_count = return_instr_count()

        instr_count = return_instr_count()
        if check_jmp(TEST_JMP_CALL):
            continue
        handle_slot2_instr(output_name)

        instr_count = return_instr_count()
        if check_jmp(TEST_JMP_CALL):
            continue
        handle_slot3_instr(output_name)

        instr_count = return_instr_count()
        if check_jmp(TEST_JMP_CALL):
            continue

        if FPU_TEST:
            handle_fpu_instr(output_name)
            instr_count = return_instr_count()

    print(f"\nGenerated {instr_count} instructions")
    print_reg()
    if TEST_CLA:
        print("\nCLA mode is enabled")

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    output_path = os.path.join(OUTPUT_DIR, f"{output_name}.s")

    with open(output_path, "w", encoding="utf-8") as output_file:
        if not TEST_JMP_CALL and not TEST_BACK_END:
            if os.path.exists(TEMPLATE_FILE):
                with open(TEMPLATE_FILE, "r", encoding="utf-8") as start_file:
                    output_file.write(start_file.read())
                    output_file.write("\n\n")
        elif TEST_JMP_CALL:
            if os.path.exists(TEMPLATE_FILE_JMP):
                with open(TEMPLATE_FILE_JMP, "r", encoding="utf-8") as start_file:
                    output_file.write(start_file.read())
                    output_file.write("\n\n")
        elif TEST_BACK_END:
            if os.path.exists(TEMPLATE_FILE_BACK_END):
                with open(TEMPLATE_FILE_BACK_END, "r", encoding="utf-8") as start_file:
                    output_file.write(start_file.read())
                    output_file.write("\n\n")

        write_line = 0
        command_num = 0
        total_count = 0
        in_nop_sequence = False
        s1_head = 0
        s2_head = 0
        s3_head = 0
        s1_delay_slot = 0
        function_now = " "
        pc = 0

        while slot1_queue or slot2_queue or slot3_queue:
            s1 = ""
            s2 = ""
            s3 = ""

            s1_pop = False
            s2_pop = False
            s3_pop = False
            s1_slot3_pop = False
            s1_double_pack = True
            s1_is_fintdiv = False

            if slot1_queue and can_dequeue(slot1_queue[0], s1_head, s2_head, s3_head, 1):
                entry = slot1_queue.pop(0)
                s1 = entry["inst"]
                s1_pop = True

                if s1 in START_SIGN:
                    output_file.write(f"\n{s1}:\n")
                    function_now = f"{s1}"
                    addr = START_SIGN[function_now]
                    addr = format_imm(imm=addr, src_width=32)
                    output_file.write(f"#pc = 0x{pc:08X} {function_now} addr=0x{addr} \n")
                    total_count = 0
                    s1_head += 1
                    continue

                if s1 in MARK_SIGN:
                    output_file.write(f"\n{s1}:\n")
                    total_count = 0
                    s1_head += 1
                    continue

                if s1.split()[0] in S1_DOUBLE_WB_INSTR:
                    s1_double_pack = DOUBLE_WB_PACK
                    command_num += 1
                elif s1.split()[0] in FINTDIV_INSTR:
                    s1_is_fintdiv = True
                    command_num += 1
                elif s1.endswith(HIGH_ADDR) or s1.endswith(LOW_ADDR):
                    function = s1.split()[2]
                    mov = s1.split()[0]
                    rd = s1.split()[1]
                    command_num += 1

                    if s1.endswith(HIGH_ADDR):
                        function = function.replace(HIGH_ADDR, "")
                        addr = START_SIGN[function]
                        addr = format_imm(imm=addr, src_width=32)
                        high_bits = addr[:4]
                        s1 = f"{mov} {rd} 0x{high_bits}"
                    else:
                        function = function.replace(LOW_ADDR, "")
                        addr = START_SIGN[function]
                        addr = format_imm(imm=addr, src_width=32)
                        low_bits = addr[4:]
                        s1 = f"{mov} {rd} 0x{low_bits}"
                        output_file.write(f"\n# call {function}\n")
                else:
                    command_num += 1

                if s1.split()[0] in S1_DELAY_SLOT:
                    s1_delay_slot = 3

            if slot2_queue and can_dequeue(slot2_queue[0], s1_head, s2_head, s3_head, 2):
                if s1_double_pack and not s1_is_fintdiv:
                    entry = slot2_queue.pop(0)
                    s2_pop = True
                    s2 = entry["inst"]
                    command_num += 1

            if slot3_queue and can_dequeue(slot3_queue[0], s1_head, s2_head, s3_head, 3):
                entry = slot3_queue.pop(0)
                s3_pop = True
                s3 = entry["inst"]
                command_num += 1
            else:
                if (
                    TEST_CLA
                    and s1_delay_slot == 0
                    and slot1_queue
                    and can_dequeue(slot1_queue[0], s1_head, s2_head, s3_head, 1, cla=TEST_CLA)
                ):
                    entry = slot1_queue[0]
                    first_part = entry["inst"].split(" ")[0]
                    if first_part in CLA_SUPPORT_SLOT3:
                        slot1_queue.pop(0)
                        s1_slot3_pop = True
                        command_num += 1
                        s3 = entry["inst"]

            if s1_pop:
                s1_head += 1
            if s2_pop:
                s2_head += 1
            if s3_pop:
                s3_head += 1
            if s1_slot3_pop:
                s1_head += 1
            if s1_delay_slot:
                s1_delay_slot -= 1

            if s1 and s1.split()[0] == "movc2g":
                for _ in range(5):
                    output_file.write("nop||\n")
                write_line += 5
                command_num += 5
                total_count += 5

            if PACKED_INSTR:
                output_file.write(f"{s1}|{s2}|{s3}\n")
                write_line += 1
            else:
                if s1:
                    output_file.write(f"{s1}||\n")
                    write_line += 1
                if s2:
                    output_file.write(f"|{s2}|\n")
                    write_line += 1
                if s3:
                    output_file.write(f"||{s3}\n")
                    write_line += 1

            total_count += 1
            current_is_nop = (s1 == "nop") or (s2 == "nop") or (s3 == "nop")
            pc = command_num * 4 + BASE_PC

            if current_is_nop:
                in_nop_sequence = True
            else:
                if in_nop_sequence:
                    if total_count >= 4:
                        output_file.write("\n")
                        output_file.write(f"#pc = 0x{pc:08X} {function_now}\n")
                        total_count = 0
                    in_nop_sequence = False
                else:
                    if total_count >= 4:
                        output_file.write("\n")
                        output_file.write(f"#pc = 0x{pc:08X} {function_now}\n")
                        total_count = 0

    if not PACKED_INSTR:
        print("Packed instruction mode is disabled\n")

    print(f"Generated {write_line} packed lines into {output_path}")
    return output_path


def main():
    if len(sys.argv) != 3:
        print("Usage: python main.py <output_name> <count>")
        sys.exit(1)

    try:
        run_generation(sys.argv[1], int(sys.argv[2]))
    except Exception as exc:
        print(f"Generation failed: {exc}")
        raise


if __name__ == "__main__":
    main()
