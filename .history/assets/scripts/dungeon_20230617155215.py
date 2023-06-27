import random

import pygame


class DungeonRoom:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 512, 512)
        self.color = (50, 0, 205)

    def draw(self, screen, scroll):
        pygame.draw.rect(screen, self.color,
                         (self.rect.x - scroll[0], self.rect.y - scroll[1], self.rect.width, self.rect.height))


class Corridor:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 128, 64)
        self.color = (50, 0, 205)

    def draw(self, screen, scroll):
        pygame.draw.rect(screen, self.color,
                         (self.rect.x - scroll[0], self.rect.y - scroll[1], self.rect.width, self.rect.height))


class Chest:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 64, 32)
        self.color = (255, 175, 112)

    def generate_loot():
        pass

    def draw(self, screen, scroll):
        pygame.draw.rect(screen, self.color,
                         (self.rect.x - scroll[0], self.rect.y - scroll[1], self.rect.width, self.rect.height))
