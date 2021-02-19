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

prev_author = ""
cur_author = ""
prev_committer = ""



@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    

@client.event
async def on_message(message):
    global sb
    global prev_author
    global cur_author
    global prev_committer

    if message.author != "BDC-Bot" and message.author != "GitHub":
        prev_author = cur_author
        cur_author = message.author.name

    
    if message.author == client.user:
        return

    #Give members one point for each message, but only if they are not posting multiple times in a row
    if cur_author != prev_author and prev_author != "" and not message.content.startswith('/') and not message.content.startswith('\''):
        sb.add(cur_author, 1)


    #Give members 20 points for each GitHub commit, but only if they are nonconsecutive
    if message.author.name=="GitHub":
        committer = message.embeds[0].to_dict()["author"]["name"]
        #Test for previous committer
        if committer in sb.df.GitHub.values and committer != prev_committer:
            prev_committer = committer
            name = sb.df[sb.df.GitHub == committer].Member.iloc[0]
            sb.add(name, 20)
            await message.channel.send(name + " has earned 20 points for committing to GitHub!")
    else:
        prev_committer = ""

    # Adds member to scoreboard.csv if they are already not added on message
    if message.author.name not in sb.df.Member.values:
        sb.create_user(name = message.author.name)


    #Administrator-only commands
    try:
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

    except AttributeError:
        pass

    
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
    mathematics_role = 812062467198025748
    datascience_role = 812057868743868426
    computerscience_role = 812058129261002792
    business_role = 812058223582117949
    undergraduate_role = 812059883469537290
    graduate_role = 812059646092115989
    colorblind_role = 804467590931808298

    #replace this role id with the role id from BDC discord server, I used this other role on my testing server
    # add more roles by copying the role id in discord, for example you could add a data sceince role and copy the id into data_science.
    member_role = get(Guild.roles, id = role_member)
    math_role = get(Guild.roles, id = mathematics_role)
    data_role = get(Guild.roles, id = datascience_role)
    compsci_role = get(Guild.roles, id = computerscience_role)
    suits_role = get(Guild.roles, id = business_role)
    undergrad_role = get(Guild.roles, id = undergraduate_role)
    grad_role = get(Guild.roles, id = graduate_role)
    color_role = get(Guild.roles, id = colorblind_role)
    #each role will need an emoji to go along with it.
    if message_id == message and reaction.emoji == '👍':
        channel = reaction.message.channel
        await user.add_roles(member_role)
    elif message_id == message and reaction.emoji == '🧮':
        channel = reaction.message.channel
        await user.add_roles(math_role)
    elif message_id == message and reaction.emoji == '📊':
        channel = reaction.message.channel
        await user.add_roles(data_role)
    elif message_id == message and reaction.emoji == '🖥️':
        channel = reaction.message.channel
        await user.add_roles(compsci_role)
    elif message_id == message and reaction.emoji == '👔':
        channel = reaction.message.channel
        await user.add_roles(suits_role)
    elif message_id == message and reaction.emoji == '📚':
        channel = reaction.message.channel
        await user.add_roles(undergrad_role)
    elif message_id == message and reaction.emoji == '👨‍🎓':
        channel = reaction.message.channel
        await user.add_roles(grad_role)
    elif message_id == message and reaction.emoji == '🌈':
        channel = reaction.message.channel
        await user.add_roles(color_role)

        

client.run(os.getenv('TOKEN'))

