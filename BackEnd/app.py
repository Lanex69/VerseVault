from flask import Flask, request, jsonify
from flask_cors import CORS  # Import CORS
import json

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Load the merged Quran data
try:
    with open("quran.json", "r", encoding="utf-8") as f:
        quran = json.load(f)
except FileNotFoundError:
    print("Error: quran.json not found.")
    quran = []
except json.JSONDecodeError:
    print("Error: quran.json is not a valid JSON file.")
    quran = []

@app.route("/search")
def search():
    keyword = request.args.get("keyword", "").lower()
    if not quran:
        return jsonify({"error": "Quran data not available."}), 500
    results = [
        verse for verse in quran
        if keyword in verse["english"].lower() or keyword in verse["arabic"].lower()
    ]
    return jsonify(results)

if __name__ == "__main__":
    app.run(debug=True)