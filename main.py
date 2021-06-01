import discord
import os
from active import active
from functions import confess

intents = discord.Intents.all()
client = discord.Client(intents=intents)

gameName = ""
server_name = ""
channel_name = ""

@client.event
async def on_ready():
  print('Login successful as {0.user}'.format(client))
  #await client.change_presence(activity=discord.Game(gameName))
  
@client.event
async def on_message(message):
    if isinstance(message.channel, discord.channel.DMChannel) and message.author != client.user:
        await confess(message,client,server_name, channel_name)

active()
client.run(os.environ['BOT_TOKEN'])
