import random


from load_store.load_function import generate_load,generate_loadu,generate_loadi,generate_loadui
from load_store.store_function import generate_store,generate_storeu,generate_storei,generate_storeui,generate_store_loado
from config.config import TestConfig,ClaConfig
from config.weight_model import LOAD_WEIGHT,STORE_WEIGHT

#权重模式配置
WEIGHT_MODE = TestConfig.WEIGHT_MODE
load_instr_weight = LOAD_WEIGHT.load_instr_weight
MAX_LOAD_WEIGHT = LOAD_WEIGHT.MAX_LOAD_WEIGHT

store_instr_weight = STORE_WEIGHT.store_instr_weight
MAX_STORE_WEIGHT = STORE_WEIGHT.MAX_STORE_WEIGHT


CR_MODEL = TestConfig.CR_MODEL
TEST_CLA = TestConfig.TEST_CLA
CLA_NOT_SUPPORT_LOAD = ClaConfig.CLA_NOT_SUPPORT_LOAD
CLA_NOT_SUPPORT_STORE = ClaConfig.CLA_NOT_SUPPORT_STORE
DISABLE_CLA_ADDR_REGS = TestConfig.DISABLE_CLA_ADDR_REGS
# loado*/storeo* use OFF/BAR/MR indirect addressing; they cannot be generated
# when address registers are disabled (the OFF/BAR/MR pools are emptied).
# loadu*/storeu* are NOT OFF/BAR/MR based (they use a plain GR base + imm), but
# they auto-update (post-modify) the base GR via the extended (wenx) write port,
# which is a Bug-A interrupt-resume drop trigger. When DISABLE_CLA_ADDR_REGS is
# on we also exclude them so the stream has no auto-update (wenx) writebacks.
ADDR_REG_LOAD = {"loado16", "loado32", "loadu8", "loadu16", "loadu32"}
ADDR_REG_STORE = {"storeo16", "storeo32", "storeu8", "storeu16", "storeu32"}


def handle_slot3_instr(instr_name: str):
    """
    MOV 指令分发函数，根据 instr_name 调用对应子函数
    支持 random - 随机选择一个指令执行
    其他无效指令将静默忽略
    """
    instr_name = instr_name.lower()
    store_instr_map = {
         "store8": generate_store8,
         "store16": generate_store16,
         "store32": generate_store32,

         "storeu8": generate_storeu8,
         "storeu16": generate_storeu16,
         "storeu32": generate_storeu32,

         "storeo16": generate_storeo16,
         "storeo32": generate_storeo32,

         "storei8": generate_storei8,
         "storei16": generate_storei16,
         "storei32": generate_storei32,

#          "storeui8": generate_storeui8,
#          "storeui16": generate_storeui16,
#          "storeui32": generate_storeui32,
        "random": None,  # 特殊标记
        "random3": None  # 特殊标记
    }


    if CR_MODEL:
        # 在 CR 模式下，禁用 store 指令
        return

    if instr_name == "random" or instr_name == "random3":
        weight = 1
        if WEIGHT_MODE:
            weight = random.randint(1,MAX_STORE_WEIGHT)
        # 创建随机选择池（排除 random 自身）
        if not TEST_CLA:
            choices = [key for key in store_instr_weight.keys() if key != "random" and key != "random2" and store_instr_weight[key] >= weight]
        else:
            choices = [key for key in store_instr_weight.keys() if key != "random" and key != "random2" and store_instr_weight[key] >= weight and key not in CLA_NOT_SUPPORT_STORE and not (DISABLE_CLA_ADDR_REGS and key in ADDR_REG_STORE)]
             
        # 随机选择一个指令并执行
        store_instr_map[random.choice(choices)]()
    elif instr_name in store_instr_map:
        store_instr_map[instr_name]()  # 执行指定指令
    # 其他情况静默不执行

def handle_slot2_instr(instr_name: str):
    """
    MOV 指令分发函数，根据 instr_name 调用对应子函数
    支持 random - 随机选择一个指令执行
    其他无效指令将静默忽略
    """
    instr_name = instr_name.lower()
    load_instr_map = {
        "load8": generate_load8,
        "load16": generate_load16,
        "load32": generate_load32,

        "loadu8": generate_loadu8,
        "loadu16": generate_loadu16,
        "loadu32": generate_loadu32,
 
        "loado16": generate_loado16,
        "loado32": generate_loado32,

        "loadi8": generate_loadi8,
        "loadi16": generate_loadi16,
        "loadi32": generate_loadi32,

#          "loadui8": generate_loadui8,
#          "loadui16": generate_loadui16,
#          "loadui32": generate_loadui32,
        "random": None,  # 特殊标记
        "random2": None  # 特殊标记
    }

    if CR_MODEL:
        # 在 CR 模式下，禁用 load 指令
        return


    if instr_name == "random" or instr_name == "random2":
        weight = 1
        if WEIGHT_MODE:
            weight = random.randint(1,MAX_LOAD_WEIGHT)
        # 创建随机选择池（排除 random 自身）
        if not TEST_CLA:
            choices = [key for key in load_instr_weight.keys() if key != "random" and key != "random2" and load_instr_weight[key] >= weight]
        else:
            choices = [key for key in load_instr_weight.keys() if key != "random" and key != "random2" and load_instr_weight[key] >= weight and key not in CLA_NOT_SUPPORT_LOAD and not (DISABLE_CLA_ADDR_REGS and key in ADDR_REG_LOAD)]
        # 随机选择一个指令并执行
        load_instr_map[random.choice(choices)]()
    elif instr_name in load_instr_map:
        load_instr_map[instr_name]()  # 执行指定指令
    # 其他情况静默不执行

def generate_load8(): 
    generate_load(8)

def generate_load16(): 
    generate_load(16)

def generate_load32(): 
    generate_load(32)

def generate_loadu8(): 
    generate_loadu(8)

def generate_loadu16(): 
    generate_loadu(16)

def generate_loadu32(): 
    generate_loadu(32)

def generate_loadi8(): 
    generate_loadi(8)

def generate_loadi16(): 
    generate_loadi(16)

def generate_loadi32(): 
    generate_loadi(32)

def generate_loadui8(): 
    generate_loadui(8)

def generate_loadui16(): 
    generate_loadui(16)

def generate_loadui32(): 
    generate_loadui(32)

def generate_loado16(): 
    generate_store_loado(16,mode = "load")

def generate_loado32(): 
    generate_store_loado(32,mode = "load")

#===== store函数========#
#bit_width调宽度8,16,32
#store
def generate_store8():
     generate_store(8)

def generate_store16():
     generate_store(16)

def generate_store32():
     generate_store(32)

#storeu
def generate_storeu8():
     generate_storeu(8)

def generate_storeu16():
     generate_storeu(16)

def generate_storeu32():
     generate_storeu(32)

#storei
def generate_storei8():
     generate_storei(8)

def generate_storei16():
     generate_storei(16)

def generate_storei32():
     generate_storei(16)

#storeui
def generate_storeui8():
     generate_storeui(8)

def generate_storeui16():
     generate_storeui(16)

def generate_storeui32():
     generate_storei(16)

def generate_storeo16():
     generate_store_loado(16)

def generate_storeo32():
     generate_store_loado(32)



