# BreakoutAI-assessment

## Overview

This project involves developing Python functions to fetch options trading data from the Upstox API and calculate margin requirements and premiums for options contracts. This was created as part of a Python Development Internship assessment for BreakoutAI.

## Project Structure

```
.
├── main.py                 # Main script to execute the program
├── utils/
│   └── utils.py            # Contains core functions for data retrieval and calculations
├── requirements.txt        # Lists dependencies
├── .env                    # Stores sensitive information like API keys
├── login.py                # Handles token generation
├── README.md               # Project documentation
```

## Prerequisites

- **Python 3.8+**: Ensure Python is installed on your system.
- **Upstox API Access**: Register for an account and obtain your API key and secret.
- **Dependencies**: Install required packages by running:
  ```bash
  pip install -r requirements.txt
  ```

## Environment Setup

1. **Generate Access Token**: Use `login.py` to authenticate with Upstox API and obtain an access token.
2. **Store Access Token**: Save the access token in the `.env` file for secure access.

## Files and Functions

- **main.py**: Main entry point of the project. It:
  - Loads environment variables.
  - Calls the `get_option_chain_data` and `calculate_margin_and_premium` functions from `utils.py` to fetch options data and calculate margins.
  
- **utils/utils.py**: Contains the core functions:
  - `get_option_chain_data`: Fetches options chain data for the specified instrument, expiry date, and side (PE or CE) from the Upstox API.
  - `calculate_margin_and_premium`: Calculates margin requirements and premiums based on the options data.
  
- **requirements.txt**: Lists all the Python packages required to run the project.
- **.env**: Stores sensitive data such as access token, API key, and secret key. Example structure:
  ```plaintext
  YOUR_ACCESS_TOKEN = 'YOUR_ACCESS_TOKEN'
  SECRETKEY = 'your_secret_key'
  RURI = 'your_redirect_uri'
  ```

## Function Details

### `get_option_chain_data`
- **Purpose**: Fetches the options chain data for a specific instrument, expiry date, and side.
- **Parameters**:
  - `instrument_name`: Name of the instrument (e.g., Nifty 50).
  - `expiry_date`: Expiry date of the options contract.
  - `side`: Type of option, "PE" for put or "CE" for call.
  - `access_token`: Access token for Upstox API authentication.
- **Returns**: A DataFrame containing the fetched options data, including `instrument_key`, `strike_price`, `side`, and `bid/ask` prices.
- **Note**: The `instrument_key` is fetched from the API as it is needed to calculate the `margin_required` in the next function.

### `calculate_margin_and_premium`
- **Purpose**: Calculates the margin requirements and premiums for options trades.
- **Parameters**:
  - `data`: DataFrame containing options data (output from `get_option_chain_data`).
  - `lot_size`: Number of options in a lot.
  - `access_token`: Access token for Upstox API authentication.
- **Returns**: A DataFrame with additional columns for `margin_required` and `premium_earned`.

### Token Validation

To validate if the access token is valid, use the following code snippet:

```python
import requests

url = 'https://api.upstox.com/v2/option/chain'
params = {
    'instrument_key': 'NSE_INDEX|Nifty 50',
    'expiry_date': '2024-11-07'
}
headers = {
    'Accept': 'application/json',
    'Authorization': f'Bearer {your_access_token}'
}

response = requests.get(url, params=params, headers=headers)
print(response.json())
```

## How AI Tools Assisted

- **ChatGPT**: Assisted in drafting the code overview and guided structuring of the code and handling specific challenges.
- **YouTube Tutorials**: Helped in learning how to make API calls to Upstox effectively.
- **Upstox API Documentation**: Referenced for understanding the API endpoints and required parameters for margin required and put/call parameters.

## Error Handling

Some common errors faced:
- **Access Token Errors**: Incorrect or expired tokens result in authentication failures.
- **API Rate Limits**: Exceeding rate limits may lead to delayed responses or request denials.

## Usage

1. Update your `.env` file with the correct access token and keys.
2. Run the main script to fetch options data and calculate margin and premium:
   ```bash
   python main.py
   ```

3. The results will be displayed as a DataFrame in the console.

## License

This project is created for assessment purposes and is intended for internal use only.

