import pyomo.environ as pyo

def add_cycles_real_constraints(model):
    def cycles_real_rule(m, t):
        return m.v_CYCLES[t] == (m.e_TOTAL_CHARGE[t] + m.e_TOTAL_DISCHARGE[t]) / (2 * m.p_INITIAL_BATTERY_CAPACITY_YEAR)
    model.c_CYCLES_REAL = pyo.Constraint(model.T, rule=cycles_real_rule)

    def cumulative_cycles_rule(m, t):
        if t == m.T.first():
            return m.v_CYCLES_CUMSUM[t] == m.p_INITIAL_CYCLES_YEAR + m.v_CYCLES[t]
        
        else:
            return m.v_CYCLES_CUMSUM[t] == m.v_CYCLES_CUMSUM[m.T.prev(t)] + m.v_CYCLES[t]
    model.c_CYCLES_CUMSUM = pyo.Constraint(model.T, rule=cumulative_cycles_rule)

    return model



def add_cycles_eq_piecewise_constraints_sos2(model):

    cyc_breakpoints = [0, 0.025, 0.05, 0.075, 0.1, 0.125, 0.15, 0.175, 0.2, 0.225, 0.25]
    stress_breakpoints = [0, 0.4, 0.8, 1.2, 1.6, 2.0, 2.4, 2.8, 3.2, 3.6, 4.0]
    def f_equivalent_cycles(m, t, cycles, stress):
        return cycles * stress

    model.c_linearize_product = pyo.Piecewise(
        model.T,                               # Index-Set
        model.v_CYCLES_EQ,                     # Output-Variable (z)
        model.v_CYCLES,                        # 1. Input-Variable (x)
        model.v_STRESS,                        # 2. Input-Variable (y)
        pw_repn='SOS2',                        # Die Darstellungsmethode
        pw_ptsx=cyc_breakpoints,               # Breakpoints für die x-Achse
        pw_ptsy=stress_breakpoints,            # Breakpoints für die y-Achse
        f_rule=f_equivalent_cycles             # Die Funktion, die an den Gitterpunkten ausgewertet wird
    )
    

    def cumulative_cycles_eq_rule(m, t):
        if t == m.T.first():
            return m.v_CYCLES_EQ_CUMSUM[t] == m.p_INITIAL_CYCLES_EQ_YEAR + m.v_CYCLES_EQ[t]
        
        else:
            return m.v_CYCLES_EQ_CUMSUM[t] == m.v_CYCLES_EQ_CUMSUM[m.T.prev(t)] + m.v_CYCLES_EQ[t]
    model.c_CYCLES_EQ_CUMSUM = pyo.Constraint(model.T, rule=cumulative_cycles_eq_rule)

    return model
