import pandas as pd
import logging
import sys
import os

# Add the project root directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def analyze_topic_accuracy(historical_quiz_df):
    """
    Analyze topic-wise accuracy from historical quiz data.
    :param historical_quiz_df: pd.DataFrame - Preprocessed historical quiz data.
    :return: pd.DataFrame - Topic-wise accuracy report.
    """
    if historical_quiz_df is None or historical_quiz_df.empty:
        logger.warning("Historical quiz data is empty or None.")
        return None

    try:
        # Extract topic data from the 'quiz' column and flatten
        historical_quiz_df['topic'] = historical_quiz_df['quiz'].apply(lambda x: x.get('topic', 'Unknown') if isinstance(x, dict) else 'Unknown')
        
        # Group by topic and calculate accuracy
        topic_accuracy = historical_quiz_df.groupby('topic')['accuracy_percentage'].mean().reset_index()
        topic_accuracy.rename(columns={'accuracy_percentage': 'average_accuracy'}, inplace=True)
        topic_accuracy.sort_values(by='average_accuracy', ascending=True, inplace=True)
        
        logger.info("Topic-wise accuracy analysis complete.")
        return topic_accuracy

    except Exception as e:
        logger.error(f"Error analyzing topic accuracy: {e}")
        return None

def analyze_difficulty_performance(historical_quiz_df):
    """
    Analyze performance by difficulty level from historical quiz data.
    :param historical_quiz_df: pd.DataFrame - Preprocessed historical quiz data.
    :return: pd.DataFrame - Difficulty-level performance report.
    """
    if historical_quiz_df is None or historical_quiz_df.empty:
        logger.warning("Historical quiz data is empty or None.")
        return None

    try:
        # Extract difficulty level from the 'quiz' column and flatten
        historical_quiz_df['difficulty_level'] = historical_quiz_df['quiz'].apply(lambda x: x.get('difficulty_level', 'Unknown') if isinstance(x, dict) else 'Unknown')
        
        # Group by difficulty level and calculate accuracy
        difficulty_performance = historical_quiz_df.groupby('difficulty_level')['accuracy_percentage'].mean().reset_index()
        difficulty_performance.rename(columns={'accuracy_percentage': 'average_accuracy'}, inplace=True)
        difficulty_performance.sort_values(by='average_accuracy', ascending=True, inplace=True)
        
        logger.info("Difficulty-level performance analysis complete.")
        return difficulty_performance

    except Exception as e:
        logger.error(f"Error analyzing difficulty performance: {e}")
        return None

def analyze_improvement_trends(historical_quiz_df):
    """
    Analyze improvement trends over time from historical quiz data.
    :param historical_quiz_df: pd.DataFrame - Preprocessed historical quiz data.
    :return: pd.DataFrame - Improvement trend report.
    """
    if historical_quiz_df is None or historical_quiz_df.empty:
        logger.warning("Historical quiz data is empty or None.")
        return None

    try:
        # Sort data by submission time to ensure correct chronological order
        historical_quiz_df['submitted_at'] = pd.to_datetime(historical_quiz_df['submitted_at'])
        historical_quiz_df.sort_values(by='submitted_at', inplace=True)
        
        # Calculate cumulative accuracy trend
        historical_quiz_df['cumulative_accuracy'] = historical_quiz_df['accuracy_percentage'].expanding().mean()
        
        logger.info("Improvement trend analysis complete.")
        return historical_quiz_df[['submitted_at', 'accuracy_percentage', 'cumulative_accuracy']]

    except Exception as e:
        logger.error(f"Error analyzing improvement trends: {e}")
        return None

def analyze_all(historical_quiz_df):
    """
    Perform all analyses and return a comprehensive summary.
    :param historical_quiz_df: pd.DataFrame - Preprocessed historical quiz data.
    :return: dict - Contains topic accuracy, difficulty performance, and improvement trends.
    """
    topic_accuracy = analyze_topic_accuracy(historical_quiz_df)
    difficulty_performance = analyze_difficulty_performance(historical_quiz_df)
    improvement_trends = analyze_improvement_trends(historical_quiz_df)
    
    return {
        "topic_accuracy": topic_accuracy,
        "difficulty_performance": difficulty_performance,
        "improvement_trends": improvement_trends,
    }

if __name__ == "__main__":
    # Load preprocessed data (assuming it's already preprocessed)
    from data.preprocess_data import preprocess_all_data
    from data.fetch_data import fetch_all_data

    # Fetch and preprocess data
    quiz_df, current_quiz_df, historical_quiz_df = fetch_all_data()
    _, _, processed_historical_quiz_df = preprocess_all_data(quiz_df, current_quiz_df, historical_quiz_df)

    # Perform analysis
    analysis_results = analyze_all(processed_historical_quiz_df)

    # Display results
    if analysis_results["topic_accuracy"] is not None:
        print("\nTopic-wise Accuracy:")
        print(analysis_results["topic_accuracy"])

    if analysis_results["difficulty_performance"] is not None:
        print("\nDifficulty-level Performance:")
        print(analysis_results["difficulty_performance"])

    if analysis_results["improvement_trends"] is not None:
        print("\nImprovement Trends:")
        print(analysis_results["improvement_trends"].head())
