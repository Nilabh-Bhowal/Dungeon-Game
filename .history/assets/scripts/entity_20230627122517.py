import pygame
class Entity:
    def __init__(x, y, width, height, img):
        self.rect = pygame.Rect(x, y, width, height)
