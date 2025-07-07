from pathlib import Path

TITLE = "Bachelor-Thesis-Electricity-Market Test Überschrift"
#Data Config
START_DATE = "2022-12-29" #included
END_DATE = "2023-01-03" #excluded

#Battery Config
BAT_CAPACITY = 1 #MWh
SYSTEM_POWER = 1 #MW (1MW = 1MWh/1h) # AC Seitig
BAT_PRICE = 270000 * BAT_CAPACITY #€
LIFETIME_CYCLES = 9000
EFFICIENCY = 0.8 # AC Seitig vom Umrichter. einseitiger Wirkungsgrad (jeweils Lade- und Entladeverluste)
SPECIFIC_AGING_COST = BAT_PRICE / (BAT_CAPACITY * LIFETIME_CYCLES * 2) #€/(MWh durchsatz) sowohl Laden als auch Entladen
CHARGE_RATE = SYSTEM_POWER * (15/60) 


#Regelleistungsmarkt ConfigPROFIT_FACTOR_SRL_POS = 1.5
PROFIT_FACTOR_SRL_NEG = 1
PROFIT_FACTOR_SRL_POS = 1.5 #Faktor für die positive Regelleistung

#Märkte
MARKET_SWITCH = 1
PRL_SWITCH = 1
SRL_SWITCH = 1








