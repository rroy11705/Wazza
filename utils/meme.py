import discord
import asyncio
import random

async def hotmeme(message, reddit, n):
    if n > 20:
      await message.channel.send("Look at u, how addicted u are to memes. I can send 20 memes at most at a time!")
    count = 0
    for submission in reddit.subreddit("meme").hot(limit=100):
        if ('.jpg' in submission.url) and count < n:
            embed = discord.Embed(
                title=submission.title,
                description=submission.selftext,
                colour=0xff69b4,
            )
            embed.set_image(url=submission.url)
            embed.set_footer(text=f"Posted by By: {submission.author}")
            count += 1
            await message.channel.send(embed=embed)
        elif count > n:
            return
    return


async def automeme(client, reddit):
    await client.wait_until_ready()
    global my_guild
    my_guild = client.get_guild(829778974359814195)
    meme_channel = client.get_channel(826804773848219738) #meme chanel
    no_filter_channel = client.get_channel(826804841808265266) #no filter chanel
    subr_list = ["meme", "pesmobile", "dankmeme", "darkmeme", "animememes", "soccercirclejerk", "goodanimeme", "ShittyLifeProTips", "technicallythetruth", "cursedcomments", "wholesomememes", "wholesomeanimemes", "cosplaygirls"]
    while not client.is_closed():
        try:
            temp = random.choice(subr_list)
            subr = reddit.subreddit(temp)
            meme = subr.random()
            if ('.jpg' in meme.url):
              embed = discord.Embed(
                  title=meme.title,
                  description=meme.selftext,
                  colour=0xfcba03,
              )
              embed.set_image(url=meme.url)
              embed.set_footer(text=f"Posted by by {meme.author} in r/{temp}")
              if (meme.over_18):
                await no_filter_channel.send(embed=embed)
                await asyncio.sleep(60)
              else:
                await meme_channel.send(embed=embed)
                await asyncio.sleep(5*60)
            else:
              pass
        except Exception as e:
            print(str(e))
            await asyncio.sleep(5*60)
