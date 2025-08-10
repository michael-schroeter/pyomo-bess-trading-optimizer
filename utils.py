import os
import re
from pathlib import Path
from datetime import datetime
import pandas as pd
from params.params import SYSTEM_POWER
import params.params as params
import inspect


def get_interval_minutes(df: pd.DataFrame) -> int:
    diffs = df.index.to_series().diff().dropna()
    time_interval = diffs.mode()[0]
    return int(time_interval.total_seconds() / 60)


def calculate_period_in_days(start_date: str, end_date: str) -> int:
    return (datetime.strptime(end_date, '%Y-%m-%d') - datetime.strptime(start_date, '%Y-%m-%d')).days


def get_charge_rate(interval_minutes):
    return SYSTEM_POWER * (interval_minutes/60)


def convert_datetime_to_string(df: pd.DataFrame) -> pd.DataFrame:
    formated_df = df.copy()
    formatted_index = []
    for idx in formated_df.index:
        timestamp_str = idx.strftime("%Y-%m-%d %H:%M:%S%z")
        if timestamp_str[-5:]:  # If there's a timezone offset
            formatted_str = timestamp_str[:-2] + ":" + timestamp_str[-2:]
            formatted_index.append(formatted_str)
        else:
            formatted_index.append(timestamp_str)
    
    formated_df.index = formatted_index
    return formated_df


def get_pickle_path(source_path: str) -> str:
    base, _ext = os.path.splitext(source_path)
    return f"{base}.pkl"


def get_params_as_dict_old() -> dict:

    config_data = {}
    for name, value in params.__dict__.items():
        if name.isupper():
            if isinstance(value, params.Path):
                config_data[name] = str(value)
            else:
                config_data[name] = value
    return config_data


def get_params_as_dataframe(params_module) -> pd.DataFrame:
    """
    Liest ein Konfigurationsmodul, extrahiert großgeschriebene Variablen,
    ihre berechneten Werte und die zugehörigen Kommentare aus der Quelldatei.

    Args:
        params_module: Das importierte Konfigurationsmodul (z. B. 'params').

    Returns:
        Ein pandas DataFrame mit den Spalten 'Parameter', 'Value' und 'Kommentar'.
    """
    # Schritt 1: Berechnete Werte aus dem importierten Modul extrahieren
    config_values = {}
    for name, value in params_module.__dict__.items():
        if name.isupper():
            # Konvertiere Path-Objekte in Strings für die Anzeige
            config_values[name] = str(value) if isinstance(value, Path) else value

    # Schritt 2: Kommentare aus der .py-Datei als Text extrahieren
    comments = {}
    filepath = Path(params_module.__file__)  # Finde den Dateipfad des Moduls

    # Regex: Findet eine Zeile mit VARIABLENNAME = Wert # Kommentar
    # Gruppe 1: Der Variablenname (z.B. "INITIAL_BATTERY_CAPACITY")
    # Gruppe 2: Der Kommentartext (z.B. "MWh")
    regex = re.compile(r"^\s*([A-Z_][A-Z0-9_]*)\s*=[^#]*#\s*(.*)")

    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            match = regex.match(line)
            if match:
                name = match.group(1).strip()
                comment = match.group(2).strip()
                if name in config_values:
                    comments[name] = comment

    # Schritt 3: Werte und Kommentare zu einer Liste zusammenfügen
    combined_data = []
    for name, value in config_values.items():
        combined_data.append({
            'Parameter': name,
            'Value': value,
            'Kommentar': comments.get(name, '')  # Fügt Kommentar hinzu, falls vorhanden
        })

    return pd.DataFrame(combined_data)