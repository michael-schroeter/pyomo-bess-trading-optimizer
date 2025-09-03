import pyomo.environ as pyo
from params.scenario_config1 import SYSTEM_POWER, EFFICIENCY_BAT


def add_srl_mode_constraints(model):
    """
    Fügt die Constraints für den semi-kontinuierlichen SRL-Modus hinzu.
    Logik:
    - v_MODE_SRL ist der Hauptschalter.
    - Wenn v_MODE_SRL=1, kann  keine, eine oder beide Leistungen (POS oder NEG) aktiv sein.
    - Jede aktive Leistung muss >= 1 sein (keine Werte zwischen 0 und 1).
    """


    model.v_USE_POS = pyo.Var(model.D4, domain=pyo.Binary)
    model.v_USE_NEG = pyo.Var(model.D4, domain=pyo.Binary)


    def link_use_neg_to_mode_rule(m, d, q):
        iv = (d, q)
        return m.v_USE_NEG[iv] <= m.v_MODE_SRL[iv]
    model.c_srl_link_use_neg = pyo.Constraint(model.D4, rule=link_use_neg_to_mode_rule)

    def link_use_pos_to_mode_rule(m, d, q):
        iv = (d, q)
        return m.v_USE_POS[iv] <= m.v_MODE_SRL[iv]
    model.c_srl_link_use_pos = pyo.Constraint(model.D4, rule=link_use_pos_to_mode_rule)


    def neg_power_limit_rule(m, d, q):
        iv = (d, q)
        return m.v_SRL_POWER_NEG[iv] <= SYSTEM_POWER * m.v_USE_NEG[iv]
    model.c_srl_neg_upper_bound = pyo.Constraint(model.D4, rule=neg_power_limit_rule)


    def pos_power_limit_rule(m, d, q):
        iv = (d, q)
        return m.v_SRL_POWER_POS[iv] <= SYSTEM_POWER * m.v_USE_POS[iv]
    model.c_srl_pos_upper_bound = pyo.Constraint(model.D4, rule=pos_power_limit_rule)


    def neg_power_logic_rule(m, d, q):
        iv = (d, q)
        return m.v_SRL_POWER_NEG[iv] >= m.v_USE_NEG[iv] # minimum of 1MW if active
    model.c_srl_neg_lower_bound = pyo.Constraint(model.D4, rule=neg_power_logic_rule)


    def pos_power_logic_rule(m, d, q):
        iv = (d, q)
        return m.v_SRL_POWER_POS[iv] >= m.v_USE_POS[iv] # minimum of 1MW if active
    model.c_srl_pos_lower_bound = pyo.Constraint(model.D4, rule=pos_power_logic_rule)



    
def add_srl_energy_constraints(model):
    """
    Fügt die SOC-Constraints hinzu. Die Bedingung für ein 4h-Intervall
    basiert auf dem SOC des 15-Minuten-Zeitschritts davor.
    """
    
    model.interval_to_start_time = {
        iv: min(t for t, interval in model.time_to_interval.items() if interval == iv)
        for iv in model.D4
    }

    def energy_srl_pos_rule(m, d, q):
        iv = (d, q)
        start_t = m.interval_to_start_time[iv]
        relevant_t = start_t if start_t == m.T.first() else m.T.prev(start_t)
        required_energy = m.v_SRL_POWER_POS[iv] / EFFICIENCY_BAT
        return m.v_STORED_ENERGY[relevant_t] >= required_energy
    model.c_SRL_energy_pos = pyo.Constraint(model.D4, rule=energy_srl_pos_rule)

    def energy_srl_neg_rule(m, d, q):
        iv = (d, q)
        start_t = m.interval_to_start_time[iv]
        relevant_t = start_t if start_t == m.T.first() else m.T.prev(start_t) 
        required_headroom = m.v_SRL_POWER_NEG[iv] * EFFICIENCY_BAT 
        return m.v_STORED_ENERGY[relevant_t] <= m.v_BATTERY_CAPACITY[relevant_t] - required_headroom
       
    model.c_SRL_energy_neg = pyo.Constraint(model.D4, rule=energy_srl_neg_rule)