import pygame

import os

import assets.scripts.dungeon as dungeon

class Entity:
    def __init__(self, x, y, width, height, speed, img):
        self.rect = pygame.Rect(x, y, width, height)
        self.speed = speed
        self.movement = [0, 0]
        f = os.getcwd()
        p = os.path.dirname(f)
        self.img = pygame.image.load(f"/assets/images/entity/{img}")
        self.direction = "up"

    def move(self, rooms):
        self.rect.x += self.speed * self.movement[0]
        self.rect.y += self.speed * self.movement[1]
        dungeon.collide(self, rooms)

    def draw(self, screen, scroll):
        if self.direction == "left":
            screen.blit(pygame.transform.rotate(self.img, -90),
                        (self.rect.x - scroll[0], self.rect.y - scroll[1]))
        elif self.direction == "right":
            screen.blit(pygame.transform.rotate(self.img, 90),
                        (self.rect.x - scroll[0], self.rect.y - scroll[1]))
        elif self.direction == "up":
            screen.blit(pygame.transform.rotate(self.img, 180),
                        (self.rect.x - scroll[0], self.rect.y - scroll[1]))
        else:
            screen.blit(self.img, (self.rect.x -
                        scroll[0], self.rect.y - scroll[1]))
