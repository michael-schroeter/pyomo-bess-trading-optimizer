import pyomo.environ as pyo



def add_cumulative_stored_energy_constraints(model):
    def cumulative_stored_energy_rule(model, t):
        if t == model.T.first():
            return model.v_STORED_ENERGY[t] == (model.e_TOTAL_CHARGE[t] - model.e_TOTAL_DISCHARGE[t]) + model.p_INITIAL_STORED_ENERGY
        else:
            prev_t = model.T.prev(t)  
            return model.v_STORED_ENERGY[t] == model.v_STORED_ENERGY[prev_t] + (model.e_TOTAL_CHARGE[t] - model.e_TOTAL_DISCHARGE[t])
    model.c_CUMULATIVE_ENERGY = pyo.Constraint(model.T, rule=cumulative_stored_energy_rule)

    def energy_upper_bound_rule(m, t):
        return m.v_STORED_ENERGY[t] <= m.v_BATTERY_CAPACITY[t]
    model.c_energy_upper_bound = pyo.Constraint(model.T, rule=energy_upper_bound_rule)