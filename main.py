#!/usr/bin/python3
import yaml
import os
from os import listdir
from os.path import isfile, join
from datetime import datetime, timedelta
import logging
from io import BytesIO

import discord
from discord import Embed
from discord.ext import commands
from discord_components import DiscordComponents, Button, ButtonStyle, InteractionType
import time

import asyncio
import threading

from Leaderboard import Leaderboard, Player
from Graph import PlayerGraph, MultiGraph
from Career import Career

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

bot = commands.Bot(command_prefix=localConfig['command_prefix'], help_command=None)
logging.info('Created Bot')

# Create Leaderboards
leaderboards = {}
for server in [f for f in listdir('storage/leaderboard') if isfile(join('storage/leaderboard', f))]:
    leaderboards[server] = Leaderboard(server)

# Load player data into graph
graphs = {}
for filename in listdir('storage/graphs'):
    graphs[filename] = PlayerGraph(filename.split('#')[0], filename.split('#')[1])

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
    DiscordComponents(bot, change_discord_methods=True)
    with open('version') as f:
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f.read()))
    x = threading.Thread(target=background_task, daemon=True)
    x.start()
    
@bot.event
async def on_message(message):
    logging.debug('Recieved Message: ' + message.content)
    if message.author == bot.user:
        return

    await handle_leaderboard(message)
    await handle_graphs(message)
    await handle_career(message)

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

async def handle_graphs(message):
    if message.content[0:6].lower() == "=graph":
        arguments = message.content.split(' ')
        if len(arguments) == 2:
            msg = await message.channel.send("Generating Graph")
            if not arguments[1].lower() in graphs:
                player = arguments[1].split('#')
                
                Graph = PlayerGraph(player[0].lower(), player[1].lower())
                response = Graph.update()
                if response == PlayerGraph.Status.INVALID:
                    await message.channel.send("Invalid Player")
                    return
                graphs[arguments[1].lower()] = Graph
            
            file = graphs[arguments[1].lower()].draw()
            await msg.delete()
            if file is None:
                await message.channel.send("No competitive games in history. Please play a competitive game first.")
                return
            await message.channel.send(file=file)

        else:
            await message.channel.send("Incorrect User Syntax")
            return
    
    if message.content[0:11].lower() == "=multigraph":
        arguments = message.content.split(' ')[1:]
        msg = await message.channel.send("Generating Graph")
        players = []
        for argument in arguments:
            player = tuple(argument.split('#'))
            players.append(player)
        try:
            Graph = MultiGraph(players)
        except:
            await message.channel.send("Check syntax and try again")
        file = Graph.draw()
        await msg.delete()
        if file is None:
            await message.channel.send("No competitive games in history. Please play a competitive game first.")
            return
        await message.channel.send(file=file)

async def handle_career(message):
    if message.content[0:7].lower() == "=career":
        arguments = message.content.split(' ')
        if len(arguments) >= 2:
            try:
                myMessage = await message.channel.send("Generating Career (this may take a while) USING CACHED DATA DONT FORGET TO CHANGE THIS")
                arguments.pop(0)
                arguments = ' '.join(arguments)
                player = arguments.split('#')
                career = Career(player[0], player[1], True)
                if career.isValid:
                    with BytesIO() as image_binary:
                        embed, file = career.Graphic()

                        button1 = Button(style=ButtonStyle.red, label="Game 1", custom_id=f"{player[0]}#{player[1]}#1")
                        button2 = Button(style=ButtonStyle.red, label="Game 2", custom_id=f"{player[0]}#{player[1]}#2")
                        button3 = Button(style=ButtonStyle.red, label="Game 3", custom_id=f"{player[0]}#{player[1]}#3")
                        button4 = Button(style=ButtonStyle.red, label="Game 4", custom_id=f"{player[0]}#{player[1]}#4")
                        button5 = Button(style=ButtonStyle.red, label="Game 5", custom_id=f"{player[0]}#{player[1]}#5")

                        await myMessage.delete()
                        await message.channel.send(file=file, embed=embed, type=InteractionType.ChannelMessageWithSource, components=[[button1, button2, button3, button4, button5]])
                else:
                    await message.channel.send("Invalid Player")
            except:
                await message.channel.send("Check syntax and try again")


@bot.event
async def on_button_click(interaction):
    if interaction.component.label.startswith("Game"):
        id = interaction.component.custom_id.split('#')
        career = Career(id[0], id[1], True)
        gameNumber = int(id[2])
        await interaction.respond(type=InteractionType.ChannelMessageWithSource, content='Button Clicked')

# Background thread that runs once every 10 minutes
def background_task():
    while not bot.is_closed():
        logging.info("Starting Update Sequence")
        for key in leaderboards:
            logging.info(f"Updating Leaderboad {key}")
            leaderboards[key].update()
        for key in graphs:
            logging.info(f"Updating Graph {key}")
            graphs[key].update()
        time.sleep(10*60)

bot.run(TOKEN)