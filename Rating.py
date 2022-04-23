ranked_emblems = {'Apex Predator': 'Apex_Predator.png',
                  'Master': 'Master.png',
                  'Red Raptor': 'Red_Raptor.png',
                  'Green Raptor': 'Green_Raptor.png',
                  'Grey Raptor': 'Grey_Raptor.png',
                  'Brown Raptor': 'Brown_Raptor.png',
                  'banned': ''}


number_of_predators = 4


def check_rating(elo, i=1000000):
    if elo >= 1000 and i <= number_of_predators:
        return 'Apex Predator'
    elif elo >= 1000:
        return 'Master'
    elif 1000 > elo >= 800:
        return 'Red Raptor'
    elif 800 > elo >= 600:
        return 'Green Raptor'
    elif 600 > elo >= 400:
        return 'Grey Raptor'
    elif 400 > elo:
        return 'Brown Raptor'
    else:
        return 'Unranked'