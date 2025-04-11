from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_cors import CORS
from datetime import datetime
import os

app = Flask(__name__)
CORS(app)

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

# ========== RUN ==========
if __name__ == '__main__':
    app.run(debug=True)
