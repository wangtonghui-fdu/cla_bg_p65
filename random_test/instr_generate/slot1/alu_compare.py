import random


from config.config import TestConfig
from tool.tool import TEST_CLA, distribute_reg, generate_imm, select_registers 
from tool.tool import insert_data_reg,probability_return

from global_state.global_state import update_written_registers, update_recent_written_registers,update_slot_rely
from global_state.global_state import recent_written_registers
from global_state.global_state import enqueue_instruction,get_queue_tail_index

from global_state.global_state import slot1_queue
from slot1.alu_calculate import check_control

TEST_CLA = TestConfig.TEST_CLA

WAIT_TIMES_BASE = {
    "eqi": 1,  
    "eq": 1,  
}

# 根据 TEST_CLA 设置系数
if TEST_CLA:
    SCALE_FACTOR = 1  # 或者其他你想要的系数
else:
    SCALE_FACTOR = 1

# 应用系数得到最终的等待时间
WAIT_TIMES = {key: value * SCALE_FACTOR for key, value in WAIT_TIMES_BASE.items()}



def generate_eqi():
    generate_compare_imm(mode = "eqi")

def generate_neqi():
    generate_compare_imm(mode = "neqi")

def generate_gti():
    generate_compare_imm(mode = "gti")

def generate_lti():
    generate_compare_imm(mode = "lti")

def generate_gei():
    generate_compare_imm(mode = "gei")

def generate_lei():
    generate_compare_imm(mode = "lei")

def generate_eqiu():
    generate_compare_imm(mode = "eqiu")

def generate_neqiu():
    generate_compare_imm(mode = "neqiu")

def generate_ltiu():
    generate_compare_imm(mode = "ltiu")

def generate_gtiu():
    generate_compare_imm(mode = "gtiu")

def generate_geiu():
    generate_compare_imm(mode = "geiu")

def generate_leiu():
    generate_compare_imm(mode = "leiu")


def generate_eq():
    generate_compare(mode = "eq")

def generate_neq():
    generate_compare(mode = "neq")

def generate_gt():
    generate_compare(mode = "gt")

def generate_lt():
    generate_compare(mode = "lt")

def generate_ge():
    generate_compare(mode = "ge")

def generate_le():
    generate_compare(mode = "le")

def generate_gtu():
    generate_compare(mode = "gtu")

def generate_ltu():
    generate_compare(mode = "ltu")

def generate_geu():
    generate_compare(mode = "geu")

def generate_leu():
    generate_compare(mode = "leu")

def generate_equ():
    generate_compare(mode = "equ")

def generate_nequ():
    generate_compare(mode = "nequ")

def generate_compare_imm(mode = "eqi"):
    Rs = select_registers(
        mode="GR",
        method="RANDOM",
        used_regs = [key for key, value in recent_written_registers.items() if value > 1]
    )
    probability = 3

    #各种比较有对应概率使用相同的立即数,eqi和neqi使用相同立即数的概率为0.5
    if mode == "neqi" or mode == "eqi" or mode == "neqiu" or mode == "eqiu":
        probability = 1
    elif mode == "lti" or mode == "gti" or mode == "ltiu" or mode == "gtiu":
        probability = 3
    elif mode == "lei" or mode == "gei" or mode == "leiu" or mode == "geiu":
        probability = 2

    mode_random = random.randint(0, probability)
    imm9 = generate_imm(9, 0)
    instr = f"{mode} {Rs} {imm9}"

    if mode_random == 0:
        # 随机选择是否拓展
        mode_signed = random.choice(["signed", "unsigned"])
        insert_data_reg(Rs,imm9,WAIT_TIMES["eqi"],mode=mode_signed)
    else:
        # 取另一个立即数
        imm9 = generate_imm(9, 0)

        # 随机选择是否拓展
        mode_signed = random.choice(["signed", "unsigned"])
        insert_data_reg(Rs,imm9,WAIT_TIMES["eqi"],mode=mode_signed)

    dep_list = update_slot_rely(mode="read",reg_list=[Rs])
    enqueue_instruction(slot_queue = slot1_queue,inst_str = instr,dep_list=dep_list)
    # 读取控制寄存器，确认状态
    check_control()

def generate_compare(mode = "eq"):

    Rs,Rt = distribute_reg(reg1_bits=32,reg1_set=True,reg2_bits=32,reg2_set=True)

    probability = 0.25 
    #各种比较有对应概率使用相同的值,eq和neq使用相同值的概率为0.5
    if mode == "neq" or mode == "eq" or mode == "equ" or mode == "nequ":
        probability = 0.5 
    elif mode == "lt" or mode == "gt" or mode == "ltu" or mode == "geu":
        probability = 0.25 
    elif mode == "le" or mode == "ge" or mode == "leu" or mode == "geu":
        probability = 0.33 


    if probability_return(probability):
        # 随机选择是否拓展
        imm31 = generate_imm(31, 0)

        mode_signed = random.choice(["signed", "unsigned"])
        insert_data_reg(Rs,imm31,WAIT_TIMES["eq"],mode=mode_signed)

        mode_signed = random.choice(["signed", "unsigned"])
        insert_data_reg(Rt,imm31,WAIT_TIMES["eq"],mode=mode_signed)

    instr = f"{mode} {Rs} {Rt}"
    dep_list = update_slot_rely(mode="read",reg_list=[Rs,Rt])
    enqueue_instruction(slot_queue = slot1_queue,inst_str = instr,dep_list=dep_list)
    # 读取控制寄存器，确认状态
    check_control()


