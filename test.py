import pygame
import os
import assets.scripts.animation as animation

pygame.init()

screen = pygame.display.set_mode((800, 600))

test = animation.Animation("bow")

clock = pygame.time.Clock()

running = True
while running:
    screen.fill((255, 255, 255))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if clock.get_time() >= 60:
        test.change_animation("attack")
    test.update(1)
    screen.blit(test.get_image(), (0, 0))
    pygame.display.update()
    clock.tick(60)

pygame.quit()
