import time
import pandas as pd
from utils import convert_datetime_to_string
from params.scenario_config1 import (
    START_DATE,
    END_DATE,
)
from config_column_names import ColumnNamesRaw as CR,  ColumnNamesClean as CC
from dataloader import (

    load_compared_auc_data,
    load_prl_data,
    load_srl_power_data,
    load_srl_work_cbmp_data,

)
from cost_calculator import calculate_specific_aging_cost
import logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')


def create_dataframe(start_date, end_date, specific_aging_cost, debug=False):
    df_master = create_master_df(start_date, end_date)

    loader_tasks = [
        (load_compared_auc_data, ()),
        #(load_da_auc_data,      ()),
        #(load_id_auc_data,      ()),
        (load_prl_data,          ()),
        (load_srl_power_data,    ()),
        (load_srl_work_cbmp_data, (specific_aging_cost, )),
    ]

    for loader, args in loader_tasks:
        df = loader(*args)
        if debug:
            logging.debug(
                "Joining %s: %s bis %s (%d)",
                loader.__name__, df.index.min(), df.index.max(), len(df)
            )
        df_master = df_master.join(df, how="left")

    df_master.fillna(0, inplace=True)
    df_master.index.name = CC.DATE
    if debug:
        logging.info("Finaler Master-DataFrame: Shape=%s", df_master.shape)
    return df_master



def create_master_df(start_date, end_date):
    master_index = pd.date_range(start=start_date, end=end_date, freq='15min', tz='Europe/Berlin', inclusive='left')
    df = pd.DataFrame(index=master_index)
    return df


if __name__ == "__main__":
    # mesure time
    specific_aging_cost = calculate_specific_aging_cost()
    start_time = time.time()
    df = create_dataframe(START_DATE, END_DATE, specific_aging_cost, debug=False)
    print(f"Berechnungszeit: {round(time.time() - start_time, 1)} Sekunden")
    print(df)
    print(len(df))
    # to excel

    formated_df = convert_datetime_to_string(df)       
    formated_df.to_excel("data/market price data.xlsx", index=True, sheet_name="Market Price Data")
