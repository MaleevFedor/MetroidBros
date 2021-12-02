import math
import pygame

bullets = []



class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, mouse_x, mouse_y, gun):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((10, 10))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.centery = y
        self.rect.centerx = x
        self.lifetime, self.speed = gun
        self.angle = math.atan2(mouse_y - y, mouse_x - x)
        self.mouse_x = mouse_x
        self.mouse_y = mouse_y
        self.x_vel = math.cos(self.angle) * self.speed
        self.y_vel = math.sin(self.angle) * self.speed
        print(gun)

    def update(self, screen):
        self.rect.x += self.x_vel
        self.rect.y += self.y_vel
        self.lifetime -= 1

    #ToDo коллайдеры на пули