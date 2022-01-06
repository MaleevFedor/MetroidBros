import pygame


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
