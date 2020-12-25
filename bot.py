import os
import discord
import requests
import json
import random
from dotenv import load_dotenv
from discord.ext import commands
from discord.ext.commands import MissingPermissions
import traceback
import logging

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='>')
bot.remove_command('help')


# load cogs

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')

# command cooldown

bot.run(TOKEN)
