import requests
import const


class DataCollector:
    def __init__(self, player):
        self.player = player
        self.kills = 0
        self.deaths = 0
        self.wins = 0
        self.hp_healed = 0

    def post(self):
        if self.player.id == 0:
            req = requests.post(const.STATISTIC_CHECK_ADRESS,
                                json={'user': const.player1_name, 'kills': self.kills, 'deaths': self.deaths,
                                      'wins': self.wins, 'hp': self.hp_healed})
        else:
            req = requests.post(const.STATISTIC_CHECK_ADRESS,
                                json={'user': const.player2_name, 'kills': self.kills, 'deaths': self.deaths,
                                      'wins': self.wins, 'hp': self.hp_healed})



