from dataclasses import dataclass

global g_param_defs
g_param_defs = None

@dataclass
class ParamDef:
    name: str
    unit: str
    variants: list[str]
    display_graph: bool
    display_live: bool
    low_value: float
    high_value: float
    
def set_param_defs(new_param_defs):
    global g_param_defs
    g_param_defs = new_param_defs

def get_param_defs():
    return g_param_defs

def get_param_def(param_idx):
    return g_param_defs[param_idx]
