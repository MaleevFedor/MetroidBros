import pygame
import const


class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, sizeX, sizeY):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((sizeX, sizeY))
        self.image.fill((0, 0, 0))

        self.rect = self.image.get_rect(topleft=pos)


class Saw(pygame.sprite.Sprite):
    def __init__(self, pos, sizeX, sizeY):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((sizeX * 2, sizeY * 2))
        self.image.blit(pygame.image.load('Saw/Saw1.png'), (0, 0))
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect(topleft=pos)
        self.current_sprite = 0

    def animate(self):
        self.current_sprite += 1
        if self.current_sprite >= len(const.saw_sprite_list):
            self.current_sprite = 0
        self.image = const.saw_sprite_list[int(self.current_sprite)]


class Slime(pygame.sprite.Sprite):
    def __init__(self, pos, sizeX, sizeY):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((sizeX * 2, sizeY))
        self.image.blit(pygame.image.load('SlimeTile.jpg'), (0, 0))
        self.rect = self.image.get_rect(topleft=pos)
