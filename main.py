import discord
import os
from active import active
from functions import confess, message_delete, change_channel, send_help

intents = discord.Intents.all()
client = discord.Client(intents=intents)
cache = []

#Initiate values
serverName = "Gamers Rise Up"
channelName = "confessions"
adminNames = ["Shadows#2426"]
gameName = "with your identity"

@client.event
async def on_ready():
  print('Login successful as {0.user}'.format(client))
  await client.change_presence(activity=discord.Game(gameName))
  
@client.event
async def on_message(message):
  if isinstance(message.channel, discord.channel.DMChannel) and message.author != client.user:
    if message.content.startswith("!delete") and str(message.author) in adminNames:
      await message_delete(message,cache)
    elif message.content.startswith("!channel") and str(message.author) in adminNames:
      global channelName
      channelName = await change_channel(message,channelName)
    elif message.content.startswith("!help"):
      await send_help(message,adminNames)
    else:
      await confess(message,client,serverName,channelName,cache)
  elif message.content.startswith("!help") and message.author != client.user:
      await send_help(message,[])

active()
client.run(os.environ['BOT_TOKEN'])
