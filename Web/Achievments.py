def check_Phoenix(user):
    return user.comeback


def check_Marksman(user):
    return user.marksman


def check_Medic(user):
    return user.heal_500


def check_Flawless(user):
    return user.perfect


def check_Popular(user):
    return user.views >= 100


def check_Hero_of_Industrial(user):
    return user.industrial_wins >= 25


def check_Tokyo_Ghoul(user):
    return user.tokyo_wins >= 25


def check_Robin_Hood(user):
    return user.forest_wins >= 25


def check_Survivalist(user):
    return user.apocalypse_wins >= 25


def check_Plains_hero(user):
    return user.plains_wins >= 25


def check_Not_your_day(user):
    return user.bullseye


def check_Legion(user):
    return user.win_100
