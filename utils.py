import requests
import pandas as pd

def get_option_chain_data(instrument_name: str, expiry_date: str, side: str, access_token: str) -> pd.DataFrame:
    url = 'https://api.upstox.com/v2/option/chain'
    params = {
        'instrument_key': f'NSE_INDEX|{instrument_name}',
        'expiry_date': expiry_date
    }
    headers = {
        'Accept': 'application/json',
        'Authorization': f'Bearer {access_token}'
    }

    response = requests.get(url, params=params, headers=headers)

    if response.status_code != 200:
        raise Exception(f"Failed to fetch data: {response.json().get('message', 'Unknown error')}")

    data = response.json().get("data", [])

    rows = []
    for option in data:
        strike_price = option["strike_price"]
        if side == "PE" and "put_options" in option:
            bid_price = option["put_options"]["market_data"]["bid_price"]
            instrument_key = option["put_options"]["instrument_key"]
            rows.append([instrument_name, instrument_key, strike_price, "PE", bid_price])
        elif side == "CE" and "call_options" in option:
            ask_price = option["call_options"]["market_data"]["ask_price"]
            instrument_key = option["call_options"]["instrument_key"]
            rows.append([instrument_name, instrument_key, strike_price, "CE", ask_price])

    df = pd.DataFrame(rows, columns=["instrument_name", "instrument_key", "strike_price", "side", "bid/ask"])

    return df

def calculate_margin_and_premium(data: pd.DataFrame, lot_size: int, access_token: str) -> pd.DataFrame:
    url = "https://api.upstox.com/v2/charges/margin"
    headers = {
        "Accept": "application/json",
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    margin_required_list = []
    premium_earned_list = []

    for _, row in data.iterrows():
        instrument_key = row["instrument_key"]
        transaction_type = "SELL" 
        price = row["bid/ask"]

        request_data = {
            "instruments": [
                {
                    "instrument_key": instrument_key,
                    "quantity": lot_size,
                    "transaction_type": transaction_type,
                    "product": "D",
                }
            ]
        }

        response = requests.post(url, headers=headers, json=request_data, timeout=10)

        if response.status_code != 200:
            print(f"Failed to retrieve margin for {instrument_key}: {response.json().get('message', 'Unknown error')}")
            margin_required_list.append(None)
        else:
            margin_data = response.json().get("data", {})
            margin_required = margin_data.get("required_margin", 0)
            margin_required_list.append(margin_required)

        premium_earned = price * lot_size
        premium_earned_list.append(premium_earned)

    data["margin_required"] = margin_required_list
    data["premium_earned"] = premium_earned_list

    return data