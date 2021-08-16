from discord import message
import discord
from discord import Embed
from discord.ext import commands
import Scraper
from io import BytesIO
import os
from pathlib import Path

class Valorant(commands.Cog):
    """ValorantCog"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='agents', brief='Pass username#tag gameType (unrated, comp, etc)', description="Returns agent data")
    async def config_valorant_agent(self, context, *command, type=None):
        command = list(command)
        type = command.pop()
        if not (type == "unrated" or type == "comp" or type == "competitive" or type == "spike" or type == "spikerush"):
            command.append(type)
            type = None
        command = ' '.join(command)
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
                message = await context.send("Pulling latest data")
                code, URL, results, player = Scraper.PlayerSetup(name, tag, type)

                code, player = Scraper.GetAgents(player=player, results=results)

                if (code == 0):
                    image = Scraper.GenerateAgentGraphic(player)
                    image.save(image_binary, 'PNG')
                    image_binary.seek(0)
                    file=discord.File(fp=image_binary, filename='image.png')

                    embed = Embed(color=0xfa4454)
                    embed.set_author(name=f"{name} {type} stats", url=player.url, icon_url=player.avatar)
                    embed.title="Top 3 Agents"
                    embed.description=type
                    embed.set_image(url="attachment://image.png")
                    await message.delete()
                    await context.send(file=file, embed=embed)
                elif (code == 1):
                    await context.send("User not authenicated. Please authenticate " + player[1])
                elif (code == 404):
                    await context.send("User does not exist")
        except:
            await context.send("Error. Please check syntax and try again")
    
    @commands.command(name='weapons', brief='Pass username#tag gameType (unrated, comp, etc)', description="Returns weapon data")
    async def config_valorant_weapon(self, context, *command, type=None):
        command = list(command)
        type = command.pop()
        if not (type == "unrated" or type == "comp" or type == "competitive" or type == "spike" or type == "spikerush"):
            command.append(type)
            type = None
        command = ' '.join(command)
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
                message = await context.send("Pulling latest data")
                code, URL, results, player = Scraper.PlayerSetup(name, tag, type)

                code, player = Scraper.GetWeapons(player=player, results=results)

                if (code == 0):
                    image = Scraper.GenerateWeaponGraphic(player)
                    image.save(image_binary, 'PNG')
                    image_binary.seek(0)
                    file=discord.File(fp=image_binary, filename='image.png')

                    embed = Embed(color=0xfa4454)
                    embed.set_author(name=f"{name} {type} stats", url=player.url, icon_url=player.avatar)
                    embed.title="Top 3 Weapons"
                    embed.description=type
                    embed.set_image(url="attachment://image.png")
                    await message.delete()
                    await context.send(file=file, embed=embed)
                elif (code == 1):
                    await context.send("User not authenicated. Please authenticate " + player[1])
                elif (code == 404):
                    await context.send("User does not exist")
        except:
            await context.send("Error. Please check syntax and try again")
    
    @commands.command(name='stats', brief='Pass username#tag gameType (unrated, comp, etc)', description="Returns player stats")
    async def config_valorant_stats(self, context, *command, type=None):
        command = list(command)
        type = command.pop()
        if not (type == "unrated" or type == "comp" or type == "competitive" or type == "spike" or type == "spikerush"):
            command.append(type)
            type = None
        command = ' '.join(command)
        try:
            if type == None:
                type = "unrated"
            elif type == "comp":
                type = "competitive"
            elif type == "spike":
                type = "spikerush"

            name = command.split('#')[0]
            tag = command.split('#')[1]
            message = await context.send("Pulling latest data")

            code, URL, results, player = Scraper.PlayerSetup(name, tag, type)

            code, player = Scraper.GetStats(player=player, results=results)

            if (code == 0):
                embed = Embed(color=0xfa4454)
                embed.set_author(name=f"{name} {type} stats", url=player.url, icon_url=player.avatar)
                embed.title=f"Playtime: {str(player.game.playtime)}"
                embed.description=f"Matches: {str(player.game.matches)}"
                
                embed.add_field(name="Wins", value=str(player.game.wins), inline=True)
                embed.add_field(name="Win Rate", value=str(player.game.winRate), inline=True)
                embed.add_field(name="Score/Round", value=str(player.game.scorePerRound), inline=True)

                embed.add_field(name="KDA", value=str(player.damage.kda), inline=True)
                embed.add_field(name="KD", value=str(player.damage.kd), inline=True)
                embed.add_field(name="Damage/Round", value=str(player.damage.dmg), inline=True)

                embed.add_field(name="Kills", value=str(player.damage.kills) , inline=True)
                embed.add_field(name="Deaths", value=str(player.damage.deaths) , inline=True)
                embed.add_field(name="Assists", value=str(player.damage.assists) , inline=True)

                embed.add_field(name="Kills/Round", value=str(player.damage.killsPerRound), inline=True)
                embed.add_field(name="Most Kills", value=str(player.game.mostKills), inline=True)
                embed.add_field(name="Headshots", value=str(player.damage.Headshots), inline=True)
                embed.add_field(name="Clutches", value=str(player.game.clutch), inline=True)
                embed.add_field(name="Flawless", value=str(player.game.flawless), inline=True)
                embed.add_field(name="Ace", value=str(player.game.ace), inline=True)
                embed.add_field(name="First Blood", value=str(player.game.firstBlood), inline=True)
                embed.add_field(name="Headshot%", value=str(player.damage.headshotRate), inline=True)

                await message.delete()
                await context.send(embed=embed)
            elif (code == 1):
                await context.send("User not authenicated. Please authenticate " + URL)
            elif (code == 404):
                await context.send("User does not exist")
        except:
            await context.send("Error. Please check syntax and try again")
    
    @commands.command(name='accuracy', brief='Pass username#tag gameType (unrated, comp, etc)', description="Returns player accuracy")
    async def config_accuracy(self, context, *command, type=None):
        command = list(command)
        type = command.pop()
        if not (type == "unrated" or type == "comp" or type == "competitive" or type == "spike" or type == "spikerush"):
            command.append(type)
            type = None
        command = ' '.join(command)
        try:
            if type == None:
                type = "unrated"
            elif type == "comp":
                type = "competitive"
            elif type == "spike":
                type = "spikerush"

            name = command.split('#')[0]
            tag = command.split('#')[1]
            message = await context.send("Pulling latest data")
            code, URL, results, player = Scraper.PlayerSetup(name, tag, type)

            code, player = Scraper.GetAccuracy(player=player, results=results)

            if (code == 0):
                embed = Embed(color=0xfa4454)
                embed.set_author(name=f"{name} {type} stats", url=player.url, icon_url=player.avatar)
                embed.title="Accuracy"
                embed.description=type
                
                embed.add_field(name="Head %", value=str(player.accuracy.headRate)+"%", inline=True)
                embed.add_field(name="Body %", value=str(player.accuracy.bodyRate)+"%", inline=True)
                embed.add_field(name="Leg %", value=str(player.accuracy.legRate)+"%", inline=True)

                embed.add_field(name="Head Hits", value=str(player.accuracy.head), inline=True)
                embed.add_field(name="Body Hits", value=str(player.accuracy.body), inline=True)
                embed.add_field(name="Leg Hits", value=str(player.accuracy.leg), inline=True)
                
                await message.delete()
                await context.send( embed=embed)
            elif (code == 1):
                await context.send("User not authenicated. Please authenticate " + player[1])
            elif (code == 404):
                await context.send("User does not exist")
        except:
            await context.send("Error. Please check syntax and try again")


            

def setup(bot):
    bot.add_cog(Valorant(bot))
