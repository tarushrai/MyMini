from flask import Flask, request, jsonify, session
from transformers import pipeline
from textblob import TextBlob
import random

# Initialize Flask app
app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Required for session management

# Load pre-trained empathy model
empathy_model = pipeline('text-generation', model='gpt-3')

# Route to manage chatbot interactions with session-based memory
@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message")
    user_id = request.json.get("user_id")  # Assume user_id is sent by the front end
    
    # Initialize session if not present
    if "conversation" not in session:
        session["conversation"] = []
    
    # Analyze sentiment of user input
    sentiment = analyze_sentiment(user_input)

    # Generate an empathetic response
    empathy_response = empathy_model(f"{user_input}. Respond with empathy.")[0]['generated_text']

    # If user is showing negative sentiment, suggest helpful resources
    if sentiment == "negative":
        resources = suggest_mental_health_resources()
        empathy_response += f" I noticed you're feeling down. Here are some resources that might help: {resources}"

    # Store the conversation in session
    session["conversation"].append({"user": user_input, "bot": empathy_response})
    
    # Return the chatbot response
    return jsonify({"response": empathy_response, "conversation": session["conversation"]})

# Sentiment analysis
def analyze_sentiment(text):
    analysis = TextBlob(text)
    if analysis.sentiment.polarity > 0:
        return "positive"
    elif analysis.sentiment.polarity == 0:
        return "neutral"
    else:
        return "negative"

# Suggest mental health resources based on user input
def suggest_mental_health_resources():
    resources = [
        "https://www.mentalhealth.gov/",
        "https://www.headspace.com/",
        "https://www.7cups.com/"
    ]
    return random.choice(resources)

# Route to reset conversation session
@app.route("/reset", methods=["POST"])
def reset_conversation():
    session.pop("conversation", None)
    return jsonify({"message": "Conversation reset."})

if __name__ == "__main__":
    app.run(debug=True)

# Multilingual Support (Translation)
from googletrans import Translator

# Initialize Google Translate API
translator = Translator()

# Translate input text to English before processing
def translate_to_english(text):
    return translator.translate(text, dest='en').text

# Translate bot's response to the user's language
def translate_to_user_language(text, lang_code):
    return translator.translate(text, dest=lang_code).text
