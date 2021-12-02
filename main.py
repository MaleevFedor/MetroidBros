import pygame
from Level_Config import FirstLevel
from Shooting import Bullet

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
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    player = game.player
                    player.can_jump = True
                    player.get_damage(1)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    bullet_sprites = Bullet(game.player.rect.centerx, game.player.rect.centery, mouse_x, mouse_y, game.gun)
                    game.bullet_sprites.add(bullet_sprites)

        game.update()
        game.render(screen)
        pygame.display.flip()
        game.clock.tick(60)
