from flask import Flask, request
from flask_socketio import SocketIO, send, emit
from flask_cors import CORS
from terminal import Terminal
from threading import Lock
from bot import send_dm
import os

app = Flask(__name__)
CORS(app)
app.config["SECRET_KEY"] = "secret"
socketio = SocketIO(app, cors_allowed_origins="*")

# setting a path to root of all projects
root_path = os.getenv("ROOT_PATH")

# keep track of executing programs and block conflicting modifications
programs_running = {}
programs_locked = Lock()


@app.route("/ping")
def ping():
    return "Hello world!"

@app.route("/submit", methods=["POST"])
async def submit():
    data = request.json
    userid = int(os.getenv("USER_ID"))
    message = f"```Title: {data['title']}\nMessage: {data['message']}```"
    await send_dm(userid, message)
    return data

@app.route("/notify", methods=["POST"])
def notify():
    message = "**someone** have just visited your portfolio"
    return {"message": message}

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
            send("INTERNAL SERVER ERROR: Requested program is not defined")

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
        send(message)
