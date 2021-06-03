import discord
import os
from active import active
from functions import confess

intents = discord.Intents.all()
client = discord.Client(intents=intents)

#Initiate values
serverName = "Gamers Rise Up"
channelName = "confessions"
gameName = "with your feelings"

@client.event
async def on_ready():
  print('Login successful as {0.user}'.format(client))
  await client.change_presence(activity=discord.Game(gameName))
  
@client.event
async def on_message(message):
    if isinstance(message.channel, discord.channel.DMChannel) and message.author != client.user:
        await confess(message,client,serverName, channelName)

active()
client.run(os.environ['BOT_TOKEN'])
