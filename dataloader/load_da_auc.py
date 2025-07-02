import os
import locale
import pandas as pd
from utils import get_pickle_path
from config import PATH_DA_AUC_DATA
from config_column_names import ColumnNamesRaw as CR, ColumnNamesClean as CC


def load_da_auc_data() -> pd.DataFrame:
    locale.setlocale(locale.LC_NUMERIC, 'de_DE.UTF-8')
    pkl_path = get_pickle_path(PATH_DA_AUC_DATA)
    if os.path.exists(pkl_path):
        print(f"Loading data from {pkl_path}")
        return pd.read_pickle(pkl_path)
    
    print(f"Loading data from {PATH_DA_AUC_DATA}")
    df = pd.read_excel(
        PATH_DA_AUC_DATA,
        usecols=[CR.ENERGIE_CHARTS_DATE, CR.DA_AUC_PRICE],
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
    # fillna(0) falls es Lücken gibt
    df[CC.DA_AUC_PRICE] = df[CR.DA_AUC_PRICE].fillna(0)

    df_clean = df[[CC.DA_AUC_PRICE]]
    df_clean.to_pickle(pkl_path)
    print(f"Data saved to {pkl_path}")
    return df_clean
