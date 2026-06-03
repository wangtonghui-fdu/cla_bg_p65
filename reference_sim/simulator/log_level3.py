import re
import sys

log_file_path = sys.argv[1]
output_file_path = 'gr_trace.txt'

write_pattern = re.compile(r'^write gr(\d+)\s*=\s*0x([0-9a-fA-F]+)')
pc_pattern = re.compile(r'PC\s*=\s*0x([0-9a-fA-F]+)')

def to_signed(value, bit_width=32):
    """将无符号数转换为有符号数（二进制补码解析）"""
    if value >= (1 << (bit_width - 1)):
        return value - (1 << bit_width)
    return value

with open(log_file_path, 'r', encoding='utf-8') as log_file, \
        open(output_file_path, 'w', encoding='utf-8') as output_file:

    lines = log_file.readlines()
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        match = write_pattern.match(line)

        if match:
            reg_num = int(match.group(1))
            if reg_num in (30, 31):
                i += 1
                continue  # 跳过 gr30 和 gr31

            value = int(match.group(2), 16)

            # 向下查找第一个 PC = 0x... 行
            pc_val = None
            for j in range(i + 1, len(lines)):
                pc_match = pc_pattern.search(lines[j])
                if pc_match:
                    pc_val = int(pc_match.group(1), 16)
                    break

            # 格式化输出
            if reg_num >= 0 and reg_num < 32 and pc_val is not None:
                output_line = (
                    f"0x{reg_num:02x}(GR{reg_num:<2d})    "
#                      f"0x{pc_val:08x}   "
                    f"0x{value:08x}({to_signed(value):11d})\n"
                )
                output_file.write(output_line)

        i += 1

