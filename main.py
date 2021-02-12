# -*- coding: utf-8 -*-
import discord
import os
import boto3
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

client = discord.Client()
s3 = boto3.resource(
    service_name='s3',
    region_name='us-east-2',
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
)

obj = s3.Bucket('bdc-scoreboard').Object("scoreboard.csv").get()
scoreboard = pd.read_csv(obj["Body"], index_col = 0)
scoreboard.to_csv("scoreboard.csv")

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    scoreboard = pd.read_csv("scoreboard.csv", index_col = "Unnamed: 0")
    
    if message.author.name=="GitHub":
        await message.channel.send(str(message.embeds[0].to_dict()))
    
    if message.author.name not in scoreboard.Member.values:
        scoreboard = scoreboard.append(pd.DataFrame({"Member" : [message.author.name], "Score" : [0]}), ignore_index = True, sort = True)
        scoreboard.to_csv("scoreboard.csv")
        s3.Bucket('bdc-scoreboard').upload_file(Filename='scoreboard.csv', Key='scoreboard.csv')
        
    if message.content.startswith('/add'):
        name = " ".join(message.content.split(" ")[2:])
        value = int(message.content.split(" ")[1])
        scoreboard.at[scoreboard[scoreboard.Member == name].index[0], "Score"] += value
        scoreboard.to_csv("scoreboard.csv")
        s3.Bucket('bdc-scoreboard').upload_file(Filename='scoreboard.csv', Key='scoreboard.csv')
    
    
    if message.content.startswith('/scoreboard'):
        scoreboard = scoreboard.sort_values("Score", axis = 0, ascending = False).reset_index(drop = True)
        await message.channel.send(scoreboard)
        
    if message.content.startswith('/awards'):
        content = \
        """
        Here is the list of awards available at the end of season:
        Consulting Award - to any member that completes a BDC-sponsored consulting project - 100 points
        Recruiting Award - to any member that recruits a new active member to the club - 100 points
        Presentation Award - to any member that gives a presentation - 50 points
        """
        await message.channel.send(content)

client.run(os.getenv('TOKEN'))

