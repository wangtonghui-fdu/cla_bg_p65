# 假设宏定义如下（使用十六进制形式）
# 处理指令寄存器和内存分配的函数(可能要针对不同芯片进行修改)

import random
import math
from config.config import MemoryConfig
from config.config import BASE_PC
from global_state.global_state import slot2_queue,slot3_queue
from tool.tool import enqueue_instruction, insert_data_reg,distribute_reg
from tool.tool import get_queue_tail_index

RAM_START = MemoryConfig.RAM_START
RAM_END = MemoryConfig.RAM_END

BANK_NUM = MemoryConfig.BANK_NUM
DATA_BLOCK_SIZE = MemoryConfig.DATA_BLOCK_SIZE


DATA_BLOCK = {
    "FLASH": [MemoryConfig.PERIPH_START, MemoryConfig.PERIPH_END],
    "RAM": (0,0),
}


# 全局字典（初始为空）
STACK_RANGE_DICT = {}
STACK_REG_DICT = {}


# 为每个函数分配一块内存，模拟调用函数的时候的存储临时数据栈
def add_function_range(function_name: str, num_range: tuple,reg_num = 1) -> None:
    """
    将函数名和对应的数字区间写入全局字典 STACK_RANGE_DICT
    
    Args:
        function_name: 函数名称（字符串）
        num_range: 数字区间（元组，如 (start, end)）
    """
    global STACK_RANGE_DICT  # 声明操作全局变量
    STACK_RANGE_DICT[function_name] = num_range
    STACK_REG_DICT[function_name] = reg_num

# 处理分配内存的函数，把部分寄存器（主要是GR31）的值存入地址中,但是还需要扩展
def handle_function_range(function_name,is_ret = False):
    if function_name in STACK_RANGE_DICT:
        begin_addr= STACK_RANGE_DICT[function_name][0]
        #预留，后续可以加入类似保留寄存器的操作
        reg_num = STACK_REG_DICT[function_name] 

        if not is_ret:
            _,Rs = distribute_reg()
            insert_data_reg(Rs,begin_addr,5)
            instr = f"store32 GR31 {Rs} 0x000"
            slot1_tail = get_queue_tail_index(1)
            slot2_tail = get_queue_tail_index(2)
            slot3_tail = get_queue_tail_index(3)
            enqueue_instruction(slot_queue = slot3_queue,inst_str = instr,dep_list=[slot1_tail,slot2_tail,slot3_tail])
        else:
            _,Rs = distribute_reg()
            insert_data_reg(Rs,begin_addr,5)
            instr = f"load32 GR31 {Rs} 0x000"
            slot1_tail = get_queue_tail_index(1)
            slot2_tail = get_queue_tail_index(2)
            slot3_tail = get_queue_tail_index(3)
            enqueue_instruction(slot_queue = slot2_queue,inst_str = instr,dep_list=[slot1_tail,slot2_tail,slot3_tail])

    

# 根据指令数量，确定有指令占用了哪些ram块 
def calc_data_region(instruction_count: int):
    """
    根据指令数量计算被指令占用的块数，并返回允许 data 存放的地址范围（首尾地址）
    """
    INSN_SIZE = 4  # 每条指令 4 字节
    total_ram_bytes = BANK_NUM * DATA_BLOCK_SIZE

    # 计算指令总大小（字节）
    insn_bytes = instruction_count * INSN_SIZE + RAM_START

    # 计算占用了多少个块（向上取整）
    used_blocks = (BASE_PC + insn_bytes + DATA_BLOCK_SIZE - 1) // DATA_BLOCK_SIZE

    if used_blocks >= BANK_NUM:
        return 0 , 0

    # 可用的首块 index = used_blocks
    data_start_addr = used_blocks * DATA_BLOCK_SIZE
    data_end_addr = total_ram_bytes - 1

    print(f"指令共 {instruction_count} 条，BASE_PC = 0x{BASE_PC:08X} 共占用 {used_blocks} 个块")
    print(f"可用于 data 的地址范围：0x{data_start_addr:08X} ~ 0x{data_end_addr:08X}")

    return data_start_addr, data_end_addr

# 产生store用的地址，地址使用范围在ram的区间，同时避开函数的保留栈
def generate_memory_imm(bit_width, low_zero=0, need_base=True, imm_width=9, MR=0):
    """
    分配地址空间给加载/存储指令用，因为是随机测试器，不用sp指针分配内存空间
    后续可以考虑引入用sp分配内存的版本
    
    Args:
        bit_width: 加载存储指令的bit长度
        low_zero: 低几位为0
        imm_width: 立即数位数
        immMR: MR大小，loado指令和storeo指令防止内存访问越界,也可以用来分配一段内存空间
    """

    # 获取地址范围
    if DATA_BLOCK["RAM"] == (0, 0):
        addr_start, addr_end = DATA_BLOCK["FLASH"]
    else:
        addr_start, addr_end = DATA_BLOCK["RAM"]

    # 最大尝试次数（避免无限循环）
    max_attempts = 1000
    attempts = 0
    offset = 0  # 需要在此处定义 offset

    # 计算偏移量（根据 bit_width）
    if bit_width in (8, 16, 32):  # 确保 bit_width 是合法值
        offset = int(math.log2(bit_width // 8))
    else:
        raise ValueError("bit_width 必须是 8、16 或 32")

    imm_base = 0
    imm = 0
    imm_signed = 0  # 偏移的“有符号”真值，用于按硬件语义计算地址

    while attempts < max_attempts:
        attempts += 1

        # 生成 imm_base，并确保其低位有 low_zero 个 0
        imm_base = 0
        imm = 0
        imm_signed = 0
        if need_base:
            imm_base = random.randint(addr_start, addr_end - 4 * MR)
            imm_base = (imm_base >> low_zero) << low_zero  # 强制低位清零
            if MR:
                # loado/storeo：返回的 imm 偏移用不上（BAR 间接寻址），保留原正向探针
                imm = random.randint(0, 2 ** imm_width - 1)
                imm_signed = imm
            else:
                # 普通 load/store：硬件把这 imm_width 位偏移当“有符号补码”解释
                # （如 9 位 -> [-256, 255]）。必须按有符号生成、并用有符号值做范围检查，
                # 否则生成器以为是 +imm、硬件却当成负偏移，地址会跌出数据区（见 Bug：基址
                # 近数据区底部时负偏移下溢到代码段）。imm 存为补码位段供汇编器编码。
                imm_signed = random.randint(-(1 << (imm_width - 1)), (1 << (imm_width - 1)) - 1)
                imm = imm_signed & ((1 << imm_width) - 1)
        else:
            # 不需要基地址时，imm_base 固定为 0
            imm_base = 0
            imm = random.randint(addr_start >> offset, addr_end >> offset)
            imm_signed = imm
            if addr_start >> offset > 2 ** imm_width - 1:
                return "0x0000","0x0000"

        # 计算最终地址（用有符号偏移，匹配硬件行为）
        final_addr = imm_base + (imm_signed << offset)
        # mr = memory renge，相对于分配内存段的范围
        final_addr_mr = imm_base + MR
        start_addr_mr = imm_base - MR

        max_addr = max(final_addr, final_addr_mr)

        # 检查是否越界（主内存范围）
        if not (max_addr < addr_end and final_addr >= addr_start):
            continue  # 越界，重新生成

        # 仅当 STACK_RANGE_DICT 非空时检查栈冲突
        if STACK_RANGE_DICT:  # 字典非空时进入检查
            conflict_with_stack = False
            for stack_start, stack_end in STACK_RANGE_DICT.values():
                if stack_start <= final_addr <= stack_end:
                    conflict_with_stack = True
                    break
                if MR !=0:
                    if max(stack_start, start_addr_mr) <= min(stack_end, final_addr_mr):
                        conflict_with_stack = True
                        break

            if conflict_with_stack:
                continue  # 冲突，重新生成

        # 通过所有检查，返回结果
        return f"0x{imm_base:X}", f"0x{imm:0{(imm_width + 3) // 4}X}"

    # 超过最大尝试次数仍未找到合法地址（理论上不应发生）
    raise ValueError(f"无法生成合法的内存地址，请检查输入参数或内存范围配置\n base = {imm_base} imm = {imm}")


MEMORY_RANGE_DICT = []
def write_memory_range_dict(addr_range, data_type = [int], is_range = False, range_num = 0,rs_num = 0, mr_num = 0, off_num = 0, bar_num = 0, bit_width = 32):
    """
    向MEMORY_RANGE_DICT数组中写入数据
    
    Args:
        MEMORY_RANGE_DICT: 目标数组
        其他参数为要写入的结构体字段值
    """
    # 创建新条目
    new_entry = {
        'addr_range': addr_range,
        'data_type': data_type,
        'is_range': is_range,
        'range_num': range_num,
        'rs_num': rs_num,
        'mr_num': mr_num,
        'off_num': off_num,
        'bar_num': bar_num,
        'bit_width': bit_width
    }
    # 添加到数组
    MEMORY_RANGE_DICT.append(new_entry)
