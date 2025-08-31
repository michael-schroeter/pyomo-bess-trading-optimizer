import pyomo.environ as pyo


def add_stress_constraint(model):

    soc_breakpoints = [0.5, 0.8, 1.1, 1.4, 1.7, 2.0]
    power_breakpoints = [0.8, 1.2, 1.6, 2.0, 2.5, 3.0]
    def f_stress(m, t, soc_stress, power_stress):
        return soc_stress * power_stress

    # Erstellen der Constraint. Sie wird für jeden Zeitschritt t erstellt.
    model.c_stress_multiplication = pyo.Piecewise(
        model.T,                               # Index-Set (für jeden Zeitschritt)
        model.v_STRESS,                        # Output-Variable (z)
        model.v_SOC_STRESS_FACTOR,             # 1. Input-Variable (x)
        model.v_POWER_STRESS_FACTOR,           # 2. Input-Variable (y)
        pw_ptsx=soc_breakpoints,               # Breakpoints für x
        pw_ptsy=power_breakpoints,             # Breakpoints für y
        pw_repn='SOS2',                        # 'SOS2' ist eine gängige und gute Wahl
        f_rule=f_stress                        # Die Funktion, die approximiert wird
    )
    return model

def add_soc_stress_factor_constraint(model):

    tangents_as_tuples_soc = [(0.00784, 1.3137), (-0.000784, 1.0490), (0.02431, -0.5196)] # sehe kommentar unten
    model.I_SOC_TANGENTS = pyo.RangeSet(0, len(tangents_as_tuples_soc) - 1)
    def soc_stress_factor_rule(m, i, t):
        tangent = tangents_as_tuples_soc[i]
        mi = tangent[0]
        ni = tangent[1]
        return m.v_SOC_STRESS_FACTOR[t] >= mi * m.e_APPROX_SOC[t] + ni
    model.c_soc_stress_factor = pyo.Constraint(model.I_SOC_TANGENTS, model.T, rule=soc_stress_factor_rule)


def add_power_stress_factor_constraint(model, tangents_as_tuples_power):
    model.I_POWER_TANGENTS = pyo.RangeSet(0, len(tangents_as_tuples_power) - 1)
    def power_stress_factor_rule(m, i, t):
        tangent = tangents_as_tuples_power[i]
        mi = tangent[0]
        ni = tangent[1]

        throughput = m.e_TOTAL_CHARGE[t] + m.e_TOTAL_DISCHARGE[t] # als c rate
        return m.v_POWER_STRESS_FACTOR[t] >= mi * throughput + ni
    model.c_power_stress_factor = pyo.Constraint(model.I_POWER_TANGENTS, model.T, rule=power_stress_factor_rule)

"""
0% bis 37,5% SOC: Die Funktion, die die Punkte (12,5 | 1,216) und (37,5 | 1,020) verbindet, wird bis zu 0% extrapoliert.
y=−0,00784x+1,3137
37,5% bis 62,5% SOC: Diese Funktion verbindet die Punkte (37,5 | 1,020) und (62,5 | 1,0).
y=−0,000784x+1,0490
62,5% bis 100% SOC: Die Funktion, die die Punkte (62,5 | 1,0) und (87,5 | 1,608) verbindet, wird bis zu 100% extrapoliert.
y=0,02431x−0,5196
"""