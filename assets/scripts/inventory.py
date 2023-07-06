import pygame

class Inventory:
    def __init__(self, x, y):
        self.space = [[], [], []]
        for row in self.space:
            row.extend("empty" for _ in range(9))
        self.hotbar = []
        self.hotbar.extend("empty" for _ in range(9))
        self.active_slot = 0
        self.x = x
        self.y = y

    def draw(self, screen):
        for spot, item in enumerate(self.hotbar):
            s = pygame.surface.Surface((75, 75))
            s.set_alpha(200)
            if spot == self.active_slot:
                s.fill((200, 200, 200))
            else:
                s.fill((127, 127, 127))
            screen.blit(s, (self.x - 450 + spot * 100, self.y, 75, 75))
            pygame.draw.rect(screen, (0, 0, 0), (self.x - 450 + spot * 100, self.y, 75, 75), 5)

            if item == "sword":
                pygame.draw.rect(screen, (255, 255, 255), (self.x - 450 + 22 + spot * 100, self.y + 22, 32, 32))
