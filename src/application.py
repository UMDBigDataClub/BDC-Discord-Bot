# -*- coding: utf-8 -*-
import discord
import os
from discord.ext import commands

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)
bot.load_extension("cogs.scoreboard_awards")
bot.load_extension("cogs.roles")

@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))

@bot.command(name='honk')
async def honk(ctx):
    await ctx.send(":bird: *doot doot* :bird:")

bot.run(os.getenv('TOKEN'))
