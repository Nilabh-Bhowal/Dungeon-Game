import pygame

def display_text(font, size, color, text, screen):
    font = pygame.font.Font(font, size)
    text = font.render(text, True, color)
    screen
