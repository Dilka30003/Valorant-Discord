from discord import message
from Player import Player
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
                message = await context.send("Pulling latest data")
                player = Scraper.GetStats(name, tag, type)

                if (player[0] == 0):
                    image = Scraper.GenerateAgentGraphic(player[1])
                    image.save(image_binary, 'PNG')
                    image_binary.seek(0)
                    file=discord.File(fp=image_binary, filename='image.png')

                    embed = Embed(color=0xfa4454)
                    embed.set_author(name=f"{name}", url=player[1].url, icon_url=player[1].avatar)
                    embed.title="Top 3 Agents"
                    embed.description=type
                    embed.set_image(url="attachment://image.png")
                    await message.delete()
                    await context.send(file=file, embed=embed)
                elif (player[0] == 1):
                    await context.send("User not authenicated. Please authenticate " + player[1])
                elif (player[0] == 404):
                    await context.send("User does not exist")
        except:
            await context.send("Error. Please check syntax and try again")
    
    @commands.command(name='weapons', brief='Pass username#tag gameType (unrated, comp, etc)', description="Returns weapon data")
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
                message = await context.send("Pulling latest data")
                player = Scraper.GetStats(name, tag, type)

                if (player[0] == 0):
                    image = Scraper.GenerateWeaponGraphic(player[1])
                    image.save(image_binary, 'PNG')
                    image_binary.seek(0)
                    file=discord.File(fp=image_binary, filename='image.png')

                    embed = Embed(color=0xfa4454)
                    embed.set_author(name=f"{name}", url=player[1].url, icon_url=player[1].avatar)
                    embed.title="Top 3 Weapons"
                    embed.description=type
                    embed.set_image(url="attachment://image.png")
                    await message.delete()
                    await context.send(file=file, embed=embed)
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
            message = await context.send("Pulling latest data")
            player = Scraper.GetStats(name, tag, type)

            if (player[0] == 0):
                embed = Embed(color=0xfa4454)
                embed.set_author(name=f"{name} {type} stats", url=player[1].url, icon_url=player[1].avatar)
                embed.title=f"Playtime: {str(player[1].game.playtime)}"
                embed.description=f"Matches: {str(player[1].game.matches)}"
                
                embed.add_field(name="Wins", value=str(player[1].game.wins), inline=True)
                embed.add_field(name="Win Rate", value=str(player[1].game.winRate), inline=True)
                embed.add_field(name="Score/Round", value=str(player[1].game.scorePerRound), inline=True)

                embed.add_field(name="KDA", value=str(player[1].damage.kda), inline=True)
                embed.add_field(name="KD", value=str(player[1].damage.kd), inline=True)
                embed.add_field(name="Damage/Round", value=str(player[1].damage.dmg), inline=True)

                embed.add_field(name="Kills", value=str(player[1].damage.kills) , inline=True)
                embed.add_field(name="Deaths", value=str(player[1].damage.deaths) , inline=True)
                embed.add_field(name="Assists", value=str(player[1].damage.assists) , inline=True)

                embed.add_field(name="Kills/Round", value=str(player[1].damage.killsPerRound), inline=True)
                embed.add_field(name="Most Kills", value=str(player[1].game.mostKills), inline=True)
                embed.add_field(name="Headshots", value=str(player[1].damage.Headshots), inline=True)
                embed.add_field(name="Clutches", value=str(player[1].game.clutch), inline=True)
                embed.add_field(name="Flawless", value=str(player[1].game.flawless), inline=True)
                embed.add_field(name="Headshot%", value=str(player[1].damage.headshotRate), inline=True)

                await message.delete()
                await context.send(embed=embed)
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


            

def setup(bot):
    bot.add_cog(Valorant(bot))
