import pygame

pygame.init()

screen = pygame.display.set_mode((600, 800))

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    key = pygame.key.get_pressed()

    print(int(key[pygame.K_RIGHT]) - int(key[pygame.K_LEFT]))

    pygame.display.update()

pygame.quit()
