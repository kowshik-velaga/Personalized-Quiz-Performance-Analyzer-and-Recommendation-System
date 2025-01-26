import pandas as pd
from .fetch_data import fetch_all_data
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def preprocess_current_quiz_data(current_quiz_df):
    """
    Preprocess Current Quiz Data.
    """
    if current_quiz_df is None or current_quiz_df.empty:
        logger.warning("Current quiz data is empty or None.")
        return None

    try:
        # First, let's log the columns we have
        logger.info(f"Current quiz columns: {current_quiz_df.columns.tolist()}")
        
        # Convert accuracy from string to float (remove '%' sign and spaces)
        if 'accuracy' in current_quiz_df.columns:
            current_quiz_df['accuracy_percentage'] = current_quiz_df['accuracy'].str.strip().str.rstrip('%').astype(float)
        
        return current_quiz_df

    except Exception as e:
        logger.error(f"Error preprocessing current quiz data: {e}")
        return None

def preprocess_historical_data(historical_quiz_df):
    """
    Preprocess Historical Quiz Data.
    """
    if historical_quiz_df is None or historical_quiz_df.empty:
        logger.warning("Historical quiz data is empty or None.")
        return None

    try:
        # Log the columns
        logger.info(f"Historical quiz columns: {historical_quiz_df.columns.tolist()}")
        
        # Convert accuracy from string to float
        if 'accuracy' in historical_quiz_df.columns:
            historical_quiz_df['accuracy_percentage'] = historical_quiz_df['accuracy'].str.strip().str.rstrip('%').astype(float)
        
        return historical_quiz_df

    except Exception as e:
        logger.error(f"Error preprocessing historical data: {e}")
        return None

def preprocess_quiz_endpoint_data(quiz_df):
    """
    Preprocess Quiz Endpoint Data.
    """
    if quiz_df is None or quiz_df.empty:
        logger.warning("Quiz endpoint data is empty or None.")
        return None

    try:
        # Log the columns we have
        logger.info(f"Quiz endpoint columns: {quiz_df.columns.tolist()}")
        
        # Create a copy to avoid modifying the original
        processed_df = quiz_df.copy()
        
        # Map columns if they exist
        column_mapping = {
            'name': 'quiz_title',  # Assuming 'name' instead of 'title'
            'id': 'quiz_id',
            'topic': 'topic',
            'duration': 'duration',
            'difficulty_level': 'difficulty_level'
        }
        
        # Only map columns that exist
        for old_col, new_col in column_mapping.items():
            if old_col in processed_df.columns:
                processed_df[new_col] = processed_df[old_col]
                logger.info(f"Mapped column {old_col} to {new_col}")
        
        return processed_df

    except Exception as e:
        logger.error(f"Error preprocessing quiz endpoint data: {e}")
        return None

def preprocess_all_data(quiz_df, current_quiz_df, historical_quiz_df):
    """
    Preprocess all datasets and return cleaned versions.
    """
    processed_quiz_df = preprocess_quiz_endpoint_data(quiz_df)
    processed_current_quiz_df = preprocess_current_quiz_data(current_quiz_df)
    processed_historical_quiz_df = preprocess_historical_data(historical_quiz_df)

    return processed_quiz_df, processed_current_quiz_df, processed_historical_quiz_df

def main():
    """Main function to demonstrate usage."""
    # Fetch the data
    quiz_df, current_quiz_df, historical_quiz_df = fetch_all_data()

    # Preprocess the data
    processed_quiz_df, processed_current_quiz_df, processed_historical_quiz_df = preprocess_all_data(
        quiz_df, current_quiz_df, historical_quiz_df
    )

    # Display processed data for verification
    if processed_quiz_df is not None:
        print("\nProcessed Quiz Endpoint Data:")
        print("\nColumns:", processed_quiz_df.columns.tolist())
        print("\nSample data:")
        print(processed_quiz_df.head())

    if processed_current_quiz_df is not None:
        print("\nProcessed Current Quiz Data:")
        print("\nColumns:", processed_current_quiz_df.columns.tolist())
        print("\nSample data:")
        print(processed_current_quiz_df.head())

    if processed_historical_quiz_df is not None:
        print("\nProcessed Historical Quiz Data:")
        print("\nColumns:", processed_historical_quiz_df.columns.tolist())
        print("\nSample data:")
        print(processed_historical_quiz_df.head())

if __name__ == "__main__":
    main()
