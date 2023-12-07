from flask import Flask, request

app = Flask(__name__)

with open("templates/login.html", "r", encoding="utf-8") as f:
    login = f.read()

@app.route('/')
def index():
    document = login.replace("{tag}", "Hello!")

    return document

@app.route('/favicon.ico')
def favicon():
    return ''
