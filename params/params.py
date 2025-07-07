from pathlib import Path

TITLE = "tst"

#Data Config
START_DATE = "2022-12-29" #included
END_DATE = "2023-01-03" #excluded

##Battery Hardware
INITIAL_BATTERY_CAPACITY = 1 #MWh
SYSTEM_POWER = 1 #MW (1MW = 1MWh/1h) # AC Seitig
LIFETIME_CYCLES = 9000
EFFICIENCY = 0.8 # AC Seitig vom Umrichter. einseitiger Wirkungsgrad (jeweils Lade- und Entladeverluste)
CHARGE_RATE = SYSTEM_POWER * (15/60) 


## Einmalige Investitionskosten (CAPEX)
SPECIFIC_BATTERY_INVEST = 180000  # €/MWh; (2MWh/MW)Quelle Torsten Batterieinfos
SPECIFIC_INVERTER_INVEST = 20000  # €/MW
SPECIFIC_TRANSFORMER_INVEST = 25000  # €/MW
SPECIFIC_CONSTRUCTION_ALLOWANCE_INVEST = 50000  # €/MW, z.B. zwischen 50-100k€; Quelle Torsten Batterieinfos
SPECIFIC_GRID_CONNECTION_INVEST = 5000  # €/MW


## Laufende Betriebskosten (OPEX, jährlich)
# Betriebskosten = 20-40K€ pro MW pro Jahr (alles zusammen); Quelle: Torsten Batteriespeicherinfos
INSURANCE_RATE = 0.01  # % der Investitionskosten (abzüglich CONSTRUCTION_ALLOWANCE_INVEST)
SPECIFIC_TECHNICAL_MANAGEMENT_COST = 3000 # €/MW pro Jahr
SPECIFIC_MAINTENANCE_COST = 3000  # €/MW pro Jahr
SPECIFIC_REPAIRS_COST = 3000 # €/MW pro Jahr
SPECIFIC_MEASUREMENTS_COST = 3000 # €/MW pro Jahr
ACCOUNTING_COST = 3000 # € pro Jahr

## Taxes
TAX_RATE = 0.20 # % 
DEPRECIATION_YEARS = 10 #Abschreibungsdauer in Jahren










#Regelleistungsmarkt ConfigPROFIT_FACTOR_SRL_POS = 1.5
PROFIT_FACTOR_SRL_NEG = 1
PROFIT_FACTOR_SRL_POS = 1.5 #Faktor für die positive Regelleistung

#Märkte
MARKET_SWITCH = 1
PRL_SWITCH = 1
SRL_SWITCH = 1