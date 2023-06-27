import pygame
class Entity:
    def __init__(self, x, y, width, height, speed, img):
        self.rect = pygame.Rect(x, y, width, height)
        self.speed = speed
        self.movement = [0, 0]
        self.img = img
        self.direction = "up"

    def move(self, rooms)
