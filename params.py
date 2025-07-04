from pathlib import Path


#Data Config
START_DATE = "2022-01-01" #included
END_DATE = "2025-01-01" #excluded

#Battery Config
BAT_CAPACITY = 1.2 #MWh
SYSTEM_POWER = 1.2 #MW (1MW = 1MWh/1h)
BAT_PRICE = 270000 * BAT_CAPACITY #€
LIFETIME_CYCLES = 9000
EFFICIENCY = 0.9 # AC Seitig vom Umrichter. einseitiger Wirkungsgrad (jeweils Lade- und Entladeverluste)
SPECIFIC_AGING_COST = BAT_PRICE / (BAT_CAPACITY * LIFETIME_CYCLES * 2) #€/(MWh durchsatz) sowohl Laden als auch Entladen
CHARGE_RATE = SYSTEM_POWER * (15/60) 


#Regelleistungsmarkt ConfigPROFIT_FACTOR_SRL_POS = 1.5
PROFIT_FACTOR_SRL_NEG = 1
PROFIT_FACTOR_SRL_POS = 1.5 #Faktor für die positive Regelleistung

#Märkte
MARKET_SWITCH = 1
PRL_SWITCH = 1
SRL_SWITCH = 1








