import requests
import const


class DataCollector:
    def __init__(self, player):
        self.player = player
        self.kills = 0

    def post(self):
        if self.player.id == 0:
            req = requests.post(const.STATISTIC_CHECK_ADRESS,
                                json={'user': const.player1_name, 'kills': self.kills})
        else:
            req = requests.post(const.STATISTIC_CHECK_ADRESS,
                                json={'user': const.player2_name, 'kills': self.kills})



