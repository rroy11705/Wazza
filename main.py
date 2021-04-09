import discord
import os
import praw

from utils.guildReport import user_metrics_background_task, community_report

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

    if message.content.startswith('w.meme'):
        for submission in reddit.subreddit("soccercirclejerk").new(limit=5):
            embed = discord.Embed(
                title=submission.title,
                description=submission.selftext,
                colour=0xff69b4,
            )
            embed.set_image(url=submission.url)
            embed.set_footer(text=f"Posted by By: {submission.author}")

            await message.channel.send(embed=embed)

    if "w.creport" == message.content.lower():
        online, idle, offline = community_report(my_guild)
        await message.channel.send(f"```Online: {online}.\nIdle/busy/dnd: {idle}.\nOffline: {offline}```")

client.loop.create_task(user_metrics_background_task(client))
client.run(os.getenv('TOKEN'))
