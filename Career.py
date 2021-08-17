import requests
import yaml
from PIL import Image, ImageFont, ImageDraw, ImageEnhance


class Game():
    def __init__(self, name:str, tag:str, gameData):
        self.name = name.lower()
        self.tag = tag.lower()

        self.__metadata(gameData['metadata'])
        self.__players(gameData['players'])

        self.roundWins = gameData['teams'][self.colour]['rounds_won']
        self.roundLoss = gameData['teams'][self.colour]['rounds_lost']
        self.hasWon = gameData['teams'][self.colour]['has_won']
        
    def __metadata(self, data):
        self.map = data['map']
        self.mode = data['mode']
        
    
    def __players(self, data):
        playerList = []
        isUser = False
        for player in data['red']:
            playerList.append(player)
            if player['name'].lower() == self.name and player['tag'].lower() == self.tag:
                isUser = True
                self.agent = player['character'].lower()
                self.score = player['stats']['score']
                self.k = player['stats']['kills']
                self.d = player['stats']['deaths']
                self.a = player['stats']['assists']
                if self.mode == 'Competitive':
                    self.icon = str(player['currenttier'])
                else:
                    self.icon = 'normal'
        if isUser:
            self.allies = playerList
            self.colour = 'red'
        else:
            self.enemies = playerList
            self.colour = 'blue'
        
        playerList = []
        for player in data['blue']:
            playerList.append(player)
            if player['name'].lower() == self.name and player['tag'].lower() == self.tag:
                self.agent = player['character'].lower()
                self.score = player['stats']['score']
                self.k = player['stats']['kills']
                self.d = player['stats']['deaths']
                self.a = player['stats']['assists']
                self.score = player['stats']['score']
                if self.mode == 'Competitive':
                    self.icon = str(player['currenttier'])
                else:
                    self.icon = 'normal'
        if isUser:
            self.enemies = playerList
        else:
            self.allies = playerList

        playerList = []
        for i in range(len(data['all_players'])):
            player = data['all_players'][i]
            playerList.append((player['name'].lower(), player['tag'].lower()))
            self.position = i+1


class Career():
    def __init__(self, name, tag):
        data = requests.get(f'https://api.henrikdev.xyz/valorant/v3/matches/ap/{name}/{tag}')
        # Do some error checking im too lazy to do
        games = data.json()['data']

        self.GameList = []
        for gameData in games:
            self.GameList.append(Game(name, tag, gameData))
    
    def Graphic(self):
        img = Image.new('RGBA', (1920, 1280), (255, 0, 0, 0))
        LargeFont = ImageFont.truetype("Roboto/Roboto-Medium.ttf", 100)
        subtextFont = ImageFont.truetype("Roboto/Roboto-Medium.ttf", 70)
        MARGIN = 10

        for i in range(len(self.GameList)):
            game = self.GameList[i]
            
            with Image.open(f'resources/maps/{game.map}.png', 'r') as map:              # Add Map
                width, height = map.size
                left = 0
                top = (height/2)-128
                right = width
                bottom = (height/2)+128

                cropped = map.crop((left, top, right, bottom)).convert("RGBA")
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
            
            with Image.open(f'resources/agents/{game.agent}.png', 'r') as agent:        # Add Agent
                img.paste(agent, (MARGIN, i*256), agent)
            
            with Image.open(f'resources/icons/{game.icon}.png', 'r') as icon:           # Add Icon
                if icon.size[0] != 256:
                    basewidth = 256
                    wpercent = (basewidth/float(icon.size[0]))
                    hsize = int((float(icon.size[1])*float(wpercent)))
                    icon = icon.resize((basewidth,hsize), Image.ANTIALIAS)

                img.paste(icon, (MARGIN + 256 + MARGIN, i*256), icon.convert("RGBA"))

            draw = ImageDraw.Draw(img)

            draw.text((550, i*256 + 128-100), f"{game.roundWins}",(127,255,183),font=LargeFont, stroke_width=1, stroke_fill=(0,0,0))
            draw.text((550, i*256 + 128), f"{game.roundLoss}",(255,88,90),font=LargeFont, stroke_width=1, stroke_fill=(0,0,0))

            headingSize = subtextFont.getsize("ACS")
            scoreSize = LargeFont.getsize(f"{game.score//(game.roundWins+game.roundLoss)}")

            draw.text((550+150 +scoreSize[0]-headingSize[0], i*256 + 43), "ACS",(200,200,200),font=subtextFont, stroke_width=1, stroke_fill=(0,0,0))
            draw.text((550+150, i*256 + 70+43), f"{game.score//(game.roundWins+game.roundLoss)}",(255,255,255),font=LargeFont, stroke_width=1, stroke_fill=(0,0,0))

            headingSize = subtextFont.getsize("K/D/A")
            kdaSize = LargeFont.getsize(f"{game.k}/{game.d}/{game.a}")

            draw.text((550+350 +kdaSize[0]-headingSize[0], i*256 + 43), "K/D/A",(200,200,200),font=subtextFont, stroke_width=1, stroke_fill=(0,0,0))
            draw.text((550+350, i*256 + 70+43), f"{game.k}/{game.d}/{game.a}",(255,255,255),font=LargeFont, stroke_width=1, stroke_fill=(0,0,0))

        img.show()
            

if __name__ == '__main__':
    career = Career('Dilka30003', '0000')
    career.Graphic()
    pass