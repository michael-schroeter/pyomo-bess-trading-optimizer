from pathlib import Path
import pandas as pd
import pickle
from utils import convert_datetime_to_string 
from config import (
    RESULTS_DIR
)
from .filename_creator import create_random_filename

def export_results(df_timeseries: pd.DataFrame,
                   df_attrs: pd.DataFrame,
                   df_params: pd.DataFrame,  # <-- Akzeptiert jetzt einen DataFrame
                   results_dir: Path = RESULTS_DIR,
                   ):
    filename = create_random_filename()
    excel_path = results_dir / (f"{filename}.xlsx")
    pickle_path = results_dir / (f"{filename}.pkl")
    params_dict_for_pickle = df_params.set_index('Parameter')['Value'].to_dict()

    export_to_pickle(df_timeseries, df_attrs, params_dict_for_pickle, pickle_path)
    export_to_excel(df_timeseries, df_attrs, df_params, excel_path) # <-- Übergibt den DF


def export_to_pickle(df_timeseries: pd.DataFrame,
                     df_attrs: pd.DataFrame,
                     param_data: dict, 
                     path: Path):

    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        'timeseries': df_timeseries,
        'attributes': df_attrs,
        'config': param_data  
    }
    with open(path, 'wb') as f:
        pickle.dump(payload, f)


def export_to_excel(df_timeseries: pd.DataFrame,
                    df_attrs: pd.DataFrame,
                    df_params: pd.DataFrame,  # <-- Akzeptiert jetzt einen DataFrame
                    path: Path):

    path.parent.mkdir(parents=True, exist_ok=True)
    df_ts_fmt = convert_datetime_to_string(df_timeseries)

    # DIESE ZEILE WIRD ENTFERNT, da df_params schon fertig ist.
    # df_params = pd.DataFrame(list(param_data.items()), columns=['Parameter', 'Value'])

    with pd.ExcelWriter(path, engine='xlsxwriter') as writer:
        df_ts_fmt.to_excel(writer, sheet_name='Data')
        df_attrs.to_excel(writer, sheet_name='Attributes', index=True)
        # Schreibt den fertigen DataFrame mit allen drei Spalten direkt in die Excel-Datei.
        df_params.to_excel(writer, sheet_name='Params', index=False)