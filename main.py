#!/usr/bin/python3
import yaml
import os
from os import listdir
from os.path import isfile, join
from datetime import datetime, timedelta
import logging

import discord
from discord.ext import commands

import asyncio
from Leaderboard import Leaderboard

# Remove the old log file if it exists and start logging
try:
    os.remove('logs/bot.log')
except OSError:
    pass
logging.basicConfig(filename='logs/bot.log', level=logging.DEBUG)

# Open config files
with open('credentials.yaml') as f:
    credentials = yaml.load(f, Loader=yaml.FullLoader)
    logging.info('Loaded Credentials')
with open('config.yaml') as f:
    localConfig = yaml.load(f, Loader=yaml.FullLoader)
    logging.info('Loaded Local Config')

# Init Bot
TOKEN = credentials['token']

bot = commands.Bot(command_prefix=localConfig['command_prefix'])
logging.info('Created Bot')

# Create Leaderboards
leaderboards = []
for server in [f for f in listdir('storage/leaderboard') if isfile(join('storage/leaderboard', f))]:
    leaderboards.append(Leaderboard(server))

if __name__ == '__main__':
    for extension in [f for f in listdir('modules') if isfile(join('modules', f))]:
        bot.load_extension('modules.' + extension[:-3])
        logging.info('Loaded ' + extension)

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    logging.info('Successfully Logged In as ' + bot.user.name + '   ' + str(bot.user.id))
    with open('version') as f:
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f.read()))

@bot.event
async def on_message(message):
    logging.debug('Recieved Message: ' + message.content)
    if message.author == bot.user:
        return
    
    if message.content[0:12].lower() == "=leaderboard":
        arguments = message.content.split(' ').pop()
        if arguments[0].lower == 'add':
            pass
            


    await bot.process_commands(message)

# Background thread that runs once every 10 minutes
async def background_task():
    await bot.wait_until_ready()
    while not bot.is_closed():
        print("hi")
        await asyncio.sleep(10*60)

bot.loop.create_task(background_task())
bot.run(TOKEN)