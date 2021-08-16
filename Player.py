from PIL.Image import MODES
from requests import models
from PlayerStats import PlayerStats, CODES, MODE

class Player:
    def __init__(self, name, tag):
        self.name = name
        self.tag = tag
        self.Unrated = PlayerStats(name, tag, MODE.UNRATED)
        self.Competitive = PlayerStats(name, tag, MODE.COMPETITIVE)

        #self.Unrated.UpdateStats()
        #self.Competitive.UpdateStats()
    
    def __getitem__(self, key):
        if key == MODE.UNRATED:
            return self.Unrated
        elif key == MODE.COMPETITIVE:
            return self.Competitive
        else:
            raise ValueError("Value must be MODE item")

if __name__ == '__main__':
    player = Player("Dilka30003", "0000")
    z = player[MODE.UNRATED]