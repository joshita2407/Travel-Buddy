# app.py
from flask import Flask, render_template, request, jsonify
import requests
import os
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

# Hugging Face API config
API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.1"
headers = {
    "Authorization": f"Bearer {os.getenv('HUGGINGFACE_API_KEY')}",
    "Content-Type": "application/json"
}

def query_huggingface(prompt):
    response = requests.post(API_URL, headers=headers, json={"inputs": prompt})
    if response.status_code == 200:
        return response.json()[0]['generated_text']
    else:
        raise Exception(f"Error {response.status_code}: {response.text}")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    try:
        data = request.get_json()
        destination = data['destination']
        budget = data['budget']
        people = data['people']
        kids = data['kids']
        duration = data['duration']
        interests = data['interests']

        prompt = (
            f"Generate a structured and well-formatted, day-wise travel itinerary in HTML format (using tables, bullet points, and line breaks) "
            f"for a trip to {destination}. There are {people} people going, {'including kids' if kids.lower() == 'yes' else 'no kids'}. "
            f"The trip will last {duration} days and the total budget is ₹{budget}. Interests include: {interests}. "
            "Focus on culture, local experiences, food, and must-visit places."
        )




        itinerary = query_huggingface(prompt)
        return jsonify({'itinerary': itinerary})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
