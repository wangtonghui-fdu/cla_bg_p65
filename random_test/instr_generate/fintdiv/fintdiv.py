from tool.tool import distribute_reg, insert_data_reg, probability_return, select_pairs
from tool.tool import check_control

from global_state.global_state import update_written_registers, update_recent_written_registers,update_slot_rely
from global_state.global_state import written_registers
from global_state.global_state import enqueue_instruction

from global_state.global_state import slot1_queue

WAIT_TIMES = {
    "absi32div32": 3,  
}




def generate_absi32div32u():
    generate_fintdiv_2_reg(mode = "absi32div32u")

def generate_absi64div32u():
    generate_fintdiv_2_reg(mode = "absi64div32u")

def generate_absi64div64u():
    generate_fintdiv_2_reg(mode = "absi64div64u")

def generate_negi32div32():
    generate_fintdiv_2_reg(mode="negi32div32")

def generate_negi64div64():
    generate_fintdiv_2_reg(mode="negi64div64")

def generate_negi64div32():
    generate_fintdiv_2_reg(mode="negi64div32")

def generate_absi32div32():
    generate_fintdiv_3_reg(mode="absi32div32")

def generate_subc4ui32():
    generate_fintdiv_3_reg(mode="subc4ui32")

def generate_enegi32div32():
    generate_fintdiv_3_reg(mode="enegi32div32")

def generate_mnegi32div32():
    generate_fintdiv_3_reg(mode="mnegi32div32")

def generate_absi64div32():
    generate_fintdiv_3_reg(mode="absi64div32")

def generate_absi64div64():
    generate_fintdiv_3_reg(mode="absi64div64")

def generate_subc2ui64():
    generate_fintdiv_3_reg(mode="subc2ui64")

def generate_enegi64div64():
    generate_fintdiv_3_reg(mode="enegi64div64")

def generate_mnegi64div64():
    generate_fintdiv_3_reg(mode="mnegi64div64")

def generate_enegi64div32():
    generate_fintdiv_3_reg(mode="enegi64div32")

def generate_mnegi64div32():
    generate_fintdiv_3_reg(mode="mnegi64div32")

def generate_fintdiv_2_reg(mode = "absi32div32u"):
    RsH = None
    RdH = None
    if mode == "absi32div32u" or mode == "negi32div32":
        Rd,Rs = distribute_reg(reg1_set=True,reg2_set=True,reg1_bits=32,reg2_bits=32)
        write_Rd = [Rd,Rs]
    elif mode == "absi64div32u":
        Rd,_ = distribute_reg(reg1_set=True,reg2_set=False,reg1_bits=32,reg2_bits=32)
        Rs,RsH = select_pairs(mode="rw",used_regs=written_registers,require_even=True)
        write_Rd = [Rd,Rs,RsH]
    elif mode == "absi64div64u" or mode == "negi64div64":
        Rd,RdH = select_pairs(mode="rw",used_regs=written_registers,require_even=True)
        Rs,RsH = select_pairs(mode="rw",used_regs=written_registers,require_even=True)
        write_Rd = [Rd,RdH,Rs,RsH]
    elif mode == "negi64div32": 
        Rd,RdH = select_pairs(mode="rw",used_regs=written_registers,require_even=True)
        Rs,_ = distribute_reg(reg1_set=True,reg2_set=True,reg1_bits=32,reg2_bits=32)
        write_Rd = [Rd,RdH,Rs]
    else:
        Rd,RdH = select_pairs(mode="rw",used_regs=written_registers,require_even=True)
        Rs,RsH = select_pairs(mode="rw",used_regs=written_registers,require_even=True)
        write_Rd = [Rd,RdH,Rs,RsH]

    if probability_return(0.1):
        if mode == "absi32div32u":
            insert_data_reg(Rs,0x80000000)
        if mode == "absi64div32u" or mode == "absi64div64u":
            insert_data_reg(Rs,0x00000000)
            insert_data_reg(RsH,0x80000000)
        if mode == "negi32div32" or mode == "negi64div32" or mode == "negi64div64":
            check_control()
            

    instr = f"{mode} {Rd} {Rs}"
    instr = f"{mode} {Rd} {Rs}"
    dep_list = update_slot_rely(mode="read",reg_list=[Rs]) #获取寄存器依赖

    enqueue_instruction(slot_queue = slot1_queue,inst_str = instr,dep_list=dep_list)
    update_written_registers(write_Rd, mode="write") #更新已经使用过的寄存器
    update_recent_written_registers(write_Rd, ttl=WAIT_TIMES["absi32div32"],allow_decrease=True,type="float")  # 设置倒计时

    check_control()
 
def generate_fintdiv_3_reg(mode = "absi32div32"):
    RdH = None
    RsH = None
    RtH = None
    if mode == "absi32div32" or mode == "subc4ui32" or mode == "enegi32div32" or mode == "mnegi32div32":
        # 这里要求Rd有值，所以设置为read
        Rs,Rt = distribute_reg(reg1_set=True,reg2_set=True,reg1_bits=32,reg2_bits=32)
        Rd,_ = select_pairs(mode="rw",used_regs=written_registers)
        write_Rd = [Rd,Rs,Rt]
        if mode == "subc4ui32" or mode == "enegi32div32" or mode == "mnegi32div32":
            write_Rd = [Rd,Rs]
            
    elif mode == "absi64div32":
        Rd,Rt = distribute_reg(reg1_set=True,reg2_set=True,reg1_bits=32,reg2_bits=32)
        Rs,RsH = select_pairs(mode="rw",used_regs=written_registers,require_even=True)
        write_Rd = [Rd,Rs,RsH,Rt]
    elif mode == "absi64div64" or mode == "subc2ui64" or mode == "enegi64div64" or mode == "mnegi64div64":
        Rd,RdH = select_pairs(mode="rw",used_regs=written_registers,require_even=True)
        Rs,RsH = select_pairs(mode="rw",used_regs=written_registers,require_even=True)
        Rt,RtH = select_pairs(mode="rw",used_regs=written_registers,require_even=True)
        if mode == "absi64div64":
            write_Rd = [Rd,RdH,Rs,RsH,Rt,RtH]
        else:
            write_Rd = [Rd,RdH,Rs,RsH]
    elif mode == "enegi64div32" or mode == "mnegi64div32": 
        Rd,RdH = select_pairs(mode="rw",used_regs=written_registers,require_even=True)
        Rs,Rt = distribute_reg(reg1_set=True,reg2_set=True,reg1_bits=32,reg2_bits=32)
        write_Rd = [Rd,RdH,Rs]
    else:
        Rd,Rt = select_pairs(mode="rw",used_regs=written_registers)
        Rs,RsH = select_pairs(mode="rw",used_regs=written_registers,require_even=True)
        write_Rd = [Rd]

    if probability_return(0.1):
        if mode == "absi32div32":
            if probability_return(0.8):
                insert_data_reg(Rs,0x80000000)
            if probability_return(0.8): 
                insert_data_reg(Rt,0x80000000)
        if mode == "absi64div32":
            if probability_return(0.8):
                insert_data_reg(Rs,0x00000000)
            if probability_return(0.8):
                insert_data_reg(RsH,0x80000000)
            if probability_return(0.8):
                insert_data_reg(Rt,0x80000000)
        if mode == "absi64div64":
            if probability_return(0.8):
                insert_data_reg(Rs,0x00000000)
            if probability_return(0.8):
                insert_data_reg(RsH,0x80000000)
            if probability_return(0.8):
                insert_data_reg(Rt,0x00000000)
            if probability_return(0.8):
                insert_data_reg(RtH,0x80000000)
        if mode == "subc2ui64":
            insert_data_reg(Rt,0x00000000)
        if mode == "subc2ui64":
            if probability_return(0.8):
                insert_data_reg(Rt,0x00000000)
            if probability_return(0.8):
                insert_data_reg(RtH,0x00000000)
        if mode == "enegi32div32" or mode == "mnegi32div32" or mode == "enegi64div32" or mode == "mnegi64div32" or mode == "enegi64div64" or mode == "mnegi64div64":
            check_control()
            


    instr = f"{mode} {Rd} {Rs} {Rt}"
    dep_list = update_slot_rely(mode="read",reg_list=[Rs]) #获取寄存器依赖

    enqueue_instruction(slot_queue = slot1_queue,inst_str = instr,dep_list=dep_list)
    update_written_registers(write_Rd, mode="write") #更新已经使用过的寄存器
    update_recent_written_registers(write_Rd, ttl=WAIT_TIMES["absi32div32"],allow_decrease=True,type="float")  # 设置倒计时

    check_control()


