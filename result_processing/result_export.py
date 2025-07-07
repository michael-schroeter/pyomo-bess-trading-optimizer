from pathlib import Path
import pandas as pd
import pickle
from utils import convert_datetime_to_string 
from config import (
    RESULTS_DIR
)
from .filename_creator import create_unique_filename

def export_results(df_timeseries: pd.DataFrame,
                   df_attrs: pd.DataFrame,
                   config_data: dict,  
                   results_dir: Path = RESULTS_DIR,
                   excel_name: str = create_unique_filename() + '.xlsx',
                   pickle_name: str = create_unique_filename() + '.pkl'
                   ):

    excel_path = results_dir / excel_name
    pickle_path = results_dir / pickle_name

    export_to_pickle(df_timeseries, df_attrs, config_data, pickle_path)
    export_to_excel(df_timeseries, df_attrs, config_data, excel_path)


def export_to_pickle(df_timeseries: pd.DataFrame,
                     df_attrs: pd.DataFrame,
                     config_data: dict, 
                     path: Path):

    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        'timeseries': df_timeseries,
        'attributes': df_attrs,
        'config': config_data  
    }
    with open(path, 'wb') as f:
        pickle.dump(payload, f)


def export_to_excel(df_timeseries: pd.DataFrame,
                    df_attrs: pd.DataFrame,
                    config_data: dict, 
                    path: Path):

    path.parent.mkdir(parents=True, exist_ok=True)
    df_ts_fmt = convert_datetime_to_string(df_timeseries)
    
    df_params = pd.DataFrame(list(config_data.items()), columns=['Parameter', 'Value'])

    with pd.ExcelWriter(path, engine='xlsxwriter') as writer:
        df_ts_fmt.to_excel(writer, sheet_name='Data')
        df_attrs.to_excel(writer, sheet_name='Attributes', index=True)
        df_params.to_excel(writer, sheet_name='Params', index=False)