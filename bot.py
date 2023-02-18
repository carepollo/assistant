import discord
from discord.ext import commands
import os

# bot creation and configuration
intents = discord.Intents.all()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')
    
    # changing general information
    activity = discord.Game("Analysing...")
    status = discord.Status.do_not_disturb
    await bot.change_presence(activity=activity, status=status)

    # automatic messages
    userid = int(os.getenv("USER_ID"))
    await send_dm(userid, "Automatic messages enabled")

@bot.command()
async def sync(ctx):
    await bot.tree.sync()
    await ctx.send("Syncronization succesful")

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
