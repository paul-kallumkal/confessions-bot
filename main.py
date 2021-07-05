import discord
import os
from active import active
from functions import confess, message_delete

intents = discord.Intents.all()
client = discord.Client(intents=intents)
cache = []

#Initiate values
serverName = "Gamers Rise Up"
channelName = "confessions"
gameName = "with your identity"
adminNames = ["Shadows#5555"]


@client.event
async def on_ready():
  print('Login successful as {0.user}'.format(client))
  await client.change_presence(activity=discord.Game(gameName))
  
@client.event
async def on_message(message):
  if isinstance(message.channel, discord.channel.DMChannel) and message.author != client.user:
      if message.content.startswith("!delete") and str(message.author) in adminNames:
        await message_delete(message,cache)
      else:
        await confess(message,client,serverName,channelName,cache)

active()
client.run(os.environ['BOT_TOKEN'])
