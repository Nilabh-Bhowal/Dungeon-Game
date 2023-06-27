import pygame


def display_text(font, size, color, text, x, y, screen):
    font = pygame.font.Font(font, size)
    text = font.render(text, True, color)
    text_rect = text.get_rect()
    screen.blit(text, (x - text_rect.width // 2, y - text_rect.height // 2))


class Button:
    def __init__(self, font, size, color, text, x, y, width, height, text_color=(0, 0, 0)):
        self.font = font
        self.size = size
        self.color = color
        self.text = text
        self.rect = pygame.Rect(x, y, width, height)
        self.text_color = text_color

    def draw(self, screen):

        if self.rect.collidepoint(pygame.mouse.get_cursor()[0], pygame.mouse.get_cursor()[1]):
            hover = True
            if pygame.mouse.get_pressed()[0]:
                pressed = True
                print("a")
            else:
                pressed = False
        else:
            hover = False

        display_text(self.font, self.size, self.text_color, self.text, self.rect.x +
                     self.rect.width // 2, self.rect.y + self.rect.height // 2, screen)

        pygame.draw.rect(screen, self.color, self.rect)
        return pressed
