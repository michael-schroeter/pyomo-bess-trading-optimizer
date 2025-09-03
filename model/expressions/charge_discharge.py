import pyomo.environ as pyo
from params.scenario_config1 import (
    EFFICIENCY_BAT,
)
from config import SPECIFIC_PRL_ENERGY_NEED_15MIN

import pyomo.environ as pyo

def define_charge_discharge_expr(model):

    def market_charge(m, t):
        return m.v_BUY_VOL[t] * EFFICIENCY_BAT
    model.e_MARKET_CHARGE = pyo.Expression(model.T, rule=market_charge)
    model.e_MARKET_CHARGE_SUM = pyo.Expression(
        expr=sum(model.e_MARKET_CHARGE[t] for t in model.T)
    )

    def market_discharge(m, t):
        return m.v_SELL_VOL[t] / EFFICIENCY_BAT
    model.e_MARKET_DISCHARGE = pyo.Expression(model.T, rule=market_discharge)
    model.e_MARKET_DISCHARGE_SUM = pyo.Expression(
        expr=sum(model.e_MARKET_DISCHARGE[t] for t in model.T)
    )


    def prl_charge(m, t):
        return m.e_PRL_POWER[t] * SPECIFIC_PRL_ENERGY_NEED_15MIN / 2 * EFFICIENCY_BAT
    model.e_PRL_CHARGE = pyo.Expression(model.T, rule=prl_charge)
    model.e_PRL_CHARGE_SUM = pyo.Expression(
        expr=sum(model.e_PRL_CHARGE[t] for t in model.T)
    )


    def prl_discharge(m, t):
        return m.e_PRL_POWER[t] * SPECIFIC_PRL_ENERGY_NEED_15MIN / 2 / EFFICIENCY_BAT
    model.e_PRL_DISCHARGE = pyo.Expression(model.T, rule=prl_discharge)
    model.e_PRL_DISCHARGE_SUM = pyo.Expression(
        expr=sum(model.e_PRL_DISCHARGE[t] for t in model.T)
    )


    def srl_neg_charge(m, t):
        if m.p_SRL_WORK_PRICE_NEG[t] != 0:
            return m.e_SRL_POWER_NEG[t] * 15/60 * EFFICIENCY_BAT # MW * 15 minutes/60 minutes
        else:
            return 0
    model.e_SRL_NEG_CHARGE = pyo.Expression(model.T, rule=srl_neg_charge)
    model.e_SRL_NEG_CHARGE_SUM = pyo.Expression(
        expr=sum(model.e_SRL_NEG_CHARGE[t] for t in model.T)
    )


    def srl_pos_discharge(m, t):
        if m.p_SRL_WORK_PRICE_POS[t] != 0:
            return m.e_SRL_POWER_POS[t] * 15/60  / EFFICIENCY_BAT # MW * 15 minutes/60 minutes
        else:
            return 0
    model.e_SRL_POS_DISCHARGE = pyo.Expression(model.T, rule=srl_pos_discharge)
    model.e_SRL_POS_DISCHARGE_SUM = pyo.Expression(
        expr=sum(model.e_SRL_POS_DISCHARGE[t] for t in model.T)
    )


    def total_charge(m, t):
        return (m.e_MARKET_CHARGE[t] + m.e_PRL_CHARGE[t] +
               m.e_SRL_NEG_CHARGE[t])
    model.e_TOTAL_CHARGE = pyo.Expression(model.T, rule=total_charge)
    model.e_TOTAL_CHARGE_SUM = pyo.Expression(
        expr=sum(model.e_TOTAL_CHARGE[t] for t in model.T)
    )

    def total_discharge(m, t):
        return (m.e_MARKET_DISCHARGE[t] + m.e_PRL_DISCHARGE[t] +
                 m.e_SRL_POS_DISCHARGE[t]) 
    model.e_TOTAL_DISCHARGE = pyo.Expression(model.T, rule=total_discharge)
    model.e_TOTAL_DISCHARGE_SUM = pyo.Expression(
        expr=sum(model.e_TOTAL_DISCHARGE[t] for t in model.T)
    )