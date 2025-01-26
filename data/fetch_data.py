import requests
import pandas as pd
from typing import Dict, Tuple, Optional
import logging
from datetime import datetime

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Define API endpoints
QUIZ_ENDPOINT = "https://jsonkeeper.com/b/LLQT"
QUIZ_SUBMISSION_DATA = "https://api.jsonserve.com/rJvd7g"
HISTORICAL_DATA = "https://api.jsonserve.com/XgAgFJ"

def fetch_data(api_url: str) -> Optional[Dict]:
    """
    Fetch data from a given API endpoint.
    
    Args:
        api_url (str): The API endpoint URL.
        
    Returns:
        Optional[Dict]: Parsed JSON data or None if request fails.
    """
    try:
        # Disable SSL verification but keep a warning
        response = requests.get(api_url, timeout=10, verify=False)
        response.raise_for_status()
        
        # Ensure we get a list or dict
        data = response.json()
        if not isinstance(data, (list, dict)):
            logger.error(f"Unexpected data format from {api_url}")
            return None
            
        return data
        
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching data from {api_url}: {e}")
        return None
    except ValueError as e:
        logger.error(f"Error parsing JSON from {api_url}: {e}")
        return None

def process_data_to_df(data: Optional[Dict], data_type: str) -> Optional[pd.DataFrame]:
    """
    Convert JSON data to DataFrame with proper handling of nested structures.
    
    Args:
        data (Optional[Dict]): JSON data to convert
        data_type (str): Type of data for logging purposes
        
    Returns:
        Optional[pd.DataFrame]: Converted DataFrame or None if conversion fails
    """
    if data is None:
        logger.warning(f"No {data_type} data available")
        return None
        
    try:
        # Handle both list and dict inputs
        if isinstance(data, dict):
            df = pd.DataFrame([data])  # Convert single dict to DataFrame
        else:
            df = pd.DataFrame(data)  # Convert list of dicts to DataFrame
            
        # Add timestamp
        df['processed_at'] = datetime.now()
        
        if df.empty:
            logger.warning(f"Empty DataFrame created from {data_type} data")
            return None
            
        logger.info(f"Successfully created DataFrame for {data_type} data with {len(df)} rows")
        return df
        
    except Exception as e:
        logger.error(f"Error converting {data_type} data to DataFrame: {e}")
        return None

def fetch_all_data() -> Tuple[Optional[pd.DataFrame], Optional[pd.DataFrame], Optional[pd.DataFrame]]:
    """
    Fetch data from all endpoints and return them as DataFrames.
    
    Returns:
        Tuple[Optional[pd.DataFrame], Optional[pd.DataFrame], Optional[pd.DataFrame]]: 
        DataFrames for quiz endpoint, current quiz data, and historical quiz data.
    """
    # Show warning about SSL verification
    import warnings
    warnings.filterwarnings('once', message='Unverified HTTPS request')
    
    # Fetch all data
    quiz_endpoint_data = fetch_data(QUIZ_ENDPOINT)
    quiz_submission_data = fetch_data(QUIZ_SUBMISSION_DATA)
    historical_data = fetch_data(HISTORICAL_DATA)
    
    # Convert to DataFrames with proper error handling
    quiz_df = process_data_to_df(quiz_endpoint_data, "quiz")
    current_quiz_df = process_data_to_df(quiz_submission_data, "submission")
    historical_quiz_df = process_data_to_df(historical_data, "historical")
    
    return quiz_df, current_quiz_df, historical_quiz_df

def main():
    """Main function to demonstrate usage."""
    quiz_df, current_df, historical_df = fetch_all_data()
    
    # Print data summaries if available
    if quiz_df is not None:
        print("\nQuiz Data Summary:")
        print(quiz_df.info())
        print("\nFirst few rows:")
        print(quiz_df.head())
        
    if current_df is not None:
        print("\nCurrent Quiz Submission Summary:")
        print(current_df.info())
        print("\nFirst few rows:")
        print(current_df.head())
        
    if historical_df is not None:
        print("\nHistorical Data Summary:")
        print(historical_df.info())
        print("\nFirst few rows:")
        print(historical_df.head())

if __name__ == "__main__":
    main()
