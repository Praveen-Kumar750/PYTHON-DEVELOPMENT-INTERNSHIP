import pandas as pd
import requests
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Set your broker's API key
API_KEY = 'YOUR_API_KEY'

# Set lot size for calculations (modify according to instrument)
LOT_SIZE = 75

# Define base URLs for the broker's API (replace with actual API URLs)
OPTIONS_API_URL = "https://api.broker.com/options"
MARGIN_API_URL = "https://api.broker.com/margin"

def get_option_chain_data(instrument_name: str, expiry_date: str, side: str) -> pd.DataFrame:
    """
    Retrieves option chain data for a specified instrument and expiry date, returning the highest
    bid price for put options (PE) or the highest ask price for call options (CE) at each strike price.
    
    Parameters:
    - instrument_name: Name of the financial instrument (e.g., NIFTY or BANKNIFTY)
    - expiry_date: Expiry date of the options in YYYY-MM-DD format
    - side: Option type, either "PE" for Put or "CE" for Call
    
    Returns:
    - A DataFrame containing instrument_name, strike_price, side, and bid/ask price
    """
    headers = {'Authorization': f'Bearer {API_KEY}'}
    params = {'symbol': instrument_name, 'expiry': expiry_date}
    
    try:
        response = requests.get(OPTIONS_API_URL, headers=headers, params=params)
        response.raise_for_status()  # Raise HTTPError for bad requests
        data = response.json()  # Parse JSON response
        logging.info(f"Data retrieved successfully for {instrument_name} on {expiry_date}")
        
        # Process the option chain data
        records = []
        for option in data['options']:
            if option['type'] == side:
                if side == 'PE':
                    highest_bid = max(option['bids'], key=lambda x: x['price'])['price']
                    records.append([instrument_name, option['strike_price'], side, highest_bid])
                elif side == 'CE':
                    highest_ask = max(option['asks'], key=lambda x: x['price'])['price']
                    records.append([instrument_name, option['strike_price'], side, highest_ask])
        
        # Create DataFrame from records
        df = pd.DataFrame(records, columns=['instrument_name', 'strike_price', 'side', 'bid/ask'])
        return df
    
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching data from API: {e}")
        return pd.DataFrame()  # Return empty DataFrame if there's an error

def calculate_margin_and_premium(data: pd.DataFrame) -> pd.DataFrame:
    """
    Calculates the margin required and premium earned for each option in the given DataFrame.
    
    Parameters:
    - data: DataFrame containing option chain data from get_option_chain_data
    
    Returns:
    - DataFrame with additional columns for margin_required and premium_earned
    """
    headers = {'Authorization': f'Bearer {API_KEY}'}
    margins = []
    premiums = []
    
    for _, row in data.iterrows():
        # Calculate premium earned
        premium_earned = row['bid/ask'] * LOT_SIZE
        premiums.append(premium_earned)
        
        # Get margin requirement from the API
        try:
            params = {
                'symbol': row['instrument_name'],
                'type': 'sell',
                'strike': row['strike_price'],
                'optionType': row['side']
            }
            response = requests.get(MARGIN_API_URL, headers=headers, params=params)
            response.raise_for_status()
            margin_required = response.json().get('margin', 0)  # Default to 0 if margin not available
            margins.append(margin_required)
            logging.info(f"Margin for {row['instrument_name']} at strike {row['strike_price']} is {margin_required}")
        
        except requests.exceptions.RequestException as e:
            logging.error(f"Error retrieving margin data: {e}")
            margins.append(0)  # Default to 0 if there's an error

    # Add margin and premium columns to the DataFrame
    data['margin_required'] = margins
    data['premium_earned'] = premiums
    return data

# Main script execution
if __name__ == "__main__":
    # Example usage of the functions
    
    # Fetch option chain data
    instrument_name = "NIFTY"
    expiry_date = "2024-11-05"
    side = "PE"  # Choose "PE" for Put or "CE" for Call
    
    option_data = get_option_chain_data(instrument_name, expiry_date, side)
    
    # Calculate margin and premium if data retrieval was successful
    if not option_data.empty:
        final_data = calculate_margin_and_premium(option_data)
        print(final_data)
    else:
        logging.warning("No data available to calculate margin and premium.")
