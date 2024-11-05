import os
from dotenv import load_dotenv
from utils.utils import get_option_chain_data, calculate_margin_and_premium

load_dotenv()

access_token = os.getenv("YOUR_ACCESS_TOKEN")
if access_token is None:
    raise ValueError("Access token not found. Please check your .env file.")

instrument_name = "Nifty 50"
expiry_date = "2024-11-07"
side = "PE" 
lot_size = 50  

data = get_option_chain_data(instrument_name, expiry_date, side, access_token)
print(data)

data_with_margin = calculate_margin_and_premium(data, lot_size, access_token)

print(data_with_margin)