import discord
import os

client = discord.Client()

g = 1

@client.event
async def on_ready():
    print("bot is ready !")

client.run(os.environ['TOKEN'])