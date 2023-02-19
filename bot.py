import discord
from discord.ext import commands
import os

# bot creation and configuration
intents = discord.Intents.all()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Bot logged in as {bot.user}")
    
    # changing general information
    activity = discord.Game("Analysing...")
    status = discord.Status.do_not_disturb
    await bot.change_presence(activity=activity, status=status)

@bot.tree.command(name="sync", description="sycronize commands with discord")
async def sync(interaction: discord.Interaction):
    ownerid = os.getenv("USER_ID")
    message = ""

    if interaction.user.id == int(ownerid):
        try:
            await bot.tree.sync()
            message = "Syncronization succesful"
        except Exception as e:
            message = f"Error syncronising: {e}"
    else:
        message = "You are not owner of the bot"

    await interaction.response.send_message(message)

@bot.tree.command(name="test", description="a ping command")
async def test(interaction: discord.Interaction):
    await interaction.response.send_message("All systems online 👁")

@bot.tree.command(name="myid", description="what is my discord unique id")
async def myid(interacion: discord.Interaction):
    message = f"your Discord user is ||{interacion.user.id}||"
    await interacion.response.send_message(message, ephemeral=True)

async def send_dm(userid: int, message: str):
    user = await bot.fetch_user(userid)
    channel = await user.create_dm()
    await channel.send(message)
