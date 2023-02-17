from server import socketio, app
from bot import client
from dotenv import load_dotenv
import os
import multiprocessing
from gevent.pywsgi import WSGIServer

env_path = os.path.dirname(__file__) + "/.env"
load_dotenv(env_path)

def start_server():
    http_server = WSGIServer(("127.0.0.1", 5000), socketio)
    http_server.serve_forever()
    socketio.run(app)

def start_bot():
    token = os.getenv("TOKEN")
    client.run(token)

def start_multiprocess():
    queue = multiprocessing.Queue()
    bot_thread = multiprocessing.Process(name="bot_thread", target=start_bot)
    server_thread = multiprocessing.Process(name="server_thread", target=start_server)

    bot_thread.start()
    server_thread.start()
    queue.close()

def run():
    # start_multiprocess()
    # start_server()
    start_bot()

if __name__ == "__main__":
    run()
