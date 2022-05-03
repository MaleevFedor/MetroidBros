from Rating import check_rating
elo_to_points = {'Master': 5,
                  'Red Raptor': 4,
                  'Green Raptor': 3,
                  'Grey Raptor': 2,
                  'Brown Raptor': 1}


def generate(winrate, elo, kd, accuracy, healed, saws):
    print(winrate, elo, kd, accuracy, healed, saws)
    points = 0
    if winrate >= 75:
        points += 3
    elif winrate >= 50:
        points += 2
    elif winrate >= 25:
        points += 1
    points += elo_to_points[check_rating(elo)]
    if kd > 50:
        points += 2
    else:
        points += 1
    if accuracy >= 75:
        points += 3
    elif accuracy >= 50:
        points += 2
    elif accuracy >= 25:
        points += 1
    if healed >= 2000:
        points += 4
    elif healed >= 1000:
        points += 2
    elif healed >= 200:
        points += 1
    if saws == 0:
        points += 3
    elif 5 >= saws >= 1:
        points += 1
    elif saws > 5:
        points += 0
    if points >= 13:
        return 'Excellent'
    elif 12 >= points >= 10:
        return 'Good'
    elif 9 >= points >= 6:
        return 'Poor'
    else:
        return 'Awful'
