import math
import pygame

bullets = []
from random import uniform


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, mouse_x, mouse_y, gun):
        pygame.sprite.Sprite.__init__(self)
        self.lifetime, self.speed, self.bullet_count, self.spread, self.path, self.size, self.delay = gun
        self.image = pygame.Surface((self.size, self.size))
        self.image.fill((0, 255, 0))
        self.rect = self.image.get_rect()
        self.rect.centery = y
        self.rect.centerx = x
        self.angle = math.atan2(mouse_y - y, mouse_x - x)

        self.x_vel = math.cos(self.angle + uniform(-self.spread, self.spread)) * self.speed
        self.y_vel = math.sin(self.angle + uniform(-self.spread, self.spread)) * self.speed

    def update(self, screen):
        self.rect.x += self.x_vel
        self.rect.y += self.y_vel
        self.lifetime -= 1


