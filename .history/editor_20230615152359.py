import pygame

import dungeon
import ui

pygame.init()

screen = pygame.display.set_mode((1280, 720))


def save(num, level):
    with open(f'levels/{num}.txt', 'w') as f:
        for item in level:
            if isinstance(item, dungeon.DungeonRoom):
                l = 0
            elif isinstance(item, dungeon.Corridor):
                l = 1
            f.write(f"[{l}, {item.rect.x}, {item.rect.y}]\n")


def check_collision(rect, level, scroll):
    for item in level:
        if rect != item.rect and item.rect.colliderect(rect):
            if rect.bottom > item.rect.top and pygame.mouse.get_pos()[1] < item.rect.top:
                rect.bottom = item.rect.top
            elif rect.top < item.rect.bottom and pygame.mouse.get_pos()[1] > item.rect.bottom:
                rect.top = item.rect.bottom
            if rect.right > item.rect.left and pygame.mouse.get_pos()[0] < item.rect.left:
                rect.right = item.rect.left
            elif rect.left < item.rect.right and pygame.mouse.get_pos()[0] > item.rect.right:
                rect.left = item.rect.right


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
            level.append(dungeon.DungeonRoom((pygame.mouse.get_pos()[
                         0] + scroll[0]) - 512, pygame.mouse.get_pos()[1] + scroll[1] - 512))
        elif current_item == "corridor":
            level.append(dungeon.Corridor(pygame.mouse.get_pos()[
                         0] + scroll[0] - 128, pygame.mouse.get_pos()[1] + scroll[1] - 64))
    if not pygame.mouse.get_pressed()[0]:
        pressed = False

    if pygame.mouse.get_pos()[0] <= 980 and pygame.mouse.get_pressed()[2]:
        for room in level:
            if room.rect.collidepoint((pygame.mouse.get_pos()[0] + scroll[0], pygame.mouse.get_pos()[1] + scroll[1])):
                level.remove(room)

    for item in reversed(level):
        check_collision(item.rect, level, scroll)

    scroll[0] += cam_movement[0] * 20
    scroll[1] += cam_movement[1] * 20

    screen.fill((255, 100, 100))
    for room in level:
        room.draw(screen, scroll)
    for i in range(17):
        pygame.draw.line(screen, (0, 0, 0), (i * 64 - scroll[0] % 64, 0), (i * 64 - scroll[0] % 64, 720))
    for i in range(13):
        pygame.draw.line(screen, (0, 0, 0), (0, i * 64 - scroll[1] % 64), (980, i * 64 - scroll[1] % 64))
    pygame.draw.rect(screen, (0, 0, 0), (980, 0, 300, 720))

    if room_button.draw(screen):
        current_item = "room"
    if corridor_button.draw(screen):
        current_item = "corridor"

    pygame.display.update()
    clock.tick(60)

pygame.quit()
