import discord
import os
import praw
from keep_alive import keep_alive 

from utils.guildReport import *
from utils.meme import *

intents = discord.Intents.all()
client = discord.Client(intents=intents)

reddit = praw.Reddit(client_id=os.getenv('REDDITCLIENTID'),
                     client_secret=os.getenv('REDDITSECRET'),
                     password=os.getenv('REDDITPASSWORD'),
                     user_agent='Wazza',
                     username=os.getenv('REDDITUSER'),
                     check_for_async=False)


@client.event
async def on_ready():
    global my_guild
    my_guild = client.get_guild(826778526299979836)
    print('We have logges in as {0.user}'.format(client))


@client.event
async def on_message(message):
    global my_guild
    if message.author == client.user:
        return

    if message.content.startswith('w.hottestmeme'):
        await hotmeme(message, reddit, 1)

    if message.content.startswith('w.hotmeme'):
        string = message.content.lower()
        words = string.split()
        if words[-1] == 'w.hotmeme':
          await hotmeme(message, reddit, 10)
        if words[-1].isdigit():
          await hotmeme(message, reddit, int(words[-1]))
        else:
          await message.channel.send("String after w.hotmeme is not allowed. \nWrite `number of Memes` after w.hotmeme")

    if "w.creport" == message.content.lower():
        online, idle, dnd, offline, other = community_report(my_guild)
        await message.channel.send(
            f"```py\nOnline: {online}\nIdle: {idle}\nDnD: {dnd}\nOffline: {offline}\nOther: {other}```"
        )
        plot_community_report()
        file = discord.File("online.png", filename="online.png")
        await message.channel.send("Total Users V Online Users", file=file)


client.loop.create_task(automeme(client, reddit))
client.loop.create_task(user_metrics_background_task(client))
keep_alive()
client.run(os.getenv('TOKEN'))
