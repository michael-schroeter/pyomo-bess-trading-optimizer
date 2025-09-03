import pyomo.environ as pyo
from model.utils import get_global_bounds

def add_cycles_real_constraints(model):
    def cycles_real_rule(m, t):
        return m.v_CYCLES[t] == (m.e_TOTAL_CHARGE[t] + m.e_TOTAL_DISCHARGE[t]) / (2 * m.p_INITIAL_BATTERY_CAPACITY)
    model.c_CYCLES_REAL = pyo.Constraint(model.T, rule=cycles_real_rule)

    def cumulative_cycles_rule(m, t):
        if t == m.T.first():
            return m.v_CYCLES_CUMSUM[t] == m.p_INITIAL_CYCLES + m.v_CYCLES[t]
        
        else:
            return m.v_CYCLES_CUMSUM[t] == m.v_CYCLES_CUMSUM[m.T.prev(t)] + m.v_CYCLES[t]
    model.c_CYCLES_CUMSUM = pyo.Constraint(model.T, rule=cumulative_cycles_rule)

    return model



