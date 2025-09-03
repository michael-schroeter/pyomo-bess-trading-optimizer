import pyomo.environ as pyo
from params.scenario_config1 import (
    SYSTEM_POWER,
    CHARGE_RATE,
    INITIAL_BATTERY_CAPACITY,
    LIFETIME_CYCLES
)


def define_variables(model):
    # market
    model.v_BUY_VOL  = pyo.Var(model.T, within=pyo.NonNegativeReals, bounds=(0, CHARGE_RATE))
    model.v_SELL_VOL = pyo.Var(model.T, within=pyo.NonNegativeReals, bounds=(0, CHARGE_RATE))

    # prl and srl
    model.v_PRL_POWER   = pyo.Var(model.D4, within=pyo.NonNegativeReals, bounds=(0, SYSTEM_POWER))
    model.v_SRL_POWER_NEG = pyo.Var(model.D4, within=pyo.NonNegativeReals, bounds=(0, SYSTEM_POWER))
    model.v_SRL_POWER_POS = pyo.Var(model.D4, within=pyo.NonNegativeReals, bounds=(0, SYSTEM_POWER))

    model.v_STORED_ENERGY = pyo.Var(model.T, within=pyo.NonNegativeReals, bounds=(0, INITIAL_BATTERY_CAPACITY*2))

    # Ccles
    model.v_CYCLES = pyo.Var(model.T, domain=pyo.NonNegativeReals, bounds=(0, CHARGE_RATE / (INITIAL_BATTERY_CAPACITY * 2)*2))
    model.v_CYCLES_EQ = pyo.Var(model.T, domain=pyo.NonNegativeReals, bounds=(0, 4 * CHARGE_RATE / (INITIAL_BATTERY_CAPACITY * 2)*2)) 
    model.v_CYCLES_CUMSUM = pyo.Var(model.T, domain=pyo.NonNegativeReals, bounds=(0, LIFETIME_CYCLES * 1.5))
    model.v_CYCLES_EQ_CUMSUM = pyo.Var(model.T, domain=pyo.NonNegativeReals, bounds=(0, LIFETIME_CYCLES * 1.5))

    # Degradation
    model.v_REST_CAPACITY_CYCLE = pyo.Var(model.T, domain=pyo.NonNegativeReals, bounds=(0.7 * INITIAL_BATTERY_CAPACITY, INITIAL_BATTERY_CAPACITY))
    model.v_BATTERY_CAPACITY = pyo.Var(model.T, within=pyo.NonNegativeReals, bounds=(0.7 * INITIAL_BATTERY_CAPACITY, INITIAL_BATTERY_CAPACITY)) 
    model.v_X_BIN = pyo.Var(model.T, model.K, domain=pyo.NonNegativeReals)

    model.v_EFFICIENCY = pyo.Var(model.T, within=pyo.NonNegativeReals, bounds=(0.7, 1.0))

    model.v_TAX_BASE  = pyo.Var(domain=pyo.NonNegativeReals, bounds=(0, 1e7))
