class I2C_Config:
    # I2C 配置序列

    
    FIFO_ADDR = 0x108201C
    MIN_TIMES = 10
    MAX_TIMES = 100
# 名字数组（中文注释）
    I2C_REG = [
        "I2C_O_MDR",           # 禁用模块
        "I2C_O_PSC",           # 设置模块时钟预分频器
        "I2C_O_CLKH",          # 设置SCL高电平时间分频器
        "I2C_O_CLKL",          # 设置SCL低电平时间分频器
        "I2C_O_MDR",           # 写入模式寄存器选项
        "I2C_O_OAR",           # 设置自身地址
        "I2C_O_TAR",           # 设置目标地址
        "I2C_O_MDR",           # 确认模式配置
        "I2C_O_FFTX",          # 设置TX FIFO中断级别
        "I2C_O_FFRX",          # 设置RX FIFO中断级别
        "I2C_O_IER",           # 禁用基本中断
        "I2C_O_MDR",           # 启用前最终配置
        "PIE_O_IER",           # 启用PIE中断
        "I2C_O_MDR"            # 启用模块并设置START条件
    ]
    
    # 配置字典（中文注释放在value上）
    I2C_REG_CONFIG = {
        "I2C_O_MDR": {
            'addr': "0x1082024",
            'value': "0x2EA0"  # 禁用模块
        },
        "I2C_O_PSC": {
            'addr': "0x1082030", 
            'value': "0x9"  # 设置模块时钟预分频器
        },
        "I2C_O_CLKH": {
            'addr': "0x1082010",
            'value': "0xFFFF"  # 设置SCL高电平时间分频器
        },
        "I2C_O_CLKL": {
            'addr': "0x108200C",
            'value': "0x6"  # 设置SCL低电平时间分频器
        },
        "I2C_O_MDR": {
            'addr': "0x1082024",
            'value': "0x26A0"  # 写入模式寄存器选项
        },
        "I2C_O_OAR": {
            'addr': "0x1082000",
            'value': "0x10"  # 设置自身地址
        },
        "I2C_O_TAR": {
            'addr': "0x108201C",
            'value': "0x50"  # 设置目标地址
        },
        "I2C_O_MDR": {
            'addr': "0x1082024",
            'value': "0x26A0"  # 确认模式配置
        },
        "I2C_O_FFTX": {
            'addr': "0x1082034",
            'value': "0x6080"  # 设置TX FIFO中断级别
        },
        "I2C_O_FFRX": {
            'addr': "0x1082038",
            'value': "0x202F"  # 设置RX FIFO中断级别
        },
        "I2C_O_IER": {
            'addr': "0x1082004",
            'value': "0x0"  # 禁用基本中断
        },
        "I2C_O_MDR": {
            'addr': "0x1082024",
            'value': "0x26A0"  # 启用前最终配置
        },
        "PIE_O_IER": {
            'addr': "0x7F0104",
            'value': "0x4080"  # 启用PIE中断
        },
        "I2C_O_MDR": {
            'addr': "0x1082024",
            'value': "0x26A0"  # 启用模块并设置START条件
        }
    }
        
