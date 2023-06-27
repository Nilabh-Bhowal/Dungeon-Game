import pygame

def display_text(font, size, color, text, x, y, screen):
    font = pygame.font.Font(font, size)
    text = font.render(text, True, color)
    text_rect = text.get_rect()
    screen.blit(text, (x - te, y))
