import pygame

import assets.scripts.dungeon as dungeon

class Entity:
    def __init__(self, x, y, width, height, speed, health, img):
        self.rect = pygame.Rect(x, y, width, height)
        self.speed = speed
        self.movement = [0, 0]
        self.img = pygame.image.load(f"assets/images/entity/{img}")
        self.direction = "up"
        self.state = "idle"
        self.health = health
        self.alive = True
        self.immune = False
        self.immune_timer = 15

    def move(self, dt, rooms):
        self.rect.x += self.speed * self.movement[0] * dt
        self.rect.y += self.speed * self.movement[1] * dt
        if self.state == "stunned":
            self.movement = [0, 0]
            if self.knockback_direction == "left":
                self.rect.x -= self.immune_timer
            elif self.knockback_direction == "right":
                self.rect.x += self.immune_timer
            elif self.knockback_direction == "up":
                self.rect.y -= self.immune_timer
            else:
                self.rect.y += self.immune_timer
        dungeon.collide(self, rooms)

    def draw(self, screen, scroll):
        if self.direction == "left":
            screen.blit(pygame.transform.rotate(self.img, -90), (self.rect.x - scroll[0], self.rect.y - scroll[1]))
        elif self.direction == "right":
            screen.blit(pygame.transform.rotate(self.img, 90), (self.rect.x - scroll[0], self.rect.y - scroll[1]))
        elif self.direction == "up":
            screen.blit(pygame.transform.rotate(self.img, 180), (self.rect.x - scroll[0], self.rect.y - scroll[1]))
        else:
            screen.blit(self.img, (self.rect.x - scroll[0], self.rect.y - scroll[1]))
