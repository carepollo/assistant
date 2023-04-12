from flask import Flask, request
from flask_cors import CORS
from threading import Lock
from os import getenv
from shared import shared_queue

app = Flask(__name__)
CORS(app)
app.config["SECRET_KEY"] = "secret"

# setting a path to root of all projects
root_path = getenv("ROOT_PATH")
userid = int(getenv("USER_ID"))

# keep track of executing programs and block conflicting modifications
programs_running = {}
programs_locked = Lock()

@app.route("/ping")
def ping():
    return "Hello world!"

@app.route("/notify", methods=["POST"])
def submit():
    data = request.json
    code_snippet = f"```Title: {data['title']}\nContact: {data['contact']}\nMessage: {data['message']}```"
    message = f"New notification:\n{code_snippet}"
    notification = {"userid": userid, "message": message}
    shared_queue.append(notification)
    return {}
