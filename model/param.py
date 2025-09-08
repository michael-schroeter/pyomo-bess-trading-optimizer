import pyomo.environ as pyo
from typing import Mapping, Any
from config_column_names import ColumnNamesClean as CC
from cost_calculator import calculate_opex_per_month, calculate_depreciation_amount_per_month, calculate_specific_aging_cost
from params.scenario_config import MAX_CHARGE_RATE, SYSTEM_POWER, INITIAL_BATTERY_CAPACITY
from config_degradation import SOC_FACTORS, BATTERY_DEGRADATION_CAL_VALUE, EFFICIENCY_DEGRADATION_CAL_VALUE

def define_params(model: pyo.ConcreteModel, df_data_period, initial_battery_capacity_for_year, initial_cycles, initial_cycles_eq, initial_efficiency, initial_stored_energy) -> None:
    
    #market prices
    higher_market_price_dict = df_data_period[CC.HiGHER_MARKET_PRICE].to_dict()
    higher_market_price_label_dict = df_data_period[CC.HiGHER_MARKET_PRICE_LABEL].to_dict()
    lower_market_price_dict = df_data_period[CC.LOWER_MARKET_PRICE].to_dict()
    lower_market_price_label_dict = df_data_period[CC.LOWER_MARKET_PRICE_LABEL].to_dict()

    #PRL and SRL prices
    prl_price_dict = df_data_period[CC.PRL_PRICE].to_dict()
    srl_power_price_neg_dict = df_data_period[CC.SRL_POWER_PRICE_NEG].to_dict()
    srl_power_price_pos_dict = df_data_period[CC.SRL_POWER_PRICE_POS].to_dict()
    srl_work_price_neg_dict = df_data_period[CC.SRL_NEG_WORK_CBMP].to_dict()
    srl_work_price_pos_dict = df_data_period[CC.SRL_POS_WORK_CBMP].to_dict()

    
    # prices
    model.p_HIGHER_MARKET_PRICE = pyo.Param(model.T, initialize=higher_market_price_dict)
    model.p_LOWER_MARKET_PRICE = pyo.Param(model.T, initialize=lower_market_price_dict)
    model.p_HIGHER_MARKET_PRICE_LABEL = pyo.Param(model.T, initialize=higher_market_price_label_dict, within=pyo.Any)
    model.p_LOWER_MARKET_PRICE_LABEL  = pyo.Param(model.T, initialize=lower_market_price_label_dict,  within=pyo.Any)

    model.p_PRLPRICE    = pyo.Param(model.T, initialize=prl_price_dict)
    model.p_SRL_PRICE_NEG = pyo.Param(model.T, initialize=srl_power_price_neg_dict)
    model.p_SRL_PRICE_POS = pyo.Param(model.T, initialize=srl_power_price_pos_dict)
    model.p_SRL_WORK_PRICE_NEG = pyo.Param(model.T, initialize=srl_work_price_neg_dict)
    model.p_SRL_WORK_PRICE_POS = pyo.Param(model.T, initialize=srl_work_price_pos_dict)

    model.p_OPEX = pyo.Param(initialize=calculate_opex_per_month())
    model.p_DEPRECIATION_AMOUNT = pyo.Param(initialize=calculate_depreciation_amount_per_month()) 
    model.p_SPECIFIC_AGING_COST = pyo.Param(initialize=calculate_specific_aging_cost())

    # initial values
    model.p_INITIAL_BATTERY_CAPACITY = pyo.Param(initialize=initial_battery_capacity_for_year) # kommt aus der main und ergibt sich aus der End Batterie-Kapazität des Vorjahres
    model.p_INITIAL_EFFICIENCY = pyo.Param(initialize=initial_efficiency) 
    model.p_INITIAL_CYCLES = pyo.Param(initialize=initial_cycles)
    model.p_INITIAL_CYCLES_EQ = pyo.Param(initialize=initial_cycles_eq) 
    model.p_INITIAL_STORED_ENERGY = pyo.Param(initialize=initial_stored_energy)

    # degradation
    model.p_DEGRADATION_CAL = pyo.Param(initialize=BATTERY_DEGRADATION_CAL_VALUE)
    model.p_MAX_THROUGHPUT = pyo.Param(initialize=MAX_CHARGE_RATE)
    model.p_SOC_FACTORS = pyo.Param(model.K, initialize=SOC_FACTORS)

    model.p_C_RATE = pyo.Param(initialize=SYSTEM_POWER / INITIAL_BATTERY_CAPACITY)
    

