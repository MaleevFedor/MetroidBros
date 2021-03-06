from random import choice
from Level_Maps import *
import const
from const import level_ended
import pygame
from Tiles import Tile, Saw, Slime, Heal, Trampoline
from player import Player
from Shooting import guns
from particle import create_particles
from data_collector import DataCollector


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
        self.gun = guns[choice(['usp', 'pistol', 'shotgun', 'AWP', 'ak', 'p90', 'mac10', 'deagle', 'm4'])]
        self.playable = True
        self.cursor1 = None
        self.cursor2 = None
        self.ended = False

        self.playable = True
        screen.blit(self.bg, (0, 0))

    def setup_level(self):
        self.trampoline = pygame.sprite.Group()
        self.heals = pygame.sprite.Group()
        self.tiles = pygame.sprite.Group()
        self.saws = pygame.sprite.Group()
        self.slimes = pygame.sprite.Group()
        self.bullet_sprites = pygame.sprite.Group()
        self.bullet_sprites_2 = pygame.sprite.Group()
        self.all_bullets = pygame.sprite.Group()
        self.player_sprite = pygame.sprite.GroupSingle()
        self.player2_sprite = pygame.sprite.GroupSingle()
        self.particle_sprites = pygame.sprite.Group()
        self.tiles.add(Tile((-1, 0), 1, 720))
        self.tiles.add(Tile((1281, 0), 1, 720))
        self.tiles.add(Tile((0, 0), 1280, 1))

        for row_index, row in enumerate(self.level_map):
            for col_index, col in enumerate(row):
                x = col_index * tile_size
                y = row_index * tile_size
                if col == '1':
                    y -= tile_size
                    self.player = Player((x, y), self.gravity, self.speed, self.jump_force, self.screen,
                                         self.gun[4], const.color1, True, 0)
                    self.dc_1 = DataCollector(self.player)
                    self.player_sprite.add(self.player)
                    self.cursor1 = pygame.image.load(f'Crosshairs/{self.player.color}.png').convert_alpha()
                elif col == '2':
                    y -= tile_size - 10
                    self.player2 = Player((x, y), self.gravity, self.speed, self.jump_force, self.screen,
                                          self.gun[4], const.color2, False, 1)
                    self.dc_2 = DataCollector(self.player2)
                    self.player2_sprite.add(self.player2)

                    self.cursor2 = pygame.image.load(f'Crosshairs/{self.player2.color}.png').convert_alpha()
                elif col == 'X':
                    self.tiles.add(Tile((x, y), tile_size, tile_size))
                elif col == 'S':
                    self.saws.add(Saw((x, y), tile_size, tile_size))
                elif col == '_':
                    self.slimes.add(Slime((x, y), tile_size, tile_size))
                elif col == 'H':
                    if choice([True, False, True, False, False]):
                        self.heals.add(Heal((x, y), tile_size, tile_size))
                elif col == 'T':
                    self.trampoline.add(Trampoline((x, y), tile_size, tile_size))

    def quit(self):
        self.running = False


    def update(self):
        self.player.update(self.tiles, self.saws, self.slimes, self.particle_sprites, self.heals, self.trampoline,
                           self.player2_sprite, self.dc_1)

        self.player2.update(self.tiles, self.saws, self.slimes, self.particle_sprites, self.heals, self.trampoline,
                            self.player_sprite, self.dc_2)

    def bullet_col_check(self, bullet_group, player_sprite, player):
        for bullet in bullet_group:
            bullets1_player = pygame.sprite.groupcollide(bullet_group, player_sprite, True, False)
            for hit in bullets1_player:
                create_particles((hit.rect.x, hit.rect.y), self.particle_sprites, const.blood_particle_path)
                player.get_damage(bullet.damage)
                if player.id == 0:
                    self.dc_2.hits += 1
                else:
                    self.dc_1.hits += 1

    def check_map_win(self, dc):
        if self.level_map == Tokyo_level:
            dc.tokyo += 1
        elif self.level_map == Forest_level:
            dc.forest += 1
        elif self.level_map == Plain:
            dc.plains += 1
        elif self.level_map == Industrial_level:
            dc.industrial += 1
        elif self.level_map == Apocalypsis:
            dc.apocalypse += 1

    def render(self, screen):
        screen.blit(self.bg, (0, 0))
        pygame.draw.rect(screen, pygame.Color(self.player.color), pygame.Rect(580, 0, 60, 60))
        pygame.draw.rect(screen, pygame.Color(self.player2.color), pygame.Rect(640, 0, 60, 60))
        font = pygame.font.Font(None, 70)
        text = font.render(str(const.score[0]), True, (255, 255, 255))
        screen.blit(text, (595, 7))
        text = font.render(str(const.score[1]), True, (255, 255, 255))
        screen.blit(text, (657, 7))

        self.bullet_col_check(self.bullet_sprites, self.player2_sprite, self.player2)
        self.bullet_col_check(self.bullet_sprites_2, self.player_sprite, self.player)

        for bullet in self.all_bullets:
            bullet.update(screen)
            if bullet.lifetime <= 0:
                bullet.kill()
            tiles_bullets = pygame.sprite.groupcollide(self.tiles, self.all_bullets, False, True)
            trampoline_bullets = pygame.sprite.groupcollide(self.trampoline, self.all_bullets, False, True)
            slime_bullets = pygame.sprite.groupcollide(self.slimes, self.all_bullets, False, True)
            medkit_bullets = pygame.sprite.groupcollide(self.heals, self.all_bullets, True, True)
            for hit in trampoline_bullets:
                create_particles((bullet.rect.x, bullet.rect.y), self.particle_sprites, const.trampoline_path)
            for hit in tiles_bullets:
                create_particles((bullet.rect.x, bullet.rect.y), self.particle_sprites, const.tile_particle_path)
            for hit in slime_bullets:
                create_particles((bullet.rect.x, bullet.rect.y), self.particle_sprites, const.slime_particle)
            for hit in medkit_bullets:
                create_particles((bullet.rect.x, bullet.rect.y), self.particle_sprites, const.MedKitDestroy_path)

        for particle in self.particle_sprites:
            particle.update()
        for i in self.saws:
            i.animate()
        self.trampoline.draw(screen)
        self.tiles.draw(screen)
        self.saws.draw(screen)
        self.heals.draw(screen)
        self.slimes.draw(screen)
        self.bullet_sprites.draw(screen)
        self.bullet_sprites_2.draw(screen)
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
        x, y = self.player.scope
        x -= 15
        y -= 15
        screen.blit(self.cursor1, (x, y))
        x, y = self.player2.scope
        x -= 15
        y -= 15
        screen.blit(self.cursor2, (x, y))
        font = pygame.font.Font('Fonts/orange kid.ttf', 100)
        if self.player.killed or self.player2.killed:
            if not self.ended:
                pygame.time.set_timer(level_ended, 3000, 1)
                self.ended = True
                if self.player.killed:
                    self.check_map_win(self.dc_2)
                    const.score[1] += 1
                    self.dc_2.kills += 1
                    const.match_result += 'L'
                    const.match_result_2 += 'V'
                    self.dc_1.deaths += 1
                elif self.player2.killed:
                    self.check_map_win(self.dc_1)
                    const.score[0] += 1
                    const.match_result += 'V'
                    const.match_result_2 += 'L'
                    self.dc_1.kills += 1
                    self.dc_2.deaths += 1
                if const.score[0] != 3 and const.score[1] != 3:
                   self.dc_1.post()
                   self.dc_2.post()
                if 3 in const.score:
                    const.block_gamepad_menu = True
            if self.player.killed:
                win_player = self.player2
                self.player2.current_health = 200
            elif self.player2.killed:
                win_player = self.player
                self.player.current_health = 200
            pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(225, 300, 850, 150))
            text = font.render(str(win_player.color).capitalize() + ' player ' + 'wins round', True, (255, 255, 255))
            screen.blit(text, (250, 300))
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


class TokyoLevel(Level):
    def __init__(self, screen):
        Level.__init__(self, screen, 'BackGrounds/Level/DevsTokyo.png')
        self.speed = 4
        self.gravity = 0.3
        self.jump_force = -13
        self.screen = screen
        self.level_map = Tokyo_level
        pygame.mixer.music.load('Music/Ambients/TokyoAmbient.mp3')
        pygame.mixer.music.play(-1)
        self.setup_level()


class ForestLevel(Level):
    def __init__(self, screen):
        Level.__init__(self, screen, 'BackGrounds/Level/Forest.png')
        self.speed = 4
        self.gravity = 0.3
        self.jump_force = -13
        self.screen = screen
        self.level_map = Forest_level
        pygame.mixer.music.load('Music/Ambients/ForestAmbient.wav')
        pygame.mixer.music.play(-1)
        self.setup_level()


class IndustrialLevel(Level):
    def __init__(self, screen):
        Level.__init__(self, screen, 'BackGrounds/Level/Industrial.png')
        self.speed = 4
        self.gravity = 0.3
        self.jump_force = -13
        self.screen = screen
        self.level_map = Industrial_level
        pygame.mixer.music.load('Music/Ambients/industrial.mp3')
        pygame.mixer.music.play(-1)
        self.setup_level()


class ApocalypsisLevel(Level):
    def __init__(self, screen):
        Level.__init__(self, screen, 'BackGrounds/Level/Apocalypsis.jpg')
        self.speed = 4
        self.gravity = 0.3
        self.jump_force = -13
        self.screen = screen
        self.level_map = Apocalypsis
        pygame.mixer.music.load('Music/Ambients/The Last of Us (You and Me).mp3')
        pygame.mixer.music.play(-1)
        self.setup_level()


class PlainLevel(Level):
    def __init__(self, screen):
        Level.__init__(self, screen, 'BackGrounds/Level/Plain.png')
        self.speed = 4
        self.gravity = 0.3
        self.jump_force = -13
        self.screen = screen
        self.level_map = Plain
        pygame.mixer.music.load('Music/Ambients/PlainsAmbient.mp3')
        pygame.mixer.music.play(-1)
        self.setup_level()
