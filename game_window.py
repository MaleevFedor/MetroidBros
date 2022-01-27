import const
import pygame


class GameWindow:
    def __init__(self, active_level):
        self.active_level = active_level

    def update(self):
        self.active_level.update()

    def render(self, screen):
        self.active_level.render(screen)

