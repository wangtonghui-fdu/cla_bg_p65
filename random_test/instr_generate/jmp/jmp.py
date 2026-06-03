import random
import re

from tool.tool import select_registers,insert_control,probability_return
from tool.ram import handle_function_range
from slot1.slot1 import handle_slot1_instr
from global_state.global_state import recent_written_registers,nop
from global_state.global_state import enqueue_instruction,get_queue_tail_index,return_instr_count



from global_state.global_state import slot1_queue
from jmp.devide import check_and_mark_point
from config.config import JmpConfig,BASE_PC,TestConfig,ClaConfig

TEST_CLA = TestConfig.TEST_CLA
REAL_TEST = TestConfig.REAL_TEST

CLA_NOT_SUPPORT_JMP = ClaConfig.CLA_NOT_SUPPORT_JMP
CLA_NOT_SUPPORT_CALL = ClaConfig.CLA_NOT_SUPPORT_CALL
CLA_NOT_SUPPORT_RET = ClaConfig.CLA_NOT_SUPPORT_RET

# ======================
# 全局宏定义
# ======================

HIGH_ADDR = JmpConfig.HIGH_ADDR
LOW_ADDR = JmpConfig.LOW_ADDR

# 开始调试
JMP_DEBUG = JmpConfig.JMP_DEBUG

# 函数名称列表（可在此处修改）
START_PART = JmpConfig.START_PART
FINISH_PART = JmpConfig.FINISH_PART
MAIN_PART = JmpConfig.MAIN_PART
FUNCTION_PART = JmpConfig.FUNCTION_PART

START_END = f"{START_PART}_end"
FINISH_END = f"{FINISH_PART}_end"
MAIN_END = f"{MAIN_PART}_end"

FUNCTION = JmpConfig.FUNCTION
FUNCTION_NAMES = [f"{FUNCTION_PART}_{name}" for name in FUNCTION]
START_SIGN = {key:"0x00000000" for key in FUNCTION_NAMES + [START_PART] + [FINISH_PART]}


def handle_jmp_instr(function_name: str,pc):
    """
    根据函数名称匹配不同模式执行操作
    
    参数:
        function_name: 函数名称
    """
    # 定义指令映射
    jmp_instr_map = {
        "jmp": generate_jmp,
        "sjmp": generate_sjmp,
        "jc": generate_jc,
        "sjc": generate_sjc,
        "jnc": generate_jnc,
        "sjnc": generate_sjnc,
        "jmpr": generate_jmpr,
        "sjmpr": generate_sjmpr,
    }
    
    call_instr_map = {
        "call": generate_call,
        "scall": generate_scall,
        "callr": generate_callr,
        "scallr": generate_scallr,
    }
    
    ret_instr_map = {
        "ret": generate_ret,
        "sret": generate_sret,
    }
    
    # 匹配不同模式
    if function_name == START_END:
        # 执行 start_end 相关操作
        if JMP_DEBUG:
            print("处理 {START_END}")
        # 使用 jmp_instr_map
        if not TEST_CLA:
            choices = [key for key in jmp_instr_map.keys() ]
        else:
            choices = [key for key in jmp_instr_map.keys() if key not in CLA_NOT_SUPPORT_JMP]
        # 随机选择一个指令并执行
        jmp_instr_map[random.choice(choices)](MAIN_PART)

    elif function_name == FINISH_END or function_name == MAIN_END:
        if JMP_DEBUG:
            print("处理 {function_name}")

    elif function_name.endswith("_end"):
        # 执行 *_end 相关操作
        part_name = function_name.replace("_end", "")
        if JMP_DEBUG:
            print(f"处理结束部分: {part_name}")

        # 使用 ret_instr_map
        if not TEST_CLA:
            choices = [key for key in ret_instr_map.keys() ]
        else:
            choices = [key for key in ret_instr_map.keys() if key not in CLA_NOT_SUPPORT_RET]
        # 随机选择一个指令并执行
        handle_function_range(function_name=part_name,is_ret=True)
        ret_instr_map[random.choice(choices)]()
    
    elif function_name.startswith(FUNCTION_PART) or function_name in [MAIN_PART,START_PART,FINISH_PART]:
        # 执行 function_* 相关操作
        if JMP_DEBUG:
            print(f"处理函数: {function_name}")
        # 插入函数标志
        instr = function_name
        slot1_tail = get_queue_tail_index(1)
        slot2_tail = get_queue_tail_index(2)
        slot3_tail = get_queue_tail_index(3)
        enqueue_instruction(slot_queue = slot1_queue,inst_str = instr,dep_list=[slot1_tail,slot2_tail,slot3_tail],is_instr=False)
        handle_function_range(function_name=function_name,is_ret=False)
        START_SIGN[function_name] = pc
    
    elif function_name.startswith("call_"):
        # 执行 call_* 相关操作
        function_name = re.sub(r'_\d+$', '', function_name)
        call_name = function_name.replace("call_", "")
        if JMP_DEBUG:
            print(f"处理调用: {call_name}")
        # 使用 call_instr_map
        if not TEST_CLA:
            choices = [key for key in call_instr_map.keys() ]
        else:
            choices = [key for key in call_instr_map.keys() if key not in CLA_NOT_SUPPORT_CALL]
        # 随机选择一个指令并执行
        call_instr_map[random.choice(choices)](call_name)
    
    
    else:
        # 默认处理
        if JMP_DEBUG:
            print(f"未知函数名称: {function_name}")
        return {}

def generate_jmp(functionName):
     generate_jump(functionName,"jmp")
    
def generate_sjmp(functionName):
     generate_jump(functionName,"sjmp")

def generate_jc(functionName):
     generate_jump(functionName,"jc")

def generate_jnc(functionName):
     generate_jump(functionName,"jnc")

def generate_sjc(functionName):
     generate_jump(functionName,"sjc")

def generate_sjnc(functionName):
     generate_jump(functionName,"sjnc")

def generate_jmpr(functionName):
     generate_jump(functionName,"jmpr")

def generate_sjmpr(functionName):
     generate_jump(functionName,"sjmpr")

def generate_jump(functionName,mode = "jmp"):
    slot1_tail = get_queue_tail_index(1)
    slot2_tail = get_queue_tail_index(2)
    slot3_tail = get_queue_tail_index(3)
    if mode == "jmp" or mode == "sjmp":
        instr = f"{mode} {functionName}"
        enqueue_instruction(slot_queue = slot1_queue,inst_str = instr,dep_list=[slot1_tail,slot2_tail,slot3_tail])
    elif mode == "jc" or mode == "sjc":
        insert_control("0x0010")
        nop(1,5)
        instr = f"{mode} {functionName}"
        enqueue_instruction(slot_queue = slot1_queue,inst_str = instr,dep_list=[slot1_tail,slot2_tail,slot3_tail])
    elif mode == "jnc" or mode == "sjnc":
        insert_control("0x0000")
        instr = f"{mode} {functionName}"
        nop(1,5)
        enqueue_instruction(slot_queue = slot1_queue,inst_str = instr,dep_list=[slot1_tail,slot2_tail,slot3_tail])
    elif mode == "jmpr" or mode == "sjmpr":
        Rd = select_registers(mode="GR",method="RANDOM",reg_type="",used_regs=recent_written_registers)
        instr = f"movigl {Rd} {functionName}{LOW_ADDR}"
        enqueue_instruction(slot_queue = slot1_queue,inst_str = instr,dep_list=[get_queue_tail_index(1),0,0])
        instr = f"movigh {Rd} {functionName}{HIGH_ADDR}"
        enqueue_instruction(slot_queue = slot1_queue,inst_str = instr,dep_list=[get_queue_tail_index(1),0,0])

        instr = f"{mode} {Rd}"
        enqueue_instruction(slot_queue = slot1_queue,inst_str = instr,dep_list=[slot1_tail,slot2_tail,slot3_tail])
    if mode in ["jmp","jc","jnc","jmpr"]:
        for _ in range(2):
            handle_slot1_instr(instr_name="random_calculate")

def generate_ret():
    generate_return("ret")

def generate_sret():
    generate_return("sret")

def generate_return(mode = "ret"):
    instr = f"{mode}"
#      if probability_return(0.5):
#          if mode == "ret":
#              instr = f"jmpr GR31"
#          elif mode == "sret":
#              instr = f"sjmpr GR31"
    slot1_tail = get_queue_tail_index(1)
    slot2_tail = get_queue_tail_index(2)
    slot3_tail = get_queue_tail_index(3)
    enqueue_instruction(slot_queue = slot1_queue,inst_str = instr,dep_list=[slot1_tail,slot2_tail,slot3_tail])
    if mode == "ret":
        for _ in range(2):
            handle_slot1_instr(instr_name="random_calculate")
     
def generate_call(functionName):
     generate_call_function(functionName,"call")

def generate_scall(functionName):
     generate_call_function(functionName,"scall")

def generate_callr(functionName):
     generate_call_function(functionName,"callr")

def generate_scallr(functionName):
     generate_call_function(functionName,"scallr")

def generate_call_function(functionName,mode = "call"):
    if mode == "call" or mode == "scall":
        slot1_tail = get_queue_tail_index(1)
        slot2_tail = get_queue_tail_index(2)
        slot3_tail = get_queue_tail_index(3)
        instr = f"{mode} {functionName}"
        enqueue_instruction(slot_queue = slot1_queue,inst_str = instr,dep_list=[slot1_tail,slot2_tail,slot3_tail])

    elif mode == "callr" or mode == "scallr":
        Rd = select_registers(mode="GR",method="RANDOM",reg_type="",used_regs=recent_written_registers)
        instr = f"movigh {Rd} {functionName}{HIGH_ADDR}"
        enqueue_instruction(slot_queue = slot1_queue,inst_str = instr,dep_list=[get_queue_tail_index(1),0,0])
        instr = f"movigl {Rd} {functionName}{LOW_ADDR}"
        enqueue_instruction(slot_queue = slot1_queue,inst_str = instr,dep_list=[get_queue_tail_index(1),0,0])

        slot1_tail = get_queue_tail_index(1)
        slot2_tail = get_queue_tail_index(2)
        slot3_tail = get_queue_tail_index(3)
        instr = f"{mode} {Rd}"
        enqueue_instruction(slot_queue = slot1_queue,inst_str = instr,dep_list=[slot1_tail,slot2_tail,slot3_tail])

    # 产生延迟槽使用的指令 
    if mode in ["call","callr"]:
        for _ in range(2):
            handle_slot1_instr(instr_name="random_calculate")


def check_jmp(test_jmp):
    if test_jmp:
        for _ in range(4):
            instr_count = return_instr_count()  # 获取当前指令数量
            point_name,set_point = check_and_mark_point(instr_count)
            if set_point:
                pc = instr_count * 4 + BASE_PC
                pc = f"0x{pc:08X}"
                handle_jmp_instr(point_name,pc)

                if JMP_DEBUG:
                    print(f"{point_name},{instr_count}")
                return True
        return False
