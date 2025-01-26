import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def generate_recommendations(analysis_results):
    """
    Generate personalized recommendations based on the analysis results.
    :param analysis_results: dict - Contains topic accuracy, difficulty performance, and improvement trends.
    :return: dict - Personalized recommendations for the user.
    """
    recommendations = {}

    try:
        # 1. Topic Recommendations
        topic_accuracy = analysis_results.get("topic_accuracy")
        if topic_accuracy is not None and not topic_accuracy.empty:
            weak_topics = topic_accuracy[topic_accuracy["average_accuracy"] < 60]
            strong_topics = topic_accuracy[topic_accuracy["average_accuracy"] >= 80]

            if not weak_topics.empty:
                recommendations["weak_topics"] = weak_topics["topic"].tolist()
                recommendations["weak_topics_action"] = "Focus on these topics with additional practice."

            if not strong_topics.empty:
                recommendations["strong_topics"] = strong_topics["topic"].tolist()
                recommendations["strong_topics_action"] = "Keep revising these topics to maintain your strength."

        # 2. Difficulty-Level Recommendations
        difficulty_performance = analysis_results.get("difficulty_performance")
        if difficulty_performance is not None and not difficulty_performance.empty:
            low_difficulty = difficulty_performance[difficulty_performance["average_accuracy"] < 60]
            if not low_difficulty.empty:
                recommendations["difficulty_focus"] = "Work on improving performance for specific difficulty levels."

        # 3. Improvement Trends
        improvement_trends = analysis_results.get("improvement_trends")
        if improvement_trends is not None and not improvement_trends.empty:
            final_accuracy = improvement_trends["cumulative_accuracy"].iloc[-1]
            recommendations["overall_performance"] = (
                f"Your current cumulative accuracy is {final_accuracy:.2f}%. "
                "Keep working to maintain your upward trend."
            )

        # 4. Final Summary
        recommendations["summary"] = "These recommendations are based on your recent performance trends and quiz data."

        logger.info("Recommendations generated successfully.")
        return recommendations

    except Exception as e:
        logger.error(f"Error generating recommendations: {e}")
        return {"error": "Failed to generate recommendations."}

if __name__ == "__main__":
    # Load analysis results
    from analyze_performance import analyze_all
    from data.preprocess_data import preprocess_all_data
    from data.fetch_data import fetch_all_data

    # Fetch and preprocess data
    quiz_df, current_quiz_df, historical_quiz_df = fetch_all_data()
    _, _, processed_historical_quiz_df = preprocess_all_data(quiz_df, current_quiz_df, historical_quiz_df)

    # Perform analysis
    analysis_results = analyze_all(processed_historical_quiz_df)

    # Generate recommendations
    recommendations = generate_recommendations(analysis_results)

    # Display recommendations
    print("\nPersonalized Recommendations:")
    for key, value in recommendations.items():
        print(f"{key}: {value}")
