import time
import asyncio


def community_report(guild):
    online = 0
    idle = 0
    offline = 0
    for m in guild.members:
        if str(m.status) == "online":
            online += 1
        elif str(m.status) == "offline":
            offline += 1
        else:
            idle += 1

    return online, idle, offline


async def user_metrics_background_task(client):
    await client.wait_until_ready()
    global my_guild
    my_guild = client.get_guild(826778526299979836)

    while not client.is_closed():
        try:
            online, idle, offline = community_report(my_guild)
            with open("usermetrics.csv", "a") as f:
                f.write(f"{int(time.time())},{online},{idle},{offline}\n")
            await asyncio.sleep(5)
        except Exception as e:
            print(str(e))
            await asyncio.sleep(5)