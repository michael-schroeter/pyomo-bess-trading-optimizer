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

import pyomo.environ as pyo
from model.utils import get_global_bounds

def add_cycles_eq_piecewise_constraints(model):

    # ---- 1) Breakpoints ----
    cyc_breakpoints    = [0, 0.025, 0.05, 0.075, 0.1, 0.125, 0.15, 0.175, 0.2, 0.225, 0.25]  
    stress_breakpoints = [0.0, 1.0, 2.0, 3.0, 4.0]   # 4 Segmente für STRESS

    # ---- 2) Globale Bounds holen ----
    xL_glob, xU_glob = get_global_bounds(model.v_CYCLES, model.T)
    yL_glob, yU_glob = get_global_bounds(model.v_STRESS, model.T)
    zL_glob, zU_glob = 0.0, xU_glob * yU_glob   # falls passend

    # Konsistenzcheck: Breakpoints müssen die globalen Bounds überdecken
    assert cyc_breakpoints[0]    <= xL_glob + 1e-9 and cyc_breakpoints[-1]    >= xU_glob - 1e-9, \
        "x-Bounds liegen außerhalb der Breakpoints"
    assert stress_breakpoints[0] <= yL_glob + 1e-9 and stress_breakpoints[-1] >= yU_glob - 1e-9, \
        "y-Bounds liegen außerhalb der Breakpoints"

    # ---- 3) Indexmengen ----
    I = range(len(cyc_breakpoints) - 1)      # x-Segmente
    J = range(len(stress_breakpoints) - 1)   # y-Segmente
    model.CYC_SEG    = pyo.Set(initialize=I)
    model.STRESS_SEG = pyo.Set(initialize=J)

    # ---- 4) Binärvariablen für Kacheln ----
    model.b_cell = pyo.Var(model.T, model.CYC_SEG, model.STRESS_SEG, within=pyo.Binary)

    # pro t genau eine aktive Kachel
    def one_cell_rule(m, t):
        return sum(m.b_cell[t,i,j] for i in m.CYC_SEG for j in m.STRESS_SEG) == 1
    model.one_cell = pyo.Constraint(model.T, rule=one_cell_rule)

    # ---- 5) x,y in aktiver Kachel einsperren ----
    def x_lb_rule(m, t):
        return m.v_CYCLES[t] >= sum(cyc_breakpoints[i]   * m.b_cell[t,i,j]
                                    for i in m.CYC_SEG for j in m.STRESS_SEG)
    def x_ub_rule(m, t):
        return m.v_CYCLES[t] <= sum(cyc_breakpoints[i+1] * m.b_cell[t,i,j]
                                    for i in m.CYC_SEG for j in m.STRESS_SEG)
    def y_lb_rule(m, t):
        return m.v_STRESS[t] >= sum(stress_breakpoints[j]   * m.b_cell[t,i,j]
                                    for i in m.CYC_SEG for j in m.STRESS_SEG)
    def y_ub_rule(m, t):
        return m.v_STRESS[t] <= sum(stress_breakpoints[j+1] * m.b_cell[t,i,j]
                                    for i in m.CYC_SEG for j in m.STRESS_SEG)

    model.x_in_cell_lb = pyo.Constraint(model.T, rule=x_lb_rule)
    model.x_in_cell_ub = pyo.Constraint(model.T, rule=x_ub_rule)
    model.y_in_cell_lb = pyo.Constraint(model.T, rule=y_lb_rule)
    model.y_in_cell_ub = pyo.Constraint(model.T, rule=y_ub_rule)

    # ---- 6) McCormick je Kachel ----
    def mc1_rule(m, t, i, j):
        xL = cyc_breakpoints[i]     ; xU = cyc_breakpoints[i+1]
        yL = stress_breakpoints[j]  ; yU = stress_breakpoints[j+1]
        M = (xU_glob - xL_glob)*yU_glob + (yU_glob - yL_glob)*xU_glob + abs(xU_glob*yU_glob) + 1.0

        return m.v_CYCLES_EQ[t] >= xL*m.v_STRESS[t] + yL*m.v_CYCLES[t] - xL*yL - M*(1 - m.b_cell[t,i,j])

    def mc2_rule(m, t, i, j):
        xL = cyc_breakpoints[i]     ; xU = cyc_breakpoints[i+1]
        yL = stress_breakpoints[j]  ; yU = stress_breakpoints[j+1]
        M = (xU_glob - xL_glob)*yU_glob + (yU_glob - yL_glob)*xU_glob + abs(xU_glob*yU_glob) + 1.0
        return m.v_CYCLES_EQ[t] >= xU*m.v_STRESS[t] + yU*m.v_CYCLES[t] - xU*yU - M*(1 - m.b_cell[t,i,j])

    def mc3_rule(m, t, i, j):
        xL = cyc_breakpoints[i]     ; xU = cyc_breakpoints[i+1]
        yL = stress_breakpoints[j]  ; yU = stress_breakpoints[j+1]
        M = (xU_glob - xL_glob)*yU_glob + (yU_glob - yL_glob)*xU_glob + abs(xU_glob*yU_glob) + 1.0
        return m.v_CYCLES_EQ[t] <= xU*m.v_STRESS[t] + yL*m.v_CYCLES[t] - xU*yL + M*(1 - m.b_cell[t,i,j])

    def mc4_rule(m, t, i, j):
        xL = cyc_breakpoints[i]     ; xU = cyc_breakpoints[i+1]
        yL = stress_breakpoints[j]  ; yU = stress_breakpoints[j+1]
        M = (xU_glob - xL_glob)*yU_glob + (yU_glob - yL_glob)*xU_glob + abs(xU_glob*yU_glob) + 1.0
        return m.v_CYCLES_EQ[t] <= xL*m.v_STRESS[t] + yU*m.v_CYCLES[t] - xL*yU + M*(1 - m.b_cell[t,i,j])

    model.mc1 = pyo.Constraint(model.T, model.CYC_SEG, model.STRESS_SEG, rule=mc1_rule)
    model.mc2 = pyo.Constraint(model.T, model.CYC_SEG, model.STRESS_SEG, rule=mc2_rule)
    model.mc3 = pyo.Constraint(model.T, model.CYC_SEG, model.STRESS_SEG, rule=mc3_rule)
    model.mc4 = pyo.Constraint(model.T, model.CYC_SEG, model.STRESS_SEG, rule=mc4_rule)

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
