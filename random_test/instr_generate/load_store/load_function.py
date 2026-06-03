

from load_store.store_function import WAIT_TIMES_BASE
from tool.tool import TEST_CLA, select_registers 
from tool.tool import distribute_reg,store_data,insert_data_reg,probability_return
from tool.ram import generate_memory_imm

from global_state.global_state import recent_written_registers
from global_state.global_state import update_written_registers,update_recent_written_registers,update_slot_rely
from global_state.global_state import get_last_written_registers
from global_state.global_state import enqueue_instruction,get_queue_tail_index

from slot1.slot1 import handle_slot1_instr
from global_state.global_state import slot2_queue
from config.config import TestConfig
BYPASS_TEST = TestConfig.INCREASE_BYPASS_TEST

#测试规模
TEST_SCALE = not TestConfig.EXPANDED_TEST_SCOPE
TEST_CLA = TestConfig.TEST_CLA

from config.config import RegConfig


# 寄存器数量
GR_NUM = RegConfig.GR_NUM
BAR_NUM = RegConfig.BAR_NUM
MR_NUM = RegConfig.MR_NUM
OFF_NUM = RegConfig.OFF_NUM

# 所有寄存器集合
GR  = [f"GR{i}" for i in range(GR_NUM)]
OFF = [f"OFF{i}" for i in range(OFF_NUM)]
BAR = [f"BAR{i}" for i in range(BAR_NUM)]
MR  = [f"MR{i}" for i in range(MR_NUM)]
# Define macro parameters for each function's waiting time

ADDR_RANGE = 16 #地址范围的2进制位数
OFF_RANGE = 4 #storeo和loado指令的访问步长

# 定义等待时间基准
WAIT_TIMES_BASE = {
    "load": 30,
    "loadu": 30,
    "loado": 30,
    "loadi": 30,
}
# 根据 TEST_CLA 设置系数
if TEST_CLA:
    SCALE_FACTOR = 1  # 或者其他你想要的系数
else:
    SCALE_FACTOR = 1

# 应用系数得到最终的等待时间
WAIT_TIMES = {key: value * SCALE_FACTOR for key, value in WAIT_TIMES_BASE.items()}


#不同访存宽度对应的基地址低位为0的位数
LOW_ZERO = {
    8 : 0,
    16 : 1,
    32 : 2,
}


#load核心函数
def generate_load(bit_width): 
    Rd,Rs = distribute_reg()
    #给Rs寄存器赋地址基值;
    low_zero = LOW_ZERO[bit_width]  #低位为0的数

    immbase,imm9 = generate_memory_imm(bit_width=bit_width,low_zero=low_zero)
    insert_data_reg(Rs,immbase,WAIT_TIMES["load"],slot2_wait=False,slot3_wait=False,use_mov=TEST_SCALE)  #将地址基值存入Rs寄存器
    if BYPASS_TEST:
        if probability_return(0.5):
            handle_slot1_instr("random_calculate")
            Rd = get_last_written_registers(slot=1)


    #偏移量
    
    store_data(base_reg=Rs,data_reg=Rd,imm=imm9,bit_width=bit_width)
    Rd = select_registers(
        mode="GR",
        method="RANDOM",
        reg_type="",
        index=0,
        used_regs = [key for key, value in recent_written_registers.items() if value > 1]
    )
    instr = f"load{bit_width} {Rd} {Rs} {imm9}"

    dep_list = update_slot_rely(mode="read",reg_list=[Rs])
    slot3_tail = get_queue_tail_index(3)
    dep_list[2] = slot3_tail

    enqueue_instruction(slot_queue = slot2_queue,inst_str = instr,dep_list=dep_list)

    slot2_tail = get_queue_tail_index(2)
    update_written_registers([Rd], mode="write",slot_rely=[0,slot2_tail,0]) #更新已经使用过的寄存器
    update_recent_written_registers([Rd], ttl=WAIT_TIMES["load"],allow_decrease=True)  # 设置倒计时

def generate_loadu(bit_width): 
    Rd,Rs = distribute_reg()
    #给Rs寄存器赋地址基值;
    low_zero = LOW_ZERO[bit_width]  #低位为0的数


    immbase,imm9 = generate_memory_imm(bit_width=bit_width,low_zero=low_zero)

    insert_data_reg(Rs,immbase,WAIT_TIMES["loadu"],slot2_wait=False,slot3_wait=False,use_mov=TEST_SCALE)

    if BYPASS_TEST:
        if probability_return(0.5):
            handle_slot1_instr("random_calculate")
            Rd = get_last_written_registers(slot=1)

    store_data(base_reg=Rs,data_reg=Rd,imm=imm9,bit_width=bit_width)
    Rd = select_registers(
        mode="GR",
        method="RANDOM",
        reg_type="",
        index=0,
        used_regs = [key for key, value in recent_written_registers.items() if value > 1]
    )

    instr = f"loadu{bit_width} {Rd} {Rs} {imm9}"
    dep_list = update_slot_rely(mode="read",reg_list=[Rs])

    slot3_tail = get_queue_tail_index(3)
    dep_list[2] = slot3_tail
    enqueue_instruction(slot_queue = slot2_queue,inst_str = instr,dep_list=dep_list)

    slot2_tail = get_queue_tail_index(2)
    update_written_registers([Rd,Rs], mode="write",slot_rely=[0,slot2_tail,0]) #更新已经使用过的寄存器
    update_recent_written_registers([Rd,Rs], ttl=WAIT_TIMES["load"],allow_decrease=True)  # 设置倒计时

def generate_loadi(bit_width): 
    Rd,_ = distribute_reg()

    #偏移量
    imm15 = generate_memory_imm(bit_width=bit_width,low_zero=0,need_base=False,imm_width=15)[1]
    if imm15 == "0x0000":
        return None
    if BYPASS_TEST:
        if probability_return(0.5):
            handle_slot1_instr("random_calculate")
            Rd = get_last_written_registers(slot=1)
    store_data(data_reg=Rd,imm=imm15,bit_width=bit_width)
    Rd = select_registers(
        mode="GR",
        method="RANDOM",
        reg_type="",
        index=0,
        used_regs = [key for key, value in recent_written_registers.items() if value > 1]
    )

    instr = f"loadi{bit_width} {Rd} {imm15}"

    slot3_tail = get_queue_tail_index(3)
    enqueue_instruction(slot_queue = slot2_queue,inst_str = instr,dep_list=[0,0,slot3_tail])
    slot2_tail = get_queue_tail_index(2)
    update_written_registers([Rd], mode="write",slot_rely=[0,slot2_tail,0]) #更新已经使用过的寄存器
    update_recent_written_registers([Rd], ttl=WAIT_TIMES["load"],allow_decrease=True)  # 设置倒计时

def generate_loadui(bit_width): 
    Rd,_ = distribute_reg()

    #偏移量
    imm15 = generate_memory_imm(bit_width=bit_width,low_zero=0,need_base=False,imm_width=15)[1]
    if imm15 == "0x0000":
        return None
    
    if BYPASS_TEST:
        if probability_return(0.5):
            handle_slot1_instr("random_calculate")
            Rd = get_last_written_registers(slot=1)


    store_data(data_reg=Rd,imm=imm15,bit_width=bit_width)
    Rd = select_registers(
        mode="GR",
        method="RANDOM",
        reg_type="",
        index=0,
        used_regs = [key for key, value in recent_written_registers.items() if value > 1]
    )

    instr = f"loadui{bit_width} {Rd} {imm15}"
    slot3_tail = get_queue_tail_index(3)
    enqueue_instruction(slot_queue = slot2_queue,inst_str = instr,dep_list=[0,get_queue_tail_index(2),slot3_tail])

    slot2_tail = get_queue_tail_index(2)
    update_written_registers([Rd], mode="write",slot_rely=[0,slot2_tail,0]) #更新已经使用过的寄存器
    update_recent_written_registers([Rd], ttl=WAIT_TIMES["load"],allow_decrease=True)  # 设置倒计时
