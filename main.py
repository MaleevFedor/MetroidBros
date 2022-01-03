import json
import os

import pygame
from Level_Config import FirstLevel
from Shooting import Bullet


if __name__ == '__main__':
    pygame.init()
    holding = False
    screen = pygame.display.set_mode((1280, 720))
    game = FirstLevel(screen)
    pygame.display.set_caption('Metroid Bros')
    pygame.mouse.set_visible(False)
    last_shot = -game.gun[6]

    joysticks = []
    for i in range(pygame.joystick.get_count()):
        joysticks.append(pygame.joystick.Joystick(i))
    for joystick in joysticks:
        joystick.init()
    try:
        gamepad1 = joysticks[0]
        gamepad2 = joysticks[1]
    except:
        pass
    print(f'Всего геймпадов: {len(joysticks)}')

    with open(os.path.join("dualshock4_buttons.json"), 'r+') as file:
        button_keys = json.load(file)
    analog_keys = {0: 0, 1: 0, 2: 0, 3: 0, 4: -1, 5: -1}
    # настройка геймпада
    player1 = game.player
    while game.running:
        now = pygame.time.get_ticks()
        for event in pygame.event.get():
            if event.type == pygame.JOYBUTTONDOWN:
                if event.button == button_keys['x'] or event.button == button_keys['R1']:
                    player1.jump()
            if event.type == pygame.JOYBUTTONUP:
                if event.button == button_keys['x'] or event.button == button_keys['R1']:
                    player1.can_jump = True
            if event.type == pygame.JOYAXISMOTION:
                analog_keys[event.axis] = event.value
                # print(analog_keys)
                # Horizontal Analog
                if abs(analog_keys[0]) > .4:
                    if analog_keys[0] < -.7:
                        player1.left = True
                    else:
                        player1.left = False
                    if analog_keys[0] > .7:
                        player1.right = True
                    else:
                        player1.right = False

            if event.type == pygame.QUIT:
                game.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player1.jump()
                elif event.key == pygame.K_1:
                    player1.get_damage(200)
                elif event.key == pygame.K_2:
                    player1.get_health(200)
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    player1.can_jump = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    if now - last_shot > game.gun[6]:
                        for i in range(game.gun[2]):
                            bullet_sprites = Bullet(player1.rect.centerx, player1.rect.centery, mouse_x, mouse_y, game.gun)
                            game.bullet_sprites.add(bullet_sprites)
                            last_shot = now
        if pygame.mouse.get_pressed()[0]:
            if game.gun[7]:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if now - last_shot > game.gun[6]:
                    for i in range(game.gun[2]):
                        bullet_sprites = Bullet(player1.rect.centerx, player1.rect.centery, mouse_x, mouse_y,
                                                game.gun)
                        game.bullet_sprites.add(bullet_sprites)
                        last_shot = now
        game.update()
        game.render(screen)
        pygame.display.flip()
        game.clock.tick(60)
