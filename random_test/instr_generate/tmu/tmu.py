
from tool.tool import distribute_reg, select_pairs, select_registers 
from tool.tool import check_control

from global_state.global_state import update_written_registers, update_recent_written_registers,update_slot_rely
from global_state.global_state import written_registers
from global_state.global_state import enqueue_instruction

from global_state.global_state import slot1_queue

WAIT_TIMES = {
    "mpy2pif32": 3,  
    "quadf": 3,  
}



def generate_mpy2pif32():
    generate_tmu_2_reg(mode = "mpy2pif32")

def generate_div2pif32():
    generate_tmu_2_reg(mode = "div2pif32")

def generate_sinpuf32():
    generate_tmu_2_reg(mode = "sinpuf32")

def generate_cospuf32():
    generate_tmu_2_reg(mode = "cospuf32")

def generate_atanpuf32():
    generate_tmu_2_reg(mode = "atanpuf32")

def generate_exppuf32():
    generate_tmu_2_reg(mode = "exppuf32")

def generate_logpuf32():
    generate_tmu_2_reg(mode = "logpuf32")

def generate_tmu_2_reg(mode = "mpy2pif32"):
    Rd,Rs = distribute_reg(reg1_set=False,reg2_set=True,reg1_bits=32,reg2_bits=32,float=True)

    instr = f"{mode} {Rd} {Rs}"
    dep_list = update_slot_rely(mode="read",reg_list=[Rs]) #获取寄存器依赖

    enqueue_instruction(slot_queue = slot1_queue,inst_str = instr,dep_list=dep_list)
    update_written_registers([Rd], mode="write") #更新已经使用过的寄存器
    update_recent_written_registers([Rd], ttl=WAIT_TIMES["mpy2pif32"],allow_decrease=True,type="float")  # 设置倒计时

    if mode in ["mpy2pif32","div2pif32","atanpif32","exppif32","logpif32"]:
        check_control()
        

def generate_quadf():
    Rs,Rt = distribute_reg(reg1_set=True,reg2_set=True,reg1_bits=32,reg2_bits=32,float=True)
    Rd,_ = select_pairs(mode="write",used_regs=written_registers,require_even=True)

    instr = f"quadf {Rd} {Rs} {Rt}"
    dep_list = update_slot_rely(mode="read",reg_list=[Rs,Rt]) #获取寄存器依赖

    enqueue_instruction(slot_queue = slot1_queue,inst_str = instr,dep_list=dep_list)
    update_written_registers([Rd], mode="write") #更新已经使用过的寄存器
    update_recent_written_registers([Rd], ttl=WAIT_TIMES["quadf"],allow_decrease=True,type="float")  # 设置倒计时

    check_control()

