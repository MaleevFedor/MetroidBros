import pygame

OPTIONS_LOAD = pygame.USEREVENT + 1
tile_particle_path = 'Particle.png'
blood_particle_path = 'Blood Particle.png'
saw_sprite_list = []
saw_sprite_list.append(pygame.image.load('Saw/Saw1.png'))
saw_sprite_list.append(pygame.image.load('Saw/Saw2.png'))
saw_sprite_list.append(pygame.image.load('Saw/Saw3.png'))
saw_sprite_list.append(pygame.image.load('Saw/Saw4.png'))
saw_sprite_list.append(pygame.image.load('Saw/Saw5.png'))
saw_sprite_list.append(pygame.image.load('Saw/Saw6.png'))
saw_sprite_list.append(pygame.image.load('Saw/Saw7.png'))
saw_sprite_list.append(pygame.image.load('Saw/Saw8.png'))
level_list = ['Forest', 'Tokyo', 'Industrial', 'Apocalypsis', 'Plain']
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
print(1)
color1 = 'Yellow'
color2 = 'Yellow'