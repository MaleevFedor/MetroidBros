import json
import os

import pygame
from Level_Config import FirstLevel
from Shooting import Bullet


def shoot(player):
    mouse_x, mouse_y = player.scope
    for i in range(game.gun[2]):
        bullet_sprites = Bullet(player.rect.centerx, player.rect.centery, mouse_x, mouse_y, player.id, game.gun)
        game.bullet_sprites.add(bullet_sprites)


if __name__ == '__main__':
    mouse_x, mouse_y = 0, 0
    pygame.init()
    holding = False
    screen = pygame.display.set_mode((1280, 720))
    game = FirstLevel(screen)
    player1 = game.player
    player2 = game.player2
    players = (player1, player2)
    pygame.display.set_caption('Metroid Bros')
    pygame.mouse.set_visible(False)
    last_shot = -game.gun[6]
    one_gamepad = False

    joysticks = []
    for i in range(pygame.joystick.get_count()):
        joysticks.append(pygame.joystick.Joystick(i))
    for joystick in joysticks:
        joystick.init()
    if len(joysticks) == 1:
        one_gamepad = True
    print(f'Всего геймпадов: {len(joysticks)}')

    with open(os.path.join("dualshock4_buttons.json"), 'r+') as file:
        button_keys = json.load(file)
    analog_keys = {0: 0, 1: 0, 2: 0, 3: 0, 4: -1, 5: -1}
    # настройка геймпада
    while game.running:
        now = pygame.time.get_ticks()
        if one_gamepad or len(joysticks) == 0:
            player1.scope = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.JOYBUTTONDOWN:
                if one_gamepad:
                    event.joy += 1
                if event.button == button_keys['x'] or event.button == button_keys['L1']:
                    players[event.joy].jump()
                if event.button == button_keys['left_arrow']:
                    players[event.joy].left = True
                if event.button == button_keys['right_arrow']:
                    players[event.joy].right = True
            if event.type == pygame.JOYBUTTONUP:
                if one_gamepad:
                    event.joy += 1
                if event.button == button_keys['x'] or event.button == button_keys['L1']:
                    players[event.joy].can_jump = True
                if event.button == button_keys['left_arrow']:
                    players[event.joy].left = False
                if event.button == button_keys['right_arrow']:
                    players[event.joy].right = False
            if event.type == pygame.JOYAXISMOTION:
                if one_gamepad:
                    event.joy += 1
                cur_player = players[event.joy]
                analog_keys[event.axis] = event.value
                if abs(analog_keys[0]) > .4:
                    if analog_keys[0] < -.7:
                        cur_player.left = True
                    else:
                        cur_player.left = False
                    if analog_keys[0] > .7:
                        cur_player.right = True
                    else:
                        cur_player.right = False
                if analog_keys[5] > 0:  # Right Trigger
                    pass
                    # shoot()
                    # last_shot = now
                # ToDo fixe r2

            if event.type == pygame.QUIT:
                game.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player1.jump()
                    player1.can_jump = False
                elif event.key == pygame.K_1:
                    player1.get_damage(200)
                elif event.key == pygame.K_2:
                    player1.get_health(200)
                if event.key == pygame.K_a:
                    player1.left = True
                if event.key == pygame.K_d:
                    player1.right = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a:
                    player1.left = False
                if event.key == pygame.K_d:
                    player1.right = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if now - last_shot > game.gun[6]:
                        shoot(player1)
                        last_shot = now
        if pygame.mouse.get_pressed()[0]:
            if game.gun[7]:
                if now - last_shot > game.gun[6]:
                    shoot(player1)
                    last_shot = now
        game.update()
        game.render(screen)
        pygame.display.flip()
        game.clock.tick(60)
