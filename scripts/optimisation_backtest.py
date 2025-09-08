import logging
logging.getLogger('pyomo').setLevel(logging.WARNING)

import time
import pandas as pd
from typing import Dict
import pyomo.environ as pyo
from model.model_builder import setup_model, solve_model
from result_processing.pyomo_extractor import add_model_timeseries_results_to_df, add_model_atrs_results_to_df
from result_processing.result_export import export_results
from scripts.dataloader_pipeline import create_dataframe
import params.scenario_config as scenario_config
from params.scenario_config import (
    START_DATE,
    END_DATE,
    INITIAL_BATTERY_CAPACITY,
    EFFICIENCY_SYS,
    SYSTEM_POWER
)
from utils import get_params_as_dataframe
from cost_calculator import calculate_specific_aging_cost


def main_optimisation(df_data_period, initial_battery_capacity_for_year, initial_cycles, initial_cycles_eq, initial_efficiency, initial_stored_energy):
    model = setup_model(df_data_period, initial_battery_capacity_for_year, initial_cycles, initial_cycles_eq, initial_efficiency, initial_stored_energy)
    solve_model(model)
    print(f" profit: {pyo.value(model.OBJ)}")
    return model

# wir starten im 1. Jahr mit dem Anfangs-Batterie-Kapazität aus config. 
# Dann wird am Ende der Optimierung die neue Batterie-Kapazität gespeichert und als Startwert für das nächste Jahr verwendet.
# Genauso mit Cyclen_sum
def build_models_by_period(df_data: pd.DataFrame) -> Dict[int, object]:
    current_start_battery_capacity = INITIAL_BATTERY_CAPACITY
    current_start_efficiency = EFFICIENCY_SYS
    current_start_cycles = 0
    current_start_cycles_eq = 0
    current_start_stored_energy = 0
    models_by_year = {}
    for year_timestamp, df_data_year in df_data.groupby(pd.Grouper(freq='ME')):
        if df_data_year.empty:
            continue

        key = (year_timestamp.year, year_timestamp.month)
        print(f"Baue Modell für Jahr {key} ({df_data_year.index[0].date()} bis {df_data_year.index[-1].date()})")
        #measure
        start_time = time.time()
        model_year = main_optimisation(df_data_year, current_start_battery_capacity, current_start_cycles, current_start_cycles_eq, current_start_efficiency, current_start_stored_energy)
        print(f"{key}:  {time.time() - start_time:.2f} Sekunden")
        models_by_year[key] = model_year
        
        final_battery_capacity_of_year = pyo.value(model_year.v_BATTERY_CAPACITY[model_year.T.last()])
        current_start_battery_capacity = final_battery_capacity_of_year

        if final_battery_capacity_of_year <= 0.8 * INITIAL_BATTERY_CAPACITY:
            break

        final_efficiency_of_year = pyo.value(model_year.v_EFFICIENCY_SYS[model_year.T.last()])
        current_start_efficiency = final_efficiency_of_year

        final_cycles_of_year = pyo.value(model_year.v_CYCLES_CUMSUM[model_year.T.last()])
        current_start_cycles = final_cycles_of_year
        
        final_cycles_eq_of_year = pyo.value(model_year.v_CYCLES_EQ_CUMSUM[model_year.T.last()])
        current_start_cycles_eq = final_cycles_eq_of_year

        final_stored_energy_of_period = pyo.value(model_year.v_STORED_ENERGY[model_year.T.last()])
        current_start_stored_energy = final_stored_energy_of_period

    return models_by_year


if __name__ == "__main__":
    specific_aging_cost = calculate_specific_aging_cost()
    df = create_dataframe(START_DATE, END_DATE, specific_aging_cost, debug=False)
    start_time = time.time()
    models_by_year = build_models_by_period(df)
    time_delta = time.time() - start_time

    df_timeseries = add_model_timeseries_results_to_df(df, models_by_year)
    df_attrs = add_model_atrs_results_to_df(models_by_year)

    #print(df_timeseries)
    print(df_attrs)
    params_data = get_params_as_dataframe(scenario_config)
    params_data.loc[0, 'Berechnungszeit Sekunden'] = time_delta
    params_data.loc[0, 'Berechnungszeit Minuten'] = time_delta/60
    params_data.loc[0, 'Berechnungszeit Stunden'] = time_delta/60/60

    c_rate = round(SYSTEM_POWER / INITIAL_BATTERY_CAPACITY, 3)
    export_results(df_timeseries, df_attrs, params_data, c_rate)



