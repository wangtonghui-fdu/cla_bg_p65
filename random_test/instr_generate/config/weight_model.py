class LOAD_WEIGHT:
    MAX_LOAD_WEIGHT = 5

    load_instr_weight  = {
        "load8": MAX_LOAD_WEIGHT,
        "load16": 4,
        "load32": 3,

        "loadu8": MAX_LOAD_WEIGHT,
        "loadu16": 4,
        "loadu32": 3,
 
        "loado16": 2,
        "loado32": 1,

        "loadi8": MAX_LOAD_WEIGHT,
        "loadi16": 4,
        "loadi32": 3,

        "random": 0,  # 特殊标记
        "random2": 0# 特殊标记
    }

class STORE_WEIGHT:
    MAX_STORE_WEIGHT = 5

    store_instr_weight= {
         "store8": MAX_STORE_WEIGHT,
         "store16": 4,
         "store32": 3,

         "storeu8": MAX_STORE_WEIGHT,
         "storeu16": 4,
         "storeu32": 3,

         "storeo16": 2,
         "storeo32": 1,

         "storei8": MAX_STORE_WEIGHT,
         "storei16": 4,
         "storei32": 3,

        "random": 0,  # 特殊标记
        "random3": 0# 特殊标记
    }


class SLOT1_WEIGHT:
    # 定义权重宏
    MAX_SLOT1_WEIGHT = 10

    MOV_WEIGHT = 2 
    IMMEDIATE_ALU_WEIGHT = 10 
    COMPARE_ALU_WEIGHT = 10 

    CR_ALU_WEIGHT = 10

    REGISTER_ALU_WEIGHT = 8
    MULTIPLY_WEIGHT = 10
    SHIFT_WEIGHT = 6
    UNARY_ALU_WEIGHT = 5
    TEST_BIT_WEIGHT = 7
    BITFIELD_WEIGHT = 5
    MAC_WEIGHT = 10
    SPECIAL_WEIGHT = 0
    TMU_WEIGHT = 5 
    VCU_WEIGHT = 5
    FINTDIV_WEIGHT = 7
    
    mov_instr_weight = {
        "movigh": MOV_WEIGHT,
        "movigl": MOV_WEIGHT,
        "moviglz": MOV_WEIGHT,
        "moviglx": MOV_WEIGHT,
        "movg2g": MOV_WEIGHT,
        # 这两个的测试通过其他指令完成
        # "movg2c": MOV_WEIGHT,
        # "movc2g": MOV_WEIGHT,
    }
    
    alu_compare_instr_weight = {
        "eqi": COMPARE_ALU_WEIGHT,
        "neqi": COMPARE_ALU_WEIGHT,
        "eqiu": COMPARE_ALU_WEIGHT,
        "neqiu": COMPARE_ALU_WEIGHT,
    
        "gti": COMPARE_ALU_WEIGHT,
        "lti": COMPARE_ALU_WEIGHT,
        "gtiu": COMPARE_ALU_WEIGHT,
        # Temporarily disable in BG random tests: ltiu immediate encoding can
        # terminate task8 early before BG coverage is understood.
        "ltiu": COMPARE_ALU_WEIGHT,
    
        "gei": COMPARE_ALU_WEIGHT,
        "lei": COMPARE_ALU_WEIGHT,
        "leiu": COMPARE_ALU_WEIGHT,
        "geiu": COMPARE_ALU_WEIGHT,
    
        "eq": COMPARE_ALU_WEIGHT,
        "neq": COMPARE_ALU_WEIGHT,
        "equ": COMPARE_ALU_WEIGHT,
        "nequ": COMPARE_ALU_WEIGHT,
    
        "gt": COMPARE_ALU_WEIGHT,
        "lt": COMPARE_ALU_WEIGHT,
        "gtu": COMPARE_ALU_WEIGHT,
        "ltu": COMPARE_ALU_WEIGHT,
    
        "ge": COMPARE_ALU_WEIGHT,
        "le": COMPARE_ALU_WEIGHT,
        "geu": COMPARE_ALU_WEIGHT,
        "leu": COMPARE_ALU_WEIGHT,
    }
    
    alu_calculate_instr_weight = {
        # === 立即数型 ALU ===
        "addi": CR_ALU_WEIGHT,
        "addic": CR_ALU_WEIGHT,
        "subi": CR_ALU_WEIGHT,
        "subic": CR_ALU_WEIGHT,
        "sli": CR_ALU_WEIGHT,
        "srli": CR_ALU_WEIGHT,
        "srai": CR_ALU_WEIGHT,
    
        # === 寄存器型 ALU（二/三操作数）===
        "add": CR_ALU_WEIGHT,
        "addc": CR_ALU_WEIGHT,
        "sub": CR_ALU_WEIGHT,
        "subc": CR_ALU_WEIGHT,

        "and": REGISTER_ALU_WEIGHT,
        "or": REGISTER_ALU_WEIGHT,
        "xor": REGISTER_ALU_WEIGHT,
        "max": REGISTER_ALU_WEIGHT,
        "min": REGISTER_ALU_WEIGHT,
    
        # 乘法
        "mul32": MULTIPLY_WEIGHT,
        "mulu32": MULTIPLY_WEIGHT,
        "mul64": MULTIPLY_WEIGHT,
        "mulu64": MULTIPLY_WEIGHT,
    
        # 移位（寄存器型）
        "sl64": SHIFT_WEIGHT,
        "sra64": SHIFT_WEIGHT,
        "srl64": SHIFT_WEIGHT,
        "sl": SHIFT_WEIGHT,
        "sra": SHIFT_WEIGHT,
        "srl": SHIFT_WEIGHT,
    
        # === 一元 ALU ===
        "not": UNARY_ALU_WEIGHT,
        "abs": UNARY_ALU_WEIGHT,
        "cbw": UNARY_ALU_WEIGHT,
        "chw": UNARY_ALU_WEIGHT,
        "neg64": UNARY_ALU_WEIGHT,
        "sat64": UNARY_ALU_WEIGHT,
    
        # === 测试/位操作/选择/标志 ===
        "test": TEST_BIT_WEIGHT,
        "testi": TEST_BIT_WEIGHT,
        "bclr": TEST_BIT_WEIGHT,
        "select": TEST_BIT_WEIGHT,
        "setc": TEST_BIT_WEIGHT,
    
        # 位域
        "bfext": BITFIELD_WEIGHT,
        "bfextu": BITFIELD_WEIGHT,
        "bfst": BITFIELD_WEIGHT,
    
        # === MAC 系列 ===
        "mac16": MAC_WEIGHT,
        "macu16": MAC_WEIGHT,
        "mac32": MAC_WEIGHT,
        "macu32": MAC_WEIGHT,
        "mac64": MAC_WEIGHT,
        "macu64": MAC_WEIGHT,
    }

    tmu_instr_weight = {
        "mpy2pif32": TMU_WEIGHT,
        "div2pif32": TMU_WEIGHT,
        "sinpuf32": TMU_WEIGHT,
        "cospuf32": TMU_WEIGHT,
        "atanpuf32": TMU_WEIGHT,
        "quadf": TMU_WEIGHT,
    }

    vcu_instr_weight = {
        "vcrc8ll": VCU_WEIGHT,
        "vcrc8lh": VCU_WEIGHT,
        "vcrc8hl": VCU_WEIGHT,
        "vcrc8hh": VCU_WEIGHT,
        "vcrc16p1ll": VCU_WEIGHT,
        "vcrc16p1lh": VCU_WEIGHT,
        "vcrc16p1hl": VCU_WEIGHT,
        "vcrc16p1hh": VCU_WEIGHT,
        "vcrc16p2ll": VCU_WEIGHT,
        "vcrc16p2lh": VCU_WEIGHT,
        "vcrc16p2hl": VCU_WEIGHT,
        "vcrc16p2hh": VCU_WEIGHT,
        "vcrc32ll": VCU_WEIGHT,
        "vcrc32lh": VCU_WEIGHT,
        "vcrc32hl": VCU_WEIGHT,
        "vcrc32hh": VCU_WEIGHT,
    }
    fintdiv_instr_weight = {
        "absi32div32": FINTDIV_WEIGHT,
        "absi32div32u": FINTDIV_WEIGHT,
        "absi64div32": FINTDIV_WEIGHT,
        "absi64div32u": FINTDIV_WEIGHT,
        "absi64div64": FINTDIV_WEIGHT,
        "absi64div64u": FINTDIV_WEIGHT,
        "negi32div32": FINTDIV_WEIGHT,
        "negi64div32": FINTDIV_WEIGHT,

        "negi64div64": FINTDIV_WEIGHT,
        "mnegi32div32": FINTDIV_WEIGHT,
        "mnegi64div32": FINTDIV_WEIGHT,
        "mnegi64div64": FINTDIV_WEIGHT,
        "subc4ui32": FINTDIV_WEIGHT,

        "subc2ui64": FINTDIV_WEIGHT,
        "enegi32div32": FINTDIV_WEIGHT,
        "enegi64div64": FINTDIV_WEIGHT,
        "enegi64div32": FINTDIV_WEIGHT,
        "mnegi32div32": FINTDIV_WEIGHT,

        "mnegi64div64": FINTDIV_WEIGHT,
        "mnegi64div32": FINTDIV_WEIGHT,
    }
        



    
    # 特殊标记
    store_instr_weight = {
        "random": 0,
        "random3": 0,
    }
