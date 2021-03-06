import json
import os
import sys
from random import choice
import const
from const import button_keys
from Shooting import Bullet
from game_window import GameWindow
import pygame
import pygame_menu
import requests
from data_collector import DataCollector


def shoot(player, game):
    try:
        if not player.killed:
            shot_sound = pygame.mixer.Sound(game.gun[9])
            pygame.mixer.Sound.set_volume(shot_sound, const.volume)
            pygame.mixer.Sound.play(shot_sound)

            mouse_x, mouse_y = player.scope
            for i in range(game.gun[2]):
                bullet_sprites = Bullet(player.rect.centerx, player.rect.centery, mouse_x, mouse_y, player.id, game.gun)
                if player == game.player:
                    game.dc_1.shots += 1
                    game.bullet_sprites.add(bullet_sprites)
                else:
                    game.dc_2.shots += 1
                    game.bullet_sprites_2.add(bullet_sprites)
                game.all_bullets.add(bullet_sprites)
    except Exception as e:
        print(e)


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


def start_the_game(actual_score=True):
    r21 = False
    r22 = False
    if not actual_score:
        const.score = [0, 0]
    one_gamepad = False

    joysticks = []
    for i in range(pygame.joystick.get_count()):
        joysticks.append(pygame.joystick.Joystick(i))
    for joystick in joysticks:
        joystick.init()
    if len(joysticks) == 1:
        one_gamepad = True
    game_window = GameWindow()
    game_window.load_level(screen)
    game = game_window.active_level
    player1 = game.player
    player2 = game.player2
    dc_1 = game.dc_1
    dc_2 = game.dc_2
    players = (player1, player2)
    pygame.display.set_caption('DinoMight')
    pygame.mouse.set_visible(False)
    dead_zone = 0.2
    last_shot = -game.gun[6]
    last_shot_2 = -game.gun[6]
    while game.running:
        game.clock.tick(60)
        if len(joysticks) != pygame.joystick.get_count() and not const.block_gamepad_menu:
            load_controller_menu()
        now = pygame.time.get_ticks()
        if len(joysticks) <= 1:
            player1.scope = [pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]]
        for joystick in joysticks:
            right_x = joystick.get_axis(2)
            right_y = joystick.get_axis(3) * 1
            if (-dead_zone < right_x < dead_zone) and (-dead_zone < right_y < dead_zone):
                pass
            else:
                if one_gamepad:
                    players[1].scope[0] += round(right_x * 10)
                    players[1].scope[1] += round(right_y * 10)
                    if players[1].scope[1] < 0:
                        players[1].scope[1] = 0
                    elif players[1].scope[1] > 720:
                        players[1].scope[1] = 720
                    if players[1].scope[0] < 0:
                        players[1].scope[0] = 0
                    elif players[1].scope[0] > 1280:
                        players[1].scope[0] = 1280
                else:
                    if joystick == joysticks[0]:
                        players[0].scope[0] += round(right_x * 10)
                        players[0].scope[1] += round(right_y * 10)
                        if players[0].scope[1] < 0:
                            players[0].scope[1] = 0
                        elif players[0].scope[1] > 720:
                            players[0].scope[1] = 720
                        if players[0].scope[0] < 0:
                            players[0].scope[0] = 0
                        elif players[0].scope[0] > 1280:
                            players[0].scope[0] = 1280
                    elif joystick == joysticks[1]:
                        players[1].scope[0] += round(right_x * 10)
                        players[1].scope[1] += round(right_y * 10)
                        if players[1].scope[1] < 0:
                            players[1].scope[1] = 0
                        elif players[1].scope[1] > 720:
                            players[1].scope[1] = 720
                        if players[1].scope[0] < 0:
                            players[1].scope[0] = 0
                        elif players[1].scope[0] > 1280:
                            players[1].scope[0] = 1280
        for joystick in joysticks:
            if joystick.get_axis(5) > 0:  # Right Trigger
                if one_gamepad:
                    if game.gun[7]:
                        if now - last_shot_2 > game.gun[6]:
                            shoot(player2, game)
                            last_shot_2 = now
                    else:
                        if not r22:
                            if now - last_shot_2 > game.gun[6]:
                                shoot(player2, game)

                                last_shot_2 = now
                        r22 = True
                elif joystick == joysticks[0]:
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
                        if now - last_shot_2 > game.gun[6]:
                            shoot(player2, game)
                            last_shot_2 = now
                    else:
                        if not r22:
                            if now - last_shot_2 > game.gun[6]:
                                shoot(player2, game)
                                last_shot_2 = now
                        r22 = True
            else:
                if one_gamepad:
                    r22 = False
                if joystick == joysticks[0]:
                    r21 = False
                elif joystick == joysticks[1]:
                    r22 = False
        for event in pygame.event.get():
            if event.type == const.level_ended and const.score[0] + const.score[1] != 0:

                if const.score[0] == 3:
                    copy_score = const.score
                    dc_1.wins += 1
                    dc_2.loses += 1
                    dc_1.post()
                    dc_2.post()
                    dc_1.match_post()
                    dc_2.match_post()
                    load_restart_menu(copy_score, players[0].color)
                if const.score[1] == 3:
                    copy_score = const.score
                    dc_2.wins += 1
                    dc_1.loses += 1
                    dc_1.post()
                    dc_2.post()
                    dc_1.match_post()
                    dc_2.match_post()
                    load_restart_menu(copy_score, players[1].color)

                start_the_game()
            if event.type == pygame.QUIT:
                pygame.quit()
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


def restart_game():
    const.block_gamepad_menu = False
    start_the_game(False)


def continue_game():
    const.block_gamepad_menu = False
    start_the_game(True)


def set_volume(blank):
    const.volume = round(blank) * 0.01
    pygame.mixer.music.set_volume(const.volume)


def save_name(name, player_num):
    if player_num == 1:
        const.player1_name = name
    else:
        const.player2_name = name


def save_password(password, player_num):
    if player_num == 1:
        const.player1_password = password
    else:
        const.player2_password = password


def login():
    req = requests.post(const.PASSWORD_CHECK_ADRESS, json={'login': const.player1_name, 'password': const.player1_password})
    req_2 = requests.post(const.PASSWORD_CHECK_ADRESS,
                        json={'login': const.player2_name, 'password': const.player2_password})
    if req.text == 'ok' and req_2.text == 'ok' and const.player1_name != const.player2_name:
        load_menu()

    else:
        load_login_menu()



def load_menu():
    const.score = [0, 0]
    const.block_gamepad_menu = False
    const.level_list = ['Forest', 'Tokyo', 'Industrial', 'Apocalypsis', 'Plain']
    pygame.display.set_icon(pygame.image.load('icon.ico'))
    pygame.display.set_caption('DinoMight')
    pygame.mixer.music.load('Music/Ambients/MainMenu.wav')
    pygame.mixer.music.play(-1)
    mytheme = pygame_menu.themes.THEME_ORANGE.copy()
    myimage = pygame_menu.baseimage.BaseImage(

        image_path=f'BackGrounds/MainMenu/{choice(os.listdir("BackGrounds/MainMenu/"))}',
        drawing_mode=pygame_menu.baseimage.IMAGE_MODE_REPEAT_XY
    )
    mytheme.background_color = myimage
    menu = pygame_menu.Menu('DinoMight', screen.get_width(), screen.get_height(),
                            theme=mytheme, joystick_enabled=False)

    menu.add.selector('Color1:', [('Blue', 1), ('Red', 2), ('Green', 3), ('Yellow', 4)],
                      onchange=set_color,
                      font_color=(0, 0, 0), font_size=60, selection_color=(0, 0, 0),
                      font_name='Fonts/m3x6.ttf',
                      )
    menu.add.selector('Color2:', [('Red', 1), ('Yellow', 2), ('Green', 3), ('Blue', 4)],
                      onchange=set_color_2, font_size=60,
                      font_color=(0, 0, 0), selection_color=(0, 0, 0), font_name='Fonts/m3x6.ttf')
    menu.add.range_slider('Volume', const.volume * 100, (0, 100), 10, onchange=set_volume, selection_color=(0, 0, 0),
                          font_size=60, font_name='Fonts/m3x6.ttf')
    menu.add.button('Play', start_the_game, font_color=(0, 0, 0), font_size=60, selection_color=(0, 0, 0),
                    font_name='Fonts/m3x6.ttf')
    menu.add.button('Quit', pygame_menu.events.EXIT, font_color=(0, 0, 0), font_size=60, selection_color=(0, 0, 0),
                    font_name='Fonts/m3x6.ttf')
    menu.mainloop(screen)


def load_restart_menu(score, color):
    const.level_list = ['Forest', 'Tokyo', 'Industrial', 'Apocalypsis', 'Plain']
    pygame.display.set_icon(pygame.image.load('icon.ico'))
    pygame.display.set_caption('DinoMight')
    pygame.mixer.music.load('Music/Ambients/MainMenu.wav')
    pygame.mixer.music.play(-1)
    mytheme = pygame_menu.themes.THEME_ORANGE.copy()
    mytheme.title_bar_style = pygame_menu.widgets.MENUBAR_STYLE_NONE
    myimage = pygame_menu.baseimage.BaseImage(
        image_path=f'BackGrounds/WinScreens/{color.lower()}.png',
        drawing_mode=pygame_menu.baseimage.IMAGE_MODE_REPEAT_XY
    )
    mytheme.background_color = myimage
    menu_restart = pygame_menu.Menu('', screen.get_width(), screen.get_height(),
                                    theme=mytheme)
    menu_restart.add.label(f"SCORE {score[0]}:{score[1]}", max_char=-1, font_size=200, font_color=(255, 0, 0),
                           align=pygame_menu.locals.ALIGN_LEFT, selection_color=(0, 0, 0), font_name='Fonts/m3x6.ttf')
    menu_restart.add.button('Restart', restart_game, font_color=(0, 0, 0), font_size=80,
                            align=pygame_menu.locals.ALIGN_LEFT,
                            selection_color=(0, 0, 0), font_name='Fonts/m3x6.ttf')
    menu_restart.add.button('Exit to main menu', load_menu, font_color=(0, 0, 0), font_size=80,
                            align=pygame_menu.locals.ALIGN_LEFT, selection_color=(0, 0, 0), font_name='Fonts/m3x6.ttf')
    menu_restart.add.button('Quit', pygame_menu.events.EXIT, font_color=(0, 0, 0), font_size=80,
                            align=pygame_menu.locals.ALIGN_LEFT, selection_color=(0, 0, 0), font_name='Fonts/m3x6.ttf')
    menu_restart.mainloop(screen)


def load_controller_menu():
    const.level_list = ['Forest', 'Tokyo', 'Industrial', 'Apocalypsis', 'Plain']
    pygame.display.set_icon(pygame.image.load('icon.ico'))
    pygame.display.set_caption('DinoMight')
    pygame.mixer.music.load('Music/Ambients/MainMenu.wav')
    pygame.mixer.music.play(-1)
    mytheme = pygame_menu.themes.THEME_ORANGE.copy()
    mytheme.title_bar_style = pygame_menu.widgets.MENUBAR_STYLE_NONE
    myimage = pygame_menu.baseimage.BaseImage(
        image_path='BackGrounds/ControllerMenu.png',
        drawing_mode=pygame_menu.baseimage.IMAGE_MODE_REPEAT_XY,
    )
    mytheme.background_color = myimage
    menu_restart = pygame_menu.Menu('', screen.get_width(), screen.get_height(),
                                    theme=mytheme)
    menu_restart.add.button('Continue', continue_game, font_color=(255, 255, 255), selection_color=(212, 213, 104),
                            align=pygame_menu.locals.ALIGN_LEFT, font_size=90, font_name='Fonts/m3x6.ttf')
    menu_restart.add.button('Restart', restart_game, font_color=(255, 255, 255), selection_color=(212, 213, 104),
                            align=pygame_menu.locals.ALIGN_LEFT, font_size=90, font_name='Fonts/m3x6.ttf')
    menu_restart.add.button('Exit to main menu', load_menu, font_color=(255, 255, 255), selection_color=(212, 213, 104),
                            align=pygame_menu.locals.ALIGN_LEFT, font_size=90, font_name='Fonts/m3x6.ttf')
    menu_restart.add.button('Quit', pygame_menu.events.EXIT, font_color=(255, 255, 255),
                            selection_color=(212, 213, 104),
                            align=pygame_menu.locals.ALIGN_LEFT, font_size=90, font_name='Fonts/m3x6.ttf')
    menu_restart.mainloop(screen)


def load_login_menu():
    const.score = [0, 0]
    const.block_gamepad_menu = False
    const.level_list = ['Forest', 'Tokyo', 'Industrial', 'Apocalypsis', 'Plain']
    pygame.display.set_icon(pygame.image.load('icon.ico'))
    pygame.display.set_caption('DinoMight')
    pygame.mixer.music.load('Music/Ambients/MainMenu.wav')
    pygame.mixer.music.play(-1)
    mytheme = pygame_menu.themes.THEME_ORANGE.copy()
    myimage = pygame_menu.baseimage.BaseImage(

        image_path=f'BackGrounds/MainMenu/{choice(os.listdir("BackGrounds/MainMenu/"))}',
        drawing_mode=pygame_menu.baseimage.IMAGE_MODE_REPEAT_XY
    )
    mytheme.background_color = myimage
    menu = pygame_menu.Menu('DinoMight', screen.get_width(), screen.get_height(),
                            theme=mytheme, joystick_enabled=False)
    menu.add.text_input('Login1: ',  onchange=save_name, player_num=1,   font_name='Fonts/m3x6.ttf', selection_color=(0, 0, 0), font_size=60)
    menu.add.text_input('Password: ', password=True,  font_name='Fonts/m3x6.ttf', selection_color=(0, 0, 0), font_size=60, onchange=save_password, player_num=1)

    menu.add.text_input('Login2: ', onchange=save_name, player_num=2,  font_color=(0, 0, 0), font_size=60, selection_color=(0, 0, 0),  font_name='Fonts/m3x6.ttf')
    menu.add.text_input('Password: ',  password=True, font_color=(0, 0, 0), font_size=60, selection_color=(0, 0, 0), font_name='Fonts/m3x6.ttf', onchange=save_password, player_num=2)
    menu.add.button('Submit', login, font_color=(0, 0, 0), font_size=60, selection_color=(0, 0, 0),
                    font_name='Fonts/m3x6.ttf')

    menu.mainloop(screen)


if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((1280, 720))
    load_login_menu()

# We did what we could
