import pyomo.environ as pyo
from params.scenario_config1 import (
    SYSTEM_POWER,
    INITIAL_BATTERY_CAPACITY,
    LIFETIME_CYCLES,
    EFFICIENCY_BAT,
    EFFICIENCY_REST,
    MAX_CHARGE_RATE,
    MAX_CYCLE_RATE
)


def define_variables(model):
    # market
    model.v_BUY_VOL  = pyo.Var(model.T, within=pyo.NonNegativeReals, bounds=(0, MAX_CHARGE_RATE))
    model.v_SELL_VOL = pyo.Var(model.T, within=pyo.NonNegativeReals, bounds=(0, MAX_CHARGE_RATE))

    # prl and srl
    model.v_PRL_POWER   = pyo.Var(model.D4, within=pyo.NonNegativeReals, bounds=(0, SYSTEM_POWER))
    model.v_SRL_POWER_NEG = pyo.Var(model.D4, within=pyo.NonNegativeReals, bounds=(0, SYSTEM_POWER))
    model.v_SRL_POWER_POS = pyo.Var(model.D4, within=pyo.NonNegativeReals, bounds=(0, SYSTEM_POWER))

    model.v_STORED_ENERGY = pyo.Var(model.T, within=pyo.NonNegativeReals, bounds=(0, INITIAL_BATTERY_CAPACITY))

    # Cyles
    model.v_CYCLES = pyo.Var(model.T, domain=pyo.NonNegativeReals, bounds=(0, MAX_CYCLE_RATE))
    model.v_CYCLES_EQ = pyo.Var(model.T, domain=pyo.NonNegativeReals, bounds=(0, MAX_CYCLE_RATE* 1.6)) #1.6 ist der maximale SOC Bin Faktor
    model.v_CYCLES_CUMSUM = pyo.Var(model.T, domain=pyo.NonNegativeReals, bounds=(0, LIFETIME_CYCLES * 2))
    model.v_CYCLES_EQ_CUMSUM = pyo.Var(model.T, domain=pyo.NonNegativeReals, bounds=(0, LIFETIME_CYCLES * 2))

    # Degradation
    model.v_CYCLE_PER_SOC_BIN = pyo.Var(model.T, model.K, domain=pyo.NonNegativeReals, bounds=(0, MAX_CYCLE_RATE))
    model.v_SOC_BIN_ACTIVE = pyo.Var(model.T, model.K, domain=pyo.Binary)

    model.v_REST_CAPACITY_CYCLE = pyo.Var(model.T, domain=pyo.NonNegativeReals, bounds=(0.8 * INITIAL_BATTERY_CAPACITY, INITIAL_BATTERY_CAPACITY))
    model.v_BATTERY_CAPACITY = pyo.Var(model.T, within=pyo.NonNegativeReals, bounds=(0.8 * INITIAL_BATTERY_CAPACITY, INITIAL_BATTERY_CAPACITY)) 

    model.v_EFFICIENCY_SYS = pyo.Var(model.T, within=pyo.NonNegativeReals, bounds=(EFFICIENCY_BAT*0.95*EFFICIENCY_REST, EFFICIENCY_BAT * EFFICIENCY_REST))

    model.v_TAX_BASE  = pyo.Var(domain=pyo.NonNegativeReals, bounds=(0, 1e7))
