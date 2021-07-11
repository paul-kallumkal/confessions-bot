import os
import asyncio
import discord
from datetime import datetime
import random
import pytz
from hashlib import sha256

async def confess(message, client, guild_name, channel_name,cache):
    for guild in message.author.mutual_guilds:
        if guild.name == guild_name:
            for c in guild.channels:
                if c.name == channel_name:
                    if True:
                        parsed = mparse(message.content, guild)
                        if "" != parsed and "@" == parsed[0]:
                            await message.add_reaction("❌")
                            return await message.author.send(
                                "Can't find user: " + parsed[1:])
                        if "" != parsed:
                            embed = embed_text(parsed,message.author)
                            confession = await c.send(embed=embed)
                            if len(cache) > 1000:
                              cache.pop(0)
                            cache.append(confession)
                        for a in message.attachments:
                            confession = await c.send(a)
                            if len(cache) > 1000:
                              cache.pop(0)
                            cache.append(confession)
                        await message.add_reaction("✅")
                        return await react_add_wait(confession, message,
                                                    client)
                    else:
                        await message.add_reaction("❌")
                        return await message.author.send("Something went wrong")
            await message.add_reaction("❌")
            return await message.author.send("Something went wrong")
    await message.add_reaction("❌")
    return await message.author.send("You're not part of " + guild_name)


def mparse(message, guild):
    output = ""
    sp = message.split()
    for word in sp:
        if word[0] == '@':
            word = word.replace(':', ' ')
            mem = guild.get_member_named(word[1:])
            if mem == None:
                return word
            word = '<@' + str(mem.id) + '>'
        elif word[0] == ':' and word[-1] == ':':
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
                    word = word = '<#' + str(c.id) + '>'
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
  if len(cache) > 0:
    await cache[-1].delete()
    cache.pop()
    await message.add_reaction("🗑️")
  else:
    await message.add_reaction("❌")
  return

random.seed(datetime.now())
DATE = str(datetime.now(pytz.timezone('Asia/Kolkata'))).split()[0]
SHIFT = str(random.random())

def embed_text(parsed, user):
  global DATE
  global SHIFT
  if DATE != str(datetime.now(pytz.timezone('Asia/Kolkata'))).split()[0]:
    DATE = str(datetime.now(pytz.timezone('Asia/Kolkata'))).split()[0]
    SHIFT = str(random.random())
  encrypted = sha256((str(user) + os.environ['ENCRYPTION_KEY'] + SHIFT).encode()).hexdigest()
  color = int(encrypted[int(encrypted[1],16):int(encrypted[1],16)+6],16)
  return discord.Embed(description=parsed, color=color)

def embed_file(file, user):
  return