from discord import message
import discord
from discord import Embed
from discord.ext import commands
#import Scraper
from io import BytesIO
import os
from pathlib import Path

from Player import Player, CODES, MODE

class Help(commands.Cog):
    """ValorantCog"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='help', brief='help', description="help")
    async def config_valorant_agent(self, context, command = None):
        embed = Embed(color=0xfa4454)
        embed.title="Help"
        embed.description="Help with Valorant Commands"

        embed.add_field(name="Stats", value="=stats name#tag\n- Returns Assorted Player Stats", inline=False)
        embed.add_field(name="Agents", value="=agents name#tag\n- Returns Graphic of Top 3 Agents", inline=False)
        embed.add_field(name="Weapons", value="=weapons name#tag\n- Returns Graphic of Top 3 Weapons", inline=False)
        embed.add_field(name="Graph", value="=graph name#tag\nReturns Ranked Rating Graph", inline=False)
        embed.add_field(name="Graph", value="=graph name1#tag1 name2#tag2 ...\n- Returns Ranked Rating Graph For All Players Provided", inline=False)
        embed.add_field(name="Leaderboard", value=  "=leaderboard add name#tag\n"+
                                                    "- Add a player to the leaderboard\n"
                                                    "=leaderboard remove name#tag\n"
                                                    "- Remove a player from the leaderboard\n"
                                                    "=leaderboard\n"
                                                    "- Show the leaderboard", inline=False)

        await context.send(embed=embed)

def setup(bot):
    bot.add_cog(Help(bot))
