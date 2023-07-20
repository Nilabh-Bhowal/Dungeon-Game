import pygame
import math
import random

import assets.scripts.dungeon as dungeon

class Entity:
    def __init__(self, x, y, width, height, speed, health, img):
        self.rect = pygame.Rect(x, y, width, height)
        self.speed = speed
        self.movement = [0, 0]
        self.img = pygame.image.load(f"assets/images/entity/{img}").convert()
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
                self.rect.x -= self.immune_timer * dt
            elif self.knockback_direction == "right":
                self.rect.x += self.immune_timer * dt
            elif self.knockback_direction == "up":
                self.rect.y -= self.immune_timer * dt
            else:
                self.rect.y += self.immune_timer * dt
        dungeon.collide(self, rooms)

    def draw(self, screen, scroll, scale=1):
        x = (self.rect.x * scale - scroll[0])
        y = (self.rect.y * scale - scroll[1])
        width = self.rect.width * scale
        height = self.rect.height * scale
        if (self.rect.left - scroll[0] <= 1280 and self.rect.right - scroll[0] >= 0) and (self.rect.top - scroll[1] <= 720 and self.rect.bottom - scroll[1] >= 0):
            if self.direction == "left":
                screen.blit(pygame.transform.scale(pygame.transform.rotate(self.img, -90), (width, height)), (x, y))
            elif self.direction == "right":
                screen.blit(pygame.transform.scale(pygame.transform.rotate(self.img, 90), (width, height)), (x, y))
            elif self.direction == "up":
                screen.blit(pygame.transform.scale(pygame.transform.rotate(self.img, 180), (width, height)), (x, y))
            else:
                screen.blit(pygame.transform.scale(self.img, (width, height)), (x, y))
