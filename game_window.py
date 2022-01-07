import const
import pygame


class GameWindow:
    def __init__(self, active_level):
        self.active_level = active_level

    def execute_controls(self, joysticks):
        self.active_level.execute_controls(joysticks)

    def update(self):
        self.active_level.update()

    def render(self, screen):
        self.active_level.render(screen)

    def on_key_escape(self):
        self.active_level.on_key_escape()

    def process_custom_event(self, event):
        if event == const.OPTIONS_LOAD:
            self.active_level = Options()



class Options:
    def __init__(self):
        self.bg_color = (255, 0, 0)
        self.playable = False
        self.clock = pygame.time.Clock()

    def update(self):
        pass

    def render(self, screen):
        screen.fill(self.bg_color)

