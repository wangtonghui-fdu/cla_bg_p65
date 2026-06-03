import random
from typing import Tuple
from config.config import JmpConfig
from tool.ram import add_function_range, generate_memory_imm
from global_state.global_state import clearRegsiter

# ======================
# 全局宏定义
# ======================
JMP_DEBUG = JmpConfig.JMP_DEBUG #输出信息
# 函数名称列表（可在此处修改）
START_PART = JmpConfig.START_PART
FINISH_PART = JmpConfig.FINISH_PART
MAIN_PART = JmpConfig.MAIN_PART
FUNCTION_PART = JmpConfig.FUNCTION_PART

FUNCTION = JmpConfig.FUNCTION
FUNCTION_NAMES = [f"{FUNCTION_PART}_{name}" for name in FUNCTION]

CALL_MAX_FREQUENCY = JmpConfig.CALL_MAX_FREQUENCY
CALL_MIN_FREQUENCY = JmpConfig.CALL_MIN_FREQUENCY

# 内存布局顺序（可在此处修改）
# 选项: "start", "finish", "main", "function"
MEMORY_LAYOUT_ORDER = JmpConfig.MEMORY_LAYOUT_ORDER

# 全局指令映射
instruction_map = {}

# 比例常量
START_MIN_PERCENT = JmpConfig.START_MIN_PERCENT
START_MAX_PERCENT = JmpConfig.START_MAX_PERCENT
FINISH_MIN_PERCENT = JmpConfig.FINISH_MIN_PERCENT
FINISH_MAX_PERCENT = JmpConfig.FINISH_MAX_PERCENT
MAIN_MIN_PERCENT = JmpConfig.MAIN_MIN_PERCENT
FUNCTION_MIN_PERCENT = JmpConfig.FUNCTION_MIN_PERCENT  # 每个函数最小占用比例
FUNCTION_MAX_PERCENT = JmpConfig.FUNCTION_MAX_PERCENT    # 每个函数最大占用比例
FUNCTION_TOTAL_MAX_PERCENT = JmpConfig.FUNCTION_TOTAL_MAX_PERCENT


# ======================;
# 生成指令映射
# ======================

def devide_instr(instr_num: int):
    """
    生成指令映射并存储在全局变量中
    
    参数:
        instr_num: 总指令数
    """
    global instruction_map
    
    # 1. 计算各部分大小
    start_size = random.randint(int(instr_num * START_MIN_PERCENT), int(instr_num * START_MAX_PERCENT))
    finish_size = random.randint(int(instr_num * FINISH_MIN_PERCENT), int(instr_num * FINISH_MAX_PERCENT))
    
    # 2. 计算剩余指令数
    remaining = instr_num - start_size - finish_size
    
    # 3. 计算函数部分总大小（不超过剩余的60%）
    max_function_total = min(int(remaining * FUNCTION_TOTAL_MAX_PERCENT), 
                            len(FUNCTION_NAMES) * int(instr_num * FUNCTION_MAX_PERCENT))
    function_total = random.randint(0, max_function_total)
    
    # 4. 计算main部分大小（至少40%）
    main_size = max(int(instr_num * MAIN_MIN_PERCENT), remaining - function_total)
    
    # 5. 调整函数总大小
    function_total = remaining - main_size
    
    # 6. 为每个函数分配大小（确保每个函数至少占用最小比例）
    function_sizes = {}
    remaining_function = function_total
    
    # 首先为每个函数分配最小大小
    min_size_per_function = max(1, int(instr_num * FUNCTION_MIN_PERCENT))
    for name in FUNCTION_NAMES:
        function_sizes[name] = min_size_per_function
        remaining_function -= min_size_per_function
    
    # 如果剩余空间不足，调整最小大小
    if remaining_function < 0:
        # 按比例缩减每个函数的最小大小
        scale_factor = function_total / (min_size_per_function * len(FUNCTION_NAMES))
        min_size_per_function = max(1, int(min_size_per_function * scale_factor))
        for name in FUNCTION_NAMES:
            function_sizes[name] = min_size_per_function
        remaining_function = function_total - (min_size_per_function * len(FUNCTION_NAMES))
    
    # 为每个函数分配剩余空间（除了最后一个）
    for name in FUNCTION_NAMES[:-1]:
        if remaining_function <= 0:
            break
            
        # 计算该函数可分配的最大大小
        max_size = min(int(instr_num * FUNCTION_MAX_PERCENT) - function_sizes[name], remaining_function)
        if max_size > 0:
            # 随机分配额外大小
            extra_size = random.randint(0, max_size)
            function_sizes[name] += extra_size
            remaining_function -= extra_size
    
    # 最后一个函数获得所有剩余空间
    if remaining_function > 0:
        function_sizes[FUNCTION_NAMES[-1]] += remaining_function
    
    # 给每个函数分配栈空间
    allocate_stack()
    # 7. 计算索引（按照内存布局顺序）
    current_index = 0
    
    # 按照内存布局顺序分配索引
    for section in MEMORY_LAYOUT_ORDER:
        if section == START_PART:
            instruction_map[START_PART] = current_index
            instruction_map[f"{START_PART}_end"] = current_index + start_size - 1
            current_index += start_size
        elif section == FINISH_PART:
            instruction_map[FINISH_PART] = current_index
            instruction_map[f"{FINISH_PART}_end"] = current_index + finish_size - 1
            current_index += finish_size
        elif section == MAIN_PART:
            instruction_map[MAIN_PART] = current_index
            instruction_map[f"{MAIN_PART}_end"] = current_index + main_size - 1
            current_index += main_size
        elif section == FUNCTION_PART:
            for name in FUNCTION_NAMES:
                size = function_sizes[name]
                if size > 0:
                    instruction_map[name] = current_index
                    instruction_map[f"{name}_end"] = current_index + size - 1
                    current_index += size
    

    # 8. 在所有段中生成函数调用点（main + 各函数段）

    call_host_sections = []
    for key in instruction_map:
        if not key.endswith("_end") and key not in [START_PART, FINISH_PART]:
            section_start = instruction_map[key]
            section_end = instruction_map[f"{key}_end"]
            call_host_sections.append((key, section_start, section_end))

    defined_functions = []
    call_points = []

    for section_name, section_start, section_end in call_host_sections:
        max_calls = (section_end - section_start + 1) // CALL_MAX_FREQUENCY
        min_calls = (section_end - section_start + 1) // CALL_MIN_FREQUENCY
        num_calls = random.randint(min_calls, max_calls)

        for _ in range(num_calls):
            # 只能调用已定义过的函数，且不能调用自己
            candidates = [f for f in defined_functions if f != section_name]
            if candidates:
                target_func = random.choice(candidates)
                call_index = random.randint(section_start, section_end)
                call_points.append((call_index, target_func))

        if section_name in FUNCTION_NAMES:
            defined_functions.append(section_name)
    
    # 按指令索引排序调用点
    call_counts = {}
    for call_index, name in sorted(call_points, key=lambda x: x[0]):
        call_counts[name] = call_counts.get(name, 0) + 1
        if call_counts[name] == 1:
            key = f"call_{name}"
        else:
            key = f"call_{name}_{call_counts[name]}"
        instruction_map[key] = call_index
    
    # 打印开始和结束部分（调试用）
    if JMP_DEBUG:
        print_start_end_info(instr_num)
    count = 0
    for name in call_counts:
         count += call_counts[name]
         print("调用点：",name,"调用次数:",call_counts[name] )
    print("调用点总数:",count)

# ======================
# 核心函数2：检查并标记点
# ======================
def check_and_mark_point(instr_num: int) -> Tuple[str, bool]:
    """
    检查当前指令数是否超过某个点，找出所有被超过的点中指令索引最小的点，
    标记为已使用并返回该点名称和True
    这个函数是在产生指令的过程中，插入各种标志位用的
    
    参数:
        instr_num: 当前指令数
    
    返回:
        (点名称, 是否触发) 元组
    """
    global instruction_map
    
    # 定义检查顺序（按执行顺序）
    point_order = [
        START_PART, f"{START_PART}_end",
        *FUNCTION_NAMES,
        *[f"{name}_end" for name in FUNCTION_NAMES],
        MAIN_PART, f"{MAIN_PART}_end",
        FINISH_PART, f"{FINISH_PART}_end",
        *[key for key in instruction_map if key.startswith("call_")]
    ]
    
    # 找出所有被超过且未使用的点
    candidate_points = []
    
    for point in point_order:
        # 跳过不存在的点
        if point not in instruction_map:
            continue
            
        # 检查是否已使用
        if f"used_{point}" in instruction_map:
            continue
            
        # 检查当前指令数是否超过该点
        if instr_num >= instruction_map[point]:
            candidate_points.append((point, instruction_map[point]))
    
    # 如果没有符合条件的点
    if not candidate_points:
        return "", False
    
    # 找出指令索引最小的点
    min_point = min(candidate_points, key=lambda x: x[1])
    point_name = min_point[0]
    
    # 标记为已使用
    instruction_map[f"used_{point_name}"] = True
    
    # 返回点名称和触发标志
    if point_name in FUNCTION_NAMES:
        print("进入函数：",point_name)
        clearRegsiter()

    return point_name, True

# ======================
# 分配每一个函数的内存空间，用来保留信息
# ======================
def allocate_stack():
    """
    分配内存空间用，目前指令生成器暂时不使用sp管理空间，后续可以引入这个操作
    """
    for name in FUNCTION_NAMES:
    # 随机生成需要存入栈的寄存器数量 
        reg_num = random.randint(1,5)
        imm_begin,_ = generate_memory_imm(bit_width=32,low_zero=2,need_base=True,imm_width=0,MR=(reg_num - 1) * 4)
        imm_begin = int(imm_begin,16)
        add_function_range(function_name=name,num_range=(imm_begin,imm_begin),reg_num = reg_num)

# ======================
# 内置调试函数：打印开始和结束部分信息
# ======================

def print_start_end_info(total_instructions: int):
    """
    打印开始和结束部分的信息（调试用）
    
    参数:
        total_instructions: 总指令数
    """
    global instruction_map
    
    print("\n===== 开始和结束部分信息 =====")
    print(f"内存布局顺序: {MEMORY_LAYOUT_ORDER}")
    
    # start部分
    start = instruction_map[START_PART]
    start_end = instruction_map[f"{START_PART}_end"]
    start_size = start_end - start + 1
    print(f"{START_PART}: [{start}-{start_end}] ({start_size}条指令, {start_size/total_instructions*100:.1f}%)")
    
    # finish部分
    finish = instruction_map[FINISH_PART]
    finish_end = instruction_map[f"{FINISH_PART}_end"]
    finish_size = finish_end - finish + 1
    print(f"{FINISH_PART}: [{finish}-{finish_end}] ({finish_size}条指令, {finish_size/total_instructions*100:.1f}%)")
    
    # main部分
    main = instruction_map[MAIN_PART]
    main_end = instruction_map[f"{MAIN_PART}_end"]
    main_size = main_end - main + 1
    print(f"{MAIN_PART}: [{main}-{main_end}] ({main_size}条指令, {main_size/total_instructions*100:.1f}%)")
    
    # 函数部分
    print("\n函数部分:")
    for name in FUNCTION_NAMES:
        if name in instruction_map:
            func_start = instruction_map[name]
            func_end = instruction_map[f"{name}_end"]
            func_size = func_end - func_start + 1
            print(f"{name}: [{func_start}-{func_end}] ({func_size}条指令, {func_size/total_instructions*100:.1f}%)")
    
    # 调用点（按顺序排列）
    print("\n调用点（按指令索引排序）:")
    call_points = []
    for key, value in instruction_map.items():
        if key.startswith("call_"):
            # 提取函数名称
            parts = key.split("_")
            function_name = "_".join(parts[1:-1]) if len(parts) > 2 else parts[1]
            call_points.append((value, key, function_name))
    
    # 按指令索引排序
    call_points.sort(key=lambda x: x[0])
    
    # 打印调用点
    for index, key, function_name in call_points:
        print(f"指令 {index}: {key} (调用 {function_name})")
    
    print("=" * 40)

