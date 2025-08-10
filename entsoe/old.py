from entsoe import EntsoePandasClient
import pandas as pd

# 1. Konstante Parameter (bleiben für alle Abfragen gleich)
# ==========================================================
client = EntsoePandasClient(api_key='382100ed-6229-44cd-87c1-3726801cc157') # Bitte deinen eigenen API-Key verwenden
start = pd.Timestamp('20171201', tz='Europe/Brussels')
end = pd.Timestamp('20171202', tz='Europe/Brussels')
country_code = 'DE'


queries_to_run = [
    {
        'name': 'day_ahead_prices',
        'method': 'query_day_ahead_prices',
        'params': {
            'country_code': country_code
        }
    },
    {
        'name': 'net_position_dayahead',
        'method': 'query_net_position',
        'params': {
            'country_code': country_code,
            'dayahead': True
        }
    },
    {
        'name': 'wind_solar_forecast',
        'method': 'query_wind_and_solar_forecast',
        'params': {
            'country_code': country_code,
            'psrtype': None # Alle Typen abfragen
        }
    },
    {
        'name': 'total_load_past_week',
        'method': 'query_load',
        'params': {
            'country_code': country_code
        }
    },

]


results = {}

print("Führe Abfragen aus...")
for query in queries_to_run:
    try:
        query_func = getattr(client, query['method'])
        
        print(f"-> Lade '{query['name']}'...")
        data = query_func(start=start, end=end, **query['params'])
        results[query['name']] = data
        
        print(f"   ... '{query['name']}' erfolgreich geladen.")

    except Exception as e:
        error_message = f"Fehler bei der Abfrage '{query['name']}': {e}"
        results[query['name']] = error_message
        print(f"   ... {error_message}")

print("\nAbfragen abgeschlossen.\n")
print(results)
