import requests
import const
import const
import Rating

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
        self.tokyo = 0
        self.plains = 0
        self.industrial = 0
        self.apocalypse = 0
        self.forest = 0


    def post(self):
        if self.player.id == 0:
            const.match_kills += self.kills
            const.match_deaths += self.deaths
            const.match_hp_healed += self.hp_healed
            const.match_saws_deaths += self.saws_deaths
            const.match_shot += self.shots
            const.match_hits += self.hits
            req = requests.post(const.STATISTIC_CHECK_ADRESS,
                                json={'user': const.player1_name, 'kills': self.kills, 'deaths': self.deaths,
                                      'wins': self.wins, 'hp': self.hp_healed, 'loses': self.loses, 'shots': self.shots,
                                      'hits': self.hits, 'saws_deaths': self.saws_deaths, 'tokyo': self.tokyo,
                                      'forest': self.forest, 'plains': self.plains,
                                      'industrial': self.industrial, 'apocalypse': self.apocalypse})
        else:
            const.match_kills_2 += self.kills
            const.match_deaths_2 += self.deaths
            const.match_hp_healed_2 += self.hp_healed
            const.match_saws_deaths_2 += self.saws_deaths
            const.match_shot_2 += self.shots
            const.match_hits_2 += self.hits
            req = requests.post(const.STATISTIC_CHECK_ADRESS,
                                json={'user': const.player2_name, 'kills': self.kills, 'deaths': self.deaths,
                                      'wins': self.wins, 'hp': self.hp_healed, 'loses': self.loses, 'shots': self.shots,
                                      'hits': self.hits, 'saws_deaths': self.saws_deaths,
                                      'tokyo': self.tokyo, 'forest': self.forest, 'plains': self.plains,
                                      'industrial': self.industrial, 'apocalypse': self.apocalypse})

    def match_post(self):
        rank_1 = Rating.check_rating(int(requests.post(const.ELO_CHECK_ADRESS, json={'name': const.player1_name}).text))
        rank_2 = Rating.check_rating(int(requests.post(const.ELO_CHECK_ADRESS, json={'name': const.player2_name}).text))
        key_list = list(Rating.ranked_emblems.keys())
        difference = key_list.index(rank_2) - key_list.index(rank_1)
        if self.player.id == 0:
            if const.match_result.count('V') == 3:
                self.elo = 30 - 2 * difference
                if 'VVV' in const.match_result:
                    self.elo *= 1.5
            else:
                self.elo = -30 + 2 * difference
                if 'LLL' in const.match_result:
                    self.elo *= 1.5
            if const.match_hits_2 == 0:
                const.perfect = True

            req = requests.post(const.STATISTIC_MATCH_ADRESS,
                                json={'player_name': const.player1_name, 'kills': const.match_kills, 'deaths': const.match_deaths,
                                      'hp':   const.match_hp_healed, 'shots': const.match_shot,
                                      'hits':  const.match_hits, 'saws_deaths': const.match_saws_deaths,
                                      'result': const.match_result, 'enemy_name': const.player2_name, 'elo': self.elo,
                                      'perfect': const.perfect})

        else:
            if const.match_result_2.count('V') == 3:
                self.elo = 30 - 2 * difference
                if 'VVV' in const.match_result_2:
                    self.elo *= 1.5
            else:
                self.elo = -30 + 2 * difference
                if 'LLL' in const.match_result_2:
                    self.elo *= 1.5
            if const.match_hits == 0:
                const.perfect_2 = True

            req = requests.post(const.STATISTIC_MATCH_ADRESS,
                                json={'player_name': const.player2_name, 'kills': const.match_kills_2, 'deaths': const.match_deaths_2,
                                      'hp': const.match_hp_healed_2, 'shots': const.match_shot_2,
                                      'hits':  const.match_hits_2, 'saws_deaths':  const.match_saws_deaths_2,
                                      'result': const.match_result_2, 'enemy_name': const.player1_name, 'elo': self.elo,
                                      'perfect': const.perfect_2})
            const.match_kills = 0
            const.match_deaths = 0
            const.match_hp_healed = 0
            const.match_saws_deaths = 0
            const.match_shot = 0
            const.match_hits = 0
            const.match_result = ''
            const.match_kills_2 = 0
            const.match_deaths_2 = 0
            const.match_hp_healed_2 = 0
            const.match_saws_deaths_2 = 0
            const.match_shot_2 = 0
            const.match_hits_2 = 0
            const.match_result_2 = ''






