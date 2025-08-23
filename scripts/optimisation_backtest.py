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
import params.scenario_config1 as scenario_config1
from params.scenario_config1 import (
    START_DATE,
    END_DATE,
    INITIAL_BATTERY_CAPACITY,
)
from utils import get_params_as_dataframe
from cost_calculator import calculate_specific_aging_cost


def main_optimisation(df_data_period, initial_battery_capacity_for_year):
    model = setup_model(df_data_period, initial_battery_capacity_for_year)
    solve_model(model)
    print(f" profit: {pyo.value(model.OBJ)}")
    return model

# wir starten im 1. Jahr mit dem Anfangs-Batterie-Kapazität aus config. 
# Dann wird am Ende der Optimierung die neue Batterie-Kapazität gespeichert und als Startwert für das nächste Jahr verwendet.
# Wie Berechnet sich die neue Batterie-Kapazität? Wird innerhalb eines Jahres eine konstante Batterie Kapazität angenommen? 
def build_models_by_year(df_data: pd.DataFrame) -> Dict[int, object]:
    current_start_battery_capacity = INITIAL_BATTERY_CAPACITY
    models_by_year = {}
    for year_timestamp, df_data_year in df_data.groupby(pd.Grouper(freq='YE')):
        if df_data_year.empty:
            continue

        year = year_timestamp.year
        print(f"Baue Modell für Jahr {year} ({df_data_year.index[0].date()} bis {df_data_year.index[-1].date()})")
        #measure
        start_time = time.time()
        model_year = main_optimisation(df_data_year, current_start_battery_capacity)
        print(f"{year}:  {time.time() - start_time:.2f} Sekunden")
        models_by_year[year] = model_year
        final_battery_capacity_of_year = pyo.value(model_year.v_BATTERY_CAPACITY[model_year.T.last()])
        current_start_battery_capacity = final_battery_capacity_of_year

    return models_by_year


if __name__ == "__main__":
    specific_aging_cost = calculate_specific_aging_cost()
    df = create_dataframe(START_DATE, END_DATE, specific_aging_cost, debug=False)
    models_by_year = build_models_by_year(df)

    df_timeseries = add_model_timeseries_results_to_df(df, models_by_year)
    df_attrs = add_model_atrs_results_to_df(models_by_year)

    #print(df_timeseries)
    print(df_attrs)
    params_data = get_params_as_dataframe(scenario_config1)
    export_results(df_timeseries, df_attrs, params_data)



