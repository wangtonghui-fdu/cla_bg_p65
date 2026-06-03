# global_state.py
# 全局控制函数的库

import random
from config.config import TestConfig
# 增强BYPASS_TEST
BYPASS_TEST = TestConfig.INCREASE_BYPASS_TEST

from config.config import RegConfig
GR_NUM = RegConfig.GR_NUM
BAR_NUM = RegConfig.BAR_NUM
MR_NUM = RegConfig.MR_NUM
OFF_NUM = RegConfig.OFF_NUM
RESERVED_GR_REGS = {"GR0", "GR30"}
# global_vars.py

# 全局集合与字典
written_registers = set()
recent_written_registers = {}
recent_written_registers_time = {}
recent_written_registers_type = {}

instr_count = 0

GR_POOL = [f"GR{i}" for i in range(GR_NUM) if f"GR{i}" not in RESERVED_GR_REGS]

ALL = GR_POOL + \
      [f"OFF{i}" for i in range(OFF_NUM)] + \
      [f"BAR{i}" for i in range(BAR_NUM)] + \
      [f"MR{i}" for i in range(MR_NUM)]


# 初始化所有依赖槽为 0 或其他默认值
recent_written_registers_rely = {reg:[0,0,0] for reg in ALL}

# 初始化三个槽位队列
slot1_queue = []
slot2_queue = []
slot3_queue = []

def return_instr_count():
    """
    返回当前指令数量
    """
    global instr_count
    return instr_count

# 该函数有两个用途，1是上传写过的寄存器，2是获得一个没写过寄存器的分配 
def update_written_registers(reg_list=[], mode="write", reg_type="ALL",slot_rely = [0,0,0]):
    """
    mode:
    - "write": 将 reg_list 中未出现在 written_registers 的寄存器添加进去
    - "read":  返回一个不在 recent_written_registers 中，或其值为 1 的特定类型寄存器
               BYPASS_TEST模式下，优先返回在recent_written_registers里面的寄存器，但是目前有报错风险

    reg_type: 指定类型（"GR", "OFF", "BAR", "MR", "ALL"）
    """
    global written_registers, recent_written_registers,recent_written_registers_time

    # 所有寄存器集合
    GR  = [f"GR{i}" for i in range(GR_NUM) if f"GR{i}" not in RESERVED_GR_REGS]
    OFF = [f"OFF{i}" for i in range(OFF_NUM)]
    BAR = [f"BAR{i}" for i in range(BAR_NUM)]
    MR  = [f"MR{i}" for i in range(MR_NUM)]
    ALL = GR + OFF + BAR + MR

    # 类型映射
    reg_type_map = {
        "GR": GR,
        "FLOAT": GR,
        "OFF": OFF,
        "BAR": BAR,
        "MR": MR,
        "ALL": ALL
    }
    if mode == "write":
        for reg in reg_list:
            if reg in RESERVED_GR_REGS:
                continue
            if reg in ALL and reg not in written_registers:
                written_registers.add(reg)

            update_slot_rely(mode="write",reg_list=[reg],slot_rely=slot_rely)

    elif mode == "read":
        if reg_list:
            valid_pool = [reg for reg in reg_type_map.get(reg_type, []) if reg not in reg_list]
        else:
            valid_pool = reg_type_map.get(reg_type)
        if valid_pool is None:
            raise ValueError("不支持的 reg_type，应为 'GR'、'OFF'、'BAR'、'MR'、'ALL'")

        if reg_type == "FLOAT":
            if valid_pool:
                valid_pool = [reg for reg in valid_pool if reg in recent_written_registers_type and recent_written_registers_type[reg] == "float"]
            else:
                return None
        
        

        if not BYPASS_TEST or random.random() < 0.2:
            candidates = [
                reg for reg in written_registers
                if reg in valid_pool
            ]
        else:
            candidates = [
                reg for reg in written_registers 
                if reg in valid_pool and (reg in recent_written_registers_time and recent_written_registers_time[reg] <= 5)
            ]
#              for reg in candidates:
#                  print(reg,recent_written_registers_time[reg])
#              print("\n")
                

            if not candidates:
#                  print("NONE")
                candidates = [
                    reg for reg in written_registers
                    if reg in valid_pool
                ]

        if not candidates:
            return None
        reg = random.choice(candidates) 
        return reg

    else:
        raise ValueError("mode 参数必须是 'write' 或 'read'")

# 上传寄存器最近被写入的指令编号，三个数字对应三个槽的指令
def update_slot_rely(mode = "write",reg_list = ["GR1"] ,slot_rely = [0,0,0]):
    global recent_written_registers_rely

    if mode == "write":
        for reg in reg_list:
            if reg in RESERVED_GR_REGS:
                continue
            if reg in recent_written_registers_rely:
                old_slot_rely = recent_written_registers_rely[reg]
                new_slot_rely = old_slot_rely
                for i in range(3):
                    if old_slot_rely[i] < slot_rely[i]:
                        new_slot_rely[i] = slot_rely[i]
                recent_written_registers_rely[reg] = new_slot_rely
            else:
                recent_written_registers_rely[reg] = slot_rely
        return [0,0,0]
    else:
        max_combination = [0, 0, 0]
        for reg in reg_list:
            if reg in RESERVED_GR_REGS:
                continue
            if reg not in recent_written_registers_rely:
                raise ValueError(f"Register {reg} is not in the written register pool.")
            rely_values = recent_written_registers_rely[reg]
            max_combination = [max(max_combination[i], rely_values[i]) for i in range(3)]
        return max_combination

# 上传最近写入的寄存器，用于防止出现无法bypass的现象
def update_recent_written_registers(reg_list, ttl, allow_decrease=False,type = "int"):
    """
    - 将 reg_list 中寄存器设为 ttl
    - 如果 allow_decrease 为 True，则未出现的寄存器 TTL -= 1
    - TTL <= 1 的寄存器将被移除
    """
    global recent_written_registers,recent_written_registers_time,recent_written_registers_rely


    # 可选减少 TTL
    if allow_decrease:
        to_remove = []
        for reg in list(recent_written_registers):
            if reg not in reg_list:
                recent_written_registers[reg] -= 1
                if recent_written_registers[reg] <= 1:
                    to_remove.append(reg)

        for reg in list(recent_written_registers_time):
            if reg not in reg_list:
                recent_written_registers_time[reg] += 1


        for reg in to_remove:
            del recent_written_registers[reg]

    # 当前写入的寄存器设置为 ttl
    for reg in reg_list:
        if reg in RESERVED_GR_REGS:
            continue
        recent_written_registers[reg] = ttl
        recent_written_registers_time[reg] = 0
        recent_written_registers_type[reg] = type

    

def enqueue_instruction(slot_queue, inst_str, dep_list,is_instr = True):
    """
    将指令压入指定的槽队列中。

    参数:
        slot_queue: 目标槽队列 (slot1_queue / slot2_queue / slot3_queue)
        inst_str: 指令文本 (字符串)
        dep_list: 指令对 slot1/2/3 的依赖（列表，如 [1,0,0]）

    插入形式:
        {
            "inst": "movigh GR0 0x1234",
            "dep": [1, 0, 0]
        }
    """
    if len(dep_list) != 3:
        raise ValueError("依赖列表 dep_list 必须有三个元素，对应 slot1、slot2、slot3")
    
    global instr_count
    if is_instr:
        instr_count += 1

    slot_queue.append({
        "inst": inst_str,
        "dep": dep_list
    })

def get_last_written_registers(slot = 1):
    """
    返回最近写入的寄存器及其依赖信息。
    如果有多个寄存器的rely最小且相同，随机返回其中之一。
    """
    import random
    global recent_written_registers_rely
    GR  = [f"GR{i}" for i in range(GR_NUM) if f"GR{i}" not in RESERVED_GR_REGS]
    last_regs = []
    last_rely = 0
    for reg in GR:
        if reg in recent_written_registers_rely:
            rely = recent_written_registers_rely[reg][slot - 1]
            if rely > last_rely:
                last_rely = rely
                last_regs = [reg]
            elif rely == last_rely:
                last_regs.append(reg)
    if last_regs:
        return random.choice(last_regs)
    return "GR1"


def nop(slot,times):
    for _ in range(times):
        if slot == 1:
            enqueue_instruction(slot1_queue, "nop", [get_queue_tail_index(1), 0, 0])
        elif slot == 2:
            enqueue_instruction(slot2_queue, "nop", [0, get_queue_tail_index(2), 0])
        elif slot == 3:
            enqueue_instruction(slot3_queue, "nop", [0, 0, get_queue_tail_index(3)])
    
def get_queue_head_index(queue, slot):
    """
    获取队列头部指令在指定槽的依赖编号。
    如果队列为空，返回 0。
    """
    if not queue:
        return 1
    return queue[0]["dep"][slot - 1] + 1

def get_queue_tail_index(slot):
    """
    获取队列的长度。
    若队列为空，返回 0。
    """
    global slot1_queue,slot2_queue,slot3_queue
    if slot == 1:
        return len(slot1_queue)
    elif slot == 2:
        return len(slot2_queue)
    elif slot == 3:
        return len(slot3_queue)
    else:
        raise ValueError("slot must be 1,2 or 3")

def clearRegsiter():
    global written_registers, recent_written_registers,recent_written_registers_time,recent_written_registers_type
    written_registers = set()
#      recent_written_registers = {}
    recent_written_registers_time = {}
    recent_written_registers_type = {}


def print_reg():
    for reg in recent_written_registers_rely:
        [s1,s2,s3] = recent_written_registers_rely[reg]
        print(f"{reg} {s1,s2,s3}")

# MARK_SIGN用于写入一些标记，会自动排出
MARK_SIGN = []

def enqueue_mark(inst_str,mode = "write"):
    """
    将标记指令压入 MARK_SIGN 列表中，如果已存在则自动添加数字标号。
    """
    global MARK_SIGN
    if mode != "write":
        if inst_str in MARK_SIGN:
            return True
    
    # 检查是否已存在相同的标记
    if inst_str in MARK_SIGN:
        # 查找所有以 inst_str 开头的标记并提取数字
        max_num = 0
        for existing_mark in MARK_SIGN:
            if existing_mark.startswith(inst_str):
                # 检查后面是否跟数字
                suffix = existing_mark[len(inst_str):]
                if suffix.isdigit():
                    num = int(suffix)
                    if num > max_num:
                        max_num = num
        
        # 生成新的标记名
        new_mark = f"{inst_str}{max_num + 1}"
#          print(f"{new_mark}")
        MARK_SIGN.append(new_mark)
        enqueue_instruction(slot1_queue, new_mark, [get_queue_tail_index(1), 0, 0],is_instr=False)
        return new_mark
    else:
        # 如果标记不存在，直接添加
        MARK_SIGN.append(inst_str)
        enqueue_instruction(slot1_queue, inst_str, [get_queue_tail_index(1), 0, 0],is_instr=False)
        return inst_str
    
