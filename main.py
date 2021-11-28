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
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game.player.jump()
        game.update()
        game.render(screen)
        pygame.display.flip()
        game.clock.tick(240)

