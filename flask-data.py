import flask
from flask import Flask, jsonify, render_template
import json
import os 

app = Flask(__name__)

@app.route("/")
def home():
    return "Welcome to extracted data API !"

@app.route("/<event_id>")
def data(event_id):
    try:
        filename = os.path.join(f"{event_id}.json")
        with open(filename, "r") as file:
            return jsonify(json.load(file))
    except FileNotFoundError:
        return jsonify({"Error": "match not found"})


if __name__ == "__main__":
    app.run(debug=True)



