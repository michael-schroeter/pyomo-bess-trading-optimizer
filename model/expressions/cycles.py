import pyomo.environ as pyo

def add_cycles_real_markets_expr(model):
    def cycles_real_spot_rule(m, t):
        return  (m.e_MARKET_CHARGE[t] + m.e_MARKET_DISCHARGE[t] ) / (2 * m.p_INITIAL_BATTERY_CAPACITY)
    model.e_CYCLES_REAL_MARKET = pyo.Expression(model.T, rule=cycles_real_spot_rule)

    def cycles_real_intraday_rule(m, t):
        charge = 0
        discharge = 0
        if m.p_HIGHER_MARKET_PRICE_LABEL[t] == 'ID':
            discharge = m.e_MARKET_DISCHARGE[t]
        if m.p_LOWER_MARKET_PRICE_LABEL[t] == 'ID':
            charge = m.e_MARKET_CHARGE[t]
        return (charge + discharge) / (2 * m.p_INITIAL_BATTERY_CAPACITY)
    model.e_CYCLES_REAL_INTRADAY = pyo.Expression(model.T, rule=cycles_real_intraday_rule)

    def cycles_days_ahead_rule(m, t):
        charge = 0
        discharge = 0
        if m.p_HIGHER_MARKET_PRICE_LABEL[t] == 'DA':
            discharge = m.e_MARKET_DISCHARGE[t]
        if m.p_LOWER_MARKET_PRICE_LABEL[t] == 'DA':
            charge = m.e_MARKET_CHARGE[t]
        return (charge + discharge) / (2 * m.p_INITIAL_BATTERY_CAPACITY)
    model.e_CYCLES_REAL_DA = pyo.Expression(model.T, rule=cycles_days_ahead_rule)


    def cycles_real_prl_rule(m, t):
        return  (m.e_PRL_CHARGE[t] + m.e_PRL_DISCHARGE[t] ) / (2 * m.p_INITIAL_BATTERY_CAPACITY)
    model.e_CYCLES_REAL_PRL = pyo.Expression(model.T, rule=cycles_real_prl_rule)

    def cycles_real_srl_pos_rule(m, t):
        return  (m.e_SRL_POS_DISCHARGE[t] ) / (2 * m.p_INITIAL_BATTERY_CAPACITY)
    model.e_CYCLES_REAL_SRL_POS = pyo.Expression(model.T, rule=cycles_real_srl_pos_rule)

    def cycles_real_srl_neg_rule(m, t):
        return  (m.e_SRL_NEG_CHARGE[t] ) / (2 * m.p_INITIAL_BATTERY_CAPACITY)
    model.e_CYCLES_REAL_SRL_NEG = pyo.Expression(model.T, rule=cycles_real_srl_neg_rule)

    def cycles_real_srl_total_rule(m, t):
        return  m.e_CYCLES_REAL_SRL_NEG[t] + m.e_CYCLES_REAL_SRL_POS[t]
    model.e_CYCLES_REAL_SRL = pyo.Expression(model.T, rule=cycles_real_srl_total_rule)

