import random

from config.config import TestConfig,ClaConfig
from tool.tool import generate_float
from tool.tool import distribute_reg, select_registers 
from tool.tool import insert_data_reg
from tool.tool import check_control
from tool.tool import probability_return

from global_state.global_state import update_written_registers, update_recent_written_registers,update_slot_rely
from global_state.global_state import recent_written_registers
from global_state.global_state import enqueue_instruction

from global_state.global_state import slot1_queue


TEST_CLA = TestConfig.TEST_CLA
CLA_NOT_SUPPORT_FPU = ClaConfig.CLA_NOT_SUPPORT_FPU

CR_MODEL = TestConfig.CR_MODEL


WAIT_TIMES = {
    "fsadd": 3,  
    "fseq": 3,
}


def handle_fpu_instr(instr_name: str):
    """
    MOV 指令分发函数，根据 instr_name 调用对应子函数
    支持 random - 随机选择一个指令执行
    其他无效指令将静默忽略
    """
    instr_name = instr_name.lower()
    fpu_instr_map = {
        "fsmul": generate_fsmul,
        "fsdiv": generate_fsdiv,
        "fsmac": generate_fsmac,
        "fsadd": generate_fsadd,
        "fssub": generate_fssub,
        "fsmax": generate_fsmax,
        "fsmin": generate_fsmin,

        "fseinv": generate_fseniv,
        "fseisqrt": generate_fseisqrt,
        "fssqrt": generate_fseisqrt,
        "fsabs": generate_fsabs,
        "fcvtsf": generate_fcvtsf,
        "fcvtfs": generate_fcvtfs,
        "fcvtsu": generate_fcvtsu,
        "fcvtus": generate_fcvtus,

        "fseq": generate_fseq,
        "fsgt": generate_fsgt,
        "fslt": generate_fslt,
        "fsge": generate_fsge,
        "fsle": generate_fsle,

        "random": None,
        "random_fpu": None,
    }
    if CR_MODEL:
        return  # CR 模式下不执行 FPU 指令

    if instr_name == "random" or instr_name == "random_fpu":
        # 创建随机选择池（排除 random 自身）
        if not TEST_CLA:
            choices = [key for key in fpu_instr_map.keys() if key != "random" and key != "random_fpu"]
        else:
            choices = [key for key in fpu_instr_map.keys() if key != "random" and key != "random_fpu" and key not in CLA_NOT_SUPPORT_FPU]
        # 随机选择一个指令并执行
        fpu_instr_map[random.choice(choices)]()
    elif instr_name in fpu_instr_map:
        fpu_instr_map[instr_name]()  # 执行指定指令
    # 其他情况静默不执行

def generate_fsmul():
    generate_fpu_3_reg("fsmul")

def generate_fsdiv():
    generate_fpu_3_reg("fsdiv")

def generate_fsmac():
    generate_fpu_3_reg("fsmac")

def generate_fsadd():
    generate_fpu_3_reg("fsadd")

def generate_fssub():
    generate_fpu_3_reg("fssub")

def generate_fsmax():
    generate_fpu_3_reg("fsmax")

def generate_fsmin():
    generate_fpu_3_reg("fsmin")


# 使用三个寄存器的计算指令
def generate_fpu_3_reg(mode = "fsmul"):
    if probability_return(0.5):
        Rs,Rt = distribute_reg(reg1_set=True,reg2_set=True,reg1_bits=32,reg2_bits=32,float=True)
    else:
        Rs,Rt = distribute_reg(reg1_set=True,reg2_set=True,reg1_bits=32,reg2_bits=32,float=False)
    [imm1,imm2,imm3] = generate_float(32,3)
    if mode in ["fsadd","fssub","fsmul","fsdiv","fsmax","fsmin"]: 
        Rd = select_registers(mode="GR",method="RANDOM",reg_type="",used_regs=recent_written_registers)
    elif mode == ["fsmac"]:
        Rd = update_written_registers([],"read","FLOAT")  # 读取一个通用寄存器
    else:
        Rd = select_registers(mode="GR",method="RANDOM",reg_type="",used_regs=recent_written_registers)

    if probability_return(0.5):  # 50% 概率使用立即数
        if mode in ["fsmac"]:
            insert_data_reg(Rd,imm3,wait_times=1)
        insert_data_reg(Rs,imm1,wait_times=1)
        insert_data_reg(Rt,imm2,wait_times=1)

    instr = f"{mode} {Rd} {Rs} {Rt}"
    dep_list = update_slot_rely(mode="read",reg_list=[Rs,Rt]) #获取寄存器依赖

    enqueue_instruction(slot_queue = slot1_queue,inst_str = instr,dep_list=dep_list)
    update_written_registers([Rd], mode="write") #更新已经使用过的寄存器
    update_recent_written_registers([Rd], ttl=WAIT_TIMES["fsadd"],allow_decrease=True,type="float")  # 设置倒计时
    check_control()

#      insert_data_reg(Rd,"0x0000")

def generate_fseniv():
    generate_fpu_2_reg("fseinv")
     
def generate_fseisqrt():
    generate_fpu_2_reg("fseisqrt")

def generate_fssqrt():
    generate_fpu_2_reg("fssqrt")

def generate_fsabs():
    generate_fpu_2_reg("fsabs")

def generate_fcvtsf():
    generate_fpu_2_reg("fcvtsf")

def generate_fcvtfs():
    generate_fpu_2_reg("fcvtfs")

def generate_fcvtsu():
    generate_fpu_2_reg("fcvtsu")

def generate_fcvtus():
    generate_fpu_2_reg("fcvtus")

# 使用两个寄存器的计算指令
def generate_fpu_2_reg(mode = "fseinv"):
    if probability_return(0.5):
        Rd,Rs = distribute_reg(reg1_set=False,reg2_set=True,reg1_bits=32,reg2_bits=32,float=True)
    else:
        Rd,Rs = distribute_reg(reg1_set=False,reg2_set=True,reg1_bits=32,reg2_bits=32,float=False)
    if probability_return(0.5):  # 50% 概率使用立即数
        imm1 = generate_float(32,1)
        insert_data_reg(Rs,imm1,wait_times=1)

    instr = f"{mode} {Rd} {Rs}"
    dep_list = update_slot_rely(mode="read",reg_list=[Rs]) #获取寄存器依赖

    enqueue_instruction(slot_queue = slot1_queue,inst_str = instr,dep_list=dep_list)
    update_written_registers([Rd], mode="write") #更新已经使用过的寄存器
    update_recent_written_registers([Rd], ttl=WAIT_TIMES["fsadd"],allow_decrease=True,type="float")  # 设置倒计时

#      insert_data_reg(Rd,"0x0000")
    check_control()

def generate_fseq():
    generate_fpu_compare("fseq")

def generate_fsgt():
    generate_fpu_compare("fsgt")

def generate_fslt():
    generate_fpu_compare("fslt")

def generate_fsge():
    generate_fpu_compare("fsge")

def generate_fsle():
    generate_fpu_compare("fsle")

# 使用两个寄存器的比较指令
def generate_fpu_compare(mode = "fseq"):
    if probability_return(0.25):
        Rs,Rt = distribute_reg(reg1_set=False,reg2_set=False,reg1_bits=32,reg2_bits=32,float=False)
        imm32 = generate_float(32)
        insert_data_reg(Rs,imm32,wait_times=1)
        insert_data_reg(Rt,imm32,wait_times=1)
    elif probability_return(0.25):
        Rs,Rt = distribute_reg(reg1_set=True,reg2_set=True,reg1_bits=32,reg2_bits=32,float=False)
        imm32 = generate_float(32)
        imm32 = generate_float(32)
        insert_data_reg(Rs,imm32,wait_times=1)
        insert_data_reg(Rt,imm32,wait_times=1)
    elif probability_return(0.25):
        Rs,Rt = distribute_reg(reg1_set=True,reg2_set=True,reg1_bits=32,reg2_bits=32,float=True)
    else:
        Rs,Rt = distribute_reg(reg1_set=False,reg2_set=False,reg1_bits=32,reg2_bits=32,float=False)

    instr = f"{mode} {Rs} {Rt}"

    dep_list = update_slot_rely(mode="read",reg_list=[Rs,Rt]) #获取寄存器依赖
    enqueue_instruction(slot_queue = slot1_queue,inst_str = instr,dep_list=dep_list)
    check_control()
