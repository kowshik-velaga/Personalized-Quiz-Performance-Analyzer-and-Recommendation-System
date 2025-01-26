import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import os
import sys
from pathlib import Path

# Add project root to Python path
sys.path.append(str(Path(__file__).parent.parent))

from data.fetch_data import fetch_all_data
from data.preprocess_data import preprocess_all_data

# Create a directory for saving visualizations
OUTPUT_DIR = "visualizations/output_visuals"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def generate_performance_visualizations(historical_df):
    """Generate basic performance visualizations."""
    
    # Set basic style instead of seaborn
    plt.style.use('default')
    
    # Create figure with multiple subplots (now 1x3 instead of 2x2)
    fig = plt.figure(figsize=(15, 5))
    
    try:
        # 1. Accuracy Trend
        plt.subplot(1, 3, 1)
        historical_df['submitted_at'] = pd.to_datetime(historical_df['submitted_at'])
        plt.plot(historical_df['submitted_at'], historical_df['accuracy_percentage'])
        plt.title('Accuracy Trend Over Time')
        plt.xticks(rotation=45)
        
        # 2. Speed vs Accuracy (moved to middle)
        plt.subplot(1, 3, 2)
        plt.scatter(historical_df['speed'], historical_df['accuracy_percentage'])
        plt.title('Speed vs Accuracy')
        
        # 3. Mistakes Distribution (moved to right)
        plt.subplot(1, 3, 3)
        plt.hist(historical_df['incorrect_answers'], bins=10)
        plt.title('Distribution of Mistakes')
        
        plt.tight_layout()
        output_path = os.path.join(OUTPUT_DIR, 'performance_summary.png')
        plt.savefig(output_path)
        plt.close()
        print(f"Visualizations saved to: {output_path}")
        
    except Exception as e:
        print(f"Error generating visualizations: {e}")
        plt.close()

def save_text_report(analysis_results, filepath='visualizations/output_visuals/report.txt'):
    """Save analysis results as a formatted text file."""
    try:
        with open(filepath, 'w') as f:
            f.write("QUIZ PERFORMANCE ANALYSIS REPORT\n")
            f.write("=" * 30 + "\n\n")
            
            f.write("STUDENT PERSONA\n")
            f.write("-" * 15 + "\n")
            f.write(f"Learning Style: {analysis_results['student_persona']}\n\n")
            
            f.write("STRENGTHS\n")
            f.write("-" * 9 + "\n")
            for strength in analysis_results['strengths']:
                f.write(f"• {strength}\n")
            f.write("\n")
            
            f.write("RECOMMENDATIONS\n")
            f.write("-" * 15 + "\n")
            for rec in analysis_results['recommendations']:
                f.write(f"• {rec}\n")
        
        print(f"Report saved to: {filepath}")
        
    except Exception as e:
        print(f"Error saving report: {e}")

def main():
    try:
        # Fetch and process data
        quiz_df, current_df, historical_df = fetch_all_data()
        processed_quiz_df, processed_current_df, processed_historical_df = preprocess_all_data(
            quiz_df, current_df, historical_df
        )
        
        if processed_historical_df is None:
            print("No historical data available for visualization")
            return
            
        # Generate visualizations
        generate_performance_visualizations(processed_historical_df)
        
        # Example analysis results (replace with actual analysis)
        analysis_results = {
            'student_persona': 'Visual Learner',
            'strengths': ['Data Structures', 'Algorithms'],
            'recommendations': [
                'Focus more on Database concepts',
                'Practice timed exercises',
                'Review fundamentals of System Design'
            ]
        }
        
        # Save text report
        save_text_report(analysis_results)
        
    except Exception as e:
        print(f"Error in main: {e}")

if __name__ == "__main__":
    main()
