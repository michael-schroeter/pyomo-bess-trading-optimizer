import pyomo.environ as pyo


def define_soc_expr(model):
    def approx_soc(m, t):
        # Der SOC wird hier als lineare Annäherung berechnet
        return m.v_STORED_ENERGY[t] / m.p_INITIAL_BATTERY_CAPACITY
    model.e_APPROX_SOC = pyo.Expression(model.T, rule=approx_soc)