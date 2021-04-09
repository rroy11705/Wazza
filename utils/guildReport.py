import time
import asyncio
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import style
style.use("fivethirtyeight")

def plot_community_report():
  df = pd.read_csv("usermetrics.csv", names=['time', 'online', 'idle', 'dnd', 'other', 'offline'])
  df['date'] = pd.to_datetime(df['time'],unit='s')
  df['total'] = df['online'] + df['offline'] + df['idle'] + df['dnd'] + df['other']
  df.drop("time", 1,  inplace=True)
  df.set_index("date", inplace=True)

  print(df.head())
  plt.clf()
  df['total'].plot()
  df['online'].plot()
  plt.legend()
  plt.savefig("online.png")

def community_report(guild):
    online = 0
    idle = 0
    dnd = 0
    offline = 0
    other = 0
    for m in guild.members:
        if str(m.status) == "online":
            online += 1
        elif str(m.status) == "offline":
            offline += 1
        elif str(m.status) == "idle":
            idle += 1
        elif str(m.status) == "dnd":
            dnd += 1
        else:
            other += 1

    return online, idle, dnd, offline, other


async def user_metrics_background_task(client):
    await client.wait_until_ready()
    global my_guild
    my_guild = client.get_guild(826778526299979836)

    while not client.is_closed():
        try:
            online, idle, dnd, offline, other = community_report(my_guild)
            with open("usermetrics.csv", "a") as f:
                f.write(f"{int(time.time())},{online},{idle},{dnd},{other},{offline}\n")
                
            await asyncio.sleep(5)
        except Exception as e:
            print(str(e))
            await asyncio.sleep(5)