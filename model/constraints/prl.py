import pyomo.environ as pyo
from params.scenario_config1 import (
    INITIAL_BATTERY_CAPACITY,
    SYSTEM_POWER,
    EFFICIENCY
)

def add_prl_mode_constraints(model):
    def prl_ub_iv(m, date, quartal):
        iv = (date, quartal)
        return m.v_PRL_POWER[iv] == SYSTEM_POWER * m.v_MODE_PRL[iv]
    model.c_PRL_POWER_UB_IV = pyo.Constraint(model.D4, rule=prl_ub_iv)

    def prl_lb_iv(m, date, quartal):
        iv = (date, quartal)
        return m.v_PRL_POWER[iv] >= 1 * m.v_MODE_PRL[iv]
    model.c_PRL_POWER_LB_IV = pyo.Constraint(model.D4, rule=prl_lb_iv)


import pyomo.environ as pyo

def add_prl_soc_constraints(model):


    def soc_prl_discharge_buffer(model, t):
        iv = model.time_to_interval[t]
        return model.v_BAT_SOC[t]   >=0.42 * model.v_PRL_POWER[iv] / (INITIAL_BATTERY_CAPACITY * EFFICIENCY)

    def soc_prl_charge_buffer(model, t):
        iv = model.time_to_interval[t]
        return  model.v_BAT_SOC[t]  <= 1 - (0.42 * model.v_PRL_POWER[iv] * EFFICIENCY / INITIAL_BATTERY_CAPACITY)

    model.soc_prl_discharge_buffer = pyo.Constraint(model.T, rule=soc_prl_discharge_buffer)
    model.soc_prl_charge_buffer    = pyo.Constraint(model.T, rule=soc_prl_charge_buffer)



