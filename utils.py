from decimal import Decimal
import pandas as pd
import requests

def get_info_response(crypto) -> str:
    try:
        response = requests.get(f'https://api.cube.exchange/md/v0/parsed/tickers')
        response.raise_for_status()
        result = response.json()
        df = pd.DataFrame(result.get('result'))
        data = df[df['base_currency'].str.lower() == crypto.lower()]
        if not data.empty:
            price = data["last_price"].iloc[0]
            base_currency = data["base_currency"].iloc[0]
            high = data["high"].iloc[0]
            low = data["low"].iloc[0]
            volume = data["quote_volume"].iloc[0]

            price_decimals = max(0, -Decimal(str(price)).as_tuple().exponent)
            high_decimals = max(0, -Decimal(str(high)).as_tuple().exponent)
            low_decimals = max(0, -Decimal(str(low)).as_tuple().exponent)
            volume_decimals = max(0, -Decimal(str(volume)).as_tuple().exponent)

            return (f'The current price of {base_currency} is {price:.{price_decimals}f}$\n'
                    f"📈 24h:\n"
                    f"--High: {high:.{high_decimals}f}$\n"
                    f"--Low: {low:.{low_decimals}f}$\n"
                    f"--Volume: {volume:.{volume_decimals}f} 💰")

        else:
            return (f'Could not find data for {crypto}. Please check the symbol.')
    except requests.exceptions.RequestException as err:
        print(f"Error fetching info: {err}")
        return None
        
