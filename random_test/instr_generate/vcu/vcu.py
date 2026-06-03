
from tool.tool import distribute_reg, select_pairs, select_registers 
from tool.tool import check_control

from global_state.global_state import update_written_registers, update_recent_written_registers,update_slot_rely
from global_state.global_state import written_registers,recent_written_registers
from global_state.global_state import enqueue_instruction

from global_state.global_state import slot1_queue

WAIT_TIMES = {
    "CRC": 3,  
    "quadf": 3,  
}



def generate_vcrc8ll():
    generate_vcu_3_reg(mode = "vcrc8ll")

def generate_vcrc8lh():
    generate_vcu_3_reg(mode = "vcrc8lh")

def generate_vcrc8hl():
    generate_vcu_3_reg(mode = "vcrc8hl")

def generate_vcrc8hh():
    generate_vcu_3_reg(mode = "vcrc8hh")

def generate_vcrc16p1ll():
    generate_vcu_3_reg(mode = "vcrc16p1ll")

def generate_vcrc16p1lh():
    generate_vcu_3_reg(mode = "vcrc16p1lh")

def generate_vcrc16p1hl():
    generate_vcu_3_reg(mode = "vcrc16p1hl")

def generate_vcrc16p1hh():
    generate_vcu_3_reg(mode = "vcrc16p1hh")

def generate_vcrc16p2ll():
    generate_vcu_3_reg(mode = "vcrc16p2ll")

def generate_vcrc16p2lh():
    generate_vcu_3_reg(mode = "vcrc16p2lh")

def generate_vcrc16p2hl():
    generate_vcu_3_reg(mode = "vcrc16p2hl")

def generate_vcrc16p2hh():
    generate_vcu_3_reg(mode = "vcrc16p2hh")

def generate_vcrc32ll():
    generate_vcu_3_reg(mode = "vcrc32ll")

def generate_vcrc32lh():
    generate_vcu_3_reg(mode = "vcrc32lh")

def generate_vcrc32hl():
    generate_vcu_3_reg(mode = "vcrc32hl")

def generate_vcrc32hh():
    generate_vcu_3_reg(mode = "vcrc32hh")

def generate_vcu_3_reg(mode = "mpy2pif32"):
    Rs,Rt = distribute_reg(reg1_set=False,reg2_set=True,reg1_bits=32,reg2_bits=32,float=True)
    Rd = select_registers(mode="GR",method="RANDOM",reg_type="",used_regs=recent_written_registers)

    instr = f"{mode} {Rd} {Rs} {Rt}"
    dep_list = update_slot_rely(mode="read",reg_list=[Rs,Rt]) #获取寄存器依赖

    enqueue_instruction(slot_queue = slot1_queue,inst_str = instr,dep_list=dep_list)
    update_written_registers([Rd], mode="write") #更新已经使用过的寄存器
    update_recent_written_registers([Rd], ttl=WAIT_TIMES["CRC"],allow_decrease=True,type="float")  # 设置倒计时

