# Confession-bot  
I started this project to improve a confessions channel in my discord server. It previously relied on a bot with a message limit for the free tier   
&nbsp;  

## Features  
No formatting! Directly type the message you want to send  
Supports tagging members within the server  
Emojis can be used (including server emojis)  
Reactions supported within 100 seconds of the message (timer resets on each reaction)  
Files, Images and GIFS are supported too  
Channel tagging has now been added  
&nbsp;  

## Services  
This bot can be hosted on a variety of free platforms like [replit.com](https://replit.com)  
To keep it active 24/7, the bot relies on http requests from [uptimerobot.com](https://uptimerobot.com/)  
&nbsp;  
  
## Setup main.py  
Provide values to serverName and channelName corresponding to the name of the server and channel the bot is intended for  

(Optional)  
Provide a value to gameName and uncomment line 17 to have a custom bot status 

The term os.environ['BOT_TOKEN'] should correspond to a secret bot token provided to you by [Discord](https://discord.com/developers/applications)  

Invite the bot to your server and it's ready for anonymous messaging
