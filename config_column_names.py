
#Table Config
class ColumnNamesRaw:
    ENERGIE_CHARTS_DATE         = 'datum und uhrzeit'
    DA_AUC_PRICE                = 'day ahead auktion exaa' # Day-Ahead Auction Price (EUR / MWh)
    ID_PRICE_AUC_15min          = 'intraday auktion, 15 minuten preis'
    ID_PRICE_AUC_IDA1_GEKOPPELT = 'gekoppelte intraday auktion, 15 minuten ida1-preis'
    PRL_PRICE                   = 'DE_SETTLEMENTCAPACITY_PRICE_[EUR/MW]' #€/MWh
    SRL_POWER_PRICE             = 'GERMANY_AVERAGE_CAPACITY_PRICE_[(EUR/MW)/h]' #€/MWh; muss neu aus original Daten gezogen werden wenn geändert wird
    SRL_NEG_WORK_CBMP              = 'Price [EUR/MWh] Down'
    SRL_POS_WORK_CBMP              = 'Price [EUR/MWh] Up' 

class ColumnNamesClean:

## timeseries
    #data
    DATE                 = 'Date'
    DA_AUC_PRICE            = 'DA'
    ID_AUC_PRICE             = 'ID'
    HiGHER_MARKET_PRICE = 'Higher Market Price'
    LOWER_MARKET_PRICE  = 'Lower Market Price'
    HiGHER_MARKET_PRICE_LABEL            = 'Market Higher'
    LOWER_MARKET_PRICE_LABEL            = 'Market Lower'

    PRL_PRICE            = 'PRL Price'
    SRL_POWER_PRICE_POS  = 'SRL Power Price Pos'
    SRL_POWER_PRICE_NEG  = 'SRL Power Price Neg'
    SRL_NEG_WORK_CBMP   = 'SRL Work Price Neg'
    SRL_POS_WORK_CBMP   = 'SRL Work Price Pos'

    #market/regelleistung
    BUY_VOL              = 'Buy Volume'
    SELL_VOL             = 'Sell Volume'
    PRL_POWER            = 'PRL Power'
    SRL_POWER_POS        = 'SRL Power Pos'
    SRL_POWER_NEG        = 'SRL Power Neg'

    #charge/discharge
    BAT_SOC              = 'Battery SOC'
    STORED_ENERGY       = 'Stored Energy'

    MARKET_CHARGE       = 'Market Charge'
    MARKET_DISCHARGE    = 'Market Discharge'
    PRL_CHARGE          = 'PRL Charge'
    PRL_DISCHARGE       = 'PRL Discharge'
    SRL_NEG_CHARGE      = 'SRL Neg Charge'
    SRL_POS_DISCHARGE   = 'SRL Pos Discharge'
    TOTAL_CHARGE        = 'Total Charge'
    TOTAL_DISCHARGE     = 'Total Discharge'

    CYCLES_ID        = 'Cycles Intraday'
    CYCLES_DA        = 'Cycles Days Ahead'
    CYCLES_SPOT      = 'Cycles Spot'
    CYCLES_PRL       = 'Cycles PRL'
    CYCLES_SRL_POS   = 'Cycles SRL Pos'
    CYCLES_SRL_NEG   = 'Cycles SRL Neg'
    CYCLES_SRL       = 'Cycles SRL'
    CYCLES          = 'Cycles'
    CYCLES_EQ       = 'Cycles EQ'
    CYCLES_CUMSUM   = 'Cycles CumSum'
    CYCLES_EQ_CUMSUM = 'Cycles EQ CumSum'

    REST_CAPACITY_CYCLE = 'Rest Capacity Cycle'
    BATTERY_CAPACITY   = 'Battery Capacity'
    EFFICIENCY         = 'Efficiency'



    
    #money
    REVENUE_MARKET       = 'Revenue Market'
    REVENUE_PRL          = 'Revenue PRL'    
    REVENUE_SRL          = 'Revenue SRL'
    REVENUE_TOTAL        = 'Total Revenue'
    AGING_COST           = 'Aging Cost'
    NET_CASHFLOW        = 'Net Cashflow'


## attrs
    #market/regelleistung
    BUY_VOL_SUM         = 'Buy Volume Sum'
    SELL_VOL_SUM        = 'Sell Volume Sum'
    PRL_POWER_SUM       = 'PRL Power Sum'
    SRL_POWER_POS_SUM   = 'SRL Power Pos Sum'
    SRL_POWER_NEG_SUM   = 'SRL Power Neg Sum'

    #charge/discharge
    MARKET_CHARGE_SUM   = 'Market Charge Sum'
    MARKET_DISCHARGE_SUM = 'Market Discharge Sum'
    PRL_CHARGE_SUM      = 'PRL Charge Sum'
    PRL_DISCHARGE_SUM   = 'PRL Discharge Sum'
    SRL_NEG_CHARGE_SUM  = 'SRL Neg Charge Sum'
    SRL_POS_DISCHARGE_SUM = 'SRL Pos Discharge Sum'
    TOTAL_CHARGE_SUM    = 'Total Charge Sum'
    TOTAL_DISCHARGE_SUM = 'Total Discharge Sum'

    CYCLES_ID_SUM        = 'Battery Cycles Intraday Sum'
    CYCLES_DA_SUM        = 'Battery Cycles Days Ahead Sum'
    CYCLES_SPOT_SUM       = 'Battery Cycles Spot Sum'
    CYCLES_PRL_SUM       = 'Battery Cycles PRL Sum'
    CYCLES_SRL_POS_SUM   = 'Battery Cycles SRL Pos Sum'
    CYCLES_SRL_NEG_SUM   = 'Battery Cycles SRL Neg Sum'
    CYCLES_SRL_SUM       = 'Battery Cycles SRL Sum'
    BATTERY_CYCLES      = 'Battery Cycles'
    BATTERY_CYCLES_EQ   = 'Battery Cycles EQ'

    #money
    REVENUE_MARKET_SUM  = 'Revenue Market Sum'
    REVENUE_PRL_SUM     = 'Revenue PRL Sum'
    REVENUE_SRL_SUM     = 'Revenue SRL Sum'  
    REVENUE_TOTAL_SUM   = 'Total Revenue Sum'
    TAXES_SUM           = 'Taxes Sum'
    OBJ                 = 'Objective Value'
    AGING_COST_SUM      = 'Aging Cost Sum'

