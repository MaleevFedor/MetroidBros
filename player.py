import pygame
import math


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, gravity, speed, jump_force, screen, weapon, color, facing_right, id):
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
        self.current_health = 1000
        self.maximum_health = 1000
        self.health_bar_length = 40
        self.health_ratio = self.maximum_health / self.health_bar_length
        self.x = pos[0]
        self.y = pos[1]
        self.y += 30
        self.id = id
        self.speed = speed
        self.gravity = gravity
        self.jump_force = jump_force
        self.extra_jumps = 2
        self.direction = pygame.math.Vector2(0.0, 0.0)
        self.right = False
        self.left = False
        self.scope = (self.rect[0], self.rect[1])
        self.animations = {'idle': [],
                           'run': [],
                           'jump': [],
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
        self.sprites = []
        self.current_state = 'idle'
        self.current_sprite = 0

    def weapon_handling(self):
        offset = pygame.math.Vector2(0, 0)
        mouse_x, mouse_y = pygame.mouse.get_pos()
        rel_x, rel_y = mouse_x - self.rect.x, mouse_y - self.rect.y
        angle = (180 / math.pi) * math.atan2(rel_y, rel_x)
        rotated_image = pygame.transform.rotozoom(self.player_weapon, -angle, 1)
        rotated_offset = offset.rotate(angle)
        rect = rotated_image.get_rect(center=self.rect.center + rotated_offset)
        rect[0] += 7
        rect[1] += 10
        self.screen.blit(rotated_image, rect)

    def get_damage(self, amount):
        if self.current_health > 0:
            self.current_health -= amount
        if self.current_health <= 0:
            self.kill()


    def get_health(self, amount):
        if self.current_health < self.maximum_health:
            self.current_health += amount
        if self.current_health > self.maximum_health:
            self.current_health = self.maximum_health

    def basic_health(self):
        pygame.draw.rect(self.screen, (255, 0, 0),
                         (self.rect.x, self.rect.y - 10, self.current_health / self.health_ratio, 5))

    def i_hate_gravity(self):
        self.direction.y += self.gravity

    def get_state(self):
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
        self.image = current_animation[int(self.current_sprite)]

    def jump(self):
        if self.extra_jumps > 0:
            if self.direction.y > 0:
                self.direction.y = 0
            self.direction.y += self.jump_force
            self.extra_jumps -= 1
            pygame.mixer.music.load('Music/jump.wav')
            pygame.mixer.music.play()
            self.can_jump = False

    def update(self, tiles, saws):
        self.get_state()
        self.animation()
        if self.right:
            self.direction.x = self.speed
        elif self.left:
            self.direction.x = -self.speed
        else:
            self.direction.x = 0
        self.rect.x += self.direction.x
        for tile in tiles:
            if self.rect.colliderect(tile.rect):
                if self.direction.x > 0:
                    self.rect.right = tile.rect.left
                elif self.direction.x < 0:
                    self.rect.left = tile.rect.right

        self.i_hate_gravity()
        self.rect.y += self.direction.y
        for tile in tiles:
            if self.rect.colliderect(tile.rect):
                if self.direction.y > 0:
                    self.rect.bottom = tile.rect.top
                    self.extra_jumps = 2
                elif self.direction.y < 0:
                    self.rect.top = tile.rect.bottom
                self.direction.y = 0

        for saw in saws:
            if self.rect.colliderect(saw.rect):
                print('you colided saw')
