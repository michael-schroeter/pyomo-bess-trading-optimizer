import pyomo.environ as pyo
from params.scenario_config import EFFICIENCY_BAT, EFFICIENCY_REST
from model.utils import get_eff_deg_factor
from config_degradation import calculate_efficiency_bat_rest, eff_deg_c_rate_factors

def add_efficiency_degradation_constraints(model: pyo.ConcreteModel) -> None:

    factor_crate = get_eff_deg_factor(pyo.value(model.p_C_RATE), eff_deg_c_rate_factors)
    def efficiency_degradation_rule(m, t):
        efficiency_bat = calculate_efficiency_bat_rest(m.v_CYCLES_EQ_CUMSUM[t], factor_crate)

        return m.v_EFFICIENCY_SYS[t] == efficiency_bat * EFFICIENCY_REST

    
    model.efficiency_degradation_constraint = pyo.Constraint(model.T, rule=efficiency_degradation_rule)

    return model

