import numpy as np
import math
import pyomo.environ as pyo
from params.scenario_config import INITIAL_BATTERY_CAPACITY, LIFETIME_CYCLES



def add_battery_degradation_constraints(model):

    def battery_capacity_rule(m, t):
        return m.v_BATTERY_CAPACITY[t] == m.v_REST_CAPACITY_CYCLE[t] - m.p_DEGRADATION_CAL
    model.c_battery_capacity = pyo.Constraint(model.T, rule=battery_capacity_rule)
        

    def degradation_function_rule(model, t, cycles):
        return INITIAL_BATTERY_CAPACITY * (
    (
        4.26384996637378232975 * math.exp(-0.00235433534616526522 * cycles)
        + 251.46065636316288305352 * math.exp(-0.00000531056139597996 * cycles)
        - 155.72450632953666627145
    ) / 100
)
    
    
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



