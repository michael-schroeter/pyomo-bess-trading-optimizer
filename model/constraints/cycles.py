import pyomo.environ as pyo
from model.utils import get_global_bounds

def add_cycles_real_constraints(model):
    def cycles_real_rule(m, t):
        return m.v_CYCLES[t] == (m.e_TOTAL_CHARGE[t] + m.e_TOTAL_DISCHARGE[t]) / (2 * m.p_INITIAL_BATTERY_CAPACITY_YEAR)
    model.c_CYCLES_REAL = pyo.Constraint(model.T, rule=cycles_real_rule)

    def cumulative_cycles_rule(m, t):
        if t == m.T.first():
            return m.v_CYCLES_CUMSUM[t] == m.p_INITIAL_CYCLES + m.v_CYCLES[t]
        
        else:
            return m.v_CYCLES_CUMSUM[t] == m.v_CYCLES_CUMSUM[m.T.prev(t)] + m.v_CYCLES[t]
    model.c_CYCLES_CUMSUM = pyo.Constraint(model.T, rule=cumulative_cycles_rule)

    return model

# Piecewise-McCormick (MILP) für z_t = CYCLES_t * STRESS_t
# - segmentiert in x := v_CYCLES (per Breakpoints)
# - y := v_STRESS bleibt kontinuierlich (nutzt nur Bounds)
# - ersetzt den unzulässigen 2D-Piecewise-Aufruf 1:1 im Funktionsrahmen

def add_cycles_eq_piecewise_constraints(model):

    cyc_breakpoints = [0, 0.025, 0.05, 0.075, 0.1, 0.125, 0.15, 0.175, 0.2, 0.225, 0.25]

    # Bounds korrekt aus indizierten Variablen holen
    xL_glob, xU_glob = get_global_bounds(model.v_CYCLES, model.T)
    yL,      yU      = get_global_bounds(model.v_STRESS, model.T)

    M = (xU_glob - xL_glob) * (yU - yL)  # konservativ

    S = range(len(cyc_breakpoints) - 1)
    model.CYC_SEG = pyo.Set(initialize=S)

    model.b_cyc = pyo.Var(model.T, model.CYC_SEG, within=pyo.Binary)
    model.one_seg_cyc = pyo.Constraint(model.T,
        rule=lambda m,t: sum(m.b_cyc[t,s] for s in m.CYC_SEG) == 1)

    # x in aktivem Segment
    model.x_lb_cyc = pyo.Constraint(model.T, rule=lambda m,t:
        m.v_CYCLES[t] >= sum(cyc_breakpoints[s]   * m.b_cyc[t,s] for s in m.CYC_SEG))
    model.x_ub_cyc = pyo.Constraint(model.T, rule=lambda m,t:
        m.v_CYCLES[t] <= sum(cyc_breakpoints[s+1] * m.b_cyc[t,s] for s in m.CYC_SEG))

    # McCormick je Segment (indikativ via (1 - b))
    def mc1_rule(m,t,s):
        xl = cyc_breakpoints[s]
        return m.v_CYCLES_EQ[t] >= xl*m.v_STRESS[t] + yL*m.v_CYCLES[t] - xl*yL - M*(1 - m.b_cyc[t,s])
    def mc2_rule(m,t,s):
        xu = cyc_breakpoints[s+1]
        return m.v_CYCLES_EQ[t] >= xu*m.v_STRESS[t] + yU*m.v_CYCLES[t] - xu*yU - M*(1 - m.b_cyc[t,s])
    def mc3_rule(m,t,s):
        xu = cyc_breakpoints[s+1]
        return m.v_CYCLES_EQ[t] <= xu*m.v_STRESS[t] + yL*m.v_CYCLES[t] - xu*yL + M*(1 - m.b_cyc[t,s])
    def mc4_rule(m,t,s):
        xl = cyc_breakpoints[s]
        return m.v_CYCLES_EQ[t] <= xl*m.v_STRESS[t] + yU*m.v_CYCLES[t] - xl*yU + M*(1 - m.b_cyc[t,s])

    model.mc1_cyc = pyo.Constraint(model.T, model.CYC_SEG, rule=mc1_rule)
    model.mc2_cyc = pyo.Constraint(model.T, model.CYC_SEG, rule=mc2_rule)
    model.mc3_cyc = pyo.Constraint(model.T, model.CYC_SEG, rule=mc3_rule)
    model.mc4_cyc = pyo.Constraint(model.T, model.CYC_SEG, rule=mc4_rule)

    return model



def xxxadd_cycles_eq_piecewise_constraints(model):

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
