import pygame

import dungeon
import ui

pygame.init()

screen = pygame.display.set_mode((1280, 720))

scroll = [0, 0]
cam_movement = [0, 0]

level = []
current_item = ""

clock = pygame.time.Clock()

room_button = ui.Button("Comic Sans MS", 15, (255, 255, 0),
                        "Dungeon Room", 1000, 200, 200, 50)
corridor_button = ui.Button(
    "Comic Sans MS", 15, (255, 255, 0), "Corridor", 1000, 300, 200, 50)

running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                cam_movement[0] = 1
            if event.key == pygame.K_LEFT:
                cam_movement[0] = -1
            if event.key == pygame.K_DOWN:
                cam_movement[1] = 1
            if event.key == pygame.K_UP:
                cam_movement[1] = -1

        if event.type == pygame.KEYUP:
            if event.key in [pygame.K_RIGHT, pygame.K_LEFT]:
                cam_movement[0] = 0
            if event.key in [pygame.K_UP, pygame.K_DOWN]:
                cam_movement[1] = 0

    scroll[0] += cam_movement[0] * 5
    scroll[1] += cam_movement[1] * 5

    screen.fill((255, 100, 100))
    pygame.draw.rect(screen, (0, 0, 0), (980, 0, 300, 720))


    pygame.display.update()
    clock.tick(60)

pygame.quit()
