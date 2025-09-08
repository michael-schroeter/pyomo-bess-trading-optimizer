import numpy as np
import math
import pyomo.environ as pyo
from params.scenario_config import INITIAL_BATTERY_CAPACITY, LIFETIME_CYCLES
from model.utils import get_bat_deg_factor
from config_degradation import cap_deg_c_rate_factors, cycle_breakpoints, calculate_rest_capacity



def add_battery_degradation_constraints(model):
    factor_crate = get_bat_deg_factor(pyo.value(model.p_C_RATE), cap_deg_c_rate_factors) 
    def battery_capacity_rule(m, t):
    
        if t == m.T.first():
            delta_rest_cap =  0
        else:
            delta_rest_cap = m.v_REST_CAPACITY_CYCLE[m.T.prev(t)] - m.v_REST_CAPACITY_CYCLE[t]

        return m.v_BATTERY_CAPACITY[t] == m.v_REST_CAPACITY_CYCLE[t] + delta_rest_cap*factor_crate - m.p_DEGRADATION_CAL
    model.c_battery_capacity = pyo.Constraint(model.T, rule=battery_capacity_rule)
        

    def degradation_function_rule(m, t, cycles):
        return calculate_rest_capacity(cycles)
    
    
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



