import pyomo.environ as pyo
from params.scenario_config import (
    SYSTEM_POWER,
)

def add_prl_mode_constraints(model):
    def prl_ub_iv(m, date, quartal):
        iv = (date, quartal)
        return m.v_PRL_POWER[iv] == SYSTEM_POWER * m.v_MODE_PRL[iv]
    model.c_PRL_POWER_UB_IV = pyo.Constraint(model.D4, rule=prl_ub_iv)


def add_prl_energy_constraints(model):

    def energy_prl_discharge_buffer_rule(m, d, q):
        iv = (d, q)
        t_start = m.interval_to_start_time[iv]
        required_energy = 0.42 * m.v_PRL_POWER[iv] / m.p_INITIAL_EFFICIENCY
        return m.e_ENERGY_AT_START[t_start] >= required_energy
    model.energy_prl_discharge_buffer = pyo.Constraint(model.D4, rule=energy_prl_discharge_buffer_rule)

    def energy_prl_charge_buffer_rule(m, d, q):
        iv = (d, q)
        t_start = m.interval_to_start_time[iv]
        required_headroom = 0.42 * m.v_PRL_POWER[iv] * m.p_INITIAL_EFFICIENCY
        return m.e_ENERGY_AT_START[t_start] <= m.v_BATTERY_CAPACITY[t_start] - required_headroom
    model.energy_prl_charge_buffer = pyo.Constraint(model.D4, rule=energy_prl_charge_buffer_rule)
