from math import cos, sin, atan2
import pygame
from random import uniform
bullets = []


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, mouse_x, mouse_y, gun):
        pygame.sprite.Sprite.__init__(self)
        self.lifetime, self.speed, self.bullet_count, self.spread, self.path, self.size, self.recoil, self.automatic = gun
        self.image = pygame.Surface((self.size, self.size))
        self.image.fill((0, 255, 0))
        self.rect = self.image.get_rect()
        self.rect.centery = y
        self.rect.centerx = x
        self.angle = atan2(mouse_y - y, mouse_x - x)
        self.x_vel = cos(self.angle + uniform(-self.spread, self.spread)) * self.speed
        self.y_vel = sin(self.angle + uniform(-self.spread, self.spread)) * self.speed


    def update(self, screen):
        self.rect.x += self.x_vel
        self.rect.y += self.y_vel
        self.lifetime -= 1


