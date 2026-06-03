import random

from slot1.mov import *
from slot1.alu_compare import *
from slot1.alu_calculate import *
from peripheral.I2C import generate_i2c_instr 

from tmu.tmu import *
from vcu.vcu import *
from fintdiv.fintdiv import *
from config.config import TestConfig,ClaConfig
from config.weight_model import SLOT1_WEIGHT
from tool.tool import probability_return 

TEST_CLA = TestConfig.TEST_CLA
CR_MODEL = TestConfig.CR_MODEL

#权重模式配置
WEIGHT_MODE = TestConfig.WEIGHT_MODE
MAX_SLOT1_WEIGHT = SLOT1_WEIGHT.MAX_SLOT1_WEIGHT
mov_instr_weight = SLOT1_WEIGHT.mov_instr_weight
alu_compare_instr_weight = SLOT1_WEIGHT.alu_compare_instr_weight
alu_calculate_instr_weight = SLOT1_WEIGHT.alu_calculate_instr_weight
tmu_instr_weight = SLOT1_WEIGHT.tmu_instr_weight
vcu_instr_weight = SLOT1_WEIGHT.vcu_instr_weight
fintdiv_instr_weight = SLOT1_WEIGHT.fintdiv_instr_weight

TEST_TMU = TestConfig.TMU_TEST
TEST_VCU = TestConfig.VCU_TEST
TEST_I2C = TestConfig.I2C_TEST
TEST_FINTDIV = TestConfig.FINTDIV_TEST
CLA_NOT_SUPPORT_ALU = ClaConfig.CLA_NOT_SUPPORT_ALU
CLA_NOT_SUPPORT_MOV = ClaConfig.CLA_NOT_SUPPORT_MOV

CLA_NOT_SUPPORT_SLOT1 = CLA_NOT_SUPPORT_MOV + CLA_NOT_SUPPORT_ALU
mov_instr_map = {
#          "movigh": generate_movigh,
#          "movigl": generate_movigl,
        "moviglz": generate_moviglz,
        "moviglx": generate_moviglx,
        "movg2g": generate_movg2g,
        #这两个的测试通过其他指令完成
#          "movg2c": generate_movg2c,
#          "movc2g": generate_movc2g,
    }

alu_compare_instr_map = {
        "eqi" : generate_eqi,
        "neqi" : generate_neqi,
        "eqiu" : generate_eqiu,
        "neqiu" : generate_neqiu,

        "gti" : generate_gti,
        "lti" : generate_lti,
        "gtiu" : generate_gtiu,
        "ltiu" : generate_ltiu,

        "gei" : generate_gei,
        "lei" : generate_lei,
        "leiu" : generate_leiu,
        "geiu" : generate_geiu,

        "eq" : generate_eq,
        "neq" : generate_neq,
        "equ" : generate_equ,
        "nequ" : generate_nequ,

        "gt" : generate_gt,
        "lt" : generate_lt,
        "gtu" : generate_gtu,
        "ltu" : generate_ltu,

        "ge" : generate_ge,
        "le" : generate_le,
        "geu" : generate_geu,
        "leu" : generate_leu,
    }

alu_calculate_instr_map = {
        # === 立即数型 ALU ===
        "addi":  generate_addi,
        "addic": generate_addic,
        "subi":  generate_subi,
        "subic": generate_subic,
        "sli":   generate_sli,
        "srli":  generate_srli,
        "srai":  generate_srai,

        # === 寄存器型 ALU（二/三操作数）===
        "add":   generate_add,
        "addc":  generate_addc,
        "sub":   generate_sub,
        "subc":  generate_subc,
        "and":   generate_and,
        "or":    generate_or,
        "xor":   generate_xor,
        "max":   generate_max,
        "min":   generate_min,

        # 乘法
        "mul32":  generate_mul32,
        "mulu32": generate_mulu32,
        "mul64":  generate_mul64,
        "mulu64": generate_mulu64,

        # 移位（寄存器型，代码里用 generate_*64 包装为 mode="sl/sra/srl"）
        "sl64":   generate_sl64,
        "sra64":  generate_sra64,
        "srl64":  generate_srl64,

        "sl":   generate_sl,
        "sra":  generate_sra,
        "srl":  generate_srl,
        # === 一元 ALU（两个寄存器格式的指令生成器）===
        "not":   generate_not,
        "abs":   generate_abs,
        "cbw":   generate_cbw,
        "chw":   generate_chw,
        "neg64": generate_neg64,
        "sat64": generate_sat64,

        # === 测试/位操作/选择/标志 ===
        "test":   generate_test,
        "testi":  generate_testi,
        "bclr":   generate_bclr,
        "select": generate_select,
        "setc":   generate_setc,

        # 位域
        "bfext":  generate_bfext,
        "bfextu": generate_bfextu,
        "bfst":   generate_bfst,

        # === MAC 系列 ===
        "mac16":  generate_mac16,
        "macu16": generate_macu16,
        "mac32":  generate_mac32,
        "macu32": generate_macu32,
        "mac64":  generate_mac64,
        "macu64": generate_macu64,
}

cr_instruction_map = {
        "addi":  generate_addi,
        "addic":  generate_addic,
        "addc":  generate_addc,
        "add":  generate_add,
        "subi":  generate_subi,
        "subic":  generate_subic,
        "subc":  generate_subc,
        "sub":  generate_sub,
        "mac32":  generate_mac32,
        "macu32": generate_macu32,
     }

tmu_instr_map = {
        "mpy2pif32": generate_mpy2pif32,
        "div2pif32": generate_div2pif32,
        "sinpuf32": generate_sinpuf32,
        "cospuf32": generate_cospuf32,
        "atanpuf32": generate_atanpuf32,
        "quadf": generate_quadf,
    }

vcu_instr_map = {
        "vcrc8ll": generate_vcrc8ll,
        "vcrc8lh": generate_vcrc8lh,
        "vcrc8hl": generate_vcrc8hl,
        "vcrc8hh": generate_vcrc8hh,
        "vcrc16p1ll": generate_vcrc16p1ll,
        "vcrc16p1lh": generate_vcrc16p1lh,
        "vcrc16p1hl": generate_vcrc16p1hl,
        "vcrc16p1hh": generate_vcrc16p1hh,
        "vcrc16p2ll": generate_vcrc16p2ll,
        "vcrc16p2lh": generate_vcrc16p2lh,
        "vcrc16p2hl": generate_vcrc16p2hl,
        "vcrc16p2hh": generate_vcrc16p2hh,
        "vcrc32ll": generate_vcrc32ll,
        "vcrc32lh": generate_vcrc32lh,
        "vcrc32hl": generate_vcrc32hl,
        "vcrc32hh": generate_vcrc32hh,
    }

fintdiv_instr_map = {
        "absi32div32": generate_absi32div32,
        "absi64div32": generate_absi64div32,
        "absi64div64": generate_absi64div64,
        "enegi32div32": generate_enegi32div32,
        "enegi64div32": generate_enegi64div32,

        "enegi64div64": generate_enegi64div64,
        "mnegi32div32": generate_mnegi32div32,
        "mnegi64div32": generate_mnegi64div32,
        "mnegi64div64": generate_mnegi64div64,
        "subc2ui64": generate_subc2ui64,

        "subc4ui32": generate_subc4ui32,
        "absi32div32u": generate_absi32div32u,
        "absi64div32u": generate_absi64div32u,
        "absi64div64u": generate_absi64div64u,
        "negi32div32": generate_negi32div32,

        "negi64div32": generate_negi64div32,
        "negi64div64": generate_negi64div64
        }




def handle_slot1_instr(instr_name: str = "random"):
    """
    MOV 指令分发函数，根据 instr_name 调用对应子函数
    支持 random - 随机选择一个指令执行
    其他无效指令将静默忽略
    """
    instr_name = instr_name.lower()

    random_instr_map = {
        "random": None,  # 特殊标记
        "random1": None  # 特殊标记
    }
#      slot1_instr_map = {**alu_compare_instr_map, **random_instr_map}
    slot1_instr_weight = {**mov_instr_weight, **alu_compare_instr_weight, **alu_calculate_instr_weight, **tmu_instr_weight, **vcu_instr_weight, **fintdiv_instr_weight}

    if not CR_MODEL:
        slot1_instr_map = {**mov_instr_map, **alu_compare_instr_map, **random_instr_map, **alu_calculate_instr_map}
        calculate_instr_map = {**alu_calculate_instr_map}
        if TEST_TMU:
            slot1_instr_map = {**slot1_instr_map, **tmu_instr_map}
            calculate_instr_map = {**calculate_instr_map, **tmu_instr_map}
        if TEST_VCU:
            slot1_instr_map = {**slot1_instr_map, **vcu_instr_map}
            calculate_instr_map = {**calculate_instr_map, **vcu_instr_map}
        if TEST_FINTDIV:
            slot1_instr_map = {**slot1_instr_map, **fintdiv_instr_map}
            calculate_instr_map = {**calculate_instr_map, **fintdiv_instr_map}
    else:
        slot1_instr_map = {**cr_instruction_map, **random_instr_map}
        calculate_instr_map = {**cr_instruction_map}


    if TEST_I2C and instr_name != "random_calculate":
        if probability_return(0.1):
            generate_i2c_instr()
            return

    if instr_name == "random" or instr_name == "random1":
        weight = 1
        if WEIGHT_MODE:
            weight = random.randint(1, MAX_SLOT1_WEIGHT)
        # 创建随机选择池（排除 random 自身）
        if not TEST_CLA:
            choices = [key for key in slot1_instr_map.keys() if key != "random" and key != "random1" and slot1_instr_weight[key] >= weight]
        else:
            choices = [key for key in slot1_instr_map.keys() if key != "random" and key != "random1" and key not in CLA_NOT_SUPPORT_SLOT1 and slot1_instr_weight[key] >= weight]
        # 随机选择一个指令并执行
        slot1_instr_map[random.choice(choices)]()
    elif instr_name == "random_calculate":
        weight = 1
        if WEIGHT_MODE:
            weight = random.randint(1, MAX_SLOT1_WEIGHT)

        if not TEST_CLA:
            choices = [key for key in calculate_instr_map.keys()]
        else:
            choices = [key for key in calculate_instr_map.keys() if key not in CLA_NOT_SUPPORT_SLOT1 and slot1_instr_weight[key] >= weight]
        # 随机选择一个指令并执行
        slot1_instr_map[random.choice(choices)]()
    elif instr_name in slot1_instr_map:
        slot1_instr_map[instr_name]()  # 执行指定指令

    # 其他情况静默不执行
