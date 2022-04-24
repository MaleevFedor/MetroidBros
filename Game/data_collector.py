import requests
import const
import const


class DataCollector:
    def __init__(self, player):
        self.player = player
        self.shots = 0
        self.hits = 0
        self.kills = 0
        self.deaths = 0
        self.wins = 0
        self.loses = 0
        self.hp_healed = 0
        self.saws_deaths = 0



    def post(self):
        const.match_kills += self.kills
        const.match_deaths += self.deaths
        const.match_hp_healed += self.hp_healed
        const.match_saws_deaths += self.saws_deaths
        const.match_shot += self.shots
        const.match_hits += self.hits
        if self.player.id == 0:
            req = requests.post(const.STATISTIC_CHECK_ADRESS,
                                json={'user': const.player1_name, 'kills': self.kills, 'deaths': self.deaths,
                                      'wins': self.wins, 'hp': self.hp_healed, 'loses': self.loses, 'shots': self.shots,
                                      'hits': self.hits, 'saws_deaths': self.saws_deaths})
        else:
            req = requests.post(const.STATISTIC_CHECK_ADRESS,
                                json={'user': const.player2_name, 'kills': self.kills, 'deaths': self.deaths,
                                      'wins': self.wins, 'hp': self.hp_healed, 'loses': self.loses, 'shots': self.shots,
                                      'hits': self.hits, 'saws_deaths': self.saws_deaths})

    def match_post(self):
        if self.player.id == 0:
            req = requests.post(const.STATISTIC_MATCH_ADRESS,
                                json={'player_name': const.player1_name, 'kills': const.match_kills, 'deaths': const.match_deaths,
                                      'hp':   const.match_hp_healed, 'shots': const.match_shot,
                                      'hits':  const.match_hits, 'saws_deaths': const.match_saws_deaths})
        else:
            req = requests.post(const.STATISTIC_MATCH_ADRESS,
                                json={'player_name': const.player2_name, 'kills': const.match_kills, 'deaths': const.match_deaths,
                                      'hp': const.match_hp_healed, 'shots': const.match_shot,
                                      'hits':  const.match_hits, 'saws_deaths':  const.match_saws_deaths})



