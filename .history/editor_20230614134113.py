import pygame

pygame.init()

screen = pygame.display.set_mode((1280, 720))

scroll = [0, 0]

cam_movement = [0, 0]

running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:

    screen.fill((255, 100, 100))
    pygame.draw.rect(screen, (0, 0, 0), (980, 0, 300, 720))

    pygame.display.update()

pygame.quit()
