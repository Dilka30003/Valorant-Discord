from Player import Player
import discord
from discord.ext import commands
import Scraper
from io import BytesIO
import os
from pathlib import Path

class Valorant(commands.Cog):
    """ValorantCog"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='agent', brief='Pass username#tag gameType (unrated, comp, etc)', description="Returns agent data")
    async def config_valorant_agent(self, context, command, type=None):
        try:
            if type == None:
                type = "unrated"
            elif type == "comp":
                type = "competitive"
            elif type == "spike":
                type = "spikerush"



            with BytesIO() as image_binary:
                name = command.split('#')[0]
                tag = command.split('#')[1]
                await context.send("Pulling latest data")
                player = Scraper.GetStats(name, tag, type)

                if (player[0] == 0):
                    image = Scraper.GenerateAgentGraphic(player[1])
                    image.save(image_binary, 'PNG')
                    image_binary.seek(0)
                    await context.send(file=discord.File(fp=image_binary, filename='image.png'))
                elif (player[0] == 1):
                    await context.send("User not authenicated. Please authenticate " + player[1])
                elif (player[0] == 404):
                    await context.send("User does not exist")
        except:
            await context.send("Error. Please check syntax and try again")
    
    @commands.command(name='weapon', brief='Pass username#tag gameType (unrated, comp, etc)', description="Returns weapon data")
    async def config_valorant_weapon(self, context, command, type=None):
        try:
            if type == None:
                type = "unrated"
            elif type == "comp":
                type = "competitive"
            elif type == "spike":
                type = "spikerush"



            with BytesIO() as image_binary:
                name = command.split('#')[0]
                tag = command.split('#')[1]
                await context.send("Pulling latest data")
                player = Scraper.GetStats(name, tag, type)

                if (player[0] == 0):
                    image = Scraper.GenerateWeaponGraphic(player[1])
                    image.save(image_binary, 'PNG')
                    image_binary.seek(0)
                    await context.send(file=discord.File(fp=image_binary, filename='image.png'))
                elif (player[0] == 1):
                    await context.send("User not authenicated. Please authenticate " + player[1])
                elif (player[0] == 404):
                    await context.send("User does not exist")
        except:
            await context.send("Error. Please check syntax and try again")
    
    @commands.command(name='stats', brief='Pass username#tag gameType (unrated, comp, etc)', description="Returns player stats")
    async def config_valorant_stats(self, context, command, type=None):
        try:
            if type == None:
                type = "unrated"
            elif type == "comp":
                type = "competitive"
            elif type == "spike":
                type = "spikerush"

            name = command.split('#')[0]
            tag = command.split('#')[1]
            await context.send("Pulling latest data")
            player = Scraper.GetStats(name, tag, type)

            if (player[0] == 0):
                message = ""
                message += '```' + '\n'
                message += 'Playtime:     ' + str(player[1].game.playtime)          + '\n'
                message += 'Matches:      ' + str(player[1].game.matches)           + '\n'
                message += 'KDA:          ' + str(player[1].damage.kda)             + '\n'
                message += 'KD:           ' + str(player[1].damage.kd)              + '\n'
                message += 'Win Rate:     ' + str(player[1].game.winRate)           + '\n'
                message += 'Total Wins    ' + str(player[1].game.wins)              + '\n'
                message += 'Damage/Round: ' + str(player[1].damage.dmg)             + '\n'
                message += 'Score/Round   ' + str(player[1].game.scorePerRound)     + '\n'
                message += 'Kills:        ' + str(player[1].damage.kills)           + '\n'
                message += 'Deaths:       ' + str(player[1].damage.deaths)          + '\n'
                message += 'Assists:      ' + str(player[1].damage.assists)         + '\n'
                message += 'Kills/Round:  ' + str(player[1].damage.killsPerRound)   + '\n'
                message += 'Most Kills:   ' + str(player[1].game.mostKills)         + '\n'
                message += 'Headshots:    ' + str(player[1].damage.Headshots)       + '\n'
                message += 'Headshot%:    ' + str(player[1].damage.headshotRate)    + '\n'
                message += 'First Bloods: ' + str(player[1].game.firstBlood)        + '\n'
                message += 'Aces:         ' + str(player[1].game.ace)               + '\n'
                message += 'Clutches:     ' + str(player[1].game.clutch)            + '\n'
                message += 'Flawless:     ' + str(player[1].game.flawless)          + '\n'
                message += '```'

                await context.send(message)
            elif (player[0] == 1):
                await context.send("User not authenicated. Please authenticate " + player[1])
            elif (player[0] == 404):
                await context.send("User does not exist")
        except:
            await context.send("Error. Please check syntax and try again")
    
    @commands.command(name='accuracy', brief='Pass username#tag gameType (unrated, comp, etc)', description="Returns player accuracy")
    async def config_accuracy(self, context, command, type=None):
        try:
            if type == None:
                type = "unrated"
            elif type == "comp":
                type = "competitive"
            elif type == "spike":
                type = "spikerush"

            name = command.split('#')[0]
            tag = command.split('#')[1]
            await context.send("Pulling latest data")
            player = Scraper.GetStats(name, tag, type)

            if (player[0] == 0):
                message = ""
                message += '```' + '\n'
                message += 'Head: ' + '{text: <6}'.format(text=str(player[1].accuracy.headRate)+"%") + ' ' + '{text: >5}'.format(text=str(player[1].accuracy.head)) + ' Hits\n'
                message += 'Body: ' + '{text: <6}'.format(text=str(player[1].accuracy.bodyRate)+"%") + ' ' + '{text: >5}'.format(text=str(player[1].accuracy.body)) + ' Hits\n'
                message += 'Legs: ' + '{text: <6}'.format(text=str(player[1].accuracy.legRate)+"%")  + ' ' + '{text: >5}'.format(text=str(player[1].accuracy.leg))  + ' Hits\n'
                message += '```'

                await context.send(message)
            elif (player[0] == 1):
                await context.send("User not authenicated. Please authenticate " + player[1])
            elif (player[0] == 404):
                await context.send("User does not exist")
        except:
            await context.send("Error. Please check syntax and try again")
    
    @commands.command(name='leaderboard', brief='show leaderboard, add or remove user', description="Returns player leaderboard")
    async def config_leaderboard(self, context, command=None, user=None):
        try:
            path = "storage/leaderboard/" + str(context.message.guild.id)
            Path("storage/leaderboard").mkdir(parents=True, exist_ok=True)

            validOptions = [[
                    "kda",
                    "kd",
                    "kills",
                    "deaths",
                    "assists",
                    "killsPerRound",
                    "Headshots",
                    "headshotRate",
                    "dmg"
                ], [
                    "winRate",
                    "wins",
                    "scorePerRound",
                    "mostKills",
                    "firstBlood",
                    "ace"
                ]]

            if command == "add":
                if user is not None:
                    user = user.lower();
                    await context.send("Checking Player")
                    name = user.split('#')[0]
                    tag = user.split('#')[1]
                    player = Scraper.GetStats(name, tag, 'unrated')

                    if (player[0] == 0):
                        pass
                    elif (player[0] == 1):
                        await context.send("Player not authenicated. Please authenticate " + player[1])
                        return
                    elif (player[0] == 404):
                        await context.send("Player does not exist")
                        return

                    user += '\n'
                    currentUsers = []
                    if os.path.isfile(path):
                        with open(path, 'r') as f:
                            currentUsers = f.readlines()

                    if user in currentUsers:
                        await context.send("Player has already been added")
                        return
                    currentUsers.append(user)

                    with open("storage/leaderboard/" + str(context.message.guild.id), 'w+') as f:
                        f.writelines(currentUsers)
                    await context.send("Player has been added")
                else:
                    await context.send("Please Provide A Valid Player")
                return
                
            elif command == "remove":
                if user is not None:
                    user = user.lower();
                    user += '\n'
                    currentUsers = []
                    if os.path.isfile(path):
                        with open(path, 'r') as f:
                            currentUsers = f.readlines()

                    if user in currentUsers:
                        currentUsers.pop(currentUsers.index(user))
                    else:
                        await context.send("Player is not in the list")
                        return

                    with open("storage/leaderboard/" + str(context.message.guild.id), 'w+') as f:
                        f.writelines(currentUsers)
                    await context.send("Player has been removed")
                else:
                    await context.send("Please Provide A Player")
                return
            elif command == "options":
                message = ""
                for item in validOptions[0]:
                    message += item + "\n"
                for item in validOptions[1]:
                    message += item + "\n"
                await context.send(message)
                return
            else:
                location = (0, 0)
                if command == None:
                    pass
                elif command.lower() in map(str.lower, validOptions[0]):
                    location = (0, [item.lower() for item in validOptions[0] ].index(command.lower()))
                elif command.lower() in map(str.lower, validOptions[1]):
                    location = (1, [item.lower() for item in validOptions[1] ].index(command.lower()))
                else:
                    await context.send("Invalid Option. See leaderboard options.")
                    return
                type = "unrated"
                

                with open(path, 'r') as f:
                    currentUsers = f.readlines()
                leaderBoard = []

                msg = await context.send("Getting Player Data: " + "0/" + str(len(currentUsers)))
                i=1
                for user in currentUsers:
                    await msg.edit(content="Getting Player Data: " + str(i) + "/" + str(len(currentUsers)))
                    i+=1
                    name = user.split('#')[0]
                    tag = user.split('#')[1]
                    player = Scraper.GetStats(name, tag, type)
                    if location[0]:
                        leaderBoard.append((user, getattr(player[1].game, validOptions[1][location[1]])))
                    else:
                        leaderBoard.append((user, getattr(player[1].damage, validOptions[0][location[1]])))

                leaderBoard.sort(key = lambda x: x[1], reverse=True) 
                message = "```\nPlayer Leaderboard " + "(" + validOptions[location[0]][location[1]] + ")\n"
                maxLen = len(max(currentUsers, key = len))
                for i in range(len(leaderBoard)):
                    message += str(i+1) + '. '
                    player = leaderBoard[i][0].strip()
                    message += '{message:{fill}{align}{width}}'.format(
                                message=player,
                                fill=' ',
                                align='<',
                                width=maxLen,
                                )
                    message += str(leaderBoard[i][1]) + '\n'
                message += "```"
                await msg.edit(content=message)
        except Exception as e:
            await context.send("Error. Please check syntax and try again")
            await context.send(e)


            

def setup(bot):
    bot.add_cog(Valorant(bot))
