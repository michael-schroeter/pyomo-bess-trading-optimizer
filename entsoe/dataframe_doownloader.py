from entsoe import EntsoePandasClient
import pandas as pd

client = EntsoePandasClient(api_key='382100ed-6229-44cd-87c1-3726801cc157')

start = pd.Timestamp('20171201', tz='Europe/Brussels')
end = pd.Timestamp('20180101', tz='Europe/Brussels')
country_code = 'FR'  # Belgium
country_code_from = 'FR'  # France
country_code_to = 'DE_LU' # Germany-Luxembourg
type_marketagreement_type = 'A01'
contract_marketagreement_type = "A01"
process_type = 'A51'

#client.query_day_ahead_prices(country_code, start=start, end=end)
x =client.query_net_position(country_code, start=start, end=end, dayahead=True)