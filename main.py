import discord
import os
from active import active
from functions import confess, message_delete

intents = discord.Intents.all()
client = discord.Client(intents=intents)

#Initiate values
serverName = ""
channelName = ""
gameName = ""
adminNames = []
cache = []

@client.event
async def on_ready():
  print('Login successful as {0.user}'.format(client))
  await client.change_presence(activity=discord.Game(gameName))
  
@client.event
async def on_message(message):
  if isinstance(message.channel, discord.channel.DMChannel) and message.author != client.user:
      if message.content.startswith("delete") and message.author.name + "#" + message.author.discriminator in adminNames:
        await message_delete(message,cache)
      else:
        await confess(message,client,serverName, channelName,cache)

active()
client.run(os.environ['BOT_TOKEN'])
