import requests
import yaml
from enum import Enum

class Player():
    def __init__(self, name:str, tag:str, elo:int = None):
        self.name = name
        self.tag = tag
        self.elo = elo
    
    def __eq__(self, other):
        return str(self) == str(other)
    
    def __str__(self) -> str:
        return f"{self.name}#{self.tag}"

class Leaderboard():
    class Status(Enum):
        ERROR = 0
        DUPLICATE = 1
        NOTFOUND = 2

        INVALID = 404
        NODATA = 204
        OK = 200

    def __init__(self, SERVER_ID):
        self.SERVER_ID = str(SERVER_ID)
        self.player_list = self.__load(self.SERVER_ID)

    def __save(self, players, filename):
        dict = {}

        for player in players:
            dict[str(player)] = [player.name, player.tag, player.elo]
        with open(f"storage/leaderboard/{filename}", 'w') as f:
            yaml.dump(dict, f)

    def __load(self, filename):
        lst = []
        try:
            with open(f"storage/leaderboard/{filename}", 'r') as f:
                data = yaml.load(f)
            for key in data:
                player = data[key]
                lst.append(Player(player[0], player[1], player[2]))
        except: pass
        return lst

    def add(self, player:Player):
        if player in self.player_list:
            return self.Status.DUPLICATE
        try:
            data = requests.get(f'https://api.henrikdev.xyz/valorant/v1/mmr/ap/{player.name}/{player.tag}')
        except:
            return self.Status.ERROR
        
        response = None

        if data.status_code == self.Status.INVALID.value:
            return self.Status.INVALID
        elif data.status_code == self.Status.NODATA.value:
            response = self.Status.NODATA
        elif data.status_code == self.Status.OK.value:
            response = self.Status.OK
            player.elo = data.json()['data']['elo']

        self.player_list.append(player)
        self.__save(self.player_list, self.SERVER_ID)

        return response
    
    def update(self):
        for player in self.player_list:
            try:
                data = requests.get(f'https://api.henrikdev.xyz/valorant/v1/mmr/ap/{player.name}/{player.tag}')
            except:
                pass

            if data.status_code == self.Status.OK.value:
                response = self.Status.OK
                player.elo = data.json()['data']['elo']

        
    def remove(self, player:Player):
        if player in self.player_list:
            self.player_list.remove(player)
            self.__save(self.player_list, self.SERVER_ID)
            return self.Status.OK
        return self.Status.NOTFOUND
        
        
    

if __name__ == '__main__':
    leaderboard = Leaderboard('test')

    faaez = Player('fakinator', '4269')
    me = Player('dilka30003', '0000')

    print(leaderboard.remove(faaez))

    print(leaderboard.add(faaez))
    print(leaderboard.add(me))

    leaderboard.update()