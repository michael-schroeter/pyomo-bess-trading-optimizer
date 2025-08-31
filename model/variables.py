import pyomo.environ as pyo
from params.scenario_config1 import (
    SYSTEM_POWER,
    CHARGE_RATE,
    INITIAL_BATTERY_CAPACITY,
)


def define_variables(model):
    # market
    model.v_BUY_VOL  = pyo.Var(model.T, within=pyo.NonNegativeReals, bounds=(0, CHARGE_RATE))
    model.v_SELL_VOL = pyo.Var(model.T, within=pyo.NonNegativeReals, bounds=(0, CHARGE_RATE))

    model.v_STORED_ENERGY = pyo.Var(model.T, within=pyo.NonNegativeReals, bounds=(0, INITIAL_BATTERY_CAPACITY))
    # prl and srl
    model.v_PRL_POWER   = pyo.Var(model.D4, within=pyo.NonNegativeReals, bounds=(0, SYSTEM_POWER))
    model.v_SRL_POWER_NEG = pyo.Var(model.D4, within=pyo.NonNegativeReals, bounds=(0, SYSTEM_POWER))
    model.v_SRL_POWER_POS = pyo.Var(model.D4, within=pyo.NonNegativeReals, bounds=(0, SYSTEM_POWER))


    model.v_CYCLES = pyo.Var(model.T, domain=pyo.NonNegativeReals, bounds=(0, CHARGE_RATE / (INITIAL_BATTERY_CAPACITY * 2)))
    model.v_CYCLES_EQ = pyo.Var(model.T, domain=pyo.NonNegativeReals, bounds=(0, 4 * CHARGE_RATE / (INITIAL_BATTERY_CAPACITY * 2))) 
    model.v_CYCLES_CUMSUM = pyo.Var(model.T, domain=pyo.NonNegativeReals)
    model.v_CYCLES_EQ_CUMSUM = pyo.Var(model.T, domain=pyo.NonNegativeReals)

    model.v_SOC_STRESS_FACTOR = pyo.Var(model.T, domain=pyo.NonNegativeReals, bounds=(0, 4))
    model.v_POWER_STRESS_FACTOR = pyo.Var(model.T, domain=pyo.NonNegativeReals, bounds=(0.2, 4))
    model.v_STRESS = pyo.Var(model.T, domain=pyo.NonNegativeReals, bounds=(0, 4))

    model.v_DEGRADATION = pyo.Var(model.T, domain=pyo.NonNegativeReals, bounds=(0, 0.2))
    model.v_BATTERY_CAPACITY = pyo.Var(model.T, within=pyo.NonNegativeReals) 

    model.v_TAX_BASE  = pyo.Var(domain=pyo.NonNegativeReals)
