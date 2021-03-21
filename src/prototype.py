# -*- coding: utf-8 -*-
import discord
import os
from discord.ext import commands
from dotenv import load_dotenv
import requests

load_dotenv()

intents = discord.Intents.default()
#intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

prev_message = ""

@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))

@bot.command(name='honk')
async def honk(ctx):
    await ctx.send(":bird: *doot doot* :bird:")

@bot.event
async def on_message(message):
    global prev_message

    if message.author == bot.user:
        return

    #When someone is tagged, it replaces the text with their user id formatted like so.
    #DON'T FORGET TO REPLACE THIS USER ID TO THE REAL BOT WHEN DEPLOYED
    #if "<@!823172527697297469>" in message.content:
    #    r = requests.post(
    #        "https://api.deepai.org/api/text-generator",
    #        data={
    #            'text': prev_message,
    #        },
    #        headers={'api-key': 'API-KEY-HERE'}
    #    )
    #    gpt2_output = r.json()['output']
    #    gpt2_output = gpt2_output.split("\n\n")[1]
    #    await message.channel.send(gpt2_output)

    prev_message = message.content


bot.run(os.getenv('TOKEN'))