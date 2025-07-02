import os
import locale
import pandas as pd
from utils import get_pickle_path
from config import (
    PATH_INTRADAY_DATA,
)
from config_column_names import ColumnNamesRaw as CR, ColumnNamesClean as CC


def load_id_auc_data() -> pd.DataFrame:
    locale.setlocale(locale.LC_NUMERIC, 'de_DE.UTF-8')
    pkl_path = get_pickle_path(PATH_INTRADAY_DATA)
    if os.path.exists(pkl_path):
        print(f"Loading data from {pkl_path}")
        return pd.read_pickle(pkl_path)

    print(f"Loading data from {PATH_INTRADAY_DATA}")
    df = pd.read_excel(
        PATH_INTRADAY_DATA,
        usecols=[
            CR.ENERGIE_CHARTS_DATE,
            CR.ID_PRICE_AUC_15min,
            CR.ID_PRICE_AUC_IDA1_GEKOPPELT,
        ],
        index_col=0,
        parse_dates=[0],
        date_format="%d.%m.%Y, %H:%M",
        engine="openpyxl",
        thousands='.',    # Punkt als Tausender
        decimal=','       # Komma als Dezimaltrennzeichen
    )

    df.index = (
        df.index
          .tz_localize('UTC')
          .tz_convert('Europe/Berlin')
    )

    # Fallback: 15-Min-Preis, sonst IDA1, sonst 0
    df[CC.ID_AUC_PRICE] = (
        df[CR.ID_PRICE_AUC_15min]
        .fillna(df[CR.ID_PRICE_AUC_IDA1_GEKOPPELT])
        .fillna(0)
    )

    df_clean = df[[CC.ID_AUC_PRICE]]
    df_clean.to_pickle(pkl_path)
    print(f"Data saved to {pkl_path}")
    return df_clean