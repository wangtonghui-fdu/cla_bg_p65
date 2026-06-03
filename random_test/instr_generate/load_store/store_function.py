import random


from tool.tool import TEST_CLA, generate_imm
from tool.tool import distribute_reg,insert_data_reg,select_registers,probability_return
from tool.ram import generate_memory_imm
from global_state.global_state import enqueue_instruction,get_queue_tail_index,update_recent_written_registers,update_written_registers,update_slot_rely,get_last_written_registers
from global_state.global_state import recent_written_registers
from slot1.slot1 import handle_slot1_instr


from global_state.global_state import slot2_queue,slot3_queue
from config.config import RegConfig
from config.config import TestConfig

#测试规模
TEST_SCALE = not TestConfig.EXPANDED_TEST_SCOPE
BYPASS_TEST = TestConfig.INCREASE_BYPASS_TEST


# 所有寄存器集合

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

ADDR_RANGE = 16 #地址范围的2进制位数
OFF_RANGE = 4 #storeo和loado指令的访问步长
TEST_CLA = TestConfig.TEST_CLA
# 定义等待时间基准
WAIT_TIMES_BASE = {
    "store": 30,
    "storeu": 30,
    "storeo": 30,
    "storei": 30,
    "storeui": 30,
    "loado": 30
}

# 根据 TEST_CLA 设置系数
if TEST_CLA:
    SCALE_FACTOR = 1  # 或者其他你想要的系数
else:
    SCALE_FACTOR = 1

# 应用系数得到最终的等待时间
WAIT_TIMES = {key: value * SCALE_FACTOR for key, value in WAIT_TIMES_BASE.items()}

#  WAIT_TIMES = {
#      "store": 30,
#      "storeu": 30,
#      "storeo": 30,
#      "storei": 30,
#      "storeui": 30,
#      "loado" : 30 
#  }
#不同访存宽度对应的基地址低位为0的位数
LOW_ZERO = {
    8 : 0,
    16 : 1,
    32 : 2,
}

WAIT_INSTR = False #设置插入等待

#核心store代码
def generate_store(bit_width):
    Rd,Rs = distribute_reg()

    #给Rs寄存器赋地址基值;
    low_zero = LOW_ZERO[bit_width]  #低位为0的数

    #偏移量
    immbase,imm9 = generate_memory_imm(bit_width=bit_width,low_zero=low_zero)
    insert_data_reg(Rs,immbase,WAIT_TIMES["store"],slot2_wait=WAIT_INSTR,slot3_wait=WAIT_INSTR,use_mov=TEST_SCALE)  #将地址基值存入Rs寄存器

    # BYPASS_TEST 随机计算指令，增加数据相关性
    if BYPASS_TEST:
        if probability_return(0.5):
            handle_slot1_instr("random_calculate")
            Rd = get_last_written_registers(slot=1)

    instr = f"store{bit_width} {Rd} {Rs} {imm9}"
    dep_list = update_slot_rely(mode="read",reg_list=[Rd,Rs])
    enqueue_instruction(slot_queue = slot3_queue,inst_str = instr,dep_list=dep_list)


def generate_storeu(bit_width):
    Rd,Rs = distribute_reg()

    #给Rs寄存器赋地址基值;
    low_zero = LOW_ZERO[bit_width]  #低位为0的数

    immbase,imm9 = generate_memory_imm(bit_width=bit_width,low_zero=low_zero)
    insert_data_reg(Rs,immbase,WAIT_TIMES["storeu"],slot2_wait=WAIT_INSTR,slot3_wait=WAIT_INSTR,use_mov=TEST_SCALE)  #将地址基值存入Rs寄存器
     
    #偏移量
    imm9 = generate_imm(bits=9, low_zero=0)

    # BYPASS_TEST 随机计算指令，增加数据相关性
    if BYPASS_TEST:
        if probability_return(0.5):
            handle_slot1_instr("random_calculate")
            Rd = get_last_written_registers(slot=1)


    instr = f"storeu{bit_width} {Rd} {Rs} {imm9}"
    dep_list = update_slot_rely(mode="read",reg_list=[Rd,Rs])
    enqueue_instruction(slot_queue = slot3_queue,inst_str = instr,dep_list=dep_list)

    slot3_tail = get_queue_tail_index(3)
    update_written_registers([Rs], mode="write",slot_rely=[0,0,slot3_tail]) #更新已经使用过的寄存器
    update_recent_written_registers([Rs], ttl=WAIT_TIMES["storeu"],allow_decrease=True)  # 设置倒计时

def generate_storei(bit_width):
    Rd,_ = distribute_reg()
     
    #偏移量
    imm15 = generate_memory_imm(bit_width=bit_width,low_zero=0,need_base=False,imm_width=15)[1]
    #最大访问地址还是没到达内存区，不生成该指令
    if imm15 == "0x0000":
        return None

    if BYPASS_TEST:
        if probability_return(0.5):
            handle_slot1_instr("random_calculate")
            Rd = get_last_written_registers(slot=1)
        else:
            Rd,_ = distribute_reg()

    instr = f"storei{bit_width} {Rd} {imm15}"

    dep_list = update_slot_rely(mode="read",reg_list=[Rd])
    enqueue_instruction(slot_queue = slot3_queue,inst_str = instr,dep_list=dep_list)

def generate_storeui(bit_width):
    Rd,_ = distribute_reg()
     
    #立即数地址
    imm15 = generate_memory_imm(bit_width=bit_width,low_zero=0,need_base=False,imm_width=15)[1]
    if imm15 == None:
        return None

    if BYPASS_TEST:
        if probability_return(0.5):
            handle_slot1_instr("random_calculate")
            Rd = get_last_written_registers(slot=1)

    instr = f"storeui{bit_width} {Rd} {imm15}"
    enqueue_instruction(slot_queue = slot3_queue,inst_str = instr,dep_list=[0,0,get_queue_tail_index(3)])

def generate_store_loado(bit_width,mode = "store"):
    Rd,Rs = distribute_reg()
    low_zero = LOW_ZERO[bit_width]  #低位为0的数

    immOFF = "0x0000" 
    while int(immOFF,16)== 0:  #确保偏移量不为0
        immOFF = generate_imm(bits=OFF_RANGE, low_zero=low_zero)

    access_number = random.randint(3, 10)
    wait_times = access_number * 3
    numMR = access_number * int(immOFF,16)
    immMR = hex(numMR)
    immbase,_ = generate_memory_imm(bit_width=bit_width,low_zero=low_zero,MR=numMR)

    
    #偏移量
    offset_number = random.randint(1, 5) * random.choice([-1, 1])

    immBar = hex(int(immbase,16) + offset_number * int(immOFF,16))

    BAR = select_registers(
             mode="BAR",
             method="RANDOM",
             used_regs=recent_written_registers
    )
    register_number = int(BAR[3:])
    
    OFF = f"OFF{register_number}" 
    MR = f"MR{register_number}" 

    #给Rs寄存器赋地址基值;
    insert_data_reg(Rs,immbase,wait_times,slot2_wait=WAIT_INSTR,slot3_wait=WAIT_INSTR,use_mov=TEST_SCALE)  #将地址基值存入Rs寄存器
    insert_data_reg(BAR,immBar,wait_times,slot2_wait=WAIT_INSTR,slot3_wait=WAIT_INSTR)
    insert_data_reg(MR,immMR,wait_times,slot2_wait=WAIT_INSTR,slot3_wait=WAIT_INSTR)
    insert_data_reg(OFF,immOFF,wait_times,slot2_wait=WAIT_INSTR,slot3_wait=WAIT_INSTR)

    for _ in range(access_number):
        # BYPASS_TEST 随机计算指令，增加数据相关性
        if BYPASS_TEST:
            if probability_return(0.5):
                handle_slot1_instr("random_calculate")
                Rd = get_last_written_registers(slot=1)
            else:
                Rd,_ = distribute_reg()

        instr = f"storeo{bit_width} {Rd} {Rs} {BAR}"
        slot1_tail = get_queue_tail_index(1)
        enqueue_instruction(slot_queue = slot3_queue,inst_str = instr,dep_list=[slot1_tail,0,get_queue_tail_index(3)])

        #更新写回的寄存器，防止storeo运行时有其他指令修改地址
        slot3_tail = get_queue_tail_index(3)
        update_written_registers([Rs], mode="write",slot_rely=[0,0,slot3_tail]) #更新已经使用过的寄存器Rs
        update_recent_written_registers([Rs], ttl=wait_times,allow_decrease=True)  # 设置倒计时

        update_written_registers([BAR], mode="write",slot_rely=[0,0,slot3_tail]) #更新已经使用过的寄存器Rs
        update_recent_written_registers([BAR], ttl=wait_times,allow_decrease=False)

        update_written_registers([MR], mode="write",slot_rely=[0,0,slot3_tail]) #更新已经使用过的寄存器Rs
        update_recent_written_registers([MR], ttl=wait_times,allow_decrease=False)
            
        update_written_registers([OFF], mode="write",slot_rely=[0,0,slot3_tail]) #更新已经使用过的寄存器Rs
        update_recent_written_registers([OFF], ttl=wait_times,allow_decrease=False)

    if mode == "load":
        Rd,Rs = distribute_reg(reg1_set=False) #loado指令使用新的寄存器
        insert_data_reg(Rs,immbase,access_number * 5,slot2_wait=False,slot3_wait=False,use_mov=TEST_SCALE)  #将地址基值存入Rs寄存器

        slot1_tail = get_queue_tail_index(1)
        slot3_tail = get_queue_tail_index(3);

        instr = f"loado{bit_width} {Rd} {Rs} {BAR}"
        for _ in range(access_number):
            enqueue_instruction(slot_queue = slot2_queue,inst_str = instr,dep_list=[slot1_tail,get_queue_tail_index(3),slot3_tail])
            update_written_registers([Rd], mode="write") #更新已经使用过的寄存器Rd
            update_recent_written_registers([Rd], ttl=wait_times,allow_decrease=True)

            #更新写回的寄存器，防止loado运行时有其他指令修改地址
            slot2_tail = get_queue_tail_index(2)
            update_written_registers([Rs], mode="write",slot_rely=[0,slot2_tail,0]) #更新已经使用过的寄存器Rs
            update_recent_written_registers([Rs], ttl=access_number * 5,allow_decrease=False)

            update_written_registers([BAR], mode="write",slot_rely=[0,slot2_tail,0]) #更新已经使用过的寄存器Rs
            update_recent_written_registers([BAR], ttl=wait_times,allow_decrease=False)

            update_written_registers([MR], mode="write",slot_rely=[0,slot2_tail,0]) #更新已经使用过的寄存器Rs
            update_recent_written_registers([MR], ttl=wait_times,allow_decrease=False)
            
            update_written_registers([OFF], mode="write",slot_rely=[0,slot2_tail,0]) #更新已经使用过的寄存器Rs
            update_recent_written_registers([OFF], ttl=wait_times,allow_decrease=False)
"""
暂时不使用这部分
    elif None:
        Rd,Rs = distribute_reg(reg1_set=False) #loado指令使用新的寄存器
        insert_data_reg(Rs,immbase,access_number * 5,slot2_wait=False,slot3_wait=False,use_mov=TEST_SCALE)  #将地址基值存入Rs寄存器

        off = 0
        base = int(immbase,16)
        mr = int(immMR,16)
        bar = int(immBar,16)
        slot1_tail = get_queue_tail_index(1)
        slot3_tail = get_queue_tail_index(3);
        for _ in range(access_number):

            # 处理有符号 9 位二进制数
            if off & 0x100:  # 如果第9位是1（负数）
                value = off - 0x200  # 转换为有符号整数
            else:
                value = off

            # 切换位数
            if bit_width == 16:
                 value = value >> 1
            elif bit_width == 32:
                 value = value >> 2

            # 转换为三位十六进制（12位二进制）
            imm = f"0x{value & 0xfff:03x}"  # 使用 & 0xfff 确保12位表示
            instr = f"load{bit_width} {Rd} {Rs} {imm}"
            enqueue_instruction(slot_queue = slot2_queue,inst_str = instr,dep_list=[slot1_tail,get_queue_tail_index(3),slot3_tail])
            update_written_registers([Rd], mode="write") #更新已经使用过的寄存器Rd
            update_recent_written_registers([Rs], ttl=wait_times,allow_decrease=False)

            update_recent_written_registers([Rd], ttl=wait_times,allow_decrease=True)

            if (base + off) > (bar + mr):
                off = off + int(immOFF,16) - mr
            elif (base + off) < bar:
                off = off + int(immOFF,16) + mr
            else:
                off = off + int(immOFF,16)
"""
