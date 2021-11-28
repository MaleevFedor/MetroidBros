from Level_Maps import *

import pygame
from Tiles import Tile
from player import Player


guns = []


class Level:
    def __init__(self, screen):
        self.clock = pygame.time.Clock()
        self.speed = 0
        self.gravity = 0.0
        self.jump_force = 0
        self.running = True
        self.level_map = []
        self.screen = screen
        self.image_path = ''

    def setup_level(self):
        self.tiles = pygame.sprite.Group()
        self.player = pygame.sprite.GroupSingle()

        for row_index, row in enumerate(self.level_map):
            for col_index, col in enumerate(row):
                x = col_index * tile_size
                y = row_index * tile_size
                if col == 'X':
                    tile = Tile((x, y), tile_size)
                    self.tiles.add(tile)
                elif col == 'P':
                    y -= tile_size
                    self.player.add(Player((x, y), self.gravity, self.speed, self.jump_force))
                    self.horizontal()

    def quit(self):
        self.running = False

    def horizontal(self):
        player = self.player.sprite
        player.rect.x += player.direction.x * player.speed

        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.direction.x < 0:
                    player.rect.left = sprite.rect.right
                elif player.direction.x > 0:
                    player.rect.right = sprite.rect.left

    def vertical(self):
        player = self.player.sprite
        player.i_hate_gravity()

        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.direction.y > 0:
                    player.extra_jumps = 2
                    player.rect.bottom = sprite.rect.top
                    player.direction.y = 0
                elif player.direction.y < 0:
                    player.rect.top = sprite.rect.bottom

    def render(self, screen):
        bg = pygame.image.load(self.image_path)
        screen.blit(bg, (0, 0))
        self.player.update()
        self.player.draw(screen)
        self.horizontal()
        self.vertical()
        self.player.sprite.i_hate_gravity()
        self.tiles.draw(screen)
        self.clock.tick()

        font = pygame.font.Font(None, 25)
        text = font.render(f"FPS: {round(self.clock.get_fps())}", True, (100, 255, 100))
        pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(0, 0, 85, 20))
        screen.blit(text, (0, 0))


class FirstLevel(Level):
    def __init__(self, screen):
        Level.__init__(self, screen)
        self.speed = 2
        self.gravity = 0.1
        self.jump_force = -3.5
        self.screen = screen
        self.level_map = first_level
        self.setup_level()
        self.image_path = 'BackGrounds/NeonTokyoBackground.jpg'
        bg = pygame.image.load(self.image_path)
        screen.blit(bg, (0, 0))
