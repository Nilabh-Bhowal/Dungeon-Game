import pygame

class Inventory:
    def __init__(self):
        self.space = [["empty" for _ in range(9)] for _ in range(3)]
        self.hotbar = ["empty" for _ in range(9)]
        self.active_slot = 0
        self.item_carrying = "empty"
        self.pressed = False
        self.x = 640
        self.y = 600

    def handle_mouse_interaction(self):
        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()[0]

        self.item_carrying = self.handle_hotbar_mouse_interaction(self.item_carrying)

        for index, row in enumerate(self.space):
            for spot, item in enumerate(row):
                rect = pygame.Rect(self.x - 450 + spot * 100, self.y - 500 + index * 100, 75, 75)

                if mouse_pressed and rect.collidepoint(mouse_pos) and not self.pressed:
                    if self.item_carrying == "empty":
                        self.item_carrying, row[spot] = item, "empty"
                    elif row[spot] == "empty":
                        print("a")
                        row[spot], self.item_carrying = self.item_carrying, "empty"
                    else:
                        row[spot], self.item_carrying = self.item_carrying, row[spot]

        self.pressed = mouse_pressed

    def handle_hotbar_mouse_interaction(self, item_carrying):
        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()[0]
        for spot, item in enumerate(self.hotbar):
            rect = pygame.Rect(self.x - 450 + spot * 100, self.y, 75, 75)
            if mouse_pressed and rect.collidepoint(mouse_pos) and not self.pressed:
                if item_carrying == "empty":
                    item_carrying, self.hotbar[spot] = item, "empty"
                elif self.hotbar[spot] == "empty":
                    self.hotbar[spot], item_carrying = item_carrying, "empty"
                else:
                    self.hotbar[spot], item_carrying = item_carrying, self.hotbar[spot]

        self.pressed = mouse_pressed
        return item_carrying

    def draw(self, screen):
        self.handle_mouse_interaction()

        self.draw_hotbar(screen)
        self.draw_inventory_space(screen)

        if self.item_carrying == "sword":
            pygame.draw.rect(screen, (255, 255, 255),
                             (pygame.mouse.get_pos()[0] - 16, pygame.mouse.get_pos()[1] - 16, 32, 32))
        elif self.item_carrying == "bow":
                    pygame.draw.rect(screen, (0, 255, 0), (pygame.mouse.get_pos()[0] - 16, pygame.mouse.get_pos()[1] - 16, 32, 32))
        if isinstance(self.item_carrying, list) and self.item_carrying[0] == "key":
                    pygame.draw.rect(screen, (255, 0, 0), (pygame.mouse.get_pos()[0] - 16, pygame.mouse.get_pos()[1] - 16, 32, 32))


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

            if item == "sword":
                pygame.draw.rect(screen, (255, 255, 255), (self.x - 450 + 22 + spot * 100, self.y + 22, 32, 32))
            elif item == "bow":
                pygame.draw.rect(screen, (0, 255, 0), (self.x - 450 + 22 + spot * 100, self.y + 22, 32, 32))
            if isinstance(item, list) and item[0] == "key":
                    pygame.draw.rect(screen, (255, 0, 0), (self.x - 450 + 22 + spot * 100, self.y + 22, 32, 32))


    def draw_inventory_space(self, screen):

        for index, row in enumerate(self.space):
            for spot, item in enumerate(row):

                rect = pygame.Rect(self.x - 450 + spot * 100, self.y - 500 + index * 100, 75, 75)
                s = pygame.surface.Surface((75, 75))
                s.set_alpha(200)
                s.fill((127, 127, 127))

                screen.blit(s, rect)
                pygame.draw.rect(screen, (0, 0, 0), rect, 5)

                if item == "sword":
                    pygame.draw.rect(screen, (255, 255, 255), (self.x - 450 + 22 + spot * 100, self.y -478 + index * 100, 32, 32))
                elif item == "bow":
                    pygame.draw.rect(screen, (0, 255, 0), (self.x - 450 + 22 + spot * 100, self.y -478 + index * 100, 32, 32))
                if isinstance(item, list) and item[0] == "key":
                    pygame.draw.rect(screen, (255, 0, 0), (self.x - 450 + 22 + spot * 100, self.y -478 + index * 100, 32, 32))



class ChestStorage:
    def __init__(self):
        self.space = [["empty" for _ in range(9)] for _ in range(3)]
        self.item_carrying = "empty"
        self.pressed = False
        self.x = 640
        self.y = 600

    def handle_mouse_interaction(self, item_carrying):
        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()[0]

        for index, row in enumerate(self.space):
            for spot, item in enumerate(row):
                rect = pygame.Rect(self.x - 450 + spot * 100, self.y - 500 + index * 100, 75, 75)

                if mouse_pressed and rect.collidepoint(mouse_pos) and not self.pressed:
                    if item_carrying == "empty":
                        item_carrying, row[spot] = item, "empty"
                    elif row[spot] == "empty":
                        row[spot], item_carrying = item_carrying, "empty"
                    else:
                        row[spot], item_carrying = item_carrying, row[spot]

        self.pressed = mouse_pressed
        return item_carrying

    def draw(self, item_carrying, screen):
        self.item_carrying = self.handle_mouse_interaction(item_carrying)

        self.draw_storage_space(screen)

        if self.item_carrying == "sword":
            pygame.draw.rect(screen, (255, 255, 255),
                             (pygame.mouse.get_pos()[0] - 16, pygame.mouse.get_pos()[1] - 16, 32, 32))
        elif self.item_carrying == "bow":
                    pygame.draw.rect(screen, (0, 255, 0), (pygame.mouse.get_pos()[0] - 16, pygame.mouse.get_pos()[1] - 16, 32, 32))
        if isinstance(self.item_carrying, list) and self.item_carrying[0] == "key":
                    pygame.draw.rect(screen, (255, 0, 0), (pygame.mouse.get_pos()[0] - 16, pygame.mouse.get_pos()[1] - 16, 32, 32))
        return self.item_carrying


    def draw_storage_space(self, screen):

        for index, row in enumerate(self.space):
            for spot, item in enumerate(row):

                rect = pygame.Rect(self.x - 450 + spot * 100, self.y - 500 + index * 100, 75, 75)
                s = pygame.surface.Surface((75, 75))
                s.set_alpha(200)
                s.fill((127, 127, 127))

                screen.blit(s, rect)
                pygame.draw.rect(screen, (0, 0, 0), rect, 5)

                if item == "sword":
                    pygame.draw.rect(screen, (255, 255, 255), (self.x - 450 + 22 + spot * 100, self.y -478 + index * 100, 32, 32))
                if item == "bow":
                    pygame.draw.rect(screen, (0, 255, 0), (self.x - 450 + 22 + spot * 100, self.y -478 + index * 100, 32, 32))
                if isinstance(item, list) and item[0] == "key":
                    pygame.draw.rect(screen, (255, 0, 0), (self.x - 450 + 22 + spot * 100, self.y -478 + index * 100, 32, 32))
