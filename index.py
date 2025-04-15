from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "Hello from Magpie Felt! This is a test page."

@app.route('/<path:path>')
def catch_all(path):
    return f"You requested: {path}"
