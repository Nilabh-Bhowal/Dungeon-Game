import pygame

import dungeon
import ui

pygame.init()

screen = pygame.display.set_mode((1280, 720))

scroll = [0, 0]
cam_movement = [0, 0]

level = []
current_item = "room"

pressed = False

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

    if pygame.mouse.get_pos()[0] <= 980 and pygame.mouse.get_pressed()[0] and not pressed:
        pressed = True
        if current_item == "corridor":
            level.append(["corridor", pygame.mouse.get_pos()[0] +
                         scroll[0], pygame.mouse.get_pos()[1] + scroll[1]])
        elif current_item == "room":
            level.append(["room", pygame.mouse.get_pos()[0] +
                         scroll[0], pygame.mouse.get_pos()[1] + scroll[1]])
    if not pygame.mouse.get_pressed()[0]:
        pressed = False

    print(pygame.mouse.get_pressed())

    if pygame.mouse.get_pos()[0] <= 980 and pygame.mouse.get_pressed()[2]:
        for room in level:
            if room[0] == "corridor" and room[1] < pygame.mouse.get_pos()[0] < room[1] + 256 and room[2] < pygame.mouse.get_pos()[1] < room[2] + 128:
                level.remove(room)
            if room[0] == "room" and room[1] < pygame.mouse.get_pos()[0] < room[1] + 256 and room[2] < pygame.mouse.get_pos()[1] < room[2] + 128:
                level.remove(room)

    scroll[0] += cam_movement[0] * 5
    scroll[1] += cam_movement[1] * 5

    screen.fill((255, 100, 100))
    for room in level:
        room.draw(screen, scroll)
    pygame.draw.rect(screen, (0, 0, 0), (980, 0, 300, 720))

    if room_button.draw(screen):
        current_item = "room"
    if corridor_button.draw(screen):
        current_item = "corridor"

    pygame.display.update()
    clock.tick(60)

pygame.quit()
