from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import logging

# Initialize Flask app
app = Flask(__name__)

# Configure CORS
CORS(app)

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Predefined intents and responses for various DoJ topics including greeting
INTENTS = {
    'greeting': ["hi", "hello", "hey", "greetings","good morning","good afternoon","good evening"],
    'divisions': ["divisions", "departments", "section", "areas", "branches"],
    'judges': ["judges", "appointments", "vacancies", "supreme court", "high courts", "district courts"],
    'case_status': ["case", "status", "check", "pending", "disposed", "njdg"],
    'traffic_fine': ["traffic", "fine", "pay", "violation", "challan"],
    'live_streaming': ["live", "streaming", "watch", "court", "hearing"],
    'efiling': ["efiling", "filing", "submit", "online", "court", "cases"],
    'fast_track': ["fast track", "courts", "speedy", "sensitive", "rape", "pocso"],
    'ecourts_app': ["download", "ecourts", "app", "mobile", "install"],
    'tele_law': ["tele law", "legal", "aid", "assistance"],
}

# Predefined chatbot responses
RESPONSES = {
    'greeting': "Hello! How can I assist you with information about the Department of Justice today?",
    'divisions': "The Department of Justice (DoJ) has various divisions including Legal Affairs, Legislative Department, and Department of Justice.",
    'judges': "Currently, there are X judges in the Supreme Court, Y judges in the High Courts, and Z judges in District and Subordinate Courts. For vacancies, check the official website.",
    'case_status': "You can check the status of your case on the National Judicial Data Grid (NJDG) website at https://njdg.ecourts.gov.in.",
    'traffic_fine': "To pay a traffic violation fine, visit the ePay portal at https://echallan.parivahan.gov.in/.",
    'live_streaming': "Live streaming of court cases is available on the official Supreme Court website and other relevant platforms.",
    'efiling': "You can submit cases online using the eFiling system at https://efiling.ecourts.gov.in.",
    'fast_track': "Fast Track Courts handle sensitive cases such as rape and POCSO-related cases for speedy justice.",
    'ecourts_app': "You can download the eCourts Services Mobile App from the Google Play Store or Apple App Store.",
    'tele_law': "Tele-Law services provide legal aid through Common Service Centers. You can avail assistance through their platform.",
}

import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import string

# Download required NLTK data
nltk.download('punkt')
nltk.download('stopwords')

# Function to clean and tokenize user input
def preprocess_input(user_input):
    try:
        # Ensure that user input is valid and not empty
        if not user_input or not isinstance(user_input, str):
            return []  # Return an empty list for invalid input
        
        # Tokenize the user input
        tokens = word_tokenize(user_input.lower())
        
        # Remove stopwords and punctuation
        tokens = [word for word in tokens if word not in stopwords.words('english') and word not in string.punctuation]
        
        return tokens
    except Exception as e:
        # Log the error for debugging
        print(f"Error preprocessing input: {e}")
        return []  # Return an empty list if an error occurs


# Function to determine the user's intent based on keywords
def detect_intent(tokens):
    try:
        # Debugging: Log tokenized input
        logger.debug(f"Detecting intent with tokens: {tokens}")
        
        # Check if greeting intent exists first
        for keyword in INTENTS['greeting']:
            if keyword in tokens:
                return 'greeting'

        # Check other intents
        for intent, keywords in INTENTS.items():
            if intent == 'greeting':
                continue  # Skip greeting since it's already checked
            if any(keyword in tokens for keyword in keywords):
                return intent

        return 'unknown'  # Return 'unknown' when no intent matches
    except Exception as e:
        logger.error(f"Error detecting intent: {e}")
        return 'unknown'

# Flask route for homepage
@app.route('/')
def index():
    return render_template('index.html')

# Flask route to handle user input (AJAX call)
@app.route('/get_response', methods=['POST'])
def get_response():
    try:
        user_input = request.form.get('user_input', '').strip()  # Get and sanitize user input

        # Ensure user input is valid
        if not user_input:
            return jsonify({'response': "Please enter a message."})

        # Preprocess user input
        tokens = preprocess_input(user_input)
        
        # If preprocessing failed or tokens are empty
        if not tokens:
            return jsonify({'response': "I couldn't process your input. Could you clarify or try again?"})

        # Detect intent and return the response
        intent = detect_intent(tokens)
        response = RESPONSES.get(intent, f"I couldn't identify the exact context of your query. Could you provide more details about {user_input}?")
        
        return jsonify({'response': response})
    
    except Exception as e:
        # Log the error for debugging
        print(f"Error: {e}")
        return jsonify({'response': "An internal error occurred. Please try again later."})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
