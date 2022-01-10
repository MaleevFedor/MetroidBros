import os
import sys
from random import choice
import const
from const import button_keys
from Level_Config import TokyoLevel, ForestLevel, IndustrialLevel, ApocalypsisLevel, PlainLevel
from Shooting import Bullet
from game_window import GameWindow
import pygame
import pygame_menu

pygame.init()
screen = pygame.display.set_mode((1280, 720))
level_list = ['Forest', 'Tokyo', 'Industrial', 'Apocalypsis', 'Plain']

def load_level():
    choiced = choice(level_list)
    if choiced == 'Forest':
        return GameWindow(ForestLevel(screen))
    elif choiced == 'Tokyo':
        return GameWindow(TokyoLevel(screen))
    elif choiced == 'Industrial':
        return GameWindow(IndustrialLevel(screen))
    elif choiced == 'Apocalypsis':
        return GameWindow(ApocalypsisLevel(screen))
    elif choiced == 'Plain':
        return GameWindow(PlainLevel(screen))





# настройка геймпада
def shoot(player, game):
    if not player.killed:
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






def set_color(value, blank):
   const.color1 = value[0][0]

def set_color_2(value, blank):
    const.color2 = value[0][0]

def start_the_game():
    r21 = False
    r22 = False
    mouse_x, mouse_y = 0, 0

    holding = False

    game_window = load_level()
    game = game_window.active_level
    player1 = game.player
    player2 = game.player2
    players = (player1, player2)
    pygame.display.set_caption('Metroid Bros')
    pygame.mouse.set_visible(False)

    one_gamepad = False

    joysticks = []
    for i in range(pygame.joystick.get_count()):
        joysticks.append(pygame.joystick.Joystick(i))
    for joystick in joysticks:
        joystick.init()
    if len(joysticks) == 1:
        one_gamepad = True
    print(f'Всего геймпадов: {len(joysticks)}')

    analog_keys = {0: 0, 1: 0, 2: 0, 3: 0, 4: -1, 5: -1}
    dead_zone = 0.2  # inner radius
    edge_zone = 0.9  # outer radius
    last_shot = -game.gun[6]
    while game.running:
        if game.player.killed or game.player2.killed:
            start_the_game()
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
                            shoot(player2, game)
                            last_shot = now
                    else:
                        if not r22:
                            if now - last_shot > game.gun[6]:
                                shoot(player2, game)
                                last_shot = now
                        r22 = True
                else:
                    if joystick == joysticks[0]:
                        if game.gun[7]:
                            if now - last_shot > game.gun[6]:
                                shoot(player1, game)
                                last_shot = now
                        else:
                            if not r21:
                                if now - last_shot > game.gun[6]:
                                    shoot(player1, game)
                                    last_shot = now
                            r21 = True
                    elif joystick == joysticks[1]:
                        if game.gun[7]:
                            if now - last_shot > game.gun[6]:
                                shoot(player2, game)
                                last_shot = now
                        else:
                            if not r22:
                                if now - last_shot > game.gun[6]:
                                    shoot(player2, game)
                                    last_shot = now
                            r22 = True
            if joystick.get_axis(5) < 0:
                if one_gamepad:
                    r22 = False
                else:
                    if joystick == joysticks[0]:
                        r21 = False
                    elif joystick == joysticks[1]:
                        r22 = False
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
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player1.jump()
                    player1.can_jump = False
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
                        shoot(player1, game)
                        last_shot = now
            if event.type == pygame.QUIT:
                sys.exit()
        if pygame.mouse.get_pressed()[0]:
            if game.gun[7]:
                if now - last_shot > game.gun[6]:
                    shoot(player1, game)
                    last_shot = now
        game_window.active_level.update()
        game_window.active_level.render(screen)
        pygame.display.flip()
        game.clock.tick(60)


mytheme = pygame_menu.themes.THEME_ORANGE.copy()
myimage = pygame_menu.baseimage.BaseImage(

    image_path=f'BackGrounds/{choice(os.listdir("BackGrounds/"))}',
    drawing_mode=pygame_menu.baseimage.IMAGE_MODE_REPEAT_XY
)
mytheme.background_color = myimage
menu = pygame_menu.Menu('DinoMight', screen.get_width(), screen.get_height(),
                       theme=mytheme)

selected_level = menu.add.selector('Color1:', [('Yellow', 1), ('Red', 2), ('Green', 3), ('Blue', 4)], onchange=set_color)
selected_level = menu.add.selector('Color2:', [('Yellow', 1), ('Red', 2), ('Green', 3), ('Blue', 4)], onchange=set_color_2)

menu.add.button('Play', start_the_game)
menu.add.button('Quit', pygame_menu.events.EXIT)
menu.mainloop(screen)

print(1)