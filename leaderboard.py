import requests
import yaml
from enum import Enum
from datetime import datetime

class Player():
    def __init__(self, name:str, tag:str, elo:int = None):
        self.name = name
        self.tag = tag
        self.elo = elo
    
    def __eq__(self, other):
        return str(self) == str(other)
    
    def __str__(self) -> str:
        return f"{self.name}#{self.tag}"

class Leaderboards():
    def __init__(self):
        self.leaderboards = []

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
        self.last_updated = datetime.now()

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

    def remove(self, player:Player):
        if player in self.player_list:
            self.player_list.remove(player)
            self.__save(self.player_list, self.SERVER_ID)
            return self.Status.OK
        return self.Status.NOTFOUND
    
    def update(self):
        for player in self.player_list:
            try:
                data = requests.get(f'https://api.henrikdev.xyz/valorant/v1/mmr/ap/{player.name}/{player.tag}')
            except:
                pass

            if data.status_code == self.Status.OK.value:
                response = self.Status.OK
                player.elo = data.json()['data']['elo']
        self.last_updated = datetime.now()
    
    def generate(self):
        # Remove anyone who doesn't have an elo
        excluded_players = []
        for i in range(len(self.player_list)):
            player = self.player_list[i]
            if player.elo is None:
                excluded_players.append(self.player_list.pop(i))

        self.player_list.sort(key = lambda x: x.elo, reverse=True)
        
        maxLen = max([len(str(x)) for x in self.player_list])
        timeDifference = datetime.now() - self.last_updated

        timeText = f"{timeDifference.seconds//60} Minute{'s' if timeDifference.seconds//60 != 1 else ''}" if timeDifference.seconds > 60 else f"{timeDifference.seconds} Second{'s' if timeDifference.seconds != 1 else ''}"

        message = f"```\nPlayer Leaderboard (Last Updated {timeText} Ago)\n"
        for i in range(len(self.player_list)):
            player = self.player_list[i]
            message += '{message:{fill}{align}{width}}'.format(
                        message=str(i+1) + '. ',
                        fill=' ',
                        align='<',
                        width=(len(self.player_list) // 10),
                        )
            message += '{message:{fill}{align}{width}}'.format(
                        message=str(player),
                        fill=' ',
                        align='<',
                        width=maxLen,
                        )
            message += str(player.elo) + '\n'
        message += "```"
        return message        
    

if __name__ == '__main__':
    leaderboard = Leaderboard('test')

    leaderboard.add(Player('fakinator', '4269'))
    leaderboard.add(Player('dilka30003', '0000'))
    leaderboard.add(Player('8888', 'nadi'))

    leaderboard.update()
    print(leaderboard.generate())
    print(leaderboard.generate())