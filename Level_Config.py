from Level_Maps import *

import pygame
from Tiles import Tile
from network import Network, FakeNetwork
from player import Player, Player2

guns = {'usp': (200, 10, 1, 0.03, 'GunsAssets/Usp-s.png', 10, 400),
        'pistol': (200, 10, 1, 0.5, 'GunsAssets/Pistol.png', 10, 200),
        'shotgun': (60, 10, 6, 0.2, 'GunsAssets/Pump Shotgun.png', 4, 800),
        'AWP': (250, 30, 1, 0, 'GunsAssets/Awp.png', 6, 1250)}


class Level:
    def __init__(self, screen, image):
        self.net = FakeNetwork()
        self.i_am_player = self.net.player_id
        self.clock = pygame.time.Clock()
        self.screen = screen
        self.speed = 0
        self.gravity = 0.0
        self.jump_force = 0
        self.running = True
        self.level_map = []
        self.screen = screen
        self.bg = pygame.image.load(image)
        self.gun = guns['shotgun']
        self.MANUAL_CURSOR = pygame.image.load('Crosshairs/Green.png').convert_alpha()
        screen.blit(self.bg, (0, 0))

    def setup_level(self):
        self.tiles = pygame.sprite.Group()
        self.bullet_sprites = pygame.sprite.Group()
        self.player_sprite = pygame.sprite.GroupSingle()
        self.player2_sprite = pygame.sprite.GroupSingle()
        self.tiles.add(Tile((-1, 0), 1, 720))
        self.tiles.add(Tile((1281, 0), 1, 720))

        for row_index, row in enumerate(self.level_map):
            for col_index, col in enumerate(row):
                x = col_index * tile_size
                y = row_index * tile_size
                if col == 'X':
                    tile = Tile((x, y), tile_size, tile_size)
                    self.tiles.add(tile)
                elif col == '1':
                    if self.i_am_player == 0:
                        y -= tile_size
                        self.player = Player((x, y), self.gravity, self.speed, self.jump_force, self.screen, self.gun[4])
                        self.player_sprite.add(self.player)
                    else:
                        self.player2 = Player2((x, y - 30))
                        self.player2_sprite.add(self.player2)

                elif col == '2':
                    if self.i_am_player == 0:
                        self.player2 = Player2((x, y - 30))
                        self.player2_sprite.add(self.player2)
                    else:
                        y -= tile_size
                        self.player = Player((x, y), self.gravity, self.speed, self.jump_force, self.screen, self.gun[4])
                        self.player_sprite.add(self.player)

    def quit(self):
        self.running = False

    def update(self):
        self.player.update(self.tiles)
        self.player2.rect.topleft = self.net.exchange_player_info(self.player)

    def render(self, screen):
        screen.blit(self.bg, (0, 0))
        for bullet in self.bullet_sprites:
            if bullet.lifetime <= 0:
                bullet.kill()
            hits = pygame.sprite.groupcollide(self.tiles, self.bullet_sprites, False, True)
            bullet.update(screen)
        self.tiles.draw(screen)
        self.bullet_sprites.draw(screen)
        self.player.basic_health()
        font = pygame.font.Font(None, 25)
        text = font.render(f"FPS: {round(self.clock.get_fps())}", True, (100, 255, 100))
        pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(0, 0, 85, 20))
        screen.blit(text, (0, 0))
        self.player2.rect.x, self.player2.y = self.net.player_positions
        self.player_sprite.draw(screen)
        self.player.weapon_handling()
        self.player.i_hate_gravity()
        self.player2_sprite.draw(screen)
        x, y = pygame.mouse.get_pos()
        x -= 15
        y -= 15
        screen.blit(self.MANUAL_CURSOR, (x, y))

    def read_pos(self, str):
        str = str.split(",")
        return int(str[0]), int(str[1])

    def make_pos(self, tup):
        return str(tup[0]) + "," + str(tup[1])


class FirstLevel(Level):
    def __init__(self, screen):
        Level.__init__(self, screen, 'BackGrounds/NeonTokyoBackground.jpg')
        self.speed = 4
        self.gravity = 0.3
        self.jump_force = -13
        self.screen = screen
        self.level_map = first_level
        self.net.send_initial_positions((100, 100))
        self.setup_level()

