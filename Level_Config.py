from Level_Maps import *

import pygame
from Tiles import Tile
from player import Player


guns = []


class Level:
    def __init__(self, screen, image):
        self.clock = pygame.time.Clock()
        self.speed = 0
        self.gravity = 0.0
        self.jump_force = 0
        self.running = True
        self.level_map = []
        self.screen = screen
        self.bg = pygame.image.load(image)
        screen.blit(self.bg, (0, 0))

    def setup_level(self):
        self.tiles = pygame.sprite.Group()
        self.player_sprite = pygame.sprite.GroupSingle()

        for row_index, row in enumerate(self.level_map):
            for col_index, col in enumerate(row):
                x = col_index * tile_size
                y = row_index * tile_size
                if col == 'X':
                    tile = Tile((x, y), tile_size)
                    self.tiles.add(tile)
                elif col == 'P':
                    y -= tile_size
                    self.player = Player((x, y), self.gravity, self.speed, self.jump_force)
                    self.player_sprite.add(self.player)

    def quit(self):
        self.running = False

    def update(self):
        self.player.update(self.tiles)
        #nice cock

    def render(self, screen):
        screen.blit(self.bg, (0, 0))
        self.player_sprite.draw(screen)
        self.player.i_hate_gravity()
        self.tiles.draw(screen)

        font = pygame.font.Font(None, 25)
        text = font.render(f"FPS: {round(self.clock.get_fps())}", True, (100, 255, 100))
        pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(0, 0, 85, 20))
        screen.blit(text, (0, 0))


class FirstLevel(Level):
    def __init__(self, screen):
        Level.__init__(self, screen, 'BackGrounds/NeonTokyoBackground.jpg')
        self.speed = 2
        self.gravity = 0.1
        self.jump_force = -3.5
        self.screen = screen
        self.level_map = first_level
        self.setup_level()

