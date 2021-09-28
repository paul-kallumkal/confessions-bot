import os
import asyncio
import discord
from datetime import datetime
import random
import pytz
from hashlib import sha256

random.seed(str(datetime.now()) + os.environ['ENCRYPTION_KEY'])
DATE = str(datetime.now(pytz.timezone('Asia/Kolkata'))).split()[0]
SHIFT = str(random.random())
CACHE_SIZE = 1000

async def confess(message, client, guild_name, channel_name, cache):
  for guild in message.author.mutual_guilds:
    if guild.name == guild_name:
      for c in guild.channels:
        if c.name == channel_name:
          try:
            parsed = mparse(message.content, guild)
            if "" != parsed and "@" == parsed[0]:
              await message.add_reaction("❌")
              return await message.author.send(
                  "Can't find user: " + parsed[1:] + '\n(Case sensitive and use : for spaces)')
            if "" != parsed:
              embed = embed_text(parsed,message.author)
              confession = await c.send(embed=embed)
              message_add(confession,cache)
            for a in message.attachments:
              embed = embed_image(a,message.author)
              if embed != None:
                confession = await c.send(embed=embed)
              else:
                embed = embed_text("Attachment",message.author)
                confession = await c.send(embed=embed)
                message_add(confession,cache)
                confession = await c.send(a)
              message_add(confession,cache)
            await message.add_reaction("✅")
            return await react_add_wait(confession, message, client)
          except:
            await message.add_reaction("❌")
            return await message.author.send("Something went wrong")
      await message.add_reaction("❌")
      return await message.author.send("Channel " + channel_name + " not found")
  await message.add_reaction("❌")
  return await message.author.send("You're not part of " + guild_name)

def mparse(message, guild):
  output = ""
  sp = message.split(' ')
  for word in sp:
    if len(word) == 0:
      continue
    if word[0] == '@':
      word = word.replace(':', ' ')
      mem = guild.get_member_named(word[1:])
      if mem == None:
        return word
      word = '<@' + str(mem.id) + '>'
    elif word[0] == ':' and word[-1] == ':' and len(word) != 1:
      emo = word.strip(':')
      for e in guild.emojis:
        if e.name == emo:
          if e.is_usable():
            word = e
            break
          else:
            return ""
    elif word[0] == '#':
      for c in guild.channels:
        if c.name == word[1:]:
          word = '<#' + str(c.id) + '>'
          break
    output = output + str(word) + ' '
  return output

async def react_add_wait(confession, message, client):
  def react_check(reaction, user):
    return reaction.message == message and user == message.author
  try:
    reaction, user = await client.wait_for('reaction_add', timeout=60.0,check=react_check)
    await confession.add_reaction(reaction)
    return await react_add_wait(confession, message, client)
  except asyncio.TimeoutError:
    return

async def message_delete(message, cache):
  if len(cache) == 0:
    await message.add_reaction("❌")
  else:
    count = 1
    if(len(message.content.split()) > 1):
      count = min(int(message.content.split()[1]),len(cache))
    for i in range(count):
      await cache[-1].delete()
      cache.pop()
    await message.add_reaction("🗑️")

def message_add(confession, cache):
  if len(cache) > CACHE_SIZE:
    cache.pop(0)
  cache.append(confession)

def embed_text(parsed, user):
  color = color_find(user)
  return discord.Embed(description=parsed, color=color)

def embed_image(file, user):
  embed = None
  if file.content_type.startswith('image'):
    color = color_find(user)
    embed = discord.Embed(color=color)
    embed.set_image(url=file)
  return embed

def color_find(user):
  global DATE
  global SHIFT
  if DATE != str(datetime.now(pytz.timezone('Asia/Kolkata'))).split()[0]:
    DATE = str(datetime.now(pytz.timezone('Asia/Kolkata'))).split()[0]
    SHIFT = str(random.random())
  encrypted = sha256((str(user) + os.environ['ENCRYPTION_KEY'] + SHIFT).encode()).hexdigest()
  return int(encrypted[int(encrypted[1],16):int(encrypted[1],16)+6],16)

async def change_channel(message, channelName):
  if len(message.content.split(' ')) == 2:
    await message.add_reaction("✅")
    return message.content.split(' ')[1]
  await message.add_reaction("❌")
  return channelName

async def send_help(message, adminNames):
  description = "Send any message/attachment and it'll be sent anonymously to a specific channel\nTag people using @username (case sensitive)\nMention channels using #channelname (case sensitive)\nYou can add reactions up to 60 seconds after posting a confession"
  color = int("2cbdf2",16)
  embed = discord.Embed(description=description, color=color)
  await message.channel.send(embed=embed)
  if str(message.author) in adminNames:
    description = "Admin commands:\n!delete to delete the most recent confession\n!delete n to delete the last n messages\n!channel channel_name to change the name of the channel for confessions"
    embed = discord.Embed(description=description, color=color)
    await message.channel.send(embed=embed)