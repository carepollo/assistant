from flask import Flask
from flask_socketio import SocketIO

app = Flask(__name__)
socketio = SocketIO(app)

@app.route("/ping")
def ping():
    return "Hello world!"

@socketio.on("connect")
def test():
    ping()
