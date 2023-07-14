import pygame


def title(text, x, y, screen):
    font = pygame.font.Font("assets/fonts/PressStart2p.ttf", 40)
    text = font.render(text, True, (0, 0, 0))
    text_rect = text.get_rect()
    screen.blit(text, (x - text_rect.width // 2, y - text_rect.height // 2))



class Button:
    def __init__(self, text, x, y, width, height):
        self.text = text
        self.rect = pygame.Rect(0, 0, width, height)
        self.rect.centerx = x
        self.rect.centery = y
        self.clicked = True

    def draw(self, screen):
        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()[0]

        if self.rect.collidepoint(mouse_pos):
            if mouse_pressed:
                if not self.clicked:
                    return self.normal_draw(True, screen)
                self.clicked = True
            else:
                self.clicked = False
            return self.hover_draw(screen)
        else:
            self.clicked = bool(mouse_pressed)
            return self.normal_draw(False, screen)


    def hover_draw(self, screen):
        pygame.draw.rect(screen, (255, 255, 255), (self.rect.x - 15,
                         self.rect.y - 15, self.rect.width + 30, self.rect.height + 30))

        self.draw_text(screen)
        return False

    def normal_draw(self, pressed, screen):
        result = pressed
        pygame.draw.rect(screen, (255, 255, 255), self.rect)

        self.draw_text(screen)
        return(result)

    def draw_text(self, screen):
        font = pygame.font.Font("assets/fonts/PressStart2p.ttf", 20)
        text = font.render(self.text, True, (0, 0, 0))
        text_rect = text.get_rect()
        screen.blit(
            text,
            (
                self.rect.centerx - text_rect.width // 2,
                self.rect.centery - text_rect.height // 2,
            ),
        )


class PromptBox:
    def __init__(self, message):
        self.rect = pygame.Rect(290, 110, 700, 500)
        self.message = message
        self.input = ""
        self.prompted = False
        self.text_box_rect = pygame.Rect(self.rect.x + 50, self.rect.y + 200, 600, 50)
        self.clicked_in = False

    def prompt(self):
        self.prompted = False
        self.input = ""

    def handle_input(self, event):
        if not self.prompted:
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.clicked_in = bool(self.text_box_rect.collidepoint(pygame.mouse.get_pos()))
            if self.clicked_in and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.prompted = True
                elif event.key == pygame.K_BACKSPACE:
                    self.input = self.input[:-1]
                elif event.key == pygame.K_SPACE:
                    self.input = f"{self.input} "
                else:
                    self.input += event.unicode

    def draw(self, screen):
        if self.prompted:
            return self.input
        pygame.draw.rect(screen, (100, 100, 100), self.rect)
        title(self.message, self.rect.centerx, self.rect.top + 50, screen)
        pygame.draw.rect(screen, (255, 255, 255), self.text_box_rect)
        text_rect = self.draw_text(screen, self.input, self.text_box_rect.left + 5, self.text_box_rect.top + 5)
        if self.clicked_in:
            if len(self.input) > 0:
                pygame.draw.rect(screen, (0, 0, 0), (text_rect.right + 5, text_rect.top, 5, 40))
            else:
                pygame.draw.rect(screen, (0, 0, 0), (self.text_box_rect.left + 5, self.text_box_rect.top + 5, 5, 40))

    def draw_text(self, screen, text, x, y, center=False):
        font = pygame.font.Font("assets/fonts/PressStart2p.ttf", 40)
        text = font.render(text, True, (0, 0, 0))
        if center:
            text_rect = text.get_rect()
            screen.blit(text, (x - text_rect.width / 2, y - text_rect.height / 2))
        else:
            screen.blit(text, (x, y))
            return pygame.Rect(x, y, text.get_rect().width, text.get_rect().height)
