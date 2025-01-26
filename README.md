# Quiz Performance Analysis System

A data-driven system that analyzes student quiz performance to provide personalized insights and recommendations.

## Project Overview

This system analyzes quiz performance data to:
- Track accuracy trends over time
- Analyze speed vs accuracy relationships
- Monitor mistake patterns
- Generate personalized recommendations
- Create visual performance insights

## Features

- **Performance Analytics**: 
  - Accuracy tracking over time
  - Speed vs accuracy analysis
  - Mistake distribution patterns

- **Personalized Insights**:
  - Student learning profile
  - Strength identification
  - Areas for improvement
  - Custom recommendations

- **Visual Reports**:
  - Interactive performance graphs
  - Progress tracking visualizations
  - Comprehensive performance dashboard

## Tech Stack

- **Backend**: Python, Flask
- **Data Processing**: Pandas
- **Visualization**: Matplotlib, Seaborn
- **API**: RESTful endpoints

## Setup Instructions

Run the following commands step-by-step to set up the project:

```bash
# Step 1: Clone the repository
git clone <repository-url>
cd quiz-analysis-system

# Step 2: Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Step 3: Install dependencies
pip install -r requirements.txt

# Step 4: Generate visualizations
python visualizations/generate_charts.py

# Step 5: Start the Flask server
python api/app.py
```

## API Endpoints

- **Dashboard**: `GET /dashboard`
  - Complete performance overview
  - Student profile
  - Recent achievements
  - Performance metrics

- **Visualizations**: `GET /visualizations/<chart_type>`
  - Performance trend charts
  - Accuracy analysis
  - Speed vs accuracy plots

- **Recommendations**: `GET /recommendations`
  - Personalized learning suggestions
  - Focus area recommendations

- **Student Profile**: `GET /student-profile`
  - Learning style analysis
  - Strength identification
  - Progress tracking

## Project Structure

```
quiz-analysis-system/
├── api/
│   └── app.py                 # Flask API endpoints
├── data/
│   ├── fetch_data.py          # Data retrieval
│   └── preprocess_data.py     # Data preprocessing
├── visualizations/
│   └── generate_charts.py     # Visualization generation
├── analysis/
│   ├── analyze_performance.py # Performance analysis
│   └── recommendations.py     # Recommendation generation
└── README.md
```

## Approach & Methodology

1. **Data Collection**:
   - Fetch quiz performance data
   - Gather historical performance metrics
   - Track attempt timestamps and durations

2. **Data Processing**:
   - Clean and normalize data
   - Calculate performance metrics
   - Identify patterns and trends

3. **Analysis**:
   - Performance trend analysis
   - Speed-accuracy correlation
   - Mistake pattern identification
   - Learning style detection

4. **Visualization**:
   - Generate performance graphs
   - Create progress visualizations
   - Produce comprehensive reports

5. **Recommendation Generation**:
   - Identify areas for improvement
   - Generate personalized suggestions
   - Track progress and adjust recommendations

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

