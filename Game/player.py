import pygame
import math
from particle import create_particles
import const


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, gravity, speed, jump_force, screen, weapon, color, facing_right, bullets_id):
        super().__init__()
        self.screen = screen
        self.health = 20
        self.can_jump = True
        self.facing_right = facing_right
        self.speed = 1
        self.image = pygame.Surface((56, 70))
        self.color = color
        self.rect = self.image.get_rect(topleft=pos)
        self.player_weapon = pygame.image.load(weapon)
        self.current_health = 200
        self.maximum_health = self.current_health
        self.health_bar_length = 40
        self.health_ratio = self.maximum_health / self.health_bar_length
        self.x = pos[0]
        self.y = pos[1]
        self.y += 30
        self.id = bullets_id
        self.normal_speed = speed
        self.speed = self.normal_speed
        self.gravity = gravity
        self.jump_force = jump_force
        self.extra_jumps = 2
        self.direction = pygame.math.Vector2(0.0, 0.0)
        self.killed = False
        self.right = False
        self.left = False
        self.jump_sound = pygame.mixer.Sound('Music/Effects/jump.wav')
        pygame.mixer.Sound.set_volume(self.jump_sound, const.volume)
        self.scope = [self.rect[0], self.rect[1]]
        self.animations = {'idle': [],
                           'run': [],
                           'jump': [],
                           'hurt': [],
                           'fall': []}
        self.animations['idle'].append(pygame.image.load(f'DinosaursAssets/{self.color}Dino/Idle/Idle1.png'))
        self.animations['idle'].append(pygame.image.load(f'DinosaursAssets/{self.color}Dino/Idle/Idle2.png'))
        self.animations['idle'].append(pygame.image.load(f'DinosaursAssets/{self.color}Dino/Idle/Idle3.png'))
        self.animations['idle'].append(pygame.image.load(f'DinosaursAssets/{self.color}Dino/Idle/Idle4.png'))

        self.animations['run'].append(pygame.image.load(f'DinosaursAssets/{self.color}Dino/Run/Run1.png'))
        self.animations['run'].append(pygame.image.load(f'DinosaursAssets/{self.color}Dino/Run/Run2.png'))
        self.animations['run'].append(pygame.image.load(f'DinosaursAssets/{self.color}Dino/Run/Run3.png'))
        self.animations['run'].append(pygame.image.load(f'DinosaursAssets/{self.color}Dino/Run/Run4.png'))
        self.animations['run'].append(pygame.image.load(f'DinosaursAssets/{self.color}Dino/Run/Run5.png'))
        self.animations['run'].append(pygame.image.load(f'DinosaursAssets/{self.color}Dino/Run/Run6.png'))

        self.animations['jump'].append(pygame.image.load(f'DinosaursAssets/{self.color}Dino/jump.png'))
        self.animations['hurt'].append(pygame.image.load(f'DinosaursAssets/{self.color}Dino/Hurt/Hurt1.png'))
        self.animations['hurt'].append(pygame.image.load(f'DinosaursAssets/{self.color}Dino/Hurt/Hurt2.png'))
        self.animations['hurt'].append(pygame.image.load(f'DinosaursAssets/{self.color}Dino/Hurt/Hurt3.png'))
        self.sprites = []
        self.current_state = 'idle'
        self.current_sprite = 0

    def weapon_handling(self):
        if self.killed:
            return None
        offset = pygame.math.Vector2(0, 0)
        mouse_x, mouse_y = self.scope[0], self.scope[1]
        rel_x, rel_y = mouse_x - self.rect.x - 7, mouse_y - self.rect.y - 10
        angle = (180 / math.pi) * math.atan2(rel_y, rel_x)
        if not -90 < angle < 90:
            rotated_image = pygame.transform.rotozoom(self.player_weapon, angle, 1)
            rotated_image = pygame.transform.flip(rotated_image, False, True)
        else:
            rotated_image = pygame.transform.rotozoom(self.player_weapon, -angle, 1)
        rotated_offset = offset.rotate(angle)
        rect = rotated_image.get_rect(center=self.rect.center + rotated_offset)
        rect[0] += 7
        rect[1] += 10
        self.screen.blit(rotated_image, rect)

    def get_damage(self, amount):
        if self.current_health > 0:
            self.current_health -= amount
            self.current_state = 'hurt'
            self.current_sprite = 0
        if self.current_health <= 0:
            self.current_health = 0
            self.kill()

            self.killed = True

    def get_health(self, amount):
        if self.current_health < self.maximum_health:
            self.current_health += amount
        if self.current_health > self.maximum_health:
            self.current_health = self.maximum_health

    def i_hate_gravity(self):
        self.direction.y += self.gravity

    def get_state(self):
        if self.current_state != 'hurt':
            if self.extra_jumps != 2:
                self.current_state = 'jump'
            elif self.right or self.left:
                self.current_state = 'run'
            else:
                self.current_state = 'idle'

    def animation(self):
        current_animation = self.animations[self.current_state]
        self.current_sprite += 0.10
        if self.current_sprite >= len(current_animation):
            self.current_sprite = 0
            if self.current_state == 'hurt':
                self.current_state = ''
        image = current_animation[int(self.current_sprite)]
        if self.facing_right:
            self.image = image
        else:
            self.image = pygame.transform.flip(image, True, False)

    def jump(self):
        if self.extra_jumps > 0:
            self.direction.y = 0
            self.direction.y += self.jump_force
            self.extra_jumps -= 1
            pygame.mixer.Sound.play(self.jump_sound)
            self.can_jump = False

    def col_x_check(self, collided_sprite):
        for tile in collided_sprite:
            if self.rect.colliderect(tile.rect):
                if self.direction.x > 0:
                    self.rect.right = tile.rect.left
                elif self.direction.x < 0:
                    self.rect.left = tile.rect.right

    def col_y_check(self, collided_sprite):
        for tile in collided_sprite:
            if self.rect.colliderect(tile.rect):
                if self.direction.y > 0:
                    self.rect.bottom = tile.rect.top
                    self.extra_jumps = 2
                elif self.direction.y < 0:
                    self.rect.top = tile.rect.bottom
                self.direction.y = 0

    def update(self, tiles, saws, slimes, particles, heals, trampolines, other_player, dc):
        if self.killed:
            return None
        self.get_state()
        self.animation()
        if self.right:
            self.direction.x = self.speed
            self.facing_right = True
        elif self.left:
            self.direction.x = -self.speed
            self.facing_right = False
        else:
            self.direction.x = 0
        self.rect.x += self.direction.x
        self.col_x_check(tiles)
        self.col_x_check(slimes)
        self.col_x_check(trampolines)

        for tile in heals:
            if self.rect.colliderect(tile.rect):
                if self.current_health <= 100 and tile.image != const.open_med:
                    tile.image = const.open_med
                    self.get_health(100)
                    dc.hp_healed += 100

                    create_particles((self.rect.x, self.rect.y), particles, const.heal_particle_path)

        self.i_hate_gravity()
        self.rect.y += self.direction.y
        self.speed = self.normal_speed
        self.col_y_check(tiles)

        for tile in slimes:
            if self.rect.colliderect(tile.rect):
                if self.direction.x != 0:
                    create_particles((self.rect.centerx, self.rect.bottom), particles, const.slime_particle, 1, 30)
                if self.direction.y > 0:
                    self.rect.bottom = tile.rect.top
                    self.extra_jumps = 2
                    self.speed *= 0.2
                elif self.direction.y < 0:
                    self.rect.top = tile.rect.bottom
                self.direction.y = 0

        for tile in saws:
            if self.rect.colliderect(tile.rect):
                if self.direction.y > 0:
                    self.rect.bottom = tile.rect.top
                    self.extra_jumps = 2
                elif self.direction.y < 0:
                    self.rect.top = tile.rect.bottom
                self.direction.y = 0
                self.jump()
                create_particles((self.rect.x, self.rect.y), particles, const.blood_particle_path)
                self.extra_jumps = 0
                self.get_damage(20)
                if self.current_health == 0:
                    dc.saws_deaths += 1


        for tile in trampolines:
            if self.rect.colliderect(tile.rect):
                if self.direction.y > 0:
                    self.rect.bottom = tile.rect.top
                    self.direction.y *= -1.07
                    self.extra_jumps = 0


