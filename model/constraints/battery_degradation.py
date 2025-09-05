import numpy as np
import math
import pyomo.environ as pyo
from params.scenario_config1 import INITIAL_BATTERY_CAPACITY, LIFETIME_CYCLES



def add_battery_degradation_constraints(model):

    def battery_capacity_rule(m, t):
        return m.v_BATTERY_CAPACITY[t] == m.v_REST_CAPACITY_CYCLE[t] - m.p_DEGRADATION_CAL
    model.c_battery_capacity = pyo.Constraint(model.T, rule=battery_capacity_rule)
        

    def degradation_function_rule(model, t, cycles):
        return INITIAL_BATTERY_CAPACITY * (((2.6817*math.exp(-0.0031*cycles) + 17.5582*math.exp(-0.0001*cycles) +79.76)) / 100)
    
    
    cycle_breakpoints = np.linspace(0, LIFETIME_CYCLES*2, 11).tolist()
    model.c_define_capacity = pyo.Piecewise(
        model.T, 
        model.v_REST_CAPACITY_CYCLE,            # y
        model.v_CYCLES_EQ_CUMSUM,            # x
        pw_pts=cycle_breakpoints,
        f_rule=degradation_function_rule,
        pw_repn='SOS2',                      # Großschreibung!
        pw_constr_type='EQ'                  # <<— explizit setzen
    )


    return model



