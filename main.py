# -*- coding: utf-8 -*-
import discord
import os
import boto3
import pandas as pd
from dotenv import load_dotenv
from discord.utils import get

load_dotenv()

s3 = boto3.resource(
        service_name='s3',
        region_name='us-east-2',
        aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
    )
obj = s3.Bucket('bdc-scoreboard').Object("scoreboard.csv").get()
scoreboard = pd.read_csv(obj["Body"], index_col = 0)
scoreboard.to_csv("scoreboard.csv")

client = discord.Client()


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
  
@client.event
async def on_disconnect():
    global S3
    s3.Bucket('bdc-scoreboard').upload_file(Filename='scoreboard.csv', Key='scoreboard.csv')

@client.event
async def on_message(message):
    global scoreboard
    
    if message.author == client.user:
        return

    if message.author.name=="GitHub":
        await message.channel.send(str(message.embeds[0].to_dict()))
    
    # Adds member to scoreboard.csv if they are already not add on
    if message.author.name not in scoreboard.Member.values:
        scoreboard = scoreboard.append(pd.DataFrame({"Member" : [message.author.name], "Score" : [0]}), ignore_index = True, sort = True)
        scoreboard.to_csv("scoreboard.csv")
    
    # Adds and subtracts values to a person's score
    if message.content.startswith('/add'):
        name = " ".join(message.content.split(" ")[2:])
        value = int(message.content.split(" ")[1])
        scoreboard.at[scoreboard[scoreboard.Member == name].index[0], "Score"] += value
        scoreboard.to_csv("scoreboard.csv")

    
    # Prints the score of everyone in the scoreboard.csv file

    if message.content.startswith('/scoreboard'):
        scoreboard = scoreboard.sort_values("Score", axis = 0, ascending = False).reset_index(drop = True)
        await message.channel.send(scoreboard)
        

    # Prints the score of the individual    
    if message.content.startswith('/score '):
        scoreboard = scoreboard.sort_values("Score", axis = 0, ascending = False).reset_index(drop = True)
        name = " ".join(message.content.split(" ")[1:])
        personalScore = scoreboard[scoreboard.Member == name]
        await message.channel.send(personalScore)

    if message.content.startswith('/awards'):
        content = \
        """
        Here is the list of awards available at the end of season:
        Consulting Award - to any member that completes a BDC-sponsored consulting project - 100 points
        Recruiting Award - to any member that recruits a new active member to the club - 100 points
        Presentation Award - to any member that gives a presentation - 50 points
        """
        await message.channel.send(content)


#reaction roles, assigns roles based on emoji used for the reaction of a specific message

@client.event
async def on_reaction_add(reaction, user):
    message_id = 'React with an emoji to be assigned a role, choose all that apply.'
    message = reaction.message.content
    channel = reaction.message.channel
    Guild = reaction.message.guild
    role_member = 809832119294492692 
    #replace this role id with the role id from BDC discord server, I used this other role on my testing server
    # add more roles by copying the role id in discord, for example you could add a data sceince role and copy the id into data_science.
    member_role = get(Guild.roles, id = role_member)
    #each role will need an emoji to go along with it.
    if message_id == message and reaction.emoji == '👍':
        #channel = reaction.message.channel
        await user.add_roles(member_role)
        


client.run(os.getenv('TOKEN'))

