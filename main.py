from server import socketio, app
from bot import bot
from dotenv import load_dotenv
import os
import asyncio

env_path = os.path.dirname(__file__) + "/.env"
load_dotenv(env_path)

async def start_server():
    socketio.run(app)

async def start_bot():
    token = os.getenv("BOT_TOKEN")
    await bot.start(token)

async def main():
    task1 = asyncio.create_task(start_bot())
    task2 = asyncio.create_task(start_server())

    await task1
    await task2
if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Program exited")
