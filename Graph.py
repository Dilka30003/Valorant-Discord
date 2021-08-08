import requests
import yaml
import math
from enum import Enum
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
import matplotlib.ticker as plticker
from io import BytesIO
import discord
from PIL import Image

class PlayerGraph():
    class Status(Enum):
        ERROR = 0
        DUPLICATE = 1
        NOTFOUND = 2

        INVALID = 404
        NODATA = 204
        OK = 200

    ranks = {
           0: 'Iron 1',
         100: 'Iron 2',
         200: 'Iron 3',
         300: 'Bronze 1',
         400: 'Bronze 2',
         500: 'Bronze 3',
         600: 'Silver 1',
         700: 'Silver 2',
         800: 'Silver 3',
         900: 'Gold 1',
        1000: 'Gold 2',
        1100: 'Gold 3',
        1200: 'Platinum 1',
        1300: 'Platinum 2',
        1400: 'Platinum 3',
        1500: 'Diamond 1',
        1600: 'Diamond 2',
        1700: 'Diamond 3',
        1800: 'Immortal'
    }

    def __init__(self, name:str, tag:str):
        self.name = name
        self.tag = tag
        self.games = None

        self.__load()
    
    def __eq__(self, other):
        return str(self) == str(other)
    
    def __str__(self) -> str:
        return f"{self.name}#{self.tag}"
    
    def update(self):
        try:
            data = requests.get(f'https://api.henrikdev.xyz/valorant/v1/mmr-history/ap/{self.name}/{self.tag}')
        except:
            pass
        
        if data.status_code == self.Status.INVALID.value:
            return self.Status.INVALID
        elif data.status_code == self.Status.NODATA.value:
            response = self.Status.NODATA
            games = []
        elif data.status_code == self.Status.OK.value:
            response = self.Status.OK
            games = data.json()['data']

        try:
            position = games.index(self.games[0])
            subList = games[:position]
        except:
            subList = games
        
        self.games = subList + self.games
        self.__save()

        return response

    def __save(self):
        with open(f"storage/graphs/{str(self)}", 'w') as f:
            yaml.dump(self.games, f)

    def __load(self):
        try:
            with open(f"storage/graphs/{str(self)}", 'r') as f:
                data = yaml.load(f)
        except:
            with open(f"storage/graphs/{str(self)}", 'w+') as f:
                pass
            data = None
        if data == None:
            data = []
        self.games = data
        
    def draw(self):
        if len(self.games) == 0:
            return None
        # Turn interactive plotting off
        plt.ioff()
        plt.clf() 

        def rankDist(x, pos):
            if x in self.ranks:
                return self.ranks[x]
            return x

        x = []
        y = []
        for game in reversed(self.games):
            unix = game['date_raw']/1000        # Convert to seconds
            time = datetime.fromtimestamp(unix)
            date = time.strftime('%Y-%d %b')
            x.append(time)
            y.append(game['elo'])

        fig, ax = plt.subplots()
        ax.plot(x, y)
        myFmt = DateFormatter("%d %b %Y")
        ax.xaxis.set_major_formatter(myFmt)
        fig.autofmt_xdate()
        ax.yaxis.set_major_formatter(plt.FuncFormatter(rankDist))

        xTicks = ax.get_xticks()
        xTicks = range(int(xTicks[0]) - 1, int(xTicks[-1]) + 2, 1)
        ax.set_xticks(xTicks)
        n = (math.ceil(len(xTicks) / 6))  # Keeps ~ 6 labels
        [l.set_visible(False) for (i,l) in enumerate(ax.xaxis.get_ticklabels()) if i % n != 0]

        plt.yticks(range(int(math.floor(min(y) / 100.0)) * 100, int(math.ceil(max(y) / 100.0)) * 100 + 1, 25))
        plt.xlabel('Date')
        plt.ylabel('MMR')
        plt.title(f'{self.name}\'s MMR History')
        #plt.show()
        
        buf = BytesIO()
        plt.savefig(buf)
        buf.seek(0)
        #img = Image.open(buf)
        #img.show()

        file=discord.File(buf, 'graph.png')
        return file

if __name__ == '__main__':
    me = PlayerGraph('Dilka30003', '0000')
    me.update()
    z = me.draw()
    print("ajfnkd")