import pygame


PASSWORD_CHECK_ADRESS = 'http://127.0.0.1:80/game_login'
ELO_CHECK_ADRESS = 'http://127.0.0.1:80/player_elo'
ELO_CHANGE_ADRESS = 'http://127.0.0.1:80/change_elo'

STATISTIC_CHECK_ADRESS = 'http://127.0.0.1:80/stats'
STATISTIC_MATCH_ADRESS = 'http://127.0.0.1:80/stats_match'
STATISTIC_MATCH_ADRESS = 'http://127.0.0.1:80/stats_match'

OPTIONS_LOAD = pygame.USEREVENT + 1
tile_particle_path = 'Particles/Particle.png'
blood_particle_path = 'Particles/Blood Particle.png'
heal_particle_path = 'Particles/HealParticle.png'
slime_particle = 'Particles/SlimeParticle.png'
MedKitDestroy_path = 'Particles/MedKitParticle.png'
trampoline_path = 'Particles/TrampolineParticle.png'
saw_sprite_list = list()
saw_sprite_list.append(pygame.image.load('Tiles/Saw/Saw1.png'))
saw_sprite_list.append(pygame.image.load('Tiles/Saw/Saw2.png'))
saw_sprite_list.append(pygame.image.load('Tiles/Saw/Saw3.png'))
saw_sprite_list.append(pygame.image.load('Tiles/Saw/Saw4.png'))
saw_sprite_list.append(pygame.image.load('Tiles/Saw/Saw5.png'))
saw_sprite_list.append(pygame.image.load('Tiles/Saw/Saw6.png'))
saw_sprite_list.append(pygame.image.load('Tiles/Saw/Saw7.png'))
saw_sprite_list.append(pygame.image.load('Tiles/Saw/Saw8.png'))
level_ended = pygame.USEREVENT + 2
timer_breaker = pygame.USEREVENT + 3
open_med = pygame.image.load('Tiles/MedKit/OpenMedKit.png')
close_med = pygame.image.load('Tiles/MedKit/CloseMedKit.png')
volume = 0.5
level_list = ['Forest', 'Tokyo', 'Industrial', 'Apocalypsis', 'Plain']
block_gamepad_menu = False
button_keys = {
    "x": 0,
    "circle": 1,
    "square": 2,
    "triangle": 3,
    "share": 4,
    "PS": 5,
    "options": 6,
    "left_stick_click": 7,
    "right_stick_click": 8,
    "L1": 9,
    "R1": 10,
    "up_arrow": 11,
    "down_arrow": 12,
    "left_arrow": 13,
    "right_arrow": 14,
    "touchpad": 15

}
color1 = 'Blue'
color2 = 'Red'
score = [0, 0]
player1_name = ''
player2_name = ''
player1_password = ''
player2_password = ''

match_kills = 0
match_deaths = 0
match_hp_healed = 0
match_saws_deaths = 0
match_shot = 0
match_hits = 0
match_result = ''


match_kills_2 = 0
match_deaths_2 = 0
match_hp_healed_2 = 0
match_saws_deaths_2 = 0
match_shot_2 = 0
match_hits_2 = 0
match_result_2 = ''
