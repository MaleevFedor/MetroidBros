import pygame
from Level_Config import FirstLevel


if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((1280, 720))
    game = FirstLevel(screen)
    pygame.display.set_caption('Metroid Bros')
    while game.running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game.quit()
        game.render(screen)
        pygame.display.flip()

