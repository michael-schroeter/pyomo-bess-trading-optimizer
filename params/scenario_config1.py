from pathlib import Path

TITLE = "ESN-Storage LFP CON 5000 (Daten von Torsten Reusch)"

#Data Config
START_DATE = "2023-06-26" #included
END_DATE = "2024-06-27" #excluded

##Battery Hardware
INITIAL_BATTERY_CAPACITY = 5.016 * 0.95  #MWh
SYSTEM_POWER = 2.5 #MW (1MW = 1MWh/1h) # AC Seitig
LIFETIME_CYCLES = 6000 # (95% DoD, 70% EOL)
EFFICIENCY = 0.949 # einseitiger Wirkungsgrad (jeweils Lade- und Entladeverluste)
DEGRADATION_FACTOR_MWH = 0.000025  # MWh pro MWh durchlaufener Energie
CHARGE_RATE = SYSTEM_POWER * (15/60) 


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



