from entsoe import EntsoePandasClient
import pandas as pd



client = EntsoePandasClient(api_key='382100ed-6229-44cd-87c1-3726801cc157')

start = pd.Timestamp('20150708', tz='Europe/Brussels')
end = pd.Timestamp('20150709', tz='Europe/Brussels')
country_code = 'FR'  # Belgium
country_code_from = 'FR'  # France
country_code_to = 'DE_LU' # Germany-Luxembourg
type_marketagreement_type = 'A01'
contract_marketagreement_type = "A01"
process_type = 'A51'
x = client.query_day_ahead_prices(country_code, start, end)
print(x)