import random
from config.peripheral import I2C_Config

from tool.tool import distribute_reg,insert_data_reg
from global_state.global_state import enqueue_instruction,get_queue_tail_index,update_slot_rely,get_last_written_registers
from global_state.global_state import enqueue_mark

from global_state.global_state import slot2_queue,slot3_queue
from config.config import RegConfig
from config.config import TestConfig

I2C_REG = I2C_Config.I2C_REG
I2C_REG_CONFIG = I2C_Config.I2C_REG_CONFIG



MAX_TIMES = I2C_Config.MAX_TIMES
MIN_TIMES = I2C_Config.MIN_TIMES
FIFO_ADDR = I2C_Config.FIFO_ADDR

def generate_i2c_instr():
    mark = "I2C_START"
    Rd,Rs = distribute_reg(reg1_bits=32,reg1_set=False,reg2_bits=32,reg2_set=False)
    if not enqueue_mark(mark,"read"):
        enqueue_mark(mark)
        for reg in I2C_REG:
            config = I2C_REG_CONFIG[reg]
            addr = config['addr']
            value  = config['value']
            insert_data_reg(Rs,addr,30,slot2_wait=False,slot3_wait=False,use_mov=True)  #将地址基值存入Rs寄存器
            insert_data_reg(Rd,value,30,slot2_wait=False,slot3_wait=False,use_mov=True)  #将地址基值存入Rs寄存器
            instr = f"store32 {Rs} {Rd} 0x000"

            dep_list = update_slot_rely(mode="read",reg_list=[Rd,Rs])
            enqueue_instruction(slot_queue = slot3_queue,inst_str = instr,dep_list=dep_list)


    mark = "I2C_WRITE_FIFO"
    enqueue_mark(mark)

    insert_data_reg(Rs,FIFO_ADDR,30,slot2_wait=True,slot3_wait=True,use_mov=True)  #将地址基值存入Rs寄存器
    for _ in range(random.randint(MIN_TIMES,MAX_TIMES)):
        Rd,_ = distribute_reg(reg1_bits=32,reg1_set=True,reg2_bits=32,reg2_set=False)
        instr = f"store32 {Rd} {Rs} 0x000"

        slot1_tail = get_queue_tail_index(1)
        slot2_tail = get_queue_tail_index(2)
        slot3_tail = get_queue_tail_index(3)
        enqueue_instruction(slot_queue = slot3_queue,inst_str = instr,dep_list=[slot1_tail,slot2_tail,slot3_tail])

    insert_data_reg(Rs,FIFO_ADDR,30,slot2_wait=True,slot3_wait=True,use_mov=True)  #将地址基值存入Rs寄存器
        
