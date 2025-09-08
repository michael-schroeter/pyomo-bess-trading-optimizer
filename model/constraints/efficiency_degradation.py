import pyomo.environ as pyo
from params.scenario_config import EFFICIENCY_BAT, EFFICIENCY_REST

def add_efficiency_degradation_constraints(model: pyo.ConcreteModel) -> None:

    def efficiency_degradation_rule(m, t):
        # e(c) = m*c + n
        factor = (1.97192 * 10**(-6)) / 100 # pro Cycle
        n = EFFICIENCY_BAT
        v = -factor*EFFICIENCY_BAT
        efficiency_bat = v*m.v_CYCLES_CUMSUM[t] + n - m.p_EFFICIENCY_DEG_CAL
        return m.v_EFFICIENCY_SYS[t] == efficiency_bat * EFFICIENCY_REST

    
    model.efficiency_degradation_constraint = pyo.Constraint(model.T, rule=efficiency_degradation_rule)

    return model