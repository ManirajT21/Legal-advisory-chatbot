from flask import Flask, request, jsonify
from .chatbot import get_legal_response

app = Flask(__name__)

@app.route("/", methods=["GET"])
def root():
    return jsonify({"message": "Welcome to the Legal Advisory Chatbot API!"})

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    if not data or "query" not in data:
        return jsonify({"error": "Missing 'query' in request body"}), 400

    user_query = data["query"]
    response = get_legal_response(user_query)
    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(debug=True)