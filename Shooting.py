import math
import pygame
bullets = []


class Bullet:
    def __init__(self, x, y, mouse_x, mouse_y):
        self.x = x
        self.y = y
        self.mouse_x = mouse_x
        self.mouse_y = mouse_y
        self.lifetime = 15
        self.speed = 20
        self.angle = math.atan2(mouse_y - y, mouse_x - x)
        self.x_vel = math.cos(self.angle) * self.speed
        self.y_vel = math.sin(self.angle) * self.speed
        self.radius = 5

    def update(self, screen):
        self.x += self.x_vel
        self.y += self.y_vel
        pygame.draw.circle(screen, (255, 255, 255), (self.x, self.y), self.radius)
        self.lifetime -= 1