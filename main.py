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
from Leaderboard import Leaderboard, Player

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
leaderboards = {}
for server in [f for f in listdir('storage/leaderboard') if isfile(join('storage/leaderboard', f))]:
    leaderboards[server] = Leaderboard(server)

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

    await handle_leaderboard(message)

    await bot.process_commands(message)

async def handle_leaderboard(message):
    if message.content[0:12].lower() == "=leaderboard":
        arguments = message.content.split(' ')
        if len(arguments) == 1:
            await message.channel.send(leaderboards[str(message.channel.guild.id)].generate())
        elif arguments[1].lower() == 'add':
            # Get User
            player = arguments[2].split('#')
            if len(player) != 2:
                await message.channel.send("Incorrect User Syntax")
                return

            key = str(message.channel.guild.id)
            if not key in leaderboards.keys():
                leaderboards[str(message.channel.guild.id)] = Leaderboard(message.channel.guild.id)
            response = leaderboards[str(message.channel.guild.id)].add(Player(player[0], player[1]))
            
            if response == Leaderboard.Status.DUPLICATE:
                await message.channel.send("Player has already been added")
                return
            elif response == Leaderboard.Status.INVALID:
                await message.channel.send("Invalid Player")
                return
            elif response == Leaderboard.Status.NODATA:
                await message.channel.send("Player has been added, however they must play a competitive game before appearing on the leaderboard")
                return
            elif response == Leaderboard.Status.OK:
                await message.channel.send("Player Successfully Added")
                return
            await message.channel.send("You shouldn't be seeing this message. Something broke")
        elif arguments[1].lower() == 'remove':
            # Get User
            player = arguments[2].split('#')
            if len(player) != 2:
                await message.channel.send("Incorrect User Syntax")
                return

            key = str(message.channel.guild.id)
            if not key in leaderboards.keys():
                await message.channel.send("This server does not have a leaderboard")
                return
            response = leaderboards[str(message.channel.guild.id)].remove(Player(player[0], player[1]))
            
            if response == Leaderboard.Status.NOTFOUND:
                await message.channel.send("Player is not on the leaderboard")
                return
            elif response == Leaderboard.Status.OK:
                await message.channel.send("Player Successfully Removed")
                return
            await message.channel.send("You shouldn't be seeing this message. Something broke")



# Background thread that runs once every 10 minutes
async def background_task():
    await bot.wait_until_ready()
    while not bot.is_closed():
        for leaderboard in leaderboards:
            leaderboard.update()
        await asyncio.sleep(10*60)

bot.loop.create_task(background_task())
bot.run(TOKEN)