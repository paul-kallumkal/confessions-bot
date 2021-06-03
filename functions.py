import asyncio

async def confess(message,client,guild_name,channel_name):
  for guild in message.author.mutual_guilds:
    if guild.name == guild_name:
      for c in guild.channels:
        if c.name == channel_name:  
          parsed = mparse(message.content,guild)
          if ""!=parsed and "@"==parsed[0]:
            await message.add_reaction("❌")
            return await message.author.send("Can't find user: " + parsed[1:])  
          if ""!=parsed:
            confession = await c.send(parsed) 
          for a in message.attachments:
            confession = await c.send(a)
          await message.add_reaction("✅")
          return await react_add_wait(confession,message,client)
      await message.add_reaction("❌")
      return await message.author.send("Something went wrong")
  await message.add_reaction("❌")
  return await message.author.send("You're not part of " + guild_name)

def mparse(message,guild):
  output=""
  sp = message.split()
  for word in sp:
    if word[0]=='@':
      word = word.replace(':',' ')
      mem = guild.get_member_named(word[1:])
      if mem == None:
        return word
      word = '<@' + str(mem.id) + '>'
    elif word[0]==':' and word[-1]==':':
      emo = word.strip(':')
      for e in guild.emojis:
        if e.name == emo:
          if e.is_usable():
            word = e;
            break;
          else:
            return ""
    elif word[0]=='#':
      for c in guild.channels:
        if c.name == word[1:]:
          word = word = '<#' + str(c.id) + '>';
          break;
    output = output + str(word) + ' '
  return output

async def react_add_wait(confession,message,client):
  def react_check(reaction, user):
    return reaction.message == message and user == message.author
  try: 
    reaction, user = await client.wait_for('reaction_add', timeout=100.0, check=react_check)
    await confession.add_reaction(reaction)
    return await react_add_wait(confession,message,client)
  except asyncio.TimeoutError:
    return