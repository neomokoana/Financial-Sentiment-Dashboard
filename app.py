import streamlit as st
import requests
import json
import os
from dotenv import load_dotenv
import plotly.express as px
import pandas as pd

# Load environment variables from .env file
load_dotenv()

# --- Configuration ---
# Get Gemini API key from environment variables
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    st.error("GEMINI_API_KEY not found in environment variables. Please set it in a .env file.")
    st.stop() # Stop the app if the API key is missing

API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"
HEADERS = {
    "Content-Type": "application/json"
}

# --- Helper Functions ---

def analyze_sentiment(text):
    """
    Analyzes the sentiment of the given text using the Gemini API.
    Returns a dictionary with sentiment, confidence, and keywords.
    """
    if not text.strip():
        return {"error": "Please enter some text to analyze."}

    prompt = f"""Analyze the sentiment of the following text and categorize it as "Positive", "Negative", or "Neutral". Also, identify up to 5 key keywords or phrases that strongly contribute to this sentiment.

    Provide the output in a JSON format like this:
    {{
        "sentiment": "SentimentCategory",
        "confidence": "ConfidenceLevel", // e.g., "High", "Medium", "Low"
        "keywords": ["keyword1", "keyword2", "keyword3"]
    }}

    Text: "{text}"
    """

    payload = {
        "contents": [
            {"role": "user", "parts": [{"text": prompt}]}
        ],
        "generationConfig": {
            "responseMimeType": "application/json",
            "responseSchema": {
                "type": "OBJECT",
                "properties": {
                    "sentiment": {"type": "STRING"},
                    "confidence": {"type": "STRING"},
                    "keywords": {
                        "type": "ARRAY",
                        "items": {"type": "STRING"}
                    }
                },
                "propertyOrdering": ["sentiment", "confidence", "keywords"]
            }
        }
    }

    try:
        response = requests.post(f"{API_URL}?key={GEMINI_API_KEY}", headers=HEADERS, data=json.dumps(payload))
        response.raise_for_status() # Raise an exception for HTTP errors (4xx or 5xx)
        result = response.json()

        if result.get("candidates") and len(result["candidates"]) > 0 and \
           result["candidates"][0].get("content") and \
           result["candidates"][0]["content"].get("parts") and \
           len(result["candidates"][0]["content"]["parts"]) > 0:
            json_text = result["candidates"][0]["content"]["parts"][0]["text"]
            parsed_json = json.loads(json_text)
            return parsed_json
        else:
            return {"error": "Could not get a valid sentiment analysis result from the API."}

    except requests.exceptions.RequestException as e:
        return {"error": f"API request failed: {e}"}
    except json.JSONDecodeError:
        return {"error": "Failed to parse API response as JSON."}
    except Exception as e:
        return {"error": f"An unexpected error occurred: {e}"}

def get_sentiment_color(sentiment):
    """Returns Tailwind-like classes for sentiment display."""
    sentiment_map = {
        'positive': {'text': 'text-green-600', 'bg': 'bg-green-100', 'border': 'border-green-400'},
        'negative': {'text': 'text-red-600', 'bg': 'bg-red-100', 'border': 'border-red-400'},
        'neutral': {'text': 'text-gray-600', 'bg': 'bg-gray-100', 'border': 'border-gray-400'},
    }
    s = sentiment.lower() if sentiment else ''
    return sentiment_map.get(s, {'text': 'text-gray-800', 'bg': 'bg-gray-50', 'border': 'border-gray-300'})

# --- Streamlit UI ---

st.set_page_config(
    page_title="Financial Sentiment Dashboard",
    layout="centered",
    initial_sidebar_state="auto"
)

# Apply custom CSS for Inter font and general styling
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    html, body, [class*="st-"] {
        font-family: 'Inter', sans-serif;
    }
    .stApp {
        background-color: #f9fafb; /* Light gray background */
    }
    .stApp > header {
        display: none; /* Hide Streamlit's default header */
    }
    .st-emotion-cache-vk3ypu { /* Targeting the main block container */
        background-color: #ffffff;
        padding: 2rem;
        border-radius: 0.75rem; /* rounded-xl */
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05); /* shadow-lg */
        border: 1px solid #e5e7eb; /* border border-gray-200 */
        max-width: 48rem; /* max-w-2xl equivalent */
        margin: auto; /* Center the content */
    }
    .stButton > button {
        width: 100%;
        background-color: #2563eb; /* bg-blue-600 */
        color: white;
        font-weight: 600; /* font-semibold */
        padding-top: 0.75rem; /* py-3 */
        padding-bottom: 0.75rem; /* py-3 */
        padding-left: 1.5rem; /* px-6 */
        padding-right: 1.5rem; /* px-6 */
        border-radius: 0.5rem; /* rounded-lg */
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06); /* shadow-md */
        transition: all 0.3s ease-in-out; /* transition duration-300 ease-in-out */
    }
    .stButton > button:hover {
        background-color: #1d4ed8; /* hover:bg-blue-700 */
        transform: scale(1.02); /* hover:scale-105 */
    }
    .stButton > button:disabled {
        opacity: 0.5;
        cursor: not-allowed;
    }
    .stTextArea > label {
        font-size: 0.875rem; /* text-sm */
        font-weight: 500; /* font-medium */
        color: #374151; /* text-gray-700 */
        margin-bottom: 0.5rem; /* mb-2 */
        display: block;
    }
    .stTextArea > div > textarea {
        border: 1px solid #d1d5db; /* border border-gray-300 */
        border-radius: 0.5rem; /* rounded-lg */
        padding: 0.75rem; /* p-3 */
        min-height: 120px; /* min-h-[120px] */
        transition: all 0.2s ease-in-out;
    }
    .stTextArea > div > textarea:focus {
        border-color: #3b82f6; /* focus:border-blue-500 */
        box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.5); /* focus:ring-2 focus:ring-blue-500 */
        outline: none;
    }
    .sentiment-result-card {
        background-color: #f9fafb; /* bg-gray-50 */
        padding: 1.5rem; /* p-6 */
        border-radius: 0.75rem; /* rounded-xl */
        border: 1px solid #e5e7eb; /* border border-gray-200 */
        box-shadow: inset 0 2px 4px 0 rgba(0, 0, 0, 0.06); /* shadow-inner */
    }
    .sentiment-value {
        padding: 0.5rem 1rem; /* px-4 py-2 */
        border-radius: 0.5rem; /* rounded-lg */
    }
    .keyword-tag {
        background-color: #dbeafe; /* bg-blue-100 */
        color: #1e40af; /* text-blue-800 */
        font-size: 0.875rem; /* text-sm */
        font-weight: 500; /* font-medium */
        padding: 0.25rem 0.75rem; /* px-3 py-1 */
        border-radius: 9999px; /* rounded-full */
        box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.05); /* shadow-sm */
    }
    .error-message {
        background-color: #fee2e2; /* bg-red-100 */
        border: 1px solid #f87171; /* border-red-400 */
        color: #b91c1c; /* text-red-700 */
        padding: 0.75rem 1rem; /* px-4 py-3 */
        border-radius: 0.5rem; /* rounded-lg */
        position: relative;
        margin-bottom: 1.5rem; /* mb-6 */
    }
    .error-message strong {
        font-weight: 700; /* font-bold */
    }
    .error-message span {
        margin-left: 0.5rem; /* ml-2 */
    }
    </style>
    """, unsafe_allow_html=True)

st.title("Financial Sentiment Dashboard")

st.markdown("""
    <div style="margin-bottom: 1.5rem;">
        <label class="block text-gray-700 text-sm font-medium mb-2">
            Enter Text for Analysis:
        </label>
    </div>
""", unsafe_allow_html=True)

text_input = st.text_area(
    label="", # Label moved to markdown for custom styling
    placeholder="e.g., 'The company's Q4 earnings exceeded expectations, leading to a strong stock performance.'",
    height=150,
    key="sentiment_text_input"
)

if st.button("Analyze Sentiment"):
    if not text_input:
        st.markdown(
            """
            <div class="error-message">
                <strong>Error:</strong>
                <span>Please enter some text to analyze.</span>
            </div>
            """, unsafe_allow_html=True
        )
    else:
        with st.spinner("Analyzing sentiment..."):
            result = analyze_sentiment(text_input)

        if "error" in result:
            st.markdown(
                f"""
                <div class="error-message">
                    <strong>Error:</strong>
                    <span>{result['error']}</span>
                </div>
                """, unsafe_allow_html=True
            )
        else:
            st.subheader("Analysis Results:")
            sentiment_colors = get_sentiment_color(result.get('sentiment'))

            col1, col2 = st.columns(2)

            with col1:
                st.markdown(f"""
                    <div class="p-4 rounded-lg shadow-sm flex flex-col items-center justify-center border {sentiment_colors['border']}">
                        <p class="text-sm font-medium text-gray-600">Sentiment:</p>
                        <p class="text-3xl font-bold {sentiment_colors['text']} {sentiment_colors['bg']} sentiment-value">
                            {result.get('sentiment', 'N/A')}
                        </p>
                    </div>
                """, unsafe_allow_html=True)

            with col2:
                st.markdown(f"""
                    <div class="p-4 rounded-lg shadow-sm flex flex-col items-center justify-center border border-gray-300">
                        <p class="text-sm font-medium text-gray-600">Confidence:</p>
                        <p class="text-2xl font-bold text-blue-700">
                            {result.get('confidence', 'N/A')}
                        </p>
                    </div>
                """, unsafe_allow_html=True)

            if result.get('keywords'):
                st.markdown("---") # Separator
                st.markdown("<h3 class='text-lg font-medium text-gray-700 mb-2'>Sentiment Drivers (Keywords):</h3>", unsafe_allow_html=True)
                keyword_html = ""
                for keyword in result['keywords']:
                    keyword_html += f"<span class='keyword-tag'>{keyword}</span>"
                st.markdown(f"<div style='display: flex; flex-wrap: wrap; gap: 0.5rem;'>{keyword_html}</div>", unsafe_allow_html=True)

            st.markdown("---") # Separator for charts
            st.subheader("Visualizations:")

            # --- Confidence Bar Chart ---
            confidence_level = result.get('confidence', 'N/A')
            confidence_value_map = {
                'Low': 1,
                'Medium': 2,
                'High': 3,
                'N/A': 0 # For cases where confidence isn't provided
            }
            data = {
                'Metric': ['Confidence'],
                'Value': [confidence_value_map.get(confidence_level, 0)],
                'Level': [confidence_level]
            }
            df_confidence = pd.DataFrame(data)

            fig_confidence = px.bar(
                df_confidence,
                x='Metric',
                y='Value',
                color='Level', # Color by confidence level
                color_discrete_map={'Low': 'red', 'Medium': 'orange', 'High': 'green', 'N/A': 'gray'},
                title='Confidence of Sentiment Classification',
                height=300,
                labels={'Value': 'Confidence Score (1-3)', 'Metric': ''}
            )
            fig_confidence.update_layout(showlegend=False) # Hide legend as color is self-explanatory
            fig_confidence.update_yaxes(range=[0, 3.5], tickvals=[1, 2, 3], ticktext=['Low', 'Medium', 'High'])
            st.plotly_chart(fig_confidence, use_container_width=True)

            # --- Placeholder for Overall Sentiment Distribution (Pie Chart) ---
            st.markdown("""
                <div class="mt-6 p-4 bg-blue-50 rounded-lg border border-blue-200">
                    <h3 class="text-lg font-semibold text-blue-800 mb-2">Overall Sentiment Distribution (Coming Soon):</h3>
                    <p class="text-sm text-blue-700">
                        A pie chart showing the distribution of Positive, Negative, and Neutral sentiments will be most useful when analyzing multiple texts (e.g., from a file upload or batch processing).
                        This feature will be added in a future update to provide a holistic view of sentiment across a dataset.
                    </p>
                </div>
            """, unsafe_allow_html=True)


            st.markdown("""
                <div class="mt-6 text-sm text-gray-500 italic">
                    <p>Note: Sentiment analysis is performed by an AI model and may not always capture the full nuance of human language, especially in complex financial contexts. Confidence levels are indicative of the model's certainty.</p>
                </div>
            """, unsafe_allow_html=True)
