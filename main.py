# -*- coding: utf-8 -*-
import discord
import os
import boto3
import pandas as pd
import json
from discord.utils import get
from scoreboard import Scoreboard



sb = Scoreboard()

client = discord.Client()



@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    

@client.event
async def on_message(message):
    global sb
    
    if message.author == client.user:
        return

    if message.author.name=="GitHub":
        await message.channel.send(str(message.embeds[0].to_dict()))
    
    # Adds member to scoreboard.csv if they are already not added on message
    if message.author.name not in sb.df.Member.values:
        sb.create_user(name = message.author.name)


    #Administrator-only commands
    if 'Administrator' in [role.name for role in message.author.roles]:

        # Adds and subtracts values to a person's score
        if message.content.startswith('/add'):
            name = " ".join(message.content.split(" ")[2:])
            value = int(message.content.split(" ")[1])
            sb.add(name, value)


    #Commands for administrator or the user themselves
    if 'Administrator' in [role.name for role in message.author.roles] or message.author.name == " ".join(message.content.split(" ")[2:]):
        # Update individual information
        if message.content.startswith('/set_github '):
            github = message.content.split(" ")[1]
            name = " ".join(message.content.split(" ")[2:])
            sb.update(name=name, github=github)

        if message.content.startswith('/set_email '):
            email = message.content.split(" ")[1]
            name = " ".join(message.content.split(" ")[2:])
            sb.update(name=name, email=email)

        if message.content.startswith('/set_participating '):
            participating = bool(message.content.split(" ")[1])
            name = " ".join(message.content.split(" ")[2:])
            sb.update(name=name, participating=participating)

    
    # Prints the score of everyone in the scoreboard.csv file
    if message.content == '/scoreboard':
        await message.channel.send(sb.display())

    elif message.content == '/scoreboard_everyone':
        await message.channel.send(sb.display(non_participating = True))

    elif message.content == '/scoreboard_all_time':
        await message.channel.send(sb.display(all_time = True, non_participating = True))
        

    # Prints the score of an individual
    elif message.content.startswith('/score_all_time '):
        name = " ".join(message.content.split(" ")[1:])
        await message.channel.send(sb.display(name = name, all_time = True))

    elif message.content.startswith('/score '):
        name = " ".join(message.content.split(" ")[1:])
        await message.channel.send(sb.display(name = name))




    #Print manual awards
    elif message.content.startswith('/awards'):
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

