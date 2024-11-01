# PYTHON-DEVELOPMENT-INTERNSHIP
## Overview
This project is designed to retrieve and process options chain data for financial instruments traded in the Indian market. The project’s goal is to develop two robust functions:
Data Retrieval Function: Gathers the highest bid or ask price for a specified instrument and expiry date.
Data Processing Function: Calculates margin requirements and premium earned for options, adding these as new data fields.
This project is part of the Python Development Internship Assessment at BreakoutAI, emphasizing data-centric programming skills.

## Project Structure
The project consists of the following files and functions:
main.py: Contains the two main functions, helper functions, and any other logic.
README.md: This documentation file.
requirements.txt: Lists dependencies like pandas and requests.


## Function Details
### 1. get_option_chain_data
Purpose
Retrieves options chain data for a specific instrument and expiry date, returning the highest bid price for Put options (PE) or the highest ask price for Call options (CE) at each strike price.

Parameters
instrument_name: str - Instrument name, e.g., NIFTY, BANKNIFTY.
expiry_date: str - Options expiry date in the format YYYY-MM-DD.
side: str - Type of option: "PE" for Put or "CE" for Call.


### 2. calculate_margin_and_premium
Purpose
Calculates the margin_required and premium_earned for each option contract using the data retrieved by get_option_chain_data.

Parameters
data: pd.DataFrame - DataFrame from get_option_chain_data.

## Error Handling
API Errors: Implement try-except blocks for API requests to handle errors like timeouts or invalid responses.
Data Validation: Check input formats for instrument_name, expiry_date, and side to prevent processing errors.
Documentation and AI Assistance

## AI tools were used to:
Generate skeletons for functions, error handling strategies, and code comments.
Research financial terms related to options trading and API usage.
Document and optimize code structure for readability and performance.

## Additional Resources
Upstox API Documentation: Upstox API
Pandas Documentation: Pandas
Python Requests Library: Requests

