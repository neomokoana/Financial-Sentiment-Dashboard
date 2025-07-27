# Financial-Sentiment-Dashboard
Financial Sentiment Dashboard
An interactive web application built with Streamlit and the Google Gemini API for analyzing sentiment in text data. This dashboard allows users to input text and receive multi-class sentiment classification (Positive, Negative, Neutral) along with a confidence score and key sentiment drivers.

Table of Contents
Features

Technical Specifications

Setup Instructions

Prerequisites

Installation

API Key Configuration

How to Run the Application

Deployment

Future Enhancements

License

Features
Text Input: Analyze sentiment by directly entering text.

Multi-class Sentiment Classification: Classifies text as "Positive," "Negative," or "Neutral."

Confidence Scoring: Provides a confidence level (e.g., "High," "Medium," "Low") for each classification.

Keyword Extraction: Highlights key words or phrases that contribute to the detected sentiment.

Confidence Visualization: Displays a simple bar chart showing the confidence of the sentiment classification.

Responsive Web Interface: Built with Streamlit for an interactive and mobile-friendly user experience.

Error Handling: Basic error messages for invalid inputs or API failures.

Technical Specifications
Frontend/Backend Framework: Streamlit (Python)

NLP API Integration: Google Gemini API (via requests library)

Environment Management: python-dotenv for secure API key handling.

Data Visualization: plotly.express and pandas for charts.

Setup Instructions
Follow these steps to get the project up and running on your local machine.

Prerequisites
Python 3.8+

pip (Python package installer, usually comes with Python)

Installation
Clone the Repository (or create the project directory):

git clone <your-github-repo-url>
cd <your-project-directory>

If you haven't set up a GitHub repo yet, simply create a folder for your project and navigate into it.

Create a Virtual Environment (Recommended):
It's best practice to use a virtual environment to manage dependencies.

python -m venv venv

Activate the Virtual Environment:

Windows (PowerShell):

.\venv\Scripts\activate

macOS / Linux (Bash/Zsh):

source venv/bin/activate

You should see (venv) at the beginning of your terminal prompt, indicating the virtual environment is active.

Install Required Python Packages:
With your virtual environment activated, install the necessary libraries:

pip install streamlit python-dotenv requests plotly pandas

API Key Configuration
Obtain a Gemini API Key:

Go to Google AI Studio and sign in with your Google account.

Follow the instructions to "Get API key" or "Create API key in new project."

Copy your generated API key.

Create a .env file:
In the root of your project directory (the same folder where app.py is located), create a new file named .env.

Add your API Key to .env:
Open the .env file and add the following line, replacing YOUR_ACTUAL_GEMINI_API_KEY_HERE with the key you just copied:

GEMINI_API_KEY=YOUR_ACTUAL_GEMINI_API_KEY_HERE

Important: Do not add quotes around the API key value in the .env file.

Security Note: Never commit your .env file directly to public version control systems like GitHub. It contains sensitive information.

How to Run the Application
Ensure your virtual environment is activated (as described in the "Installation" section).

Navigate to your project directory in the terminal.

Run the Streamlit application:

streamlit run app.py

A new tab in your web browser should automatically open, displaying the Financial Sentiment Dashboard (usually at http://localhost:8501).

Deployment
For easy deployment, Streamlit Community Cloud is highly recommended.

Push your code to a public GitHub repository.

Ensure you have a requirements.txt file in your repository's root (as described in Installation).

Go to https://share.streamlit.io/ and log in with your GitHub account.

Select your repository and branch.

Configure Secrets: Add GEMINI_API_KEY as a secret in the Streamlit Cloud dashboard.

Deploy your app.

Other deployment options include Heroku, Render, or Google Cloud Run, which offer more control but might require additional configuration (e.g., Procfile for Heroku, Dockerfile for containerization).

Future Enhancements
File Upload: Implement functionality to upload text files (e.g., CSV, TXT) for batch analysis.

Batch Processing: Process multiple texts from a file and display aggregate sentiment distribution (e.g., a pie chart of Positive/Negative/Neutral counts).

Comparative Analysis: Allow users to compare sentiment trends or results across different texts or datasets.

Explanation Features: Enhance the rationale behind sentiment scores beyond just keywords (e.g., highlighting specific sentences or phrases).

Export Results: Enable exporting analysis results in formats like CSV, JSON, or PDF.

Audio Input (Speech-to-Text): Integrate a Speech-to-Text API to allow users to record audio and have it transcribed for sentiment analysis.

License
This project is open-source and available under the MIT License. (You would typically create a LICENSE file in your repository with the license text).
