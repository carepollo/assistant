from flask import Flask, request
from flask_socketio import SocketIO, emit
from flask_cors import CORS
from terminal import Terminal
from threading import Lock
from os import getenv
from shared import shared_queue

app = Flask(__name__)
CORS(app)
app.config["SECRET_KEY"] = "secret"
socketio = SocketIO(app, cors_allowed_origins="*")

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

@socketio.on("connect")
def handle_connect():
    print(f"{request.sid} has been connected")

@socketio.on('initialize')
def handle_initialize(program: str):
    with programs_locked:
        emulator = Terminal()
        commands = {
            "hangman": f"python3 {root_path}/hangman/main.py",
            "esolang": f"{root_path}/esolang/esolang"
        }
        if program in commands:
            output = emulator.start(commands[program])
            programs_running[request.sid] = emulator
            emit("initialize", output)
        else:
            emit("INTERNAL SERVER ERROR: Requested program is not defined")

@socketio.on("command")
def handle_command(command: str):
    with programs_locked:
        output = programs_running[request.sid].run_command(command)
        emit("command", output)

@socketio.on("disconnect")
def handle_disconnect():
    with programs_locked:
        programs_running[request.sid].terminate()
        del programs_running[request.sid]
        
        message = f"{request.sid} has been terminated"
        print(message)
