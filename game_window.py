import const
from random import randint
from Level_Config import TokyoLevel, ForestLevel, IndustrialLevel, ApocalypsisLevel, PlainLevel


class GameWindow:
    def __init__(self):
        self.active_level = None

    def update(self):
        self.active_level.update()

    def render(self, screen):
        self.active_level.render(screen)

    def load_level(self, screen):
        if len(const.level_list) == 0:
            const.level_list.append('Forest')
            const.level_list.append('Tokyo')
            const.level_list.append('Industrial')
            const.level_list.append('Apocalypsis')
            const.level_list.append('Plain')
        index = randint(0, len(const.level_list) - 1)
        chosen_level = const.level_list[index]
        const.level_list.pop(index)
        if chosen_level == 'Forest':
            self.active_level = ForestLevel(screen)
        elif chosen_level == 'Tokyo':
            self.active_level = TokyoLevel(screen)
        elif chosen_level == 'Industrial':
            self.active_level = IndustrialLevel(screen)
        elif chosen_level == 'Apocalypsis':
            self.active_level = ApocalypsisLevel(screen)
        elif chosen_level == 'Plain':
            self.active_level = PlainLevel(screen)
