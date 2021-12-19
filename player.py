import pygame
import math


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, gravity, speed, jump_force, screen, weapon):
        super().__init__()
        self.screen = screen
        self.health = 20
        self.can_jump = True
        self.speed = 1
        self.image = pygame.Surface((40, 70))
        self.image.fill('green')
        self.rect = self.image.get_rect(topleft=pos)
        self.player_weapon = pygame.image.load(weapon)
        self.current_health = 200
        self.maximum_health = 1000
        self.health_bar_length = 40
        self.health_ratio = self.maximum_health / self.health_bar_length
        self.x = pos[0]
        self.y = pos[1]
        self.y += 30
        self.speed = speed
        self.gravity = gravity
        self.jump_force = jump_force
        self.extra_jumps = 2
        self.direction = pygame.math.Vector2(0.0, 0.0)

    def weapon_handling(self):
        offset = pygame.math.Vector2(0, 0)
        mouse_x, mouse_y = pygame.mouse.get_pos()
        rel_x, rel_y = mouse_x - self.rect.x, mouse_y - self.rect.y
        angle = (180 / math.pi) * math.atan2(rel_y, rel_x)
        rotated_image = pygame.transform.rotozoom(self.player_weapon, -angle, 1)  # Rotate the image.
        rotated_offset = offset.rotate(angle)
        rect = rotated_image.get_rect(center=self.rect.center + rotated_offset)
        self.screen.blit(rotated_image, rect)

    def get_damage(self, amount):
        if self.current_health > 0:
            self.current_health -= amount
        if self.current_health <= 0:
            self.current_health = 0

    def get_health(self, amount):
        if self.current_health < self.maximum_health:
            self.current_health += amount
        if self.current_health > self.maximum_health:
            self.current_health = self.maximum_health

    def basic_health(self):
        pass

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

    def jump(self):
        if self.extra_jumps > 0 and self.can_jump:
            if self.direction.y > 0:
                self.direction.y = 0
            self.direction.y += self.jump_force
            self.extra_jumps -= 1
            pygame.mixer.music.load('Music/jump.wav')
            pygame.mixer.music.play()
            self.can_jump = False

    def update(self, tiles):
        self.get_input()
        self.rect.x += self.direction.x
        for tile in tiles:
            if self.rect.colliderect(tile.rect):
                if self.direction.x > 0:
                    self.rect.right = tile.rect.left
                elif self.direction.x < 0:
                    self.rect.left = tile.rect.right

        self.i_hate_gravity()
        self.rect.y += self.direction.y
        for tile in tiles:
            if self.rect.colliderect(tile.rect):
                if self.direction.y > 0:
                    self.rect.bottom = tile.rect.top
                    self.extra_jumps = 2
                elif self.direction.y < 0:
                    self.rect.top = tile.rect.bottom
                self.direction.y = 0


class Player2(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.x = pos[0]
        self.y = pos[1]
        self.image = pygame.Surface((40, 70))
        self.image.fill('red')
        self.rect = self.image.get_rect(topleft=pos)
        self.player_weapon = pygame.Surface((50, 5), pygame.SRCALPHA)

