# config.py
# Enthält nur noch statische Pfade und feste Modellkonstanten.
from pathlib import Path

## --- Statische Dateipfade ---
PATH_DA_AUC_DATA = "data/Energy-Charts DayAhead 2021 bis 2024.xlsx"
PATH_INTRADAY_DATA = "data/Energy-Charts Intraday 2021 bis 2024.xlsx"
PATH_PRL_DATA = "data/Primär Ergebnisse 2021 bis 2024.xlsx"
PATH_SRL_POWER_DATA = 'data/Sekundär Leistung Ergebnisse 2021 bis 2024.xlsx'
PATH_SRL_WORK_DATA = 'data/srl_work_cbmp_2022-07-01 - 2025-06-29.pkl'

RESULTS_DIR = Path("results")


SPECIFIC_PRL_ENERGY_NEED_4H_CYCLE = (1/3) / 16  # MWh/MW pro 15min

