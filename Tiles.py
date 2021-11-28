import pygame


class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, sizeX, sizeY):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((sizeX, sizeY))
        self.image.fill((0, 0, 0))
        self.rect = self.image.get_rect(topleft=pos)
