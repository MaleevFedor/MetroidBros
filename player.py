import pygame
import random


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, gravity, speed, jump_force, screen):
        #отхождение от туториала, сделал переменные гравитации и скорости в классе Level
        #чтобы можно было менять скорость игроков и гравитацию на разных уровнях
        super().__init__()
        self.screen = screen
        self.health = 20
        self.can_jump = True
        self.speed = 1
        self.image = pygame.Surface((40, 70))
        self.image.fill('green')
        self.rect = self.image.get_rect(topleft=pos)
        self.x = 0
        self.y = 0
        #movement
        self.speed = speed
        self.gravity = gravity
        self.jump_force = jump_force
        self.extra_jumps = 2
        self.direction = pygame.math.Vector2(0.0, 0.0)

    def get_input(self):

        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.direction.x = self.speed
        elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.direction.x = -self.speed
        else:
            self.direction.x = 0

        if keys[pygame.K_SPACE]:
            self.jump()

    def i_hate_gravity(self):
        self.direction.y += self.gravity

    def jump(self):
        if self.extra_jumps > 0 and self.can_jump:
            if self.direction.y > 0:
                self.direction.y = 0
            self.direction.y += self.jump_force
            self.extra_jumps -= 1
            pygame.mixer.music.load('Music/jump.wav')
            pygame.mixer.music.play()
            self.can_jump = False

    def update(self, tiles):
        self.get_input()
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

    def get_damage(self, damage):
        self.health -= damage
        print(self.health)
