import os
from entsoe import EntsoePandasClient
import pandas as pd



client = EntsoePandasClient(api_key=os.environ["ENTSOE_API_KEY"])


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