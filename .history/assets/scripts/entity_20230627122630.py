import pygame
class Entity:
    def __init__(self, x, y, width, height, speed, img):
        self.rect = pygame.Rect(x, y, width, height)
        self.speed 
        self.img = img
        self.movement = [0, 0]
