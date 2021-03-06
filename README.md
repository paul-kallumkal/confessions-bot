# Confession-bot  
I started this project to improve a confessions channel in my discord server. It previously relied on a bot with a message limit for the free tier   
&nbsp;  

## Commands
!help - Get help on how to use the bot  
!delete  - Admins can delete the most recent message  
!delete n - Deletes the last n messages sent  
!channel - changes the channel the bot sends messages to  

## Features  
No formatting! Directly type the message you want to send  
Supports tagging members within the server  
Emojis can be used (including server emojis)  
Reactions supported within 100 seconds of the message (timer resets on each reaction)  
Videos, Images and GIFs are supported too  
Channel tagging has now been added  
Admin users can delete multiple confessions at once  
Confessions cached with anonymity maintained  
Embedded messages with daily changing colours associated to users

&nbsp;  

## Services  
This bot can be hosted on a variety of free platforms like [replit.com](https://replit.com)  
To keep it active 24/7, the bot relies on http requests from [uptimerobot.com](https://uptimerobot.com/)  
&nbsp;  
  
## Setup main.py  
Initiate server specific values:  
serverName  
channelName  
adminNames (optional list of strings)  
gameName (optional)  

The term os.environ['BOT_TOKEN'] should correspond to a secret bot token provided to you by [Discord](https://discord.com/developers/applications)  

Invite the bot to your server and it's ready for anonymous messaging
