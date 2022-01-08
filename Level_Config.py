from random import choice

from Level_Maps import *
import const
import pygame
from Tiles import Tile, Saw
from player import Player
from Shooting import guns
from particle import Particle, create_particles

class Level:
    def __init__(self, screen, image):
        self.clock = pygame.time.Clock()
        self.screen = screen
        self.speed = 0
        self.gravity = 0.0
        self.jump_force = 0
        self.running = True
        self.level_map = []
        self.screen = screen
        self.bg = pygame.image.load(image)
        self.gun = guns[choice(['usp', 'pistol', 'shotgun', 'AWP', 'ak', 'p90', 'mac10'])]
        self.playable = True
        self.cursor1 = None
        self.cursor2 = None
        self.players_dict = {}
        self.playable = True
        screen.blit(self.bg, (0, 0))

    def setup_level(self):
        self.tiles = pygame.sprite.Group()
        self.saws = pygame.sprite.Group()
        self.bullet_sprites = pygame.sprite.Group()
        self.player_sprite = pygame.sprite.GroupSingle()
        self.player2_sprite = pygame.sprite.GroupSingle()
        self.particle_sprites = pygame.sprite.Group()
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
                    y -= tile_size
                    self.player = Player((x, y), self.gravity, self.speed, self.jump_force, self.screen,
                                         self.gun[4], 'green', True, 1)
                    self.player_sprite.add(self.player)
                    self.cursor1 = pygame.image.load(f'Crosshairs/{self.player.color}.png').convert_alpha()
                elif col == '2':
                    y -= tile_size - 10
                    self.player2 = Player((x, y), self.gravity, self.speed, self.jump_force, self.screen,
                                          self.gun[4], 'yellow', False, 0)
                    self.player2_sprite.add(self.player2)
                    self.cursor2 = pygame.image.load(f'Crosshairs/{self.player2.color}.png').convert_alpha()
                elif col == 'S':
                    saw = Saw((x, y), tile_size, tile_size)
                    self.saws.add(saw)
        self.players_dict = {0: [self.player_sprite, self.player],
                             1: [self.player2_sprite, self.player2]}

    def quit(self):
        self.running = False

    def update(self):

        self.player.update(self.tiles, self.saws, self.particle_sprites)
        self.player2.update(self.tiles, self.saws, self.particle_sprites)

    def render(self, screen):

        screen.blit(self.bg, (0, 0))

        for bullet in self.bullet_sprites:
            if bullet.lifetime <= 0:
                bullet.kill()
            bullets_player = pygame.sprite.groupcollide(self.bullet_sprites, self.players_dict[bullet.id][0], True, False)
            for hit in bullets_player:
                create_particles((hit.rect.x, hit.rect.y), self.particle_sprites, const.blood_particle_path)
                self.players_dict[bullet.id][1].get_damage(bullet.damage)
            tiles_bullets = pygame.sprite.groupcollide(self.tiles, self.bullet_sprites, False, True)
            for hit in tiles_bullets:
                create_particles((hit.rect.x, hit.rect.y), self.particle_sprites, const.tile_particle_path)
            bullet.update(screen)

        for particle in self.particle_sprites:
            particle.update()
        for i in self.saws:
            i.animate()

        self.tiles.draw(screen)
        self.saws.draw(screen)
        self.bullet_sprites.draw(screen)
        self.player_sprite.draw(screen)
        self.particle_sprites.draw(screen)
        self.player.weapon_handling()
        self.player.i_hate_gravity()
        self.player2_sprite.draw(screen)
        self.player2.weapon_handling()
        self.player2.i_hate_gravity()
        font = pygame.font.Font('Fonts/m3x6.ttf', 35)
        text = font.render(f"FPS: {round(self.clock.get_fps())}", True, (100, 255, 100))
        pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(0, 0, 85, 20))
        screen.blit(text, (2, -7))
        font = pygame.font.Font('Fonts/orange kid.ttf', 25)
        players_hp = (round(self.player.current_health / 50), round(self.player2.current_health / 50))
        health_bar = pygame.image.load(f'HealthBars/{players_hp[0]}.png')
        screen.blit(health_bar, (0, 30))
        text = font.render(str(self.player.current_health), True, (105, 105, 105))
        screen.blit(text, (150, 36))
        health_bar = pygame.image.load(f'HealthBars/{players_hp[1]}.png')
        health_bar = pygame.transform.flip(health_bar, True, False)
        screen.blit(health_bar, (1080, 30))
        text = font.render(str(self.player2.current_health), True, (105, 105, 105))
        screen.blit(text, (1100, 36))
        x, y = self.player.scope
        x -= 15
        y -= 15
        screen.blit(self.cursor1, (x, y))
        x, y = self.player2.scope
        x -= 15
        y -= 15
        screen.blit(self.cursor2, (x, y))


class TokyoLevel(Level):
    def __init__(self, screen):
        Level.__init__(self, screen, 'BackGrounds/NeonTokyoBackground.jpg')
        self.speed = 4
        self.gravity = 0.3
        self.jump_force = -13
        self.screen = screen
        self.level_map = Tokyo_level
        self.setup_level()


class ForestLevel(Level):
    def __init__(self, screen):
        Level.__init__(self, screen, 'BackGrounds/Forest.png')
        self.speed = 4
        self.gravity = 0.3
        self.jump_force = -13
        self.screen = screen
        self.level_map = Forest_level
        self.setup_level()


class IndustrialLevel(Level):
    def __init__(self, screen):
        Level.__init__(self, screen, 'BackGrounds/Industrial.png')
        self.speed = 4
        self.gravity = 0.3
        self.jump_force = -13
        self.screen = screen
        self.level_map = Industrial_level
        pygame.mixer.music.load('Music/industrial.mp3')
        pygame.mixer.music.play(50)
        print('adsasf')
        self.setup_level()


class ApocalypsisLevel(Level):
    def __init__(self, screen):
        Level.__init__(self, screen, 'BackGrounds/Apocalypsis.jpg')
        self.speed = 4
        self.gravity = 0.3
        self.jump_force = -13
        self.screen = screen
        self.level_map = Apocalypsis
        self.setup_level()


class PlainLevel(Level):
    def __init__(self, screen):
        Level.__init__(self, screen, 'BackGrounds/Plain.png')
        self.speed = 4
        self.gravity = 0.3
        self.jump_force = -13
        self.screen = screen
        self.level_map = Plain
        self.setup_level()
