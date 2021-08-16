import requests
import yaml

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
        if isUser:
            self.allies = playerList
            self.colour = 'red'
        else:
            self.enemies = playerList
            self.colour = 'blue'
        
        playerList = []
        for player in data['blue']:
            playerList.append(player)
        if isUser:
            self.enemies = playerList
        else:
            self.allies = playerList

class Career():
    def __init__(self, name, tag):
        data = requests.get(f'https://api.henrikdev.xyz/valorant/v3/matches/ap/{name}/{tag}')
        # Do some error checking im too lazy to do
        games = data.json()['data']

        self.GameList = []
        for gameData in games:
            self.GameList.append(Game(name, tag, gameData))
            

if __name__ == '__main__':
    career = Career('Dilka30003', '0000')
    pass