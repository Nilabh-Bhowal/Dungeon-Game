import pygame
import os
import assets.scripts.ui as ui

pygame.init()

screen = pygame.display.set_mode((800, 600))

test = ui.KeybindChanger(400, 300, "UP", pygame.K_UP)

running = True
while running:
    screen.fill((255, 255, 255))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        test.handle_input(event, pygame.mouse.get_pos())
    test.draw(screen)
    pygame.display.update()

pygame.quit()
