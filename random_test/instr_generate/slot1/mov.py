

from slot1.alu_compare import WAIT_TIMES_BASE
from tool.tool import TEST_CLA, generate_imm, select_registers,distribute_reg 
from global_state.global_state import GR_NUM, update_written_registers, update_recent_written_registers
from global_state.global_state import recent_written_registers
from global_state.global_state import enqueue_instruction,get_queue_tail_index,update_slot_rely

from global_state.global_state import slot1_queue
from config.config import RegConfig,TestConfig

# 寄存器数量
GR_NUM = RegConfig.GR_NUM
OFF_NUM = RegConfig.OFF_NUM
BAR_NUM = RegConfig.BAR_NUM
MR_NUM = RegConfig.MR_NUM

# 所有寄存器集合
GR  = [f"GR{i}" for i in range(GR_NUM)]
OFF = [f"OFF{i}" for i in range(OFF_NUM)]
BAR = [f"BAR{i}" for i in range(BAR_NUM)]
MR  = [f"MR{i}" for i in range(MR_NUM)]
# Define macro parameters for each function's waiting time

TEST_CLA = TestConfig.TEST_CLA
WAIT_TIMES_BASE = {
    "movigh": 1,  
    "movigl": 1,  
    "moviglz": 1,  
    "moviglx": 1,  
    "movg2c": 1,  
    "movg2g": 1,  
    "movc2g": 1,  
}
# 根据 TEST_CLA 设置系数
if TEST_CLA:
    SCALE_FACTOR = 3  # 或者其他你想要的系数
else:
    SCALE_FACTOR = 1

# 应用系数得到最终的等待时间
WAIT_TIMES = {key: value * SCALE_FACTOR for key, value in WAIT_TIMES_BASE.items()}



#检验是否写入OFF,BAR,MR寄存器的函数，因为这三种寄存器不会打印报告，所以移出重新看看
def insert_movg2g(reg):
    if reg in MR or reg in BAR or reg in OFF:
        Rs = reg 
        Rd = select_registers(
            mode="GR",
            method="RANDOM",
            used_regs = [key for key, value in recent_written_registers.items() if value > 1]
        )
        instr = f"movg2g {Rd} {Rs}"

        dep_list = update_slot_rely(mode = "read",reg_list=[Rs]) #获取依赖

        enqueue_instruction(slot_queue = slot1_queue,inst_str = instr,dep_list=dep_list)

        slot1_tail = get_queue_tail_index(1)
        update_written_registers([Rd], mode="write",slot_rely=[slot1_tail,0,0]) #更新已经使用过的寄存器
        update_recent_written_registers([Rd], ttl=WAIT_TIMES["movg2g"],allow_decrease=True)  # 设置倒计时

# === 以下是每种 MOV 指令的处理函数 ===

#
def generate_movigh(mode="ALL"): 
    Rd = select_registers(
        mode=mode,
        method="RANDOM",
        used_regs = [key for key in recent_written_registers]
    )

    imm16 = generate_imm(bits=16, low_zero=0)
    instr = f"movigh {Rd} {imm16}"

    enqueue_instruction(slot_queue = slot1_queue,inst_str = instr,dep_list=[0,0,0]) #第一条指令可以随意插入

    imm16 = generate_imm(bits=16, low_zero=0)
    instr = f"movigl {Rd} {imm16}"

    enqueue_instruction(slot_queue = slot1_queue,inst_str = instr,dep_list=[get_queue_tail_index(1),0,0]) #第二条指令不能和第一条指令插入同一个超长指令字

    slot1_tail = get_queue_tail_index(1)
    update_written_registers([Rd], mode="write",slot_rely=[slot1_tail,0,0]) #更新已经使用过的寄存器
    update_recent_written_registers([Rd], ttl=WAIT_TIMES["movigh"],allow_decrease=True)  # 设置倒计时

    insert_movg2g(Rd) #检验BAR,MR,OFF是否写入

         

def generate_movigl():
    generate_movigh()

def generate_moviglz():
    Rd = select_registers(
        mode="ALL",
        method="RANDOM",
        reg_type="",
        index=0,
        used_regs = [key for key, value in recent_written_registers.items() if value > 1]
    )


    imm16 = generate_imm(bits=16, low_zero=0)
    instr = f"moviglz {Rd} {imm16}"

    enqueue_instruction(slot_queue = slot1_queue,inst_str = instr,dep_list=[0,0,0])

    slot1_tail = get_queue_tail_index(1)
    update_written_registers([Rd], mode="write",slot_rely=[slot1_tail,0,0]) #更新已经使用过的寄存器
    update_recent_written_registers([Rd], ttl=WAIT_TIMES["moviglz"],allow_decrease=True)  # 设置倒计时

    insert_movg2g(Rd) #检验BAR,MR,OFF是否写入



def generate_moviglx():

    Rd = select_registers(
        mode="ALL",
        method="RANDOM",
        reg_type="",
        index=0,
        used_regs = [key for key, value in recent_written_registers.items() if value > 1]
    )


    imm16 = generate_imm(bits=16, low_zero=0)
    instr = f"moviglx {Rd} {imm16}"

    enqueue_instruction(slot_queue = slot1_queue,inst_str = instr,dep_list=[0,0,0])

    slot1_tail = get_queue_tail_index(1)
    update_written_registers([Rd], mode="write",slot_rely=[slot1_tail,0,0]) #更新已经使用过的寄存器
    update_recent_written_registers([Rd], ttl=WAIT_TIMES["moviglx"],allow_decrease=True)  # 设置倒计时

    insert_movg2g(Rd)


def generate_movg2c():
    Rs = update_written_registers([],"read","GR")  # 读取一个通用寄存器
    if Rs is None:
        generate_movigh("GR")
        Rs= update_written_registers([],"read","GR")  # 读取一个通用寄存器

    instr = f"movg2c {Rs}"
    dep_list = update_slot_rely(mode = "read",reg_list=[Rs]) #获取依赖

    enqueue_instruction(slot_queue = slot1_queue,inst_str = instr,dep_list=dep_list)

    Rd = select_registers(
        mode="GR",
        method="RANDOM",
        reg_type="",
        index=0,
        used_regs = [key for key, value in recent_written_registers.items() if value > 1]
    )
    instr = f"movc2g {Rd}"

    enqueue_instruction(slot_queue = slot1_queue,inst_str = instr,dep_list=[get_queue_tail_index(1),0,0])

    slot1_tail = get_queue_tail_index(1)
    update_written_registers([Rd], mode="write",slot_rely=[slot1_tail,0,0]) #更新已经使用过的寄存器
    update_recent_written_registers([Rd], ttl=WAIT_TIMES["movg2g"],allow_decrease=True)  # 设置倒计时

def generate_movg2g():
    Rs = update_written_registers(mode="read") 
    if Rs is None:
        generate_movigh()
        Rs = update_written_registers([],"read") 

    Rd = select_registers(
        mode="ALL",
        method="RANDOM",
        reg_type="",
        index=0,
        used_regs = [key for key, value in recent_written_registers.items() if value > 1]
    )


    instr = f"movg2g {Rd} {Rs}"

    dep_list = update_slot_rely(mode = "read",reg_list=[Rs]) #获取依赖
    enqueue_instruction(slot_queue = slot1_queue,inst_str = instr,dep_list=dep_list)

    slot1_tail = get_queue_tail_index(1)
    update_written_registers([Rd], mode="write",slot_rely=[slot1_tail,0,0]) #更新已经使用过的寄存器
    update_recent_written_registers([Rd], ttl=WAIT_TIMES["movg2g"],allow_decrease=True)  # 设置倒计时

    insert_movg2g(Rd)

def generate_movc2g():
    generate_movg2c()
