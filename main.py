# -*- coding: utf-8 -*-
import discord
import os
import boto3
import pandas as pd
import json
from discord.utils import get
from discord.ext import commands
from scoreboard import Scoreboard



sb = Scoreboard()


prev_author = ""
cur_author = ""
prev_committer = ""

bot = commands.Bot(command_prefix='!')


@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))


@bot.command(name='scoreboard')
async def scoreboard(ctx):
    embed = discord.Embed(title="Big Data Club Scoreboard", description="Check out who's leading the pack in points this semester!", color=0x3357FF)
    embed.add_field(name="**Top Scorers**", value="```" + sb.display() + "```")
    await ctx.send(embed = embed)

    # Prints the score of everyone in the scoreboard.csv file
    # if message.content == '/scoreboard':
    #    await message.channel.send(sb.display())

@bot.command(name='scoreboard_everyone')
async def scoreboard_everyone(ctx):
    embed = discord.Embed(title="Big Data Club Scoreboard - All Users", description="This scoreboard includes admins as well as the users eligible for prizes.", color=0x3357FF)
    embed.add_field(name="**Top Scorers**", value="```" + sb.display(non_participating=True) + "```")
    await ctx.send(embed=embed)

@bot.command(name='scoreboard_all_time')
async def scoreboard_all_time(ctx):
    embed = discord.Embed(title="Big Data Club Scoreboard - All Time",description="This shows the total scores attained by all BDC members since time immemorial", color=0x3357FF)
    embed.add_field(name="**Top Scorers**", value="```" + sb.display(all_time=True, non_participating=True) + "```")
    await ctx.send(embed=embed)

@bot.command(name='score_all_time')
async def scoreboard_all_time(ctx, username):
    await ctx.send(sb.display(name=username, all_time=True))

@bot.command(name='score')
async def scoreboard_all_time(ctx, username):
    await ctx.send(sb.display(name=username))

@bot.command(name='add')
async def add(ctx, arg1, arg2):
    if 'Administrator' in [role.name for role in ctx.author.roles]:
        sb.add(arg1, arg2)

@bot.command(name='set_github')
async def set_github(ctx, username, github):
    if 'Administrator' in [role.name for role in ctx.author.roles] or ctx.author.name == arg2:
        sb.update(name=username, github=github)

@bot.command(name='set_email')
async def set_email(ctx, username, email):
    if 'Administrator' in [role.name for role in ctx.author.roles] or ctx.author.name == arg2:
        sb.update(name=username, email=email)

@bot.command(name='honk')
async def honk(ctx):
    await ctx.send("*doot doot*")


@bot.command(name='set_participating')
async def set_participating(ctx, username, participating_yes_or_no):
    if 'Administrator' in [role.name for role in ctx.author.roles] or ctx.author.name == participating_yes_or_no:
        sb.update(name=username, participating=participating_yes_or_no)

@bot.command(name='new_user')
async def new_user(ctx, name, email=None, github=None):
    if 'Administrator' in [role.name for role in ctx.author.roles]:
        sb.create_user(name, email, github)

@bot.command(name='awards')
async def awards(ctx):
    content = \
        """
        Here is the list of awards available at the end of season:
        Consulting Award - to any member that completes a BDC-sponsored consulting project - 100 points
        Recruiting Award - to any member that recruits a new active member to the club - 100 points
        Presentation Award - to any member that gives a presentation - 50 points
        """
    await ctx.send(content)



@bot.event
async def on_message(message):
    global sb
    global prev_author
    global cur_author
    global prev_committer

    if message.author == bot.user:
        return

    if message.author != "BDC-Bot" and message.author != "GitHub":
        prev_author = cur_author
        cur_author = message.author.name

    # Give members one point for each message, but only if they are not posting multiple times in a row
    if cur_author != prev_author and prev_author != "" and not message.content.startswith(
            '/') and not message.content.startswith('\'') and not message.content.startswith('!'):
        sb.add(cur_author, 1)

    # Give members 20 points for each GitHub commit, but only if they are nonconsecutive
    if message.author.name == "GitHub":
        committer = message.embeds[0].to_dict()["author"]["name"]
        # Test for previous committer
        if committer in sb.df.GitHub.values and committer != prev_committer:
            prev_committer = committer
            name = sb.df[sb.df.GitHub == committer].Member.iloc[0]
            sb.add(name, 20)
            await message.channel.send(name + " has earned 20 points for committing to GitHub!")
    else:
        prev_committer = ""

    await bot.process_commands(message)



# reaction roles, assigns roles based on emoji used for the reaction of a specific message
@bot.event
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

    # replace this role id with the role id from BDC discord server, I used this other role on my testing server
    # add more roles by copying the role id in discord, for example you could add a data sceince role and copy the id into data_science.
    member_role = get(Guild.roles, id=role_member)
    math_role = get(Guild.roles, id=mathematics_role)
    data_role = get(Guild.roles, id=datascience_role)
    compsci_role = get(Guild.roles, id=computerscience_role)
    suits_role = get(Guild.roles, id=business_role)
    undergrad_role = get(Guild.roles, id=undergraduate_role)
    grad_role = get(Guild.roles, id=graduate_role)
    color_role = get(Guild.roles, id=colorblind_role)
    # each role will need an emoji to go along with it.
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


bot.run(os.getenv('TOKEN'))

