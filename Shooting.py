from math import cos, sin, atan2
import pygame
from random import uniform
bullets = []
guns = {'usp': (200, 10, 1, 0.03, 'GunsAssets/Usp-s.png', 10, 450, False, 38, ''),
        'pistol': (200, 10, 1, 0.1, 'GunsAssets/Pistol.png', 10, 200, False, 20, ''),
        'deagle': (250, 30, 1, 0.02, 'GunsAssets/deagle.png', 6, 700, False, 44, 'Music/GunSounds/Deagle.wav'),
        'shotgun': (60, 10, 12, 0.2, 'GunsAssets/Pump Shotgun.png', 4, 800, False, 15, 'Music/GunSounds/shotgun.wav'),
        'AWP': (250, 30, 1, 0, 'GunsAssets/Awp.png', 6, 1250, False, 200, 'Music/GunSounds/Awp.wav'),
        'm4': (200, 10, 1, 0.04, 'GunsAssets/M4A1s.png', 10, 325, True, 48, ''),
        'ak': (200, 17, 1, 0.27, 'GunsAssets/Ak 47.png', 9, 250, True, 50, 'Music/GunSounds/Ak.mp3'),
        'p90': (200, 15, 1, 0.23, 'GunsAssets/P90.png', 8, 150, True, 33, ''),
        'mac10': (200, 18, 1, 0.35, 'GunsAssets/mac10.png', 8, 200, True, 20, '')}


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, mouse_x, mouse_y, id,  gun):
        pygame.sprite.Sprite.__init__(self)
        self.lifetime, self.speed, self.bullet_count, self.spread, self.path, self.size, self.recoil, self.automatic,\
        self.damage, self.sound = gun
        self.image = pygame.Surface((self.size, self.size))
        self.image = pygame.transform.scale(pygame.image.load('GunsAssets/Bullet2.png'), (self.size, self.size))
        self.rect = self.image.get_rect()
        self.id = id
        self.rect.centery = y
        self.rect.centerx = x
        self.angle = atan2(mouse_y - y, mouse_x - x)
        self.x_vel = cos(self.angle + uniform(-self.spread, self.spread)) * self.speed
        self.y_vel = sin(self.angle + uniform(-self.spread, self.spread)) * self.speed

    def update(self, screen):
        self.rect.x += self.x_vel
        self.rect.y += self.y_vel
        self.lifetime -= 1
