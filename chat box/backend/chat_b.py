# chat_b.py
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
from datetime import datetime

app = Flask(__name__, static_folder='../frontend', static_url_path='')
CORS(app)

questions = []
id_counter = 1

@app.route('/')
def serve_home():
    return send_from_directory('../frontend', 'chat_f.html')

@app.route('/questions', methods=['GET'])
def get_questions():
    return jsonify(questions[::-1])  # return latest questions first

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

if __name__ == '__main__':
    app.run(debug=True)