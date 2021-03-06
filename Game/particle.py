import pygame
import random


class Particle(pygame.sprite.Sprite):
    def __init__(self, pos, dx, dy, path, lifetime):
        pygame.sprite.Sprite.__init__(self)
        self.fire = [pygame.image.load(path)]
        for scale in (2, 3, 4):
            self.fire.append(pygame.transform.scale(self.fire[0], (scale, scale)))
        self.image = random.choice(self.fire)
        self.rect = self.image.get_rect()
        self.velocity = [dx, dy]
        self.rect.x, self.rect.y = pos
        self.lifetime = lifetime
        self.gravity = 0.3

    def update(self):
        self.velocity[1] += self.gravity
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]
        self.lifetime -= 1
        if self.lifetime < 0:
            self.kill()


def create_particles(position, group, path, amount=20, lifetime=100):
    particle_count = amount
    numbers = range(-5, 6)
    for _ in range(particle_count):
        group.add(Particle(position, random.choice(numbers), random.choice(numbers), path, lifetime))
