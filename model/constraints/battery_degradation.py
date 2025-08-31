import pyomo.environ as pyo
from params.scenario_config1 import INITIAL_BATTERY_CAPACITY, LIFETIME_CYCLES

def add_battery_degradation_constraints(model):
    def define_capacity_from_degradation_rule(m, t):
        # Cap_r(Cycle_r) = -0.2Cycle_r+ 1 / f(c) = - 0.2 * (c) +1
        # Lineare Kurve der Anteiligen Restkapazität in Abhängigkeit der AnteiligenZyklen (in Bezug auf LIFETIME_CYCLES) 
        # -> wenn Lifetime_Cycles erreicht sind, ist die Kapazität bei 80%
        Cycle_r = m.v_CYCLES_EQ_CUMSUM[t]/LIFETIME_CYCLES
        Cap_r = -0.2 * Cycle_r + 1
        return m.v_BATTERY_CAPACITY[t] == INITIAL_BATTERY_CAPACITY * Cap_r
    model.c_define_capacity = pyo.Constraint(model.T, rule=define_capacity_from_degradation_rule)



