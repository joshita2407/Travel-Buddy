from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_cors import CORS
from datetime import datetime
import os
import requests
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)
CORS(app)

# ===== Hugging Face API CONFIG =====
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

# ========== MAIN PAGE ==========
@app.route('/')
def home():
    return send_from_directory('main', 'main.html')

@app.route('/addEvent')
def add_event():
    return send_from_directory('main','addEvent.html')

@app.route('/upcoming')
def upcoming_events():
    return send_from_directory('main','upcoming.html')

@app.route('/calendar')
def calender():
    return send_from_directory('main','calendar.html')

@app.route('/journal')
def journel():
    return send_from_directory('main','journal.html')

@app.route('/localStay')
def localStay():
    return send_from_directory('main', 'localStay.html')

@app.route('/contact')
def contact():
    return send_from_directory('main', 'contact.html')

# ========== ITINERARY ROUTE ==========
@app.route('/itinerary')
def itinerary_page():
    return send_from_directory('main','index.html')

# ===== ITINERARY PAGE & GENERATION =====
@app.route('/itinerary')
def show_itinerary_page():
    return send_from_directory('main', 'index.html')

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
            "Focus on culture, local experiences, food, and must-visit places, give a 1 line description about the places they must visit with the timeline."
        )

        itinerary = query_huggingface(prompt)
        return jsonify({'itinerary': itinerary})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ========== CHATBOX FRONTEND ==========
@app.route('/chat')
def chat_page():
    return send_from_directory('chatbox/frontend', 'chat_f.html')

# ========== CHATBOX BACKEND API ==========
questions = []
id_counter = 1

@app.route('/questions', methods=['GET'])
def get_questions():
    return jsonify(questions[::-1])

@app.route('/ask', methods=['POST'])
def ask_question():
    global id_counter
    data = request.json
    question = {
        "id": id_counter,
        "user": data["user"],
        "type": data["type"],
        "question": data["question"],
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "answers": []
    }
    questions.append(question)
    id_counter += 1
    return jsonify({"status": "success"}), 201

@app.route('/answer/<int:qid>', methods=['POST'])
def post_answer(qid):
    data = request.json
    for q in questions:
        if q["id"] == qid:
            q["answers"].append({
                "user": data["user"],
                "type": data["type"],
                "answer": data["answer"],
                "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })
            break
    return jsonify({"status": "success"}), 201
@app.route('/generate', methods=['POST'])
def generate_itinerary():
    data = request.get_json()

    destination = data.get('destination', 'Unknown Destination')
    people = data.get('people')
    kids = data.get('kids')
    kid_count = data.get('kidCount')
    duration = int(data.get('duration', 3))
    budget = data.get('budget')
    interests = data.get('interests')

    # Placeholder itinerary logic (replace with HuggingFace later if needed)
    itinerary = ""
    for day in range(1, duration + 1):
        itinerary += f"Day {day}: Explore {interests} in {destination}.\n"

    return jsonify({"itinerary": itinerary})

# ========== RUN ==========
if __name__ == '__main__':
    app.run(debug=True)
