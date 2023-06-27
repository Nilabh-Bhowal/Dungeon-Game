import pygame

pygame.init()

screen = pygame.display.set_mode((1280, 720))

running = True
while running:

    for event in pygame.events.get():
        if event.type == pygame.QUIT:
            running = False

pygame.quit()
