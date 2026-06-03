import os


def _env_bool(name: str, default: bool) -> bool:
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


BASE_PC = 0x00030418


class TestConfig:
    EXPANDED_TEST_SCOPE = _env_bool("QX_EXPANDED_TEST_SCOPE", True)
    INCREASE_BYPASS_TEST = _env_bool("QX_INCREASE_BYPASS_TEST", True)
    WEIGHT_MODE = _env_bool("QX_WEIGHT_MODE", True)
    PACKED_INSTR = _env_bool("QX_PACKED_INSTR", True)
    TEST_JMP_CALL = _env_bool("QX_TEST_JMP_CALL", False)
    TEST_CLA = _env_bool("QX_TEST_CLA", False)
    BACK_END_TEST = _env_bool("QX_BACK_END_TEST", False)
    CR_PRINT = _env_bool("QX_CR_PRINT", False)
    CR_MODEL = _env_bool("QX_CR_MODEL", False)
    FPU_TEST = _env_bool("QX_FPU_TEST", True)
    TMU_TEST = _env_bool("QX_TMU_TEST", False)
    VCU_TEST = _env_bool("QX_VCU_TEST", False)
    FINTDIV_TEST = _env_bool("QX_FINTDIV_TEST", False)
    I2C_TEST = _env_bool("QX_I2C_TEST", False)
    REAL_TEST = _env_bool("QX_REAL_TEST", True)
    DOUBLE_WB_PACK = _env_bool("QX_DOUBLE_WB_PACK", False)
    DISABLE_CLA_ADDR_REGS = _env_bool("QX_DISABLE_CLA_ADDR_REGS", False)


class JmpConfig:
    CALL_MAX_FREQUENCY = 300
    CALL_MIN_FREQUENCY = 400

    HIGH_ADDR = "_HIGH_ADDR"
    LOW_ADDR = "_LOW_ADDR"

    START_PART = "initial"
    FINISH_PART = "finish"
    MAIN_PART = "first"
    FUNCTION_PART = "function"

    FUNCTION = ["alu", "mem", "io", "branch", "load_store"]
    FUNCTION_NAMES = [f"function_{name}" for name in FUNCTION]
    MEMORY_LAYOUT_ORDER = [START_PART, FUNCTION_PART, MAIN_PART, FINISH_PART]
    instruction_map = {}

    START_MIN_PERCENT = 0.03
    START_MAX_PERCENT = 0.05
    FINISH_MIN_PERCENT = 0.03
    FINISH_MAX_PERCENT = 0.05
    MAIN_MIN_PERCENT = 0.4
    FUNCTION_MIN_PERCENT = 0.05
    FUNCTION_MAX_PERCENT = 0.1
    FUNCTION_TOTAL_MAX_PERCENT = 0.6

    JMP_DEBUG = False


class ClaConfig:
    CLA_NOT_SUPPORT_JMP = [
        "sjmp",
        "sjc",
        "sjnc",
    ]

    CLA_NOT_SUPPORT_CALL = [
        "scall",
        "scallr",
    ]

    CLA_NOT_SUPPORT_RET = [
        "sret",
    ]

    CLA_NOT_SUPPORT_MOV = [
        "moviglz",
        "moviglx",
    ]

    CLA_NOT_SUPPORT_LOAD = [
        "loadi8",
        "loadi16",
        "loadi32",
        "loado16",
        "loado32",
    ]

    CLA_NOT_SUPPORT_STORE = [
        "storei8",
        "storei16",
        "storei32",
        "storeo16",
        "storeo32",
    ]

    CLA_NOT_SUPPORT_ALU = [
        "neg64",
        "sat64",
        "sra64",
        "srai",
        "sl64",
        "sli",
        "srl64",
        "srli",
        "select",
        "setc",
        "subic",
        "subi",
        "gtiu",
        "ltiu",
        "geiu",
        "leiu",
        "eqiu",
        "neqiu",
        "equ",
        "nequ",
        "mul32",
        "mul64",
        "mulu32",
        "mulu64",
        "mac16",
        "mac32",
        "mac64",
        "macu",
        "macu16",
        "macu32",
        "macu64",
    ]

    CLA_NOT_SUPPORT_FPU = [
        "none",
    ]

    CLA_SUPPORT_SLOT3 = [
        "fsmul",
        "fsdiv",
        "fsmac",
        "fsadd",
        "fssub",
        "fsmax",
        "fsmin",
        "fseinv",
        "fseisqrt",
        "fssqrt",
        "fsabs",
        "fcvtsf",
        "fcvtfs",
        "fcvtsu",
        "fcvtus",
    ]


class RegConfig:
    GR_NUM = 30
    BAR_NUM = 4
    MR_NUM = 4
    OFF_NUM = 4


class MemoryConfig:
    RAM_START = 0x0000_0000
    BANK_NUM = 16
    DATA_BLOCK_SIZE = 0x8000
    RAM_END = 0x0007_FFFF

    PERIPH_START = 0x3000_0000
    PERIPH_END = 0x3007_FFFF

    @staticmethod
    def get_range(name: str) -> tuple:
        return (
            getattr(MemoryConfig, f"{name}_START"),
            getattr(MemoryConfig, f"{name}_END"),
        )


class Double_WB_instr:
    S1_DOUBLE_WB_INSTR = [
        "sat64",
        "srl64",
        "sl64",
        "sra64",
        "neg64",
        "mac16",
        "macu16",
        "mac32",
        "vcrc8ll",
        "vcrc8lh",
        "vcrc8hl",
        "vcrc8hh",
        "vcrc16p1ll",
        "vcrc16p1lh",
        "vcrc16p1hl",
        "vcrc16p1hh",
        "vcrc16p2ll",
        "vcrc16p2lh",
        "vcrc16p2hl",
        "vcrc16p2hh",
        "vcrc32ll",
        "vcrc32lh",
        "vcrc32hl",
        "vcrc32hh",
    ]

    S2_DOUBLE_WB_INSTR = [
        "loado16",
        "loado32",
        "loadu8",
        "loadu16",
        "loadu32",
    ]

    S1_DELAY_SLOT = [
        "call",
        "callr",
        "jmp",
        "jmpr",
        "jc",
        "jnc",
    ]

    FINTDIV_INSTR = [
        "absi32div32",
        "negi32div32",
        "absi64div32",
        "absi64div64",
        "negi64div32",
        "negi64div64",
        "subc2ui64",
        "subc4ui32",
        "enegi32div32",
        "mnegi32div32",
        "enegi64div32",
        "mnegi64div32",
        "enegi64div64",
        "mnegi64div64",
        "absi32div32u",
        "absi64div32u",
        "absi64div64u",
    ]
