from flask import Flask, request, jsonify
from flask_cors import CORS
import openai  # Ensure you have an OpenAI API key

app = Flask(__name__)
CORS(app)

# Set your OpenAI API Key
openai.api_key = "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"

@app.route('/analyze', methods=['POST'])  # Accepts only POST requests
def analyze():
    data = request.json  # Get JSON data from frontend
    user_input = data.get("query", "")

    if not user_input:
        return jsonify({"result": "Please enter a valid question about your career."})

    response = get_career_advice(user_input)
    return jsonify({"result": response})

def get_career_advice(user_input):
    prompt = f"You are an AI career counselor. Provide personalized career guidance for: {user_input}"

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": prompt}]
        )
        return response["choices"][0]["message"]["content"]
    except Exception as e:
        return "Sorry, I couldn't process your request right now."

if __name__ == '__main__':
    app.run(debug=True, port=5000)
