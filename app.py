from flask import Flask, request, jsonify
import openai
from dotenv import load_dotenv
import os
from flask_cors import CORS

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)
CORS(app) 

def load_prompt(file_path):
    with open(file_path, 'r') as file:
        return file.read()

my_bio = load_prompt('prompt.md')

@app.route('/ask-ai', methods=['POST'])
def ask_ai():
    data = request.get_json()
    question = data.get('question', '')

    response = openai.Completion.create(
        engine="gpt-3.5-turbo-instruct",
        prompt=f"{my_bio}\n\nQ: {question}\nA:",
        max_tokens=150,
        temperature=0.2,
    )

    answer = response.choices[0].text.strip()
    return jsonify({'answer': answer})

@app.route('/')
def index():
    return "GarAi backend is running."

if __name__ == '__main__':
    app.run(debug=True)
