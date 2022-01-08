import json
import os
from random import choice
import const
import pygame
from Level_Config import TokyoLevel, ForestLevel, IndustrialLevel, ApocalypsisLevel, PlainLevel
from Shooting import Bullet
from game_window import GameWindow


def shoot(player):
    mouse_x, mouse_y = player.scope
    for i in range(game.gun[2]):
        bullet_sprites = Bullet(player.rect.centerx, player.rect.centery, mouse_x, mouse_y, player.id, game.gun)
        game.bullet_sprites.add(bullet_sprites)


def pause():
    paused = True

    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
            paused = False
        pygame.display.flip()


def load_level():
    level_list = ['Forest', 'Tokyo', 'Industrial', 'Apocalypsis', 'Plain']
    choiced = choice(level_list)
    level_list.remove(choiced)
    return GameWindow(levels[choiced])


if __name__ == '__main__':
    mouse_x, mouse_y = 0, 0
    pygame.init()
    holding = False
    screen = pygame.display.set_mode((1280, 720))
    levels = {'Forest': ForestLevel(screen),
              'Tokyo': TokyoLevel(screen),
              'Industrial': IndustrialLevel(screen),
              'Apocalypsis': ApocalypsisLevel(screen),
              'Plain': PlainLevel(screen)}
    game_window = load_level()
    game = game_window.active_level
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
    dead_zone = 0.2  # inner radius
    edge_zone = 0.9  # outer radius
    # настройка геймпада
    while game.running:
        now = pygame.time.get_ticks()
        for joystick in joysticks:
            right_x = joystick.get_axis(2)
            right_y = joystick.get_axis(3) * 1
            if (-dead_zone < right_x < dead_zone) and (-dead_zone < right_y < dead_zone):
                pass
            else:
                if one_gamepad:
                    players[1].scope[0] += round(right_x * 10)
                    players[1].scope[1] += round(right_y * 10)
                else:
                    if joystick == joysticks[0]:
                        players[0].scope[0] += round(right_x * 10)
                        players[0].scope[1] += round(right_y * 10)
                    elif joystick == joysticks[1]:
                        players[1].scope[0] += round(right_x * 10)
                        players[1].scope[1] += round(right_y * 10)

            if joystick.get_axis(5) > 0:
                if one_gamepad:
                    if game.gun[7]:
                        if now - last_shot > game.gun[6]:
                            shoot(player2)
                            last_shot = now
                else:
                    if joystick == joysticks[0]:
                        if game.gun[7]:
                            if now - last_shot > game.gun[6]:
                                shoot(player1)
                                last_shot = now
                    elif joystick == joysticks[1]:
                        if game.gun[7]:
                            if now - last_shot > game.gun[6]:
                                shoot(player2)
                                last_shot = now


        if one_gamepad or len(joysticks) == 0:
            player1.scope = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if game_window.active_level.playable:
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
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        player1.jump()
                        player1.can_jump = False
                    if event.key == pygame.K_ESCAPE:
                        game_window.process_custom_event(const.OPTIONS_LOAD)
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
            if event.type == pygame.QUIT:
                game.quit()

        if pygame.mouse.get_pressed()[0]:
            if game.gun[7]:
                if now - last_shot > game.gun[6]:
                    shoot(player1)
                    last_shot = now
        game_window.active_level.update()
        game_window.active_level.render(screen)
        pygame.display.flip()
        game.clock.tick(60)
