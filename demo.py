from flask import Flask, request, jsonify, render_template
import google.generativeai as genai
import os
from dotenv import load_dotenv
from flask_cors import CORS

# Load API key from .env (recommended)
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Configure Gemini
genai.configure(api_key=GEMINI_API_KEY)

# Flask app
app = Flask(__name__)
CORS(app)  # 🚀 enable CORS for all routes

@app.route("/", methods=["GET"])
def home():
    # Serve frontend (index.html) from templates folder
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask_gemini():
    try:
        data = request.get_json()
        question = data.get("question", "")

        if not question:
            return jsonify({"error": "No question provided"}), 400

        # Call Gemini
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(question)

        return jsonify({"answer": response.text})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
