import requests
import yaml
from enum import Enum
from datetime import datetime
import matplotlib.pyplot as plt

class Player():
    class Status(Enum):
        ERROR = 0
        DUPLICATE = 1
        NOTFOUND = 2

        INVALID = 404
        NODATA = 204
        OK = 200

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


if __name__ == '__main__':
    me = Player('Dilka30003', '0000')
    me.games.pop(0)
    me.games.pop(0)
    me.update()
    