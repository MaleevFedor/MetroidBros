import const
import pygame
from random import randint
from Level_Config import TokyoLevel, ForestLevel, IndustrialLevel, ApocalypsisLevel, PlainLevel


class GameWindow:
    def __init__(self, active_level):
        self.active_level = active_level

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
            return GameWindow(ForestLevel(screen))
        elif chosen_level == 'Tokyo':
            return GameWindow(TokyoLevel(screen))
        elif chosen_level == 'Industrial':
            return GameWindow(IndustrialLevel(screen))
        elif chosen_level == 'Apocalypsis':
            return GameWindow(ApocalypsisLevel(screen))
        elif chosen_level == 'Plain':
            return GameWindow(PlainLevel(screen))


