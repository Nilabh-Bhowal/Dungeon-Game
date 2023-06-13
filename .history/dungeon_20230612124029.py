import pygame

class DungeonRoom:
    def __init__(self):
        self.rect = pygame.Rect(128, -152, 1024, 1024)
        self.color = (50, 0, 205)

    def draw(self, screen, scroll):
        pygame.draw.rect(screen, self.color, (self.rect.x - scroll[0], self.rect.y - scroll[1], self.rect.width, self.rect.height))