import pyomo.environ as pyo

from params.scenario_config1 import DEGRADATION_FACTOR_MWH




def add_battery_degradation_constraints(model):

    def capacity_degradation_rule(m, t):
        if t == m.T.first():
            return m.v_BATTERY_CAPACITY[t] == m.p_INITIAL_BATTERY_CAPACITY_YEAR

        energy_throughput_prev_step = (m.e_TOTAL_CHARGE[m.T.prev(t)] + m.e_TOTAL_DISCHARGE[m.T.prev(t)])
        
        degradation = energy_throughput_prev_step * DEGRADATION_FACTOR_MWH 

        return m.v_BATTERY_CAPACITY[t] == m.v_BATTERY_CAPACITY[m.T.prev(t)] - degradation

    model.c_CAPACITY_DEGRADATION = pyo.Constraint(model.T, rule=capacity_degradation_rule)








