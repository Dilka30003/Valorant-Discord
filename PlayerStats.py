from abc import ABC
from enum import Enum
import enum

from os import name
from typing import Tuple
import requests
from bs4 import BeautifulSoup
import yaml
from PIL import Image, ImageFont, ImageDraw

class Statistics:
    def __init__(self):
        self.url = None
        self.avatar = None
        self.damage = Damage()
        self.game = Game()
        self.agents = [ Agent(), Agent(), Agent() ]
        self.accuracy = Accuracy()
        self.weapons = [ Weapon(), Weapon(), Weapon() ]
    
class Damage:
    dmg = None
    kda = None
    kd = None
    headshotRate = None
    kills = None
    Headshots = None
    deaths = None
    assists = None
    killsPerRound = None
    
class Game:
    winRate = None
    wins = None
    scorePerRound = None
    firstBlood = None
    ace = None
    clutch = None
    flawless = None
    mostKills = None
    playtime = None
    matches = None

class Agent:
    name = None
    image = None
    time = None
    matches = None
    winRate = None
    kd = None
    dmg = None

class Accuracy:
    headRate = None
    head = None
    bodyRate = None
    body = None
    legRate = None
    leg = None

class Weapon:
    name = None
    image = None
    type = None
    headRate = None
    bodyRate = None
    legRate = None
    kills = None

class PlayerStats(ABC):
    def __init__(self):
        self.url = None
        self.avatar = None
        self.damage = Damage()
        self.game = Game()
        self.agents = [ Agent(), Agent(), Agent() ]
        self.accuracy = Accuracy()
        self.weapons = [ Weapon(), Weapon(), Weapon() ]

    class codes(Enum):
        PRIVATE = "private"
        NOTFOUND = 404
    
    class type(Enum):
        UNRATED = 'unrated'
        COMPETITIVE = 'competitive'
        COMP = 'competitive'
    
    def UpdateStats(self, type = None):
        if type is None:
            type = self.type.UNRATED
        URL = 'https://tracker.gg/valorant/profile/riot/' + self.name + '%23' + self.tag + '/overview?playlist=' + type.value
        page = requests.get(URL)

        soup = BeautifulSoup(page.content, 'html.parser')

        results = soup.find(id='app')

        pageError = results.find_all('div', class_='content content--error')
        if (len(pageError) > 0):
            if self.codes.PRIVATE in pageError[0].text.lower():
                return self.codes.PRIVATE
            if self.codes.NOTFOUND in pageError[0].text.lower():
                return self.codes.NOTFOUND

        self.url = URL
        self.avatar = results.find('image', href=True).attrs['href']

        self.__getStats(results, type)

    def __getStats(self, results, type):
        self.damage.kda = float(results.find_all('span', class_='valorant-highlighted-stat__value')[-1].text) # Get KDA

        big_stats = results.find('div', class_='giant-stats')                                           # Get the 4 big stats from main page
        stats = []
        for stat in big_stats.find_all('div', class_='numbers'):
            stats.append(stat.find('span', class_='value').text)

        self.damage.dmg = float(stats[0])                                                             # Extract Stats from big 4
        self.damage.kd = float(stats[1])
        self.damage.headshotRate = float(stats[2][:-1])
        self.game.winRate = float(stats[3][:-1])

        main_stats = results.find('div', class_="main")                                                 # Get the main 12 stats
        stats = []
        for stat in main_stats.find_all('div', class_='numbers'):
            stats.append(stat.find('span', class_='value').text.replace(',', ''))

        self.game.wins = int(stats[0])                                                                # Extract stats from the main 12
        self.damage.kills = int(stats[1])
        self.damage.Headshots = int(stats[2])
        self.damage.deaths  = int(stats[3])
        self.damage.assists = int(stats[4])
        self.game.scorePerRound = float(stats[5])
        self.damage.killsPerRound = float(stats[6])
        self.game.firstBlood = int(stats[7])
        self.game.ace = int(stats[8])
        self.game.clutch = int(stats[9])
        self.game.flawless = int(stats[10])
        self.game.mostKills = int(stats[11])

        self.game.playtime = results.find('span', class_='playtime').text.strip()[:-10]
        self.game.matches = int(results.find('span', class_='matches').text.strip()[:-8])

    def __getAgents(self, type):
        pass

    def __getWeapons(self, type):
        pass

    def __getAccuracy(self, type):
        pass

    def AgentGraphic(self, type):
        pass

    def WeaponGraphic(self, type):
        pass

if __name__ == '__main__':
    class Test(PlayerStats):
        codes = PlayerStats.codes
        type = PlayerStats.type
        def __init__(self, name, tag):
            PlayerStats.__init__(self)
            self.name = name
            self.tag = tag
    
    test = Test('Dilka30003', '0000')
    test.UpdateStats(test.type.UNRATED)


