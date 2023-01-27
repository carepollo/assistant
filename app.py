from router import app
from bot import client
from dotenv import load_dotenv
import os

env_path = os.path.dirname(__file__) + "/.env"
load_dotenv(env_path)

if __name__ == "__main__":
    token = os.getenv("TOKEN")

    client.run(token)
    app.run()
