from os import getenv, path
from dotenv import load_dotenv

env_path = path.dirname(__file__) + "/.env"
load_dotenv(env_path)

from server import socketio, app
from bot import client
from threading import Thread

def start_server():
    socketio.run(app)

def start_bot():
    token = getenv("BOT_TOKEN")
    client.run(token)

def main():
    Thread(target=start_bot).start()
    start_server()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Program exited")
