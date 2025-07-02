import os
import pandas as pd
from utils import get_pickle_path
from config_column_names import ColumnNamesRaw as CR, ColumnNamesClean as CC
from config import PATH_PRL_DATA


def load_prl_data() -> pd.DataFrame:
    pkl_path = get_pickle_path(PATH_PRL_DATA)
    if os.path.exists(pkl_path):
        print(f"Loading data from {pkl_path}")
        return pd.read_pickle(pkl_path)
    
    print(f"Loading data from {PATH_PRL_DATA}")
    df = pd.read_excel(
        PATH_PRL_DATA,
        usecols=["DATE_FROM", "PRODUCTNAME", CR.PRL_PRICE],
        parse_dates=["DATE_FROM"],
        engine="openpyxl",           # falls du vorher kein engine explizit hattest
    )

    df["start_hour"] = (
        df["PRODUCTNAME"]
        .str.split("_")
        .str[1]        
        .astype(int)    
    )
    
    df[CC.DATE] = (
        df["DATE_FROM"].dt.floor("D")  
        + pd.to_timedelta(df["start_hour"], unit="H")
    )

    df[CC.DATE] = df[CC.DATE].dt.tz_localize("Europe/Berlin")
    df.set_index(CC.DATE, inplace=True)

    df = df[[CR.PRL_PRICE]]   
    df.columns = [CC.PRL_PRICE]
    
    df.to_pickle(pkl_path)
    print(f"Data saved to {pkl_path}")
    return df