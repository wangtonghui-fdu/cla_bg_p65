# tool.py
import random

from global_state.global_state import update_written_registers, update_recent_written_registers
from global_state.global_state import recent_written_registers,update_slot_rely
from global_state.global_state import enqueue_instruction,get_queue_tail_index

from global_state.global_state import slot1_queue,slot3_queue
from global_state.global_state import nop

from config.config import TestConfig
from config.config import ClaConfig

CLA_NOT_SUPPORT_ALU = ClaConfig.CLA_NOT_SUPPORT_ALU
# 增强BYPASS_TEST的概率
BYPASS_TEST = TestConfig.INCREASE_BYPASS_TEST
CR_PRINT = TestConfig.CR_PRINT

TEST_CLA = TestConfig.TEST_CLA
DISABLE_CLA_ADDR_REGS = TestConfig.DISABLE_CLA_ADDR_REGS

from config.config import RegConfig
GR_NUM = RegConfig.GR_NUM
BAR_NUM = RegConfig.BAR_NUM
MR_NUM = RegConfig.MR_NUM
OFF_NUM = RegConfig.OFF_NUM

RESERVED_GR_REGS = {"GR0", "GR30"}


def is_reserved_reg(reg):
    return reg in RESERVED_GR_REGS


def select_registers(mode, method, reg_type=None, index=None,used_regs = [key for key in recent_written_registers]):
    """
    随机或指定选择一个寄存器，但是不使用 used_regs 中的寄存器（仅 RANDOM 模式）。

    参数：
        mode:       使用的寄存器类别（"GR"、"OFF"、"BAR"、"MR"、"ALL"）
        method:     "RANDOM" 或 "FIXED"
        reg_type:   当 method="FIXED" 时使用，如 "GR"（返回 GR+index 的寄存器）
        index:      当 method="FIXED" 时使用的编号（int）
        used_regs:  已使用寄存器列表，仅 RANDOM 时使用

    返回：
        一个寄存器名（如 "GR5"）
    """
    if used_regs is None:
        used_regs = []

    # 所有寄存器集合
    GR  = [f"GR{i}" for i in range(GR_NUM) if f"GR{i}" not in RESERVED_GR_REGS]
    OFF = [f"OFF{i}" for i in range(OFF_NUM)]
    BAR = [f"BAR{i}" for i in range(BAR_NUM)]
    MR  = [f"MR{i}" for i in range(MR_NUM)]
    if TEST_CLA and DISABLE_CLA_ADDR_REGS:
        OFF = []
        BAR = []
        MR = []

    # 根据 mode 决定允许选择的集合
    if mode == "GR":
        available_regs = GR
    elif mode == "OFF":
        available_regs = OFF
    elif mode == "BAR":
        available_regs = BAR
    elif mode == "MR":
        available_regs = MR
    elif mode == "ALL":
        available_regs = GR + OFF + BAR + MR
    else:
        raise ValueError("mode 应为 'GR'、'OFF'、'BAR'、'MR' 或 'ALL'")

    if method == "FIXED":
        if reg_type is None or index is None:
            raise ValueError("FIXED 模式下必须提供 reg_type 和 index")
        
        # 检查 index 合法性
        if reg_type == "GR" and 0 <= index < 32:
            if is_reserved_reg(f"GR{index}"):
                raise ValueError(f"{reg_type}{index} is reserved and cannot be selected")
            return f"GR{index}"
        elif reg_type == "OFF" and 0 <= index < 4:
            return f"OFF{index}"
        elif reg_type == "BAR" and 0 <= index < 4:
            return f"BAR{index}"
        elif reg_type == "MR" and 0 <= index < 4:
            return f"MR{index}"
        else:
            raise IndexError(f"索引 {index} 对应 {reg_type} 寄存器超出范围")

    elif method == "RANDOM":
        # 过滤掉 used_regs 中已用寄存器
        filtered_regs = [reg for reg in available_regs if reg not in used_regs]
        if not filtered_regs:
            raise RuntimeError("没有可用的寄存器可供选择")
        return random.choice(filtered_regs)

    else:
        raise ValueError("method 应为 'RANDOM' 或 'FIXED'")



def select_pairs(mode="read", used_regs=None, require_even=False):
    """
    返回一对连续的 GR 寄存器（如 ("GR5","GR6")）。
    用于部分需要使用rt 和 rt+1 的指令

    参数：
      - mode:
          "read":  优先返回两个连续且在 used_regs(=已写过集合) 中的寄存器；
                   若不存在，则找“一个写过+一个没写过”，对没写过的补写一次；
                   若还不存在，则找“两者都没写过”，并补写两次。
          "write": 返回两个连续且不在 recent_written_registers 中的寄存器。
                   （注意：这里不是“没写过”，而是“最近未写过”）
          "rw"   : 返回两个连续写过且不在 recent_written_registers 中的寄存器。

      - used_regs: 已写过的寄存器集合（等价于之前描述的 written_registers）。
                   若为 None，按空集合处理。

      - require_even: 默认为 False；若为 True，则要求返回对的第一个寄存器编号为偶数。

    依赖全局:
      - GR_NUM: 总 GR 数量
      - recent_written_registers: dict，如 {"GR3": 1, "GR4": 0, ...}；write 模式只看“是否存在键”
      - generate_imm(width, signed_flag)
      - insert_data_reg(reg, imm32, wait_times=2)
    """
    # 统一 used_regs（避免 None 导致的 in 操作类型问题）
    used = set(used_regs) if used_regs is not None else set()
    recent = []
    if mode == "rw":
        recent = [ reg for reg in recent_written_registers ] 

    # 所有连续对 (GR0,GR1), (GR1,GR2), ..., (GR{N-2}, GR{N-1})
    pairs = [
        (f"GR{i}", f"GR{i+1}")
        for i in range(max(0, GR_NUM - 1))
        if not is_reserved_reg(f"GR{i}") and not is_reserved_reg(f"GR{i+1}")
    ]

    # 若要求首寄存器为偶数，则先过滤
    if require_even:
        pairs = [p for p in pairs if (int(p[0][2:]) % 2 == 0)]

    if not pairs:
        raise RuntimeError("没有可用的寄存器对可供选择（受 require_even 约束）")

    if mode == "read" or mode == "rw":
        # 1) 优先：两个都写过
        written_pairs = [p for p in pairs if p[0] in used and p[1] in used and (p[0] not in recent and p[1] not in recent)]
        if written_pairs:
            p = random.choice(written_pairs) 
            return p


        # 2) 退化：一个写过 + 一个没写过（对没写过的那个补写一次）
        half_pairs = [p for p in pairs if (p[0] in used) ^ (p[1] in used) and (p[0] not in recent and p[1] not in recent) ]
        if half_pairs:
            p = random.choice(half_pairs)
            for reg in p:
                if reg not in used:
                    imm32 = generate_imm(32, 0)
                    insert_data_reg(reg, imm32, wait_times=2)
            return p

        # 3) 最后退化：两个都没写过（补写两次）
        never_pairs = [p for p in pairs if (p[0] not in used and p[1] not in used) and (p[0] not in recent and p[1] not in recent)]
        if never_pairs:
            p = random.choice(never_pairs)
            for reg in p:
                imm32 = generate_imm(32, 0)
                insert_data_reg(reg, imm32, wait_times=2)
                # 同上，可选：used.add(reg)
            return p

        raise RuntimeError("没有可用的寄存器可供选择")

    elif mode == "write":
        # 需求：两个都不在“最近写过”列表里（仅检查键是否存在）
        recent = recent_written_registers or {}
        writable_pairs = [p for p in pairs if (p[0] not in recent and p[1] not in recent)]
        if not writable_pairs:
            raise RuntimeError("没有可用的寄存器对可供写入")
        return random.choice(writable_pairs)

    else:
        raise ValueError("mode 参数必须是 'read' 或 'write'")



def generate_imm(bits: int, low_zero: int,min = 0) -> str:
    """
    生成一个随机立即数，满足指定总位数，并确保低位为0的位数。
    返回小写十六进制字符串，如 '0x0040'
    """
    if bits <= 0 or bits > 32:
        raise ValueError("bits 必须在 1 到 32 位之间")
    if low_zero < 0 or low_zero > bits:
        raise ValueError("low_zero 不能大于 bits")

    usable_bits = bits - low_zero
    value = random.randint(min, (1 << usable_bits) - 1)
    value <<= low_zero

    # 小写十六进制格式
    hex_str = f"0x{value:0{(bits + 3) // 4}x}"
    return hex_str
 

def generate_float(bits: int = 32, n: int = 1) -> list:
    """
    生成 n 个十六进制形式的随机浮点数。
    第一个值是完全随机的。每个后续值有 50% 概率完全随机，否则将生成与第一个值数量级相差不超过 20 阶的浮点数（即指数最多相差 20）。

    参数:
        bits: 浮点位宽（32 表示单精度，64 表示双精度，默认为 32）
        n: 需要生成的浮点数个数

    返回:
        n 个类似 '0x40490fdb' 的十六进制浮点字符串列表
    """
    def rand_float(bits, exponent=None):
        if bits == 32:
            sign = random.randint(0, 1) << 31
            if exponent is None:
                exp = int(random.gauss(127, 50))
                exp = max(0, min(255, exp))
            else:
                exp = max(0, min(255, exponent))
            exp_bits = exp << 23
            mantissa = random.randint(0, (1 << 23) - 1)
            value = sign | exp_bits | mantissa
            return f"0x{value:08x}", exp
        elif bits == 64:
            sign = random.randint(0, 1) << 63
            if exponent is None:
                exp = random.randint(1, 2046)
            else:
                exp = max(1, min(2046, exponent))
            exp_bits = exp << 52
            mantissa = random.randint(0, (1 << 52) - 1)
            value = sign | exp_bits | mantissa
            return f"0x{value:016x}", exp
        else:
            raise ValueError("bits 必须是 32(单精度) 或 64(双精度)")

    results = []
    float_hex, base_exp = rand_float(bits)
    results.append(float_hex)
    for _ in range(1, n):
        if random.random() < 0.5:
            float_hex, _ = rand_float(bits)
        else:
            # generate exponent in [base_exp-20, base_exp+20], confined to legal exponent range
            if bits == 32:
                exp_min, exp_max = 0, 255
            else:
                exp_min, exp_max = 1, 2046
            target_exp = random.randint(max(exp_min, base_exp - 20), min(exp_max, base_exp + 20))
            float_hex, _ = rand_float(bits, exponent=target_exp)
        results.append(float_hex)
    return results if n > 1 else results[0]

# 为了增加随机程度，我们不止使用movigl/movigh指令
# 还可以使用其他alu指令
def insert_data_reg(reg, imm,wait_times = 1,slot2_wait = False,slot3_wait = False,mode = "unsigned",use_mov = True):
    """
    将立即数 imm 插入到寄存器 reg 中，分为高低两部分。
    imm 应为小写十六进制字符串，如 '0x0040'
    wait_times 是限制写回寄存器下次调用的时间，防止过早访问没有写回的寄存器，
    slot2_wait 和 slot3_wait 控制是否等待当前 slot2 和 slot3 的指令队列。
    use_mov = True的时候，赋值只能用mov指令完成
    """

    if is_reserved_reg(reg):
        raise ValueError(f"{reg} is reserved and cannot be written by random application code")

    # 各条指令使用的立即数
    alu_calculate_instr_map = {
        # === 立即数型 ALU ===
        "addi":11,
        "addic":11,
        "subi":11,
        "subic":11,

        # === 寄存器型 ALU（二/三操作数）===
        "add":32,
        "addc":32,
        "sub":32,
        "subc":32,
        "and":32,
        "or":32,
        "xor":32,
    }

    random_mode = random.randint(0,2)
    slot2_tail = 0
    slot3_tail = 0
    if slot2_wait:
        slot2_tail = get_queue_tail_index(2)
    if slot3_wait:
        slot3_tail = get_queue_tail_index(3)

    if random_mode != 0 or use_mov or mode == "float":
        if mode != "float":
            imm_hex = format_imm(imm = imm, mode=mode,width=32)
        else:
            imm_hex = format_imm(imm = imm, mode="unsigned",width=32)
        high_bits = imm_hex[:4] 
        low_bits = imm_hex[4:] 
        high_part = f"0x{high_bits}"
        low_part = f"0x{low_bits}"
        if high_part != "0x0000" or TEST_CLA:
 
            instr = f"movigl {reg} {low_part}"
            enqueue_instruction(slot_queue = slot1_queue,inst_str = instr,dep_list=[0,slot2_tail,slot3_tail])

            instr = f"movigh {reg} {high_part}"
            enqueue_instruction(slot_queue = slot1_queue,inst_str = instr,dep_list=[get_queue_tail_index(1),slot2_tail,slot3_tail])
        else:
            instr = f"moviglz {reg} {low_part}"
            enqueue_instruction(slot_queue = slot1_queue,inst_str = instr,dep_list=[0,slot2_tail,slot3_tail])

        slot1_tail = get_queue_tail_index(1)
        update_written_registers([reg], mode="write",slot_rely = [slot1_tail,0,0]) #更新已经使用过的寄存器
        if mode != "float":
            update_recent_written_registers([reg], ttl=wait_times,allow_decrease=True)  # 设置倒计时
        else:
            update_recent_written_registers([reg], ttl=wait_times,allow_decrease=True,type="float")  # 设置倒计时

    else:
        if not TEST_CLA:
            instr_list = list(alu_calculate_instr_map.keys())
        else:
            instr_list = [ k for k in alu_calculate_instr_map.keys() if k not in CLA_NOT_SUPPORT_ALU]
        random_instr = random.choice(instr_list)
        imm_bits = alu_calculate_instr_map[random_instr]
        insert_data_instr(reg, imm,imm_bits, random_instr, wait_times, slot2_wait, slot3_wait)


# 用其他指令处理值的插入,可以使用的指令
def insert_data_instr(reg,imm,imm_bits,instr,wait_times = 1,slot2_wait = False,slot3_wait = False):
    if slot2_wait:
        slot2_tail = get_queue_tail_index(3)
    else:
        slot2_tail = 0
    if slot3_wait:
        slot3_tail = get_queue_tail_index(3)
    else:
        slot3_tail = 0

    if instr in {"addc","addic","subc","subic"}:
        insert_control("0x0000") #清除进位

    if instr in {"addi","subi","addic","subic"}:
        imm1,imm2 = decompose_imm(imm_hex = imm,mode = instr,bit2=imm_bits)
        Rs = select_registers(
                mode="GR",
                method="RANDOM",
                reg_type="",
                index=0,
                used_regs = [key for key in recent_written_registers] + [reg]
        ) 

        
        insert_data_reg(Rs,imm1,wait_times=2)

        instr = f"{instr} {reg} {Rs} {imm2}"

        dep_list = update_slot_rely(mode="read",reg_list=[Rs]) #获取寄存器依赖
        dep_list[1] = slot2_tail
        dep_list[2] = slot3_tail

        enqueue_instruction(slot_queue = slot1_queue,inst_str = instr,dep_list=dep_list)

        slot1_tail = get_queue_tail_index(1)
        update_written_registers([reg], mode="write",slot_rely=[slot1_tail,0,0]) #更新已经使用过的寄存器
        update_recent_written_registers([reg], ttl=wait_times,allow_decrease=True)

    elif instr in {"add","sub","addc","subc","and","or","xor"}:

        imm1,imm2 = decompose_imm(imm_hex = imm,mode = instr,bit2=imm_bits)
        Rs,Rt = distribute_reg(reg1_set = False,reg2_set = False,reg1_bits = 32,reg2_bits = 32)
        while(Rs == Rt):
            Rs,Rt = distribute_reg(reg1_set = False,reg2_set = False,reg1_bits = 32,reg2_bits = 32)

        insert_data_reg(Rs,imm1,wait_times=1)
        insert_data_reg(Rt,imm2,wait_times=1)
        instr = f"{instr} {reg} {Rs} {Rt}"

        dep_list = update_slot_rely(mode="read",reg_list=[Rt,Rs]) #获取寄存器依赖
        enqueue_instruction(slot_queue = slot1_queue,inst_str = instr,dep_list=dep_list)

        slot1_tail = get_queue_tail_index(1)
        update_written_registers([reg], mode="write",slot_rely=[slot1_tail,0,0]) #更新已经使用过的寄存器
        update_recent_written_registers([reg], ttl=wait_times,allow_decrease=True)

    else:
        raise ValueError("不支持的指令类型")


# 通用的分配两个寄存器函数，主要用于load和store指令分配Rs和Rd
def distribute_reg(reg1_set = True,reg2_set = False,reg1_bits = 32,reg2_bits = 32,float = False):

    if not float:
        reg_type = "GR"
    else:
        reg_type = "FLOAT"

    used = [key for key, value in recent_written_registers.items() if value > 1]
    if reg1_set:
        Rd = update_written_registers(reg_list = used ,mode = "read",reg_type=reg_type) 
        if Rd == None:
            Rd = select_registers(
                mode="GR",
                method="RANDOM",
                reg_type="",
                index=0,
                used_regs = used
            )
            #给Rd寄存器赋值
            if not float:
                imm32 = generate_imm(bits=reg1_bits, low_zero=0)
                insert_data_reg(Rd,imm32,wait_times=5,slot2_wait=True,slot3_wait=True)
            else:
                imm32 = generate_float(bits=32)
                insert_data_reg(Rd,imm32,wait_times=5,mode="float",slot2_wait=True,slot3_wait=True)
    else:
        Rd = select_registers(
                mode="GR",
                method="RANDOM",
                reg_type="",
                index=0,
                used_regs = [key for key, value in recent_written_registers.items() if value > 1]
        )

#      if probability_return(0.8):
#           used = [Rd]
#      else:
#          used = []
    used = [Rd] + [key for key, value in recent_written_registers.items() if value > 1]

    if reg2_set :
        #避免rs和rd寄存器相同
        Rs= update_written_registers(reg_list = used,mode = "read",reg_type=reg_type) 
        if Rs == None:
            Rs = select_registers(
                mode="GR",
                method="RANDOM",
                reg_type="",
                index=0,
                used_regs = used
            )
            #给Rs寄存器赋值
            if not float:
                imm32 = generate_imm(bits=reg2_bits, low_zero=0)
                insert_data_reg(Rs,imm32,wait_times=5,slot2_wait=True,slot3_wait=True)
            else:
                imm32 = generate_float(bits=32)
                insert_data_reg(Rs,imm32,wait_times=5,mode="float",slot2_wait=True,slot3_wait=True)

    else:
        Rs = select_registers(
            mode="GR",
            method="RANDOM",
            reg_type="",
            index=0,
            #避免rs和rd寄存器相同
            used_regs = [key for key in recent_written_registers] + used
        )

    return Rd,Rs

#store数据进入某地址的函数
def store_data(data_reg,imm, base_reg = None,bit_width = 32):
    Rd = data_reg
    Rs = base_reg

    if base_reg == None:
        instr = f"storei{bit_width} {Rd} {imm}"
#          reg_list = [Rd]
    else:
        instr = f"store{bit_width} {Rd} {Rs} {imm}"
#          reg_list = [Rd,Rs]

    dep_list = update_slot_rely(mode="read",reg_list=[Rd,Rs])
    enqueue_instruction(slot_queue = slot3_queue,inst_str = instr,dep_list=dep_list)


#load某地址的函数
def load_data(data_reg,imm,base_reg = None,bit_width = 32):
    Rd = data_reg
    Rs = base_reg

    if base_reg == None:
        instr = f"loadi{bit_width} {Rd} {imm}"

    else:
        instr = f"load{bit_width} {Rd} {Rs} {imm}"

    slot1_tail = get_queue_tail_index(1)
    slot2_tail = get_queue_tail_index(2)
    slot3_tail = get_queue_tail_index(3)

    if data_reg != "GR31":
        update_written_registers(data_reg, mode="write",slot_rely=[0,slot2_tail,0]) #更新已经使用过的寄存器
        update_recent_written_registers(data_reg,ttl=3,allow_decrease=True)  # 设置倒计时

    enqueue_instruction(slot_queue = slot3_queue,inst_str = instr,dep_list=[slot1_tail,0,slot3_tail])

# 规范立即数的函数
def format_imm(imm, mode="unsigned", width=32, src_width=9):
    """
    将立即数格式化为给定位宽的十六进制字符串。
    - imm: 十六进制字符串(可带0x/下划线)或整数
    - mode: 'signed' 或 'unsigned'
    - width: 目标位宽（默认32）
    - src_width: 源位宽（用于符号扩展的基准；强烈建议显式传入）
    """
    if mode not in ("signed", "unsigned"):
        raise ValueError("mode 必须是 'signed' 或 'unsigned'")
    if not isinstance(width, int) or width <= 0:
        raise ValueError("width 必须为正整数")

    # 解析 imm -> value（Python int）
    if isinstance(imm, str):
        s = imm.strip().replace("_", "")
        if s.lower().startswith("0x"):
            s = s[2:]
        value = int(s or "0", 16)
        # 若未指定 src_width，字符串默认用其十六进制长度 * 4
        inferred_src_width = max(1, len(s) * 4) if s else 1
    elif isinstance(imm, int):
        value = imm
        # 若未指定 src_width，整数默认直接用目标位宽（更符合“我就想把它当成这个宽度的立即数”）
        inferred_src_width = width
    else:
        raise TypeError(f"imm 必须为 str 或 int，收到 {type(imm)}")

    if src_width is None:
        src_width = inferred_src_width

    if not isinstance(src_width, int) or src_width <= 0:
        raise ValueError("src_width 必须为正整数")

    # ===== 符号扩展（严格按 src_width 的最高位）=====
    if mode == "signed":
        sign_bit = (value >> (src_width - 1)) & 1
        if sign_bit:
            # 把 [src_width, width) 段全部置1
            value |= (~0) << src_width

    # 目标位宽截断
    mask = (1 << width) - 1
    value &= mask

    # 十六进制宽度：ceil(width/4)
    hex_len = (width + 3) // 4
    return f"{value:0{hex_len}X}"

# 配合扩展测试使用的分配寄存器
def decompose_imm(imm_hex, mode="add", bit2=11):
    """
    将32位立即数拆分为两个指定位数的立即数，使 imm1 <op> imm2 == imm_int
    使用insert_data函数时，如果不想用mov指令写入，需要分配成两个立即数的某种运算结果
    用来丰富指令搭配，顺便测一下bypass
    imm1 始终32位，imm2 只有 bit2 位。
    支持: add/addi, sub/subi, and, or, xor
    """
    if not (1 <= bit2 <= 32):
        raise ValueError("bit2 必须在 1..32 范围内")

    imm_int = int(imm_hex, 16) & 0xFFFFFFFF

    mask32 = 0xFFFFFFFF
    mask2  = (1 << bit2) - 1
    hex_width2 = (bit2 + 3) // 4

    if mode in ("add", "addi","addc", "addic"):
        imm2 = random.randint(0, mask2)
        # 如果 imm2 大于 bit2 位范围的一半（即超出正数范围），则将其视为负数
        if imm2 > 1 << (bit2 - 1):
            imm2_num = imm2 - (1 << bit2)
        else:
            imm2_num = imm2
        imm1 = (imm_int - imm2_num) & mask32

    elif mode in ("sub", "subi","subc", "subic"):
        imm2 = random.randint(0, mask2)
        # 如果 imm2 大于 bit2 位范围的一半（即超出正数范围），则将其视为负数
        if imm2 >= (1 << (bit2 - 1)):
            imm2_num = imm2 - (1 << bit2)
        else:
            imm2_num = imm2
        imm1 = (imm_int + imm2_num) & mask32
        # 因为 (imm1 - imm2) & 0xFFFFFFFF == imm_int

    elif mode == "xor":
        imm2 = random.randint(0, mask2)
        imm1 = (imm_int ^ imm2) & mask32
        # (imm1 ^ imm2) == imm_int

    elif mode == "and":
        # 可达性检查：imm2 高位为 0 ⇒ 结果高 bit2..31 必为 0
        if (imm_int & ~mask2) != 0:
            raise ValueError(f"AND 不可达：imm_int 高于 bit2 的位存在 1（bit2={bit2}）")

        # 令 imm2 至少覆盖 imm_int 的低 bit2 中所有 1 位（可再随机加一些补位）
        must_have = imm_int & mask2
        extra_can = (~imm_int) & mask2
        extra     = random.randint(0, extra_can)  # 只在 imm_int==0 的位上随机加 1
        imm2 = (must_have | extra) & mask2

        # 构造 imm1，使 (imm1 & imm2) == imm_int
        # 若 imm2 在某位为 1：只要 imm1 该位为 1，则结果可为 1；若 imm2 在某位为 0，则结果必为 0。
        # 经典构造：imm1 = imm_int | ~imm2 亦可，但写得更直观：
        imm1 = (imm_int | (~imm2 & mask32)) & mask32

    elif mode == "or":
        # 为了使 (imm1 | imm2) == imm_int，要求 imm2 只能在 imm_int 为 1 的低 bit2 位上取 1（不能引入新 1）
        imm_int_low = imm_int & mask2
        imm2 = random.randint(0, imm_int_low) & imm_int  # imm2 取 imm_int 低 bit2 的子集
        # 只要 imm2 是 imm_int 的子集，就可令 imm1 = imm_int（最简单的重构）
        imm1 = imm_int

        # 另一种等价写法也成立：imm1 = imm_int & ~imm2（但没必要）
        # imm1 = imm_int & (~imm2 & mask32)

    else:
        raise ValueError(f"无效模式: {mode}")

    return f"0x{imm1:08X}", f"0x{imm2:0{hex_width2}X}"


# 插入一个数到CR中
def insert_control(num = "0x0001"):
    Rd = select_registers(mode="GR",method="RANDOM",reg_type="",used_regs=recent_written_registers)
    insert_data_reg(reg = Rd,imm = num,wait_times = 1,slot2_wait = False,slot3_wait = False,mode = "unsigned")
    instr = f"movg2c {Rd}"
    enqueue_instruction(slot_queue = slot1_queue,inst_str = instr,dep_list=[get_queue_tail_index(1),0,0])
    
#检查进位是否被设置
def check_control():
    # 关闭CR_PRINT后，只输出五分之一的CR check，避免每一个CR检查的点的搭配都是movc2g

    if CR_PRINT or probability_return(0.2):
    # 因为控制寄存器的特性，控制寄存器写入之后要多几个周期才能读取
        nop(1,5)
        Rd = select_registers(mode="GR",method="RANDOM",reg_type="",used_regs=recent_written_registers)
        instr = f"movc2g {Rd}"

        enqueue_instruction(slot_queue = slot1_queue,inst_str = instr,dep_list=[get_queue_tail_index(1),0,0])
        update_recent_written_registers([Rd], ttl=5,allow_decrease=True)  # 设置倒计时

        insert_data_reg(Rd,"0x0001",wait_times=2,slot2_wait=False,slot3_wait=False,mode="unsigned") #临时指令，在修复ovf之前使用，避免错误传递影响测试
        insert_control("0x4000") #清除进位

def probability_return(probability):
    """
    按概率返回1或0
    
    :param probability: 返回1的概率 [0, 1)
    :return: 1（概率=probability）或0（概率=1-probability）
    """
    if probability < 0 or probability >= 1:
        raise ValueError("概率值需在0到1之间（含0不含1）")
    
    return 1 if random.random() < probability else 0
