import pygame


def display_text(font_file, size, color, text, x, y, screen):
    font = pygame.font.SysFont(font_file, size)
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

        if self.rect.collidepoint(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]):
            if pygame.mouse.get_pressed()[0]:
                pressed = True
                pygame.draw.rect(screen, self.color, self.rect)
                display_text(self.font, self.size, self.text_color, self.text, self.rect.x +
                     self.rect.width // 2, self.rect.y + self.rect.height // 2, screen)
            else:
                pressed = False
                pygame.draw.rect(screen, self.color, (self.rect.x - 5,
                                 self.rect.y - 5, self.rect.width + 10, self.rect.height + 10))
        else:
            pressed = False
            pygame.draw.rect(screen, self.color, self.rect)
            display_text(self.font, self.size, self.text_color, self.text, self.rect.x +
                     self.rect.width // 2, self.rect.y + self.rect.height // 2, screen)


        return pressed
