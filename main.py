import pygame
from Level_Config import FirstLevel
from Shooting import Bullet

if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((1280, 720))
    game = FirstLevel(screen)
    pygame.display.set_caption('Metroid Bros')
    pygame.mouse.set_visible(False)
    last_shot = -game.gun[6]
    while game.running:
        now = pygame.time.get_ticks()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game.player.jump()
                elif event.key == pygame.K_1:
                    game.player.get_damage(200)
                elif event.key == pygame.K_2:
                    game.player.get_health(200)
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    player = game.player
                    player.can_jump = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    if now - last_shot > game.gun[6]:
                        for i in range(game.gun[2]):
                            bullet_sprites = Bullet(game.player.rect.centerx, game.player.rect.centery, mouse_x,
                                                    mouse_y,
                                                    game.gun)
                            game.bullet_sprites.add(bullet_sprites)
                            last_shot = now

        game.update()
        game.render(screen)
        pygame.display.flip()
        game.clock.tick(60)
