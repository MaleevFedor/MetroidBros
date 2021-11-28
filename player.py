import pygame


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, gravity, speed, jump_force):
        #отхождение от туториала, сделал переменные гравитации и скорости в классе Level
        #чтобы можно было менять скорость игроков и гравитацию на разных уровнях
        super().__init__()
        self.speed = 1
        self.image = pygame.Surface((40, 80))
        self.image.fill('green')
        self.rect = self.image.get_rect(topleft=pos)

        #movement
        self.speed = speed
        self.gravity = gravity
        self.jump_force = jump_force
        self.extra_jumps = 2
        self.direction = pygame.math.Vector2(0.0, 0.0)

    def get_input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.direction.x = self.speed
        elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.direction.x = -self.speed
        else:
            self.direction.x = 0

        if keys[pygame.K_SPACE]:
            self.jump()

    def i_hate_gravity(self):
        self.direction.y += self.gravity
        self.rect.y += self.direction.y

    def jump(self):
        if self.extra_jumps > 0:
            self.direction.y += self.jump_force
            self.extra_jumps -= 1

    def update(self):
        self.get_input()
        self.rect.x += self.direction.x
        self.i_hate_gravity()
