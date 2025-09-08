from pathlib import Path

TITLE = "Szenario 1"

#Data Config
START_DATE = "2023-01-01" #included
END_DATE = "2023-04-01" #excluded
PSEUDO_END_DATE = "2040-12-31 23:45:00+01:00"

##Battery Hardware
INITIAL_BATTERY_CAPACITY = 5.016 * 0.95  #MWh
SYSTEM_POWER = 2.5 #MW (1MW = 1MWh/1h) # AC Seitig
LIFETIME_CYCLES = 6000 # (95% DoD, 70% EOL)
MAX_CHARGE_RATE = SYSTEM_POWER * (15/60)  # Max MWH pro 15min
MAX_CYCLE_RATE = MAX_CHARGE_RATE / (2 * INITIAL_BATTERY_CAPACITY)  #pro 15min
EFFICIENCY_BAT = 0.949 # einseitiger Wirkungsgrad (jeweils Lade- und Entladeverluste)
EFFICIENCY_REST = 0.97 # sonstige Wirkungsgrade (Umrichter, Transformator, Kabel, etc.)
EFFICIENCY_SYS = EFFICIENCY_BAT * EFFICIENCY_REST

## Degradation
BATTERY_DEGRADATION_CAL_VALUE = INITIAL_BATTERY_CAPACITY * 0.00002585 / 100 #pro 15min 
EFFICIENCY_DEGRADATION_CAL_VALUE = 0.0005/100 * EFFICIENCY_BAT
SOC_FACTORS = {0: 1.60, 1: 1.00, 2: 1.02, 3: 1.20}


## Einmalige Investitionskosten (CAPEX)
BATTERY_INVEST = 882353   # €/MWh Netto (inklsive Umrrichter)
INVERTER_INVEST = 9958  # €/MW Netto für eza Regler inkl Installation und Betriebnahme
TRANSFORMER_INVEST = 25000 * SYSTEM_POWER   # €
CONSTRUCTION_ALLOWANCE_INVEST = 50000 * SYSTEM_POWER  # € z.B. zwischen 50-100k€; Quelle Torsten Batterieinfos
GRID_CONNECTION_INVEST = 50000  # geschätzt (Sicher 7479 für Transport)
INSURANCE_EXTENSION  = 73529


## Laufende Betriebskosten (OPEX, jährlich)
# Betriebskosten = 20-40K€ pro MW pro Jahr (alles zusammen); Quelle: Torsten Batteriespeicherinfos
INSURANCE_RATE = 0.01  # % der Investitionskosten (abzüglich CONSTRUCTION_ALLOWANCE_INVEST)
TECHNICAL_MANAGEMENT_COST = 3000 * SYSTEM_POWER # € pro Jahr
MAINTENANCE_COST = 3000 * SYSTEM_POWER  # € pro Jahr
REPAIRS_COST = 0 # € pro Jahr
MEASUREMENTS_COST = 3000  * SYSTEM_POWER # € pro Jahr
ACCOUNTING_COST = 3000 # € pro Jahr

## Taxes
TAX_RATE = 0.20 # % 
DEPRECIATION_YEARS = 10 #Abschreibungsdauer in Jahren


#Regelleistungsmarkt Config PROFIT_FACTOR_SRL_POS = 1.5
PROFIT_FACTOR_SRL_NEG = 1
PROFIT_FACTOR_SRL_POS = 1.6 #Faktor für die positive Regelleistung

#Märkte
MARKET_SWITCH = 1
PRL_SWITCH = 1
SRL_SWITCH = 1

#Cycles
MAX_CYCLES_PER_DAY = 1





