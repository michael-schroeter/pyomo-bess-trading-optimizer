import pyomo.environ as pyo
from pyomo.core import SOSConstraint
from params.scenario_config1 import INITIAL_BATTERY_CAPACITY, MAX_CHARGE_RATE, MAX_CYCLE_RATE

import pyomo.environ as pyo

def add_cycles_eq_constraints(model):
    
    eps = 1e-6
    soc_bin_bounds = {
        0: (0.00, 0.25 - eps),
        1: (0.25, 0.50 - eps),
        2: (0.50, 0.75 - eps),
        3: (0.75, 1.00 + eps),
    }
    

    
    def _only_one_bin_active(m, t):
        return sum(m.v_SOC_BIN_ACTIVE[t, k] for k in m.K) == 1
    model.c_only_one_bin_active = pyo.Constraint(model.T, rule=_only_one_bin_active)

    def _soc_in_lower_bound(m, t):
        lower_bounds = sum(soc_bin_bounds[k][0] * m.v_SOC_BIN_ACTIVE[t, k] for k in m.K)
        return m.e_APPROX_SOC[t] >= lower_bounds
    model.c_soc_in_lower_bound = pyo.Constraint(model.T, rule=_soc_in_lower_bound)

    def _soc_in_upper_bound(m, t):
        upper_bounds = sum(soc_bin_bounds[k][1] * m.v_SOC_BIN_ACTIVE[t, k] for k in m.K)
        return m.e_APPROX_SOC[t] <= upper_bounds
    model.c_soc_in_upper_bound = pyo.Constraint(model.T, rule=_soc_in_upper_bound)
    

    def _gate_throughput(m, t, k):
        return m.v_CYCLE_PER_SOC_BIN[t, k] <= MAX_CYCLE_RATE * m.v_SOC_BIN_ACTIVE[t, k]
    model.c_gate_throughput = pyo.Constraint(model.T, model.K, rule=_gate_throughput)



    def _split_cycles_rule(m, t):
        return sum(m.v_CYCLE_PER_SOC_BIN[t, k] for k in m.K) == m.v_CYCLES[t]
    model.c_split_cycles = pyo.Constraint(model.T, rule=_split_cycles_rule)


    def cycles_eq_rule(m, t):
        return m.v_CYCLES_EQ[t] == sum(m.p_SOC_FACTORS[k] * m.v_CYCLE_PER_SOC_BIN[t, k] for k in m.K)
    model.c_equivalent_cycles = pyo.Constraint(model.T, rule=cycles_eq_rule)

    def cumulative_cycles_eq_rule(m, t):
        if t == m.T.first():
            return m.v_CYCLES_EQ_CUMSUM[t] == m.p_INITIAL_CYCLES_EQ + m.v_CYCLES_EQ[t]
        
        else:
            return m.v_CYCLES_EQ_CUMSUM[t] == m.v_CYCLES_EQ_CUMSUM[m.T.prev(t)] + m.v_CYCLES_EQ[t]
    model.c_CYCLES_EQ_CUMSUM = pyo.Constraint(model.T, rule=cumulative_cycles_eq_rule)
    
    return model




