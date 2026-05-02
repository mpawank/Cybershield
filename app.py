from flask import Flask, render_template, request, jsonify
import joblib
import re
import string
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import google.generativeai as genai
import os
from dotenv import load_dotenv
from moderation import moderate_content

app = Flask(__name__)

# Load model and vectorizer
model = joblib.load('nmodel.pkl')
vectorizer = joblib.load('nvectorizer.pkl')

# Initialize NLTK components
nltk.download('punkt')
nltk.download('punkt_tab')
nltk.download('stopwords')
nltk.download('wordnet')

lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words('english'))

load_dotenv()
os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


def clean_text(text):
    """Cleans the input text."""
    text = text.lower()
    text = re.sub(r'\[.*?\]', '', text)
    text = re.sub(r'http\S+', '', text)
    text = re.sub(r'\w*\d\w*', '', text)
    text = re.sub(r'[%s]' % re.escape(string.punctuation), '', text)
    text = re.sub(r'\n', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    return text


def preprocess_input(text):
    """Preprocess the input text for prediction."""
    text = clean_text(text)
    tokens = word_tokenize(text)
    tokens = [lemmatizer.lemmatize(word)
              for word in tokens if word not in stop_words]
    processed_text = ' '.join(tokens)
    vectorized_text = vectorizer.transform([processed_text])
    return vectorized_text


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/predict', methods=['POST'])
def predict():
    comment = request.form['comment']

    # Preprocess and vectorize the input comment
    vectorized_text = preprocess_input(comment)
    prediction = model.predict_proba(vectorized_text)[0]

    result = {
        'toxic': prediction[0],
        'severe_toxic': prediction[1],
        'obscene': prediction[2],
        'threat': prediction[3],
        'insult': prediction[4],
        'identity_hate': prediction[5]
    }

    is_bullying = prediction[6] >= 0.5

    return jsonify({'result': result, 'is_bullying': bool(is_bullying)})


@app.route('/conclude', methods=['POST'])
def conclude():
    print("called")
    predictions = request.json.get('result')
    is_bullying = request.json.get('is_bullying')

    summary = f"The comment is{' not' if not is_bullying else ''} indicative of cyberbullying. "
    summary += "Here are the detailed probabilities for each type of toxicity: "
    for label, score in predictions.items():
        summary += f"{label.capitalize()}: {score:.2f}. "

    api_key = os.getenv("GOOGLE_API_KEY")
    
    # Try Gemini API first
    if api_key:
        try:
            model = genai.GenerativeModel("gemini-3.1-flash-lite-preview")
            response = model.generate_content(
                f"Given the following summary of toxicity predictions for a comment, provide a concise conclusion about the nature of the comment. The prediction is based on a machine learning model, and you should communicate the certainty of the prediction. Here are the detailed probabilities for each type of toxicity: {summary}"
            )
            conclusion_text = response.text
            print("Using Gemini API")
            return jsonify({'conclusion': conclusion_text})
        except Exception as e:
            print(f"Gemini API error: {str(e)}")

    # Fallback to local logic
    print("Using local fallback")
    max_score = max(predictions.values()) if predictions else 0
    
    if is_bullying:
        if max_score > 0.7:
            conclusion_text = "This comment shows strong indicators of cyberbullying with high toxicity levels across multiple categories. The content appears harmful and inappropriate."
        elif max_score > 0.5:
            conclusion_text = "This comment appears to contain potentially harmful content with moderate toxicity indicators. Exercise caution when interacting with this content."
        else:
            conclusion_text = "This comment contains some concerning elements but shows low overall toxicity. The content may require monitoring but is not definitively harmful."
    else:
        if max_score > 0.3:
            conclusion_text = "This comment appears safe with minimal toxicity indicators. However, there are minor traces of concerning language in some categories."
        else:
            conclusion_text = "This comment appears to be safe with no significant toxicity indicators detected. The content is appropriate for general audiences."

    print(conclusion_text)
    return jsonify({'conclusion': conclusion_text})


@app.route('/moderate', methods=['POST'])
def moderate():
    """
    CyberShield AI Moderation Endpoint
    Accepts user-generated content and returns multilingual content moderation results

    Request JSON:
    {
        "content": "user_transcribed_text"
    }

    Response JSON:
    {
        "is_toxic": boolean,
        "category": "one of the predefined categories",
        "confidence": 0.0-1.0,
        "severity": "low | medium | high",
        "detected_language": "language name",
        "normalized_text": "cleaned version",
        "reason": "explanation"
    }
    """
    try:
        data = request.get_json()

        if not data or 'content' not in data:
            return jsonify({'error': 'Missing "content" field in request'}), 400

        content = data.get('content', '').strip()

        if not content:
            return jsonify({'error': 'Content cannot be empty'}), 400

        # Call moderation system
        moderation_result = moderate_content(content)

        # Parse JSON string back to dict for response
        import json
        result_dict = json.loads(moderation_result)

        return jsonify(result_dict), 200

    except Exception as e:
        return jsonify({'error': f'Moderation error: {str(e)}'}), 500


if __name__ == '__main__':
    app.run(debug=True)
