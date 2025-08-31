import pandas as pd
import pyomo.environ as pyo
from config_column_names import ColumnNamesClean as CC



import pandas as pd
import pyomo.environ as pyo


def add_model_timeseries_results_to_df(template_df, models_by_year):
    column_extractor_map = {
        CC.BUY_VOL:  lambda m, t: m.v_BUY_VOL[t],
        CC.SELL_VOL: lambda m, t: m.v_SELL_VOL[t],
        CC.PRL_POWER:       lambda m, t: m.e_PRL_POWER[t],
        CC.SRL_POWER_NEG:   lambda m, t: m.e_SRL_POWER_NEG[t],
        CC.SRL_POWER_POS:   lambda m, t: m.e_SRL_POWER_POS[t],
        #CC.BAT_SOC:         lambda m, t: m.v_BAT_SOC[t],
        CC.MARKET_CHARGE:    lambda m, t: m.e_MARKET_CHARGE[t],
        CC.MARKET_DISCHARGE: lambda m, t: m.e_MARKET_DISCHARGE[t],
        CC.PRL_CHARGE:     lambda m, t: m.e_PRL_CHARGE[t],
        CC.PRL_DISCHARGE:  lambda m, t: m.e_PRL_DISCHARGE[t],
        CC.SRL_NEG_CHARGE: lambda m, t: m.e_SRL_NEG_CHARGE[t],
        CC.SRL_POS_DISCHARGE: lambda m, t: m.e_SRL_POS_DISCHARGE[t],
        CC.TOTAL_CHARGE:           lambda m, t: m.e_TOTAL_CHARGE[t],
        CC.TOTAL_DISCHARGE:        lambda m, t: m.e_TOTAL_DISCHARGE[t],
        CC.REVENUE_MARKET:  lambda m, t: m.e_REVENUE_MARKET[t],
        CC.REVENUE_PRL:     lambda m, t: m.e_REVENUE_PRL[t],
        CC.REVENUE_SRL:     lambda m, t: m.e_REVENUE_SRL[t],
        CC.REVENUE_TOTAL:   lambda m, t: m.e_TOTAL_REVENUE[t],
        CC.AGING_COST:      lambda m, t: m.e_AGING_COST[t],
        'BATTERY_CAPACITY': lambda m, t: m.v_BATTERY_CAPACITY[t],
    }

    model_results_timeseries = {}
    for year, model in models_by_year.items():
        for t in model.T:
            model_results_timeseries[t] = {col: pyo.value(fn(model, t)) for col, fn in column_extractor_map.items()}

    results_timeseries_df = pd.DataFrame.from_dict(model_results_timeseries, orient='index')
    combined_df = pd.concat([template_df, results_timeseries_df], axis=1)
    return combined_df


def add_model_atrs_results_to_df(models_by_year):
    attrs = {
        #market/regelleistung
        CC.BUY_VOL_SUM: lambda m: pyo.value(sum(m.v_BUY_VOL[t] for t in m.T)),
        CC.SELL_VOL_SUM: lambda m: pyo.value(sum(m.v_SELL_VOL[t] for t in m.T)),
        CC.PRL_POWER_SUM: lambda m: pyo.value(sum(m.e_PRL_POWER[t] for t in m.T)),
        CC.SRL_POWER_NEG_SUM: lambda m: pyo.value(sum(m.e_SRL_POWER_NEG[t] for t in m.T)),
        CC.SRL_POWER_POS_SUM: lambda m: pyo.value(sum(m.e_SRL_POWER_POS[t] for t in m.T)),

        #Money
        CC.AGING_COST_SUM: lambda m: pyo.value(m.e_AGING_COST_SUM),
        CC.REVENUE_MARKET_SUM: lambda m: pyo.value(m.e_REVENUE_MARKET_SUM),
        CC.REVENUE_PRL_SUM: lambda m: pyo.value(m.e_REVENUE_PRL_SUM),
        CC.REVENUE_SRL_SUM: lambda m: pyo.value(m.e_REVENUE_SRL_SUM),
        CC.REVENUE_TOTAL_SUM: lambda m: pyo.value(m.e_TOTAL_REVENUE_SUM),
        CC.TAXES_SUM: lambda m: pyo.value(m.e_TAX),
        CC.OBJ: lambda m: pyo.value(m.OBJ),
        'NET_CASHFLOW': lambda m: pyo.value(m.e_NET_CASHFLOW),

        #charge/discharge
        CC.MARKET_CHARGE_SUM: lambda m: pyo.value(m.e_MARKET_CHARGE_SUM),
        CC.MARKET_DISCHARGE_SUM: lambda m: pyo.value(m.e_MARKET_DISCHARGE_SUM),
        CC.PRL_CHARGE_SUM: lambda m: pyo.value(m.e_PRL_CHARGE_SUM),
        CC.PRL_DISCHARGE_SUM: lambda m: pyo.value(m.e_PRL_DISCHARGE_SUM),
        CC.SRL_NEG_CHARGE_SUM: lambda m: pyo.value(m.e_SRL_NEG_CHARGE_SUM),
        CC.SRL_POS_DISCHARGE_SUM: lambda m: pyo.value(m.e_SRL_POS_DISCHARGE_SUM),
        CC.TOTAL_CHARGE_SUM: lambda m: pyo.value(m.e_TOTAL_CHARGE_SUM),
        CC.TOTAL_DISCHARGE_SUM: lambda m: pyo.value(m.e_TOTAL_DISCHARGE_SUM),
        #CC.BATTERY_CYCLES: lambda m: pyo.value(m.e_BATTERY_CYCLES),
        

    }

    data = {}
    for year, model in models_by_year.items():
        data[year] = {name: fn(model) for name, fn in attrs.items()}

    df_attrs = pd.DataFrame.from_dict(data, orient='index')
    df_attrs.index.name = 'Year'
    
    return df_attrs




