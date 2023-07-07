import pygame

import assets.scripts.weapon as weapon

class Inventory:
    def __init__(self, x, y):
        self.space = [["empty" for _ in range(9)] for _ in range(3)]
        self.hotbar = ["empty" for _ in range(9)]
        self.active_slot = 0
        self.item_carrying = "empty"
        self.pressed = False
        self.x = x
        self.y = y

    def draw_hotbar(self, screen):

        for spot, item in enumerate(self.hotbar):
            s = pygame.surface.Surface((75, 75))
            s.set_alpha(200)
            if spot == self.active_slot:
                s.fill((200, 200, 200))
            else:
                s.fill((127, 127, 127))
            screen.blit(s, (self.x - 450 + spot * 100, self.y, 75, 75))
            pygame.draw.rect(screen, (0, 0, 0), (self.x - 450 + spot * 100, self.y, 75, 75), 5)

            if isinstance(item, weapon.Sword):
                pygame.draw.rect(screen, (255, 255, 255), (self.x - 450 + 22 + spot * 100, self.y + 22, 32, 32))

    def draw(self, screen):
        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()[0]

        self.draw_hotbar(screen)

        for spot, item in enumerate(self.hotbar):
            rect = pygame.Rect(self.x - 450 + spot * 100, self.y, 75, 75)
            if mouse_pressed and rect.collidepoint(mouse_pos) and not self.pressed:
                if self.item_carrying == "empty":
                    self.item_carrying, self.hotbar[spot] = item, "empty"
                elif self.hotbar[spot] == "empty":
                    self.hotbar[spot], self.item_carrying = self.item_carrying, "empty"
                else:
                    self.hotbar[spot], self.item_carrying = self.item_carrying, self.hotbar[spot]

        for index, row in enumerate(self.space):
            for spot, item in enumerate(row):

                rect = pygame.Rect(self.x - 450 + spot * 100, self.y - 500 + index * 100, 75, 75)
                s = pygame.surface.Surface((75, 75))
                s.set_alpha(200)
                s.fill((127, 127, 127))

                screen.blit(s, rect)
                pygame.draw.rect(screen, (0, 0, 0), rect, 5)

                if isinstance(item, weapon.Sword):
                    pygame.draw.rect(screen, (255, 255, 255), (self.x - 450 + 22 + spot * 100, self.y -478 + index * 100, 32, 32))

                if mouse_pressed and rect.collidepoint(mouse_pos) and not self.pressed:
                    if self.item_carrying == "empty":
                        self.item_carrying, row[spot] = item, "empty"
                    elif row[spot] == "empty":
                        row[spot], self.item_carrying = self.item_carrying, "empty"
                    else:
                        row[spot], self.item_carrying = self.item_carrying, row[spot]

        if isinstance(self.item_carrying, weapon.Sword):
            pygame.draw.rect(screen, (255, 255, 255), (pygame.mouse.get_pos()[0] - 16, pygame.mouse.get_pos()[1] - 16, 32, 32))

        self.pressed = mouse_pressed
