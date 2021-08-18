from abc import ABC
from enum import Enum
import enum

from os import name
from typing import Tuple, Type
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

class CODES(Enum):
        PRIVATE = "private"
        NOTFOUND = 404
        OK = 0
    
class MODE(Enum):
    UNRATED = 'unrated'
    COMPETITIVE = 'competitive'
    COMP = 'competitive'

class PlayerStats():
    def __init__(self, name, tag, mode):
        self.name = name
        self.tag = tag
        self.mode = mode

        self.url = None
        self.avatar = None
        self.damage = Damage()
        self.game = Game()
        self.agents = [ Agent(), Agent(), Agent() ]
        self.accuracy = Accuracy()
        self.weapons = [ Weapon(), Weapon(), Weapon() ]

    
    
    def UpdateStats(self):
        URL = 'https://tracker.gg/valorant/profile/riot/' + self.name + '%23' + self.tag + '/overview?playlist=' + self.mode.value
        #page = requests.get(URL)

        #with open("page.html", "wb") as f:
        #    f.write(page.content)

        soup = BeautifulSoup(page.content, 'html.parser')

        results = soup.find(id='app')

        if page.text == '':
            return CODES.NOTFOUND
        pageError = results.find_all('div', class_='content content--error')
        if (len(pageError) > 0):
            if CODES.PRIVATE in pageError[0].text.lower():
                return CODES.PRIVATE
            if CODES.NOTFOUND in pageError[0].text.lower():
                return CODES.NOTFOUND

        self.url = URL
        self.avatar = results.find('image', href=True).attrs['href']

        try:
            self.__getStats(results)
        except: pass
        try:
            self.__getAgents(results)
        except: pass
        try:
            self.__getWeapons(results)
        except: pass
        try:
            self.__getAccuracy(results)
        except: pass

        return CODES.OK

    def __getStats(self, results):
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

    def __getAgents(self, results):
        agent_stats = results.find('div', class_='top-agents__table-container')                         # Get table of top 3 agents
        rows = agent_stats.next.find_all('tr')
        rows.pop(0)                                                                                     # Remove top label row
        for i in range(len(rows)):
            row = rows[i]
            self.agents[i].name = row.find('span', class_='agent__name').text
            self.agents[i].image = Image.open(requests.get(row.find('img').get('src'), stream=True).raw)
            data = row.find_all('span', class_='name')
            self.agents[i].time = data[0].text
            self.agents[i].matches = int(data[1].text)
            self.agents[i].winRate = float(data[2].text[:-1])
            self.agents[i].kd = float(data[3].text)
            self.agents[i].dmg = float(data[4].text)
        
    def __getWeapons(self, results):
        weapon_stats = results.find('div', class_='top-weapons__weapons')
        weapons = results.find_all('div', class_='weapon')
        for i in range(len(weapons)):
            weapon = weapons[i]
            self.weapons[i].name = weapon.find('div', class_='weapon__name').text
            self.weapons[i].image = Image.open(requests.get(weapon.find('img').get('src'), stream=True).raw)
            self.weapons[i].type = weapon.find('div', class_='weapon__type').text
            stats = weapon.find_all('span', class_='stat')
            self.weapons[i].headRate = int(stats[0].text[:-1])
            self.weapons[i].bodyRate = int(stats[1].text[:-1])
            self.weapons[i].legRate = int(stats[2].text[:-1])
            self.weapons[i].kills = int(weapon.find('span', class_='value').text.replace(',', ''))

    def __getAccuracy(self, results):
        try:
            accuracy_stats = results.find('div', class_='accuracy__content')                                # Get table of accuracy stats
            rows = accuracy_stats.find_all('tr')
            stats = []
            for row in rows:
                data = row.find_all('span', 'stat__value')
                stats.append(data)

            self.accuracy.headRate = float(stats[0][0].text[:-1])
            self.accuracy.head = int(stats[0][1].text)
            self.accuracy.bodyRate = float(stats[1][0].text[:-1])
            self.accuracy.body = int(stats[1][1].text)
            self.accuracy.legRate = float(stats[2][0].text[:-1])
            self.accuracy.leg = int(stats[2][1].text)
        except:
            self.accuracy.headRate = -1
            self.accuracy.head = -1
            self.accuracy.bodyRate = -1
            self.accuracy.body = -1
            self.accuracy.legRate = -1
            self.accuracy.leg = -1

    def AgentGraphic(self):
        img = Image.new('RGBA', (1920, 1200), (255, 0, 0, 0))
        timeFont = ImageFont.truetype("Roboto/Roboto-Medium.ttf", 100)
        subtextFont = ImageFont.truetype("Roboto/Roboto-Medium.ttf", 70)
        MARGIN = 10

        for i in range(len(self.agents)):
            agent = self.agents[i]
            img.paste(agent.image, (MARGIN, i*(156+256)), agent.image)
            draw = ImageDraw.Draw(img)
            draw.text((MARGIN, i*(156+agent.image.width) + agent.image.height),agent.time,(200,200,200),font=timeFont)
            draw.text((MARGIN + agent.image.width + 10, i*(156+agent.image.height) + 36),str(agent.matches) + " Matches",(255,255,255),font=timeFont)
            draw.text((MARGIN + agent.image.width + 10, i*(156+agent.image.height) + 154),str(agent.winRate) + "% Win Rate",(255,255,255),font=timeFont)
            draw.text((MARGIN + agent.image.width + 10 + 800, i*(156+agent.image.height) + 36),str(agent.kd) + " K/D",(255,255,255),font=timeFont)
            draw.text((MARGIN + agent.image.width + 10 + 800, i*(156+agent.image.height) + 154),str(agent.dmg) + " Dmg/Round",(255,255,255),font=timeFont)
            
        return img

    def WeaponGraphic(self):
        img = Image.new('RGBA', (1000, 1200), (255, 0, 0, 0))
        nameFont = ImageFont.truetype("Roboto/Roboto-Medium.ttf", 100)
        typeFont = ImageFont.truetype("Roboto/Roboto-Medium.ttf", 60)
        headerFont = ImageFont.truetype("Roboto/Roboto-Medium.ttf", 60)
        MARGIN = 10

        weaponHeight = self.weapons[0].image.height + self.weapons[1].image.height + self.weapons[2].image.height
        spacing = (img.height - weaponHeight)/2 - 90
        positions = []
        positions.append(0)
        positions.append(self.weapons[0].image.height + spacing)
        positions.append(positions[1] + self.weapons[1].image.height + spacing)

        for i in range(len(self.weapons)):
            weapon = self.weapons[i]
            img.paste(weapon.image, (MARGIN, int(positions[i])), weapon.image)
            draw = ImageDraw.Draw(img)
            draw.text((MARGIN+50, positions[i] + weapon.image.height + 10), weapon.name,(200,200,200),font=nameFont)
            draw.text((MARGIN+50, positions[i] + weapon.image.height + 100 + 20), weapon.type,(200,200,200),font=typeFont)
            draw.text((MARGIN+weapon.image.width + 30, positions[i]), "Headshot: " + str(weapon.headRate) + "%",(255,255,255),font=headerFont)
            draw.text((MARGIN+weapon.image.width + 30, positions[i] + 70), "Bodyshot: " + str(weapon.bodyRate) + "%",(255,255,255),font=headerFont)
            draw.text((MARGIN+weapon.image.width + 30, positions[i] + 70*2), "Legshot: " + str(weapon.legRate) + "%",(255,255,255),font=headerFont)
            draw.text((MARGIN+weapon.image.width + 30, positions[i] + 70*3), "Kills: " + str(weapon.kills),(255,255,255),font=headerFont)

        return img

if __name__ == '__main__':
    class Test(PlayerStats):
        def __init__(self, name, tag):
            self.name = name
            self.tag = tag
            self.Unrated = PlayerStats(name, tag, MODE.UNRATED)
    
    test = Test('Dilka30003', '0000')
    x = test.Unrated.UpdateStats()
    
    test.Unrated.WeaponGraphic().show()

