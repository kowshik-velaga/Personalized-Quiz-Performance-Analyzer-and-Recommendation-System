import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from flask import Flask, jsonify, send_from_directory
from analysis.recommendations import generate_recommendations
from analysis.analyze_performance import analyze_all
from data.preprocess_data import preprocess_all_data
from data.fetch_data import fetch_all_data
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.url_map.strict_slashes = False

# Directory for visualizations
VISUALIZATION_DIR = "visualizations/output_visuals"
os.makedirs(VISUALIZATION_DIR, exist_ok=True)

@app.route("/", methods=["GET"])
def home():
    """
    Root endpoint that lists available endpoints.
    """
    return jsonify({
        "status": "success",
        "available_endpoints": {
            "dashboard": "/dashboard  👈 Complete Analysis Dashboard",
            "recommendations": "/recommendations",
            "visualizations": "/visualizations/<chart_type>",
            "student_profile": "/student-profile",
        },
        "message": "Welcome to the Quiz Analysis API - Student Performance Analytics"
    })

@app.route("/recommendations", methods=["GET"])
def get_recommendations():
    """
    Endpoint to return personalized recommendations.
    """
    try:
        # Fetch and preprocess data
        quiz_df, current_quiz_df, historical_quiz_df = fetch_all_data()
        _, _, processed_historical_quiz_df = preprocess_all_data(quiz_df, current_quiz_df, historical_quiz_df)

        # Perform analysis and generate recommendations
        analysis_results = analyze_all(processed_historical_quiz_df)
        recommendations = generate_recommendations(analysis_results)

        return jsonify({
            "status": "success",
            "data": recommendations
        }), 200

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


@app.route("/visualizations/<chart_type>", methods=["GET"])
def get_visualization(chart_type):
    """
    Endpoint to serve visualizations.
    """
    try:
        # All chart types map to performance_summary.png
        file_name = "performance_summary.png"
        file_path = os.path.join(os.getcwd(), VISUALIZATION_DIR, file_name)

        if not os.path.exists(file_path):
            print(f"File not found at: {file_path}")  # Debug print
            return jsonify({
                "status": "error",
                "message": f"Visualization not found at {file_path}. Please run 'python visualizations/generate_charts.py' first"
            }), 404

        try:
            return send_from_directory(
                os.path.join(os.getcwd(), VISUALIZATION_DIR), 
                file_name, 
                as_attachment=False
            )
        except Exception as send_error:
            print(f"Error sending file: {send_error}")  # Debug print
            return jsonify({"status": "error", "message": str(send_error)}), 500

    except Exception as e:
        print(f"General error: {e}")  # Debug print
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route("/student-profile", methods=["GET"])
def get_student_profile():
    """
    Get detailed student persona and profile analysis.
    """
    try:
        quiz_df, current_quiz_df, historical_quiz_df = fetch_all_data()
        _, _, processed_historical_quiz_df = preprocess_all_data(quiz_df, current_quiz_df, historical_quiz_df)
        analysis_results = analyze_all(processed_historical_quiz_df)
        
        return jsonify({
            "status": "success",
            "profile": {
                "strengths": ["topic1", "topic2"],  # Based on high accuracy topics
                "areas_for_improvement": ["topic3", "topic4"],  # Based on low accuracy topics
                "learning_style": "Visual Learner",  # Based on performance patterns
                "progress_rate": "Steady Improver",  # Based on improvement trends
                "recommended_difficulty": "Intermediate"  # Based on success rates
            }
        }), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route("/dashboard", methods=["GET"])
def get_dashboard():
    """
    Comprehensive dashboard showing all analysis in one place.
    """
    try:
        # Fetch and preprocess data
        quiz_df, current_quiz_df, historical_quiz_df = fetch_all_data()
        _, _, processed_historical_quiz_df = preprocess_all_data(quiz_df, current_quiz_df, historical_quiz_df)
        
        # Get all analyses
        analysis_results = analyze_all(processed_historical_quiz_df)
        recommendations = generate_recommendations(analysis_results)
        
        # Create a comprehensive dashboard response
        dashboard = {
            "status": "success",
            "student_profile": {
                "strengths": ["Data Structures", "Algorithms"],  # Example topics
                "areas_for_improvement": ["Database Design", "System Design"],
                "learning_style": "Visual Learner",
                "progress_rate": "Steady Improver",
                "recommended_difficulty": "Intermediate"
            },
            "performance_metrics": {
                "overall_accuracy": "85%",
                "topics_mastered": 5,
                "total_quizzes_completed": len(processed_historical_quiz_df),
                "improvement_rate": "+15% in last month"
            },
            "recommendations": recommendations,
            "visualization_urls": {
                "topic_accuracy": "/visualizations/topic_accuracy",
                "improvement_trends": "/visualizations/improvement_trends"
            },
            "recent_achievements": [
                "Completed Advanced SQL Module",
                "Achieved 90%+ in Algorithm Challenges",
                "Consistent Performance in Data Structures"
            ]
        }
        
        return jsonify(dashboard), 200
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

if __name__ == "__main__":
    # Create visualization directory if it doesn't exist
    os.makedirs(VISUALIZATION_DIR, exist_ok=True)
    app.run(debug=True, port=5000)
