from flask import Flask, jsonify
from vision.analyzer import analisar

app = Flask(__name__)

@app.route("/")
def home():
    return {"status": "API ONLINE"}

@app.route("/signal")
def signal():
    return jsonify(analisar())

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
