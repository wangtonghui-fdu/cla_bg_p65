import random


from config.config import TestConfig
from tool.tool import TEST_CLA, distribute_reg, generate_imm, select_registers 
from tool.tool import insert_data_reg
from tool.tool import select_pairs
from tool.tool import check_control,insert_control 

from global_state.global_state import nop, update_written_registers, update_recent_written_registers,update_slot_rely
from global_state.global_state import recent_written_registers,written_registers
from global_state.global_state import enqueue_instruction,get_queue_tail_index

from global_state.global_state import slot1_queue

TEST_CLA = TestConfig.TEST_CLA

WAIT_TIMES_BASE = {
    "add": 1,  
    "not": 1,
}

# 根据 TEST_CLA 设置系数
if TEST_CLA:
    SCALE_FACTOR = 1  # 或者其他你想要的系数
else:
    SCALE_FACTOR = 1

# 应用系数得到最终的等待时间
WAIT_TIMES = {key: value * SCALE_FACTOR for key, value in WAIT_TIMES_BASE.items()}


def generate_add():
    generate_alu_reg(mode = "add")

def generate_addc():
    generate_alu_reg(mode = "addc")

def generate_sub():
    generate_alu_reg(mode = "sub")

def generate_subc():
    generate_alu_reg(mode = "subc")

def generate_mul32():
    generate_alu_reg(mode = "mul32")

def generate_mulu32():
    generate_alu_reg(mode = "mulu32")

def generate_mul64():
    generate_alu_reg(mode = "mul64")

def generate_mulu64():
    generate_alu_reg(mode = "mulu64")

def generate_and():
    generate_alu_reg(mode = "and")

def generate_or():
    generate_alu_reg(mode = "or")

def generate_xor():
    generate_alu_reg(mode = "xor")

def generate_max():
    generate_alu_reg(mode = "max")

def generate_min():
    generate_alu_reg(mode = "min")

def generate_sra():
    generate_alu_reg(mode = "sra")

def generate_sl():
    generate_alu_reg(mode = "sl")

def generate_srl():
    generate_alu_reg(mode = "srl")


def generate_sra64():
    generate_alu_reg(mode = "sra64")

def generate_sl64():
    generate_alu_reg(mode = "sl64")

def generate_srl64():
    generate_alu_reg(mode = "srl64")

#reg是三个寄存器的指令
def generate_alu_reg(mode = "add"):
    if mode not in ["sra64","sl64","srl64"]:
        if mode  in["srl","sra","sl"]:
            Rs,Rt = distribute_reg(reg1_set=True,reg2_set=False,reg1_bits=32)
            imm = random.randint(0,31)
            imm = f"0x{imm:08x}"
            insert_data_reg(reg = Rt,imm = imm,wait_times = 1)
        else:
            Rs,Rt = distribute_reg(reg1_set=True,reg2_set=True,reg1_bits=32,reg2_bits=32)
            

        Rd = select_registers(mode="GR",method="RANDOM",reg_type="",used_regs=recent_written_registers)

        write_Rd = Rd

        dep_list = update_slot_rely(mode="read",reg_list=[Rs,Rt]) #获取寄存器依赖
    else:
        Rs,Rs1 = select_pairs(mode="read",used_regs=written_registers,require_even=True)

        Rd,Rd1 = select_pairs(mode="write",used_regs=written_registers,require_even=True)

        write_Rd = [Rd,Rd1]

        random_check_control = random.randint(0,3)
        Rt = select_registers(mode="GR",method="RANDOM",reg_type="",used_regs=recent_written_registers)

        dep_list = update_slot_rely(mode="read",reg_list=[Rs,Rs1,Rt]) # 获取寄存器依赖

        if random_check_control == 0:
            #Rt为0的时候，CF会被设置为0
            imm = "0x0000"
        else:
            imm = random.randint(1,63)
            imm = f"0x{imm:08x}"

        insert_data_reg(reg = Rt,imm = imm,wait_times = 1)


    #随机选择是否测试进位
    is_carry = random.choice([True,False])
    has_carry = mode in ["addc","subc","add","sub"]  #指令允许处理进位

    if is_carry and has_carry:
        imm_cr = random.choice(["0x4000","0x4001"])
        insert_control(imm_cr)

    instr = f"{mode} {Rd} {Rs} {Rt}" 
    enqueue_instruction(slot_queue = slot1_queue,inst_str = instr,dep_list = dep_list)

    slot1_tail = get_queue_tail_index(1)
    update_written_registers([Rd], mode="write",slot_rely=[slot1_tail,0,0]) #更新已经使用过的寄存器
    update_recent_written_registers(reg_list=write_Rd, ttl=WAIT_TIMES["add"],allow_decrease=True)  # 设置倒计时

    # 检查进位是否被设置
    if mode in ["addc","add","subc","sub","sra","sl","srl","sra64","sl64","srl64"]:
        check_control()
def generate_not():
    generate_alu_reg_2(mode = "not")

def generate_abs():
    generate_alu_reg_2(mode = "abs")

def generate_cbw():
    generate_alu_reg_2(mode = "cbw")

def generate_chw():
    generate_alu_reg_2(mode = "chw")

def generate_neg64():
    generate_alu_reg_2(mode = "neg64")

def generate_sat64():
    generate_alu_reg_2(mode = "sat64")
# 使用两个寄存器的指令
def generate_alu_reg_2(mode = "not"):
    if mode in ["not","abs","cbw","chw","neg"]:
        Rs,_ = distribute_reg(reg1_set=True,reg1_bits=32)
        Rd = select_registers(mode="GR",method="RANDOM",reg_type="",used_regs=recent_written_registers)

        write_Rd = [Rd]

        dep_list = update_slot_rely(mode="read",reg_list=[Rs]) #获取寄存器依赖

    else:
        Rs,Rs1 = select_pairs(mode="read",used_regs=written_registers,require_even=True)
        Rd,Rd1 = select_pairs(mode="write",used_regs=written_registers,require_even=True)

        write_Rd = [Rd,Rd1] 

        dep_list = update_slot_rely(mode="read",reg_list=[Rs,Rs1]) #获取寄存器依赖

        # 设置OVF溢出标志位
        if mode == "sat64":
            random_check_control = random.randint(0,2)
            if random_check_control == 0:
                insert_control("0x0000")
            elif random_check_control == 1:
                insert_control("0x2000")
            elif random_check_control == 2:
                insert_control("0x3000")
            
            
            

    instr = f"{mode} {Rd} {Rs}" 
    enqueue_instruction(slot_queue = slot1_queue,inst_str = instr,dep_list=dep_list)

    slot1_tail = get_queue_tail_index(1)
    update_written_registers([Rd], mode="write",slot_rely=[slot1_tail,0,0]) #更新已经使用过的寄存器
    update_recent_written_registers(reg_list=write_Rd, ttl=WAIT_TIMES["not"],allow_decrease=True)  # 设置倒计时

def generate_test():
    Rs,Rt = distribute_reg(reg1_set=True,reg1_bits=32,reg2_set=True,reg2_bits=5)
    instr = f"test {Rs} {Rt}"

    dep_list = update_slot_rely(mode="read",reg_list=[Rs,Rt]) #获取寄存器依赖
    enqueue_instruction(slot_queue = slot1_queue,inst_str = instr,dep_list=dep_list)
    check_control()

def generate_testi():

    Rs = distribute_reg(reg1_set=True,reg1_bits=32)[0]
    imm5 = generate_imm(5,0)
    instr = f"testi {Rs} {imm5}"

    dep_list = update_slot_rely(mode="read",reg_list=[Rs]) #获取寄存器依赖

    enqueue_instruction(slot_queue = slot1_queue,inst_str = instr,dep_list=dep_list)
    check_control()

def generate_bclr():

    Rs = distribute_reg(reg1_set=True,reg1_bits=32)[0]
    imm5 = generate_imm(5,0)
    instr = f"bclr {Rs} {imm5}"

    dep_list = update_slot_rely(mode="read",reg_list=[Rs]) #获取寄存器依赖
    enqueue_instruction(slot_queue = slot1_queue,inst_str = instr,dep_list=dep_list)

def generate_select():
    Rs,Rt = distribute_reg(reg1_set=True,reg1_bits=32,reg2_set=True,reg2_bits=32)
    Rd = select_registers(mode="GR",method="RANDOM",reg_type="",used_regs=recent_written_registers)
    random_check_control = random.randint(0,1)
    if random_check_control == 0: 
        insert_control("0x0010")

    instr = f"select {Rd} {Rs} {Rt}"

    dep_list = update_slot_rely(mode="read",reg_list=[Rs,Rt]) #获取寄存器依赖
    enqueue_instruction(slot_queue = slot1_queue,inst_str = instr,dep_list=dep_list)

    slot1_tail = get_queue_tail_index(1)
    update_written_registers([Rd], mode="write",slot_rely=[slot1_tail,0,0]) #更新已经使用过的寄存器
    update_recent_written_registers([Rd], ttl=WAIT_TIMES["add"],allow_decrease=True)  # 设置倒计时
    
def generate_setc():
    Rd = select_registers(mode="GR",method="RANDOM",reg_type="",used_regs=recent_written_registers)
    instr = f"setc {Rd}"
    random_check_control = random.randint(0,1)
    if random_check_control == 0: 
        insert_control("0x0010")

    enqueue_instruction(slot_queue = slot1_queue,inst_str = instr,dep_list=[0,0,0])

    slot1_tail = get_queue_tail_index(1)
    update_written_registers([Rd], mode="write",slot_rely=[slot1_tail,0,0]) #更新已经使用过的寄存器
    update_recent_written_registers([Rd], ttl=WAIT_TIMES["add"],allow_decrease=True)  # 设置倒计时

def generate_bfext():
    generate_bf(mode = "bfext")

def generate_bfextu():
    generate_bf(mode = "bfextu")

def generate_bfst():
    generate_bf(mode = "bfst")

def generate_bf(mode = "bfext"):
    Rs = distribute_reg(reg1_set=True,reg1_bits=32)[0]
    imm1 = generate_imm(5,0)
    imm2 = generate_imm(5,0,min=1)
    Rd = select_registers(mode="GR",method="RANDOM",reg_type="",used_regs=recent_written_registers)

    instr = f"{mode} {Rd} {Rs} {imm1} {imm2}"

    dep_list = update_slot_rely(mode="read",reg_list=[Rs]) #获取寄存器依赖
    enqueue_instruction(slot_queue = slot1_queue,inst_str = instr,dep_list=dep_list)

    slot1_tail = get_queue_tail_index(1)
    update_written_registers([Rd], mode="write",slot_rely=[slot1_tail,0,0]) #更新已经使用过的寄存器
    update_recent_written_registers([Rd], ttl=WAIT_TIMES["add"],allow_decrease=True)  # 设置倒计时
def generate_addi(): 
    generate_alu_imm(mode = "addi") 

def generate_addic(): 
    generate_alu_imm(mode = "addic") 

def generate_subi():
    generate_alu_imm(mode = "subi")

def generate_subic():
    generate_alu_imm(mode = "subic")

def generate_sli():
    generate_alu_imm(mode = "sli")

def generate_srli():
    generate_alu_imm(mode = "srli")

def generate_srai():
    generate_alu_imm(mode = "srai")

#imm是两个寄存器加一个操作数的指令
def generate_alu_imm(mode = "addi"): 
    #正常接收这个函数是Rd赋值，但是这里我们需要一个赋值过的Rs寄存器
    Rd,Rs = distribute_reg()
    imm11 = generate_imm(11,0)
    imm6 = generate_imm(6,0)

    if mode == "sli" or mode == "srai" or mode == "srli":
        imm = imm6
    else:
        imm = imm11


    #随机选择是否测试进位
    is_carry = random.choice([True,False])
    has_carry = mode in ["addic","subic","addi","subi"]  #指令允许处理进位

    if is_carry and has_carry:
        imm_cr = random.choice(["0x4000","0x4001"])

        insert_control(imm_cr)

    instr = f"{mode} {Rd} {Rs} {imm}"

    dep_list = update_slot_rely(mode="read",reg_list=[Rs]) #获取寄存器依赖
    enqueue_instruction(slot_queue = slot1_queue,inst_str = instr,dep_list = dep_list)

    slot1_tail = get_queue_tail_index(1)
    update_written_registers([Rd], mode="write",slot_rely=[slot1_tail,0,0]) #更新已经使用过的寄存器
    update_recent_written_registers([Rd], ttl=WAIT_TIMES["add"],allow_decrease=True)  # 设置倒计时

    # 检查进位是否被设置
    check_control()
def generate_mac16():
    generate_mac(mode = "mac16")

def generate_macu16():
    generate_mac(mode = "macu16")

def generate_mac32():
    generate_mac(mode = "mac32")

def generate_macu32():
    generate_mac(mode = "macu32")

def generate_mac64():
    generate_mac(mode = "mac64")

def generate_macu64():
    generate_mac(mode = "macu64")

def generate_mac(mode = "mac16"):

    Rs,Rt = distribute_reg(reg1_set=True,reg2_set=True,reg1_bits=32,reg2_bits=32)
    if mode == "mac16" or mode == "macu16":
        # 这里要求Rd有值，所以设置为read
        Rd,Rd1 = select_pairs(mode="rw",used_regs=written_registers,require_even=True)
        write_Rd = [Rd,Rd1]
    else:
        Rd,_ = select_pairs(mode="rw",used_regs=written_registers)
        write_Rd = [Rd]

#      is_carry = random.choice([True,False])
#      has_carry = mode in ["mac32","macu32"]  #指令允许处理进位

#      if is_carry and has_carry:
#          imm_cr = random.choice(["0x0000","0x0020"])
#          insert_control(imm_cr)

    dep_list = update_slot_rely(mode="read",reg_list=[Rd]) #获取寄存器依赖

    instr = f"{mode} {Rd} {Rs} {Rt}"
    enqueue_instruction(slot_queue = slot1_queue,inst_str = instr,dep_list=dep_list)

    slot1_tail = get_queue_tail_index(1)
    update_written_registers(reg_list=write_Rd, mode="write",slot_rely=[slot1_tail,0,0]) #更新已经使用过的寄存器
    update_recent_written_registers(write_Rd, ttl=WAIT_TIMES["add"],allow_decrease=True)  # 设置倒计时
    if mode in ["mac16","macu16"]:
        nop(1,5)

    if mode in ["macu32","mac32"]:
        check_control()

