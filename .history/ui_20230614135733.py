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
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text
