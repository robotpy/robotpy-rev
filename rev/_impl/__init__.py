import hal

if hal.isSimulation():
    from .autogen.sim_enums import *
    from .autogen.sim import *
else:
    from .rev_roborio import *
