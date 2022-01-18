import os
from dotenv import load_dotenv
import discord
from discord.ext import commands
import Music

load_dotenv()

TOKEN = os.getenv('TOKEN')
cogs = [Music]

client = commands.Bot(command_prefix='.', intents=discord.Intents.all())
intents = discord.Intents.all()

for i in range(len(cogs)):
    cogs[i].setup(client)

client.run(TOKEN)
