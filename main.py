import discord
from discord.ext import commands
import Music

cogs = [Music]

client = commands.Bot(command_prefix='?', intents=discord.Intents.all())
intents = discord.Intents.all()

for i in range(len(cogs)):
  cogs[i].setup(client)

client.run('OTMxNzQ4OTA4NDU4MTg0NzI0.YeI8yg.A2nR54gFzJwHZjbSSn5a1xc-3yY')