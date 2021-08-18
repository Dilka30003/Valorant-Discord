import requests
import yaml
from enum import Enum
from datetime import datetime, timedelta, timezone
from PIL import Image, ImageFont, ImageDraw, ImageEnhance
from io import BytesIO

import discord
from discord import Embed

class Player():
    def __init__(self, data):
        self.name = data['name'].lower()
        self.tag = data['tag'].lower()
        self.agent = data['character'].lower()
        self.score = data['stats']['score']
        self.k = data['stats']['kills']
        self.d = data['stats']['deaths']
        self.a = data['stats']['assists']
        self.rank = data['currenttier']
        self.abilities = data['ability_casts']
        self.card = f"https://titles.trackercdn.com/valorant-api/playercards/{data['player_card']}/displayicon.png"


    def __str__(self) -> str:
        return f"{self.name}#{self.tag}"

class Game():
    def __init__(self, name:str, tag:str, gameData):
        # Store player name and tag
        self.name = name.lower()
        self.tag = tag.lower()
        self.player = None

        self.__metadata(gameData['metadata'])   # Read metadata secion
        self.__players(gameData['players'])     # Read Players Section

        self.roundWins = gameData['teams'][self.colour]['rounds_won']
        self.roundLoss = gameData['teams'][self.colour]['rounds_lost']
        self.hasWon = gameData['teams'][self.colour]['has_won']
        
    def __metadata(self, data):
        # Get the map and mode of the game
        self.map = data['map']
        self.mode = data['mode']
        self.gameStart = datetime.fromtimestamp(data['game_start']/1000).astimezone(tz=None)
        self.gameLength = timedelta(milliseconds=data['game_length'])
        
    
    def __players(self, data):
        # Player really should be a a class but i cant be bothered right now
        playerList = []
        allPlayers = []
        isUser = False
        for playerData in data['red']:
            player = Player(playerData)
            playerList.append(player) # Append Player to a list
            if player.name == self.name and player.tag == self.tag:   # If our player is in this team, the team is allies, get their data
                isUser = True
                self.player = player

                if self.mode == 'Competitive':
                    self.icon = str(player.rank)
                elif self.mode == 'Spike Rush':
                    self.icon = 'spike-rush'
                else:
                    self.icon = 'normal'
        if isUser:
            self.allies = playerList
            self.colour = 'red'
        else:
            self.enemies = playerList
            self.colour = 'blue'
        
        allPlayers += playerList
        # Do the same thing
        playerList = []
        for playerData in data['blue']:
            player = Player(playerData)
            playerList.append(player)
            if player.name == self.name and player.tag == self.tag:
                self.player = player

                if self.mode == 'Competitive':
                    self.icon = str(player.rank)
                elif self.mode == 'Spike Rush':
                    self.icon = 'spike-rush'
                else:
                    self.icon = 'normal'
        if isUser:
            self.enemies = playerList
        else:
            self.allies = playerList

        allPlayers += playerList

        self.playerList = sorted(allPlayers, key=lambda k: k.score, reverse=True)
        self.position = next((index for (index, d) in enumerate(self.playerList) if d.name == self.name and d.tag == self.tag), None)+1


class Career():
    class CODE(Enum):
        ERROR = 0
        DUPLICATE = 1
        NOTFOUND = 2

        INVALID = 404
        NODATA = 204
        OK = 200

    def __init__(self, name, tag):
        # Get Data (Will take a while)
        self.name = name
        self.tag = tag
        data = requests.get(f'https://api.henrikdev.xyz/valorant/v3/matches/ap/{name}/{tag}')
        # Do some error checking im too lazy to do
        if data.status_code == self.CODE.INVALID.value:
            self.isValid = False
            return
        elif data.status_code == self.CODE.NODATA.value:
            self.isValid = False
            return
        self.isValid = True

        games = data.json()['data']

        # Iterate over every game (5 as of writing)
        self.GameList = []
        for gameData in games:
            if gameData['metadata']['mode'].lower() in ('unrated', 'competitive', 'spike rush'):
                self.GameList.append(Game(name.lower(), tag.lower(), gameData))
    
    def Graphic(self):
        img = Image.new('RGBA', (1920, 256*len(self.GameList)), (255, 0, 0, 0))                           # Create the main image and fonts
        LargeFont = ImageFont.truetype("Roboto/Roboto-Medium.ttf", 100)
        subtextFont = ImageFont.truetype("Roboto/Roboto-Medium.ttf", 70)
        miniFont = ImageFont.truetype("Roboto/Roboto-Medium.ttf", 50)

        MARGIN = 10

        for i in range(len(self.GameList)):
            game = self.GameList[i]
            
            with Image.open(f'resources/maps/{game.map}.png'.lower(), 'r') as map:              # Add Map
                width, height = map.size
                left = 0
                top = (height/2)-128
                right = width
                bottom = (height/2)+128

                cropped = map.crop((left, top, right, bottom)).convert("RGBA")          # Darken Map
                enhancer = ImageEnhance.Brightness(cropped)
                cropped = enhancer.enhance(0.7)
                img.paste(cropped, (MARGIN, i*256), cropped)

            base = Image.new('RGBA', (img.size[0],128), (0,0,0,0))                      # Add win/loss gradient
            if game.hasWon:
                colour = (0,255,0,150)
            else:
                colour = (255,0,0,150)
            top = Image.new('RGBA', (img.size[0],128), colour)
            mask = Image.new('L', base.size)
            mask_data = []
            for y in range(base.height):
                mask_data.extend([int(255 * (y / base.size[1]))] * base.size[0])
            mask.putdata(mask_data)
            base.paste(top, (0, 0), mask)

            img.paste(base, (MARGIN, i*256+128), base)
            
            with Image.open(f'resources/agents/{game.player.agent}.png', 'r') as agent:        # Add Agent
                img.paste(agent, (MARGIN, i*256), agent)
            
            with Image.open(f'resources/icons/{game.icon}.png', 'r') as icon:           # Add Icon
                if game.mode == 'Spike Rush':
                    basewidth = 240
                    wpercent = (basewidth/float(icon.size[0]))
                    hsize = int((float(icon.size[1])*float(wpercent)))
                    icon = icon.resize((basewidth,hsize), Image.ANTIALIAS)
                elif icon.size[0] != 256:
                    basewidth = 256
                    wpercent = (basewidth/float(icon.size[0]))
                    hsize = int((float(icon.size[1])*float(wpercent)))
                    icon = icon.resize((basewidth,hsize), Image.ANTIALIAS)

                img.paste(icon, (MARGIN + 256 + MARGIN+((256-icon.width)//2), i*256+((256-icon.height)//2)), icon.convert("RGBA"))

            draw = ImageDraw.Draw(img)

            # Score
            winSize = LargeFont.getsize(f"{game.roundWins}")
            colonSize = LargeFont.getsize(":")

            draw.text((600, i*256 + 128-100), f"{game.roundWins}",(127,255,183),font=LargeFont, stroke_width=1, stroke_fill=(0,0,0))
            draw.text((600+winSize[0]+10, i*256 + 128-100), ":",(200,200,200),font=LargeFont, stroke_width=1, stroke_fill=(0,0,0))
            draw.text((600+winSize[0]+colonSize[0]+20, i*256 + 128-100), f"{game.roundLoss}",(255,88,90),font=LargeFont, stroke_width=1, stroke_fill=(0,0,0))
            
            startPos = 650
            endPos = 800

            # Position
            if game.position == 1:
                colour = (196,183,113)
            elif game.position == 10:
                colour = (230, 67, 67)
            else:
                colour = (128,153,187)

            draw.rounded_rectangle((startPos, i*256+150, endPos, i*256+210), fill=colour, outline=(0,0,0), width=1, radius=25)

            posSize = miniFont.getsize(f"{game.position}")
            draw.text((startPos+(endPos-startPos-posSize[0])//2, i*256 + 150+(50-posSize[1])//2), f"{game.position}",(0,0,0),font=miniFont)

            # ACS
            headingSize = subtextFont.getsize("ACS")
            scoreSize = LargeFont.getsize(f"{game.player.score//(game.roundWins+game.roundLoss)}")

            draw.text((550+550-headingSize[0], i*256 + 43), "ACS",(200,200,200),font=subtextFont, stroke_width=1, stroke_fill=(0,0,0))
            draw.text((550+550-scoreSize[0], i*256 + 70+43), f"{game.player.score//(game.roundWins+game.roundLoss)}",(255,255,255),font=LargeFont, stroke_width=1, stroke_fill=(0,0,0))

            # KDA
            headingSize = subtextFont.getsize("K/D/A")
            kdaSize = LargeFont.getsize(f"{game.player.k}/{game.player.d}/{game.player.a}")

            draw.text((550+1050-headingSize[0], i*256 + 43), "K/D/A",(200,200,200),font=subtextFont, stroke_width=1, stroke_fill=(0,0,0))
            draw.text((550+1050-kdaSize[0], i*256 + 70+43), f"{game.player.k}/{game.player.d}/{game.player.a}",(255,255,255),font=LargeFont, stroke_width=1, stroke_fill=(0,0,0))

            # Date and Time
            dateSize = miniFont.getsize(game.gameStart.strftime('%b %d'))
            timeSize = miniFont.getsize(game.gameStart.strftime('%I:%M %p'))
            lengthSize = miniFont.getsize(f'{game.gameLength.seconds//60}m {game.gameLength.seconds%60}s')

            draw.text((img.width-dateSize[0]-20, i*256 + 20), game.gameStart.strftime('%b %d'),(255,255,255),font=miniFont, stroke_width=2, stroke_fill=(0,0,0))
            draw.text((img.width-timeSize[0]-20, i*256 + 30 + dateSize[1]), game.gameStart.strftime('%I:%M %p'),(255,255,255),font=miniFont, stroke_width=2, stroke_fill=(0,0,0))
            draw.text((img.width-lengthSize[0]-20, i*256 + 40 + dateSize[1] + timeSize[1]), f'{game.gameLength.seconds//60}m {game.gameLength.seconds%60}s',(255,255,255),font=miniFont, stroke_width=2, stroke_fill=(0,0,0))


        #img.show()

        with BytesIO() as image_binary:
            img.save(image_binary, 'PNG')
            image_binary.seek(0)
            file=discord.File(fp=image_binary, filename='image.png')

            embed = Embed(color=0xfa4454)
            embed.set_author(name=f"{self.name}\'s Career", url="https://www.youtube.com/watch?v=dQw4w9WgXcQ", icon_url=self.GameList[0].player.card)
            #embed.title=f"{self.name}\'s Career"
            #embed.description=mode.value
            embed.set_image(url="attachment://image.png")

            return embed, file
            

if __name__ == '__main__':
    career = Career('Dilka30003', '0000')   # Create object for player career
    if career.isValid:
        career.Graphic()
    else:
        print('invalid')