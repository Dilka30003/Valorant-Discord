from abc import ABC
from enum import Enum
import enum

from os import name
from typing import Tuple
import requests
from bs4 import BeautifulSoup
import yaml
from PIL import Image, ImageFont, ImageDraw

class Stats:
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

    def __getStats(self, type):
        pass

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


