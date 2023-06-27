import pygame

def display_text(font, size, color, text, x, y, screen):
    font = pygame.font.Font(font, size)
    text = font.render(text, True, color)
    text_rect = text.get_rect()
    screen.blit(text, (x - text_rect.width // 2, y - text_rect.height // 2))


class Button:
    def __init__(font, size, text_color)
