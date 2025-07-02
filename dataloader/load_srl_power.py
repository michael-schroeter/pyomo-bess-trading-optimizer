import os
import pandas as pd
from utils import get_pickle_path
from config_column_names import ColumnNamesRaw as CR, ColumnNamesClean as CC
from config import (
    PATH_SRL_POWER_DATA
)


def load_srl_power_data() -> pd.DataFrame:
    pkl_path = get_pickle_path(PATH_SRL_POWER_DATA)
    if os.path.exists(pkl_path):
        print(f"Loading data from {pkl_path}")
        return pd.read_pickle(pkl_path)
    
    print(f"Loading data from {PATH_SRL_POWER_DATA}")
    df = pd.read_excel(
        PATH_SRL_POWER_DATA,
        usecols=['DATE_FROM', 'DATE_TO', 'PRODUCT', CR.SRL_POWER_PRICE],
        parse_dates=['DATE_FROM', 'DATE_TO'],
        engine='openpyxl',
    )


    parts = df['PRODUCT'].str.split('_', expand=True)
    df['direction']  = parts[0]       # 'POS' oder 'NEG'
    df['start_hour'] = parts[1].astype(int)

    df['timestamp'] = (
        df['DATE_FROM'].dt.normalize()
        + pd.to_timedelta(df['start_hour'], unit='h')
    ).dt.tz_localize('Europe/Berlin')
    df = df.set_index('timestamp')

    df_wide = (
        df
        .set_index('direction', append=True)[CR.SRL_POWER_PRICE]
        .unstack('direction')
    )

    df_wide.columns = [
       CC.SRL_POWER_PRICE_POS if d == 'POS'
        else CC.SRL_POWER_PRICE_NEG
        for d in df_wide.columns
    ]

    df_wide.to_pickle(pkl_path)
    print(f"Data saved to {pkl_path}")
    return df_wide