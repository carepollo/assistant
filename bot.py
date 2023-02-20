import discord
from discord.ext import commands
from os import getenv
from shared import shared_queue
from threading import Lock, Thread
from asyncio import run, run_coroutine_threadsafe

notifications_lock = Lock()

# bot creation and configuration
intents = discord.Intents.all()
intents.message_content = True
client = commands.Bot(command_prefix="!", intents=intents)

async def send_dm(userid: int, message: str):
    user = await client.fetch_user(userid)
    channel = await user.create_dm()
    await channel.send(message)

def check_for_notifications():
    while True:
        if not len(shared_queue) == 0:
            with notifications_lock:
                notification = shared_queue.pop()
                run_coroutine_threadsafe(send_dm(notification["userid"], notification["message"]), client.loop)

def autmatic_bootload():
    run(check_for_notifications())

@client.event
async def on_ready():
    print(f"Logged in as {client.user}")
    
    # changing general information
    activity = discord.Game("Analysing...")
    status = discord.Status.do_not_disturb
    await client.change_presence(activity=activity, status=status)

    Thread(target=autmatic_bootload).start()

@client.tree.command(name="sync", description="sycronize commands with discord")
async def sync(interaction: discord.Interaction):
    ownerid = getenv("USER_ID")
    message = ""

    if interaction.user.id == int(ownerid):
        try:
            await client.tree.sync()
            message = "Syncronization succesful"
        except Exception as e:
            message = f"Error syncronising: {e}"
    else:
        message = "You are not owner of the bot"

    await interaction.response.send_message(message)

@client.tree.command(name="test", description="a ping command")
async def test(interaction: discord.Interaction):
    await interaction.response.send_message("All systems online 👁")

@client.tree.command(name="myid", description="what is my discord unique id")
async def myid(interacion: discord.Interaction):
    message = f"your Discord user is ||{interacion.user.id}||"
    await interacion.response.send_message(message, ephemeral=True)
