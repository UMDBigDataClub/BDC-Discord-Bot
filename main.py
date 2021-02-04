# -*- coding: utf-8 -*-
import discord
import os
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    scoreboard = pd.read_csv("scoreboard.csv", index_col = "Unnamed: 0")
    
    if message.author.name not in scoreboard.Member.values:
        scoreboard = scoreboard.append(pd.DataFrame({"Member" : [message.author.name], "Score" : [0]}), ignore_index = True, sort = True)
        scoreboard.to_csv("scoreboard.csv")
        
    if message.content.startswith('/add'):
        name = " ".join(message.content.split(" ")[2:])
        value = int(message.content.split(" ")[1])
        scoreboard.at[scoreboard[scoreboard.Member == name].index[0], "Score"] += value
        scoreboard.to_csv("scoreboard.csv")
    
    
    if message.content.startswith('/scoreboard'):
        await message.channel.send(scoreboard)

client.run(os.getenv('TOKEN'))

