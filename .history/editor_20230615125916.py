import pygame

import dungeon
import ui

pygame.init()

screen = pygame.display.set_mode((1280, 720))

def save(num, level):
    with open(f'levels/{num}.txt', 'a') as f:
        for item in level:
            f.write(f"{item} \n")

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

            if event.key == pygame.K_s:
                save(0, level)

        if event.type == pygame.KEYUP:
            if event.key in [pygame.K_RIGHT, pygame.K_LEFT]:
                cam_movement[0] = 0
            if event.key in [pygame.K_UP, pygame.K_DOWN]:
                cam_movement[1] = 0

    if pygame.mouse.get_pos()[0] <= 980 and pygame.mouse.get_pressed()[0] and not pressed:
        pressed = True
        if current_item == "room":
            level.append([0, pygame.mouse.get_pos()[0] +
                         scroll[0], pygame.mouse.get_pos()[1] + scroll[1]])
        elif current_item == "corridor":
            level.append([1, pygame.mouse.get_pos()[0] +
                         scroll[0], pygame.mouse.get_pos()[1] + scroll[1]])
    if not pygame.mouse.get_pressed()[0]:
        pressed = False

    if pygame.mouse.get_pos()[0] <= 980 and pygame.mouse.get_pressed()[2]:
        for room in level:
            if room[0] == 0 and room[1] < pygame.mouse.get_pos()[0] + scroll[0] < room[1] + 1024 and room[2] < pygame.mouse.get_pos()[1] + scroll[1] < room[2] + 1024:
                level.remove(room)
            if room[0] == 1 and room[1] < pygame.mouse.get_pos()[0] + scroll[0] < room[1] + 256 and room[2] < pygame.mouse.get_pos()[1] + scroll[1] < room[2] + 128:
                level.remove(room)

    scroll[0] += cam_movement[0] * 5
    scroll[1] += cam_movement[1] * 5

    screen.fill((255, 100, 100))
    for room in level:
        if room[0] == 0:
            pygame.draw.rect(screen, (50, 0, 205), (room[1] - scroll[0], room[2] - scroll[1], 1024, 1024))
        if room[0] == 1:
            pygame.draw.rect(screen, (50, 0, 205), (room[1] - scroll[0], room[2] - scroll[1], 256, 128))
    pygame.draw.rect(screen, (0, 0, 0), (980, 0, 300, 720))

    if room_button.draw(screen):
        current_item = "room"
    if corridor_button.draw(screen):
        current_item = "corridor"

    pygame.display.update()
    clock.tick(60)

pygame.quit()
