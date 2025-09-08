import pyomo.environ as pyo

def add_energy_at_start_expr(model):
    def energy_at_start_rule(m, t):
        return 0.0 if t == m.T.first() else m.v_STORED_ENERGY[m.T.prev(t)]
    model.e_ENERGY_AT_START = pyo.Expression(model.T, rule=energy_at_start_rule)
