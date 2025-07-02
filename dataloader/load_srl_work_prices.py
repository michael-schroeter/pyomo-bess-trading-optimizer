import pandas as pd
from config import (
    PATH_SRL_WORK_DATA,
)
from params import (
    SPECIFIC_AGING_COST,
    PROFIT_FACTOR_SRL_POS,
    PROFIT_FACTOR_SRL_NEG,
)

from config_column_names import (
    ColumnNamesRaw as CR,
    ColumnNamesClean as CC,
)



def load_srl_work_cbmp_data(specific_aging_cost):
    df = pd.read_pickle(PATH_SRL_WORK_DATA)
    df.fillna(0, inplace=True)
    df[CC.SRL_NEG_WORK_CBMP] = 0.0
    df[CC.SRL_POS_WORK_CBMP] = 0.0


    mask_neg = (-df[CR.SRL_NEG_WORK_CBMP] > specific_aging_cost * PROFIT_FACTOR_SRL_NEG) & (df[CR.SRL_POS_WORK_CBMP] == 0)
    df.loc[mask_neg, CC.SRL_NEG_WORK_CBMP] = df.loc[mask_neg, CR.SRL_NEG_WORK_CBMP]


    mask_pos = (df[CR.SRL_POS_WORK_CBMP] > specific_aging_cost * PROFIT_FACTOR_SRL_POS) & (df[CR.SRL_NEG_WORK_CBMP] == 0)
    df.loc[mask_pos, CC.SRL_POS_WORK_CBMP] = df.loc[mask_pos, CR.SRL_POS_WORK_CBMP] 



    df.drop(columns=[CR.SRL_NEG_WORK_CBMP, CR.SRL_POS_WORK_CBMP, 'position'], inplace=True)

    df = df.resample('15min').mean()


    return df
    

if __name__ == "__main__":

    df = load_srl_work_cbmp_data(SPECIFIC_AGING_COST)
    print(df)

    df = df.loc['2023-01-01':'2023-01-02']
    df.index = df.index.strftime('%Y-%m-%d %H:%M:%S')
    df.to_excel('srl_work_pricewedwedwedwedwedwedweds.xlsx', index=True)

