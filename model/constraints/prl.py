import pyomo.environ as pyo
from params.scenario_config1 import (
    SYSTEM_POWER,
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


def add_prl_energy_constraints(model):
    def energy_prl_discharge_buffer(m, t):
        iv = m.time_to_interval[t]
        required_energy = 0.42 * m.v_PRL_POWER[iv] / m.p_INITIAL_EFFICIENCY
        return m.v_STORED_ENERGY[t] >= required_energy

    def energy_prl_charge_buffer(m, t):
        iv = m.time_to_interval[t]
        required_headroom = 0.42 * m.v_PRL_POWER[iv] * m.p_INITIAL_EFFICIENCY
        # KORREKTUR: Die "1" wurde durch die dynamische Kapazität ersetzt
        return m.v_STORED_ENERGY[t] <= m.v_BATTERY_CAPACITY[t] - required_headroom
    

    model.energy_prl_discharge_buffer = pyo.Constraint(model.T, rule=energy_prl_discharge_buffer)
    model.energy_prl_charge_buffer    = pyo.Constraint(model.T, rule=energy_prl_charge_buffer)



        
