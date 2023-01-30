from router import socketio, app
from bot import client
from dotenv import load_dotenv
import os
import multiprocessing

env_path = os.path.dirname(__file__) + "/.env"
load_dotenv(env_path)

def start_server():
    socketio.run(app)
    # app.run()

def start_bot():
    token = os.getenv("TOKEN")
    client.run(token)

if __name__ == "__main__":
    queue = multiprocessing.Queue()
    bot_thread = multiprocessing.Process(name="p1", target=start_bot)
    server_thread = multiprocessing.Process(name="p2", target=start_server)

    bot_thread.start()
    server_thread.start()
    # queue.close()
