import pygame
import assets.scripts.dungeon as dungeon
import assets.scripts.enemy as enemy
import assets.scripts.ui as ui

pygame.init()

screen = pygame.display.set_mode((1280, 720))

def save(num, level, items):
    with open(f'assets/levels/{num}.txt', 'w') as f:
        for room in level:
            if isinstance(room, dungeon.DungeonRoom):
                l = 0
            elif isinstance(room, dungeon.Corridor):
                l = 1

            f.write(f"[{l}, {room.rect.x}, {room.rect.y}]\n")

        for item in items:
            if isinstance(item, dungeon.Chest):
                l = 2
            elif isinstance(item, enemy.Zombie):
                l = 3
            elif isinstance(item, dungeon.End):
                l = 4
            if isinstance(item, dungeon.LevelEnter):
                l = 5
                level = item.level
                f.write(f"[{l}, {item.rect.x}, {item.rect.y}, {level}]\n")
            else:
                f.write(f"[{l}, {item.rect.x}, {item.rect.y}, False]\n")

def load(num):
    with open(f'assets/levels/{num}.txt', 'r') as f:
        items = (f.read().splitlines())
        items = [eval(item) for item in items]
        level = []
        things = []
        for item in items:
            if item[0] == 0:
                level.append(dungeon.DungeonRoom(item[1], item[2]))
            elif item[0] == 1:
                level.append(dungeon.Corridor(item[1], item[2]))
            elif item[0] == 2:
                things.append(dungeon.Chest(item[1], item[2]))
            elif item[0] == 3:
                things.append(enemy.Zombie(item[1], item[2]))
            elif item[0] == 4:
                things.append(dungeon.End(item[1], item[2]))
            elif item[0] == 5:
                things.append(dungeon.LevelEnter(item[1], item[2], item[3]))

    return level, things

def check_collision(placed, level, scroll):
    for item in level:
        if placed != item and item.rect.colliderect(placed.rect) and not isinstance(placed, dungeon.Chest) and not isinstance(item, dungeon.Chest) and not isinstance(item, enemy.Enemy) and not isinstance(placed, enemy.Enemy):
            if placed.rect.bottom > item.rect.top and pygame.mouse.get_pos()[1] + scroll[1] < item.rect.top:
                placed.rect.bottom = item.rect.top
            elif placed.rect.top < item.rect.bottom and pygame.mouse.get_pos()[1] + scroll[1] > item.rect.bottom:
                placed.rect.top = item.rect.bottom
            if placed.rect.right > item.rect.left and pygame.mouse.get_pos()[0] + scroll[0] < item.rect.left:
                placed.rect.right = item.rect.left
            elif placed.rect.left < item.rect.right and pygame.mouse.get_pos()[0] + scroll[0] > item.rect.right:
                placed.rect.left = item.rect.right

scroll = [0, 0]
cam_movement = [0, 0]
scale = 1.0

rooms = []
items = []
current_item = "Room"
level = 0
level_enter_level = 0
s = 0

pressed = False

clock = pygame.time.Clock()
buttons = [ui.Button("Room", 1130, 200, 200, 50), ui.Button("Corridor", 1130, 300, 200, 50), ui.Button("Chest", 1130, 400, 200, 50), ui.Button("Zombie", 1130, 500, 200, 50), ui.Button("End", 1130, 600, 200, 50), ui.Button("Level Enter", 1130, 700, 200, 50)]

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
                save(level, rooms, items)
            if event.key == pygame.K_l:
                rooms, items = load(level)
            if event.key == pygame.K_c:
                rooms = []
                items = []
                scroll = [0, 0]
            if event.key == pygame.K_r:
                scroll = [-640, -360]

            if current_item == "Level Enter":
                if event.key == pygame.K_1:
                    level_enter_level = 1
                elif event.key == pygame.K_2:
                    level_enter_level = 2
                elif event.key == pygame.K_3:
                    level_enter_level = 3
                elif event.key == pygame.K_4:
                    level_enter_level = 4
                elif event.key == pygame.K_5:
                    level_enter_level = 5
                elif event.key == pygame.K_6:
                    level_enter_level = 6
                elif event.key == pygame.K_7:
                    level_enter_level = 7
                elif event.key == pygame.K_8:
                    level_enter_level = 8
                elif event.key == pygame.K_9:
                    level_enter_level = 9
            else:
                if event.key == pygame.K_0:
                    level = 0
                    rooms = []
                    items = []
                elif event.key == pygame.K_1:
                    level = 1
                    rooms = []
                    items = []
                elif event.key == pygame.K_2:
                    level = 2
                    rooms = []
                    items = []
                elif event.key == pygame.K_3:
                    level = 3
                    rooms = []
                    items = []
                elif event.key == pygame.K_4:
                    level = 4
                    rooms = []
                    items = []
                elif event.key == pygame.K_5:
                    level = 5
                    rooms = []
                    items = []
                elif event.key == pygame.K_6:
                    level = 6
                    rooms = []
                    items = []
                elif event.key == pygame.K_7:
                    level = 7
                    rooms = []
                    items = []
                elif event.key == pygame.K_8:
                    level = 8
                    rooms = []
                    items = []
                elif event.key == pygame.K_9:
                    level = 9
                    rooms = []
                    items = []

        if event.type == pygame.KEYUP:
            if event.key in [pygame.K_RIGHT, pygame.K_LEFT]:
                cam_movement[0] = 0
            if event.key in [pygame.K_UP, pygame.K_DOWN]:
                cam_movement[1] =0

        if event.type == pygame.MOUSEWHEEL:
            scale_change = event.y * 0.1  # Amount to change scale by based on mouse wheel movement
            scale = max(scale + scale_change, 0.1)  # Update scale factor

    if pygame.mouse.get_pressed()[0]:
        s = 0
        if not pressed and pygame.mouse.get_pos()[0] <= 980:
            pressed = True
            if current_item == "Room":
                rooms.append(dungeon.DungeonRoom(round(((pygame.mouse.get_pos()[0] + scroll[0]) / scale - (1024 / 2)) / 32) * 32, round(((pygame.mouse.get_pos()[1] + scroll[1]) / scale - (1024 / 2)) / 32) * 32))
            elif current_item == "Corridor":
                rooms.append(dungeon.Corridor(round(((pygame.mouse.get_pos()[0] + scroll[0]) / scale - (256 / 2)) / 32) * 32, round(((pygame.mouse.get_pos()[1] + scroll[1]) / scale - (128 / 2)) / 32) * 32))
            elif current_item == "Chest":
                items.append(dungeon.Chest(round(((pygame.mouse.get_pos()[0] + scroll[0]) / scale - (64 / 2)) / 32) * 32, round(((pygame.mouse.get_pos()[1] + scroll[1]) / scale - (32 / 2)) / 32) * 32))
            elif current_item == "Zombie":
                items.append(enemy.Zombie(round(((pygame.mouse.get_pos()[0] + scroll[0]) / scale - (32 / 2)) / 32) * 32, round(((pygame.mouse.get_pos()[1] + scroll[1]) / scale - (32 / 2)) / 32) * 32))
            elif current_item == "End":
                items.append(dungeon.End(round(((pygame.mouse.get_pos()[0] + scroll[0]) / scale - (128 / 2)) / 32) * 32, round(((pygame.mouse.get_pos()[1] + scroll[1]) / scale - (128 / 2)) / 32) * 32))
            elif current_item == "Level Enter":
                items.append(dungeon.LevelEnter(round(((pygame.mouse.get_pos()[0] + scroll[0]) / scale - (256 / 2)) / 32) * 32, round(((pygame.mouse.get_pos()[1] + scroll[1]) / scale - (128 / 2)) / 32) * 32, level_enter_level))

    else:
        if current_item == "Room":
            s = pygame.surface.Surface((1024 * scale, 1024 * scale))
        elif current_item == "Corridor":
            s = pygame.surface.Surface((256 * scale, 128 * scale))
        elif current_item == "Chest":
            s = pygame.surface.Surface((128 * scale, 64 * scale))
        elif current_item == "Zombie":
            s = pygame.surface.Surface((64 * scale, 64 * scale))
        elif current_item == "End":
            s = pygame.surface.Surface((128 * scale, 128 * scale))
        elif current_item == "Level Enter":
            s = pygame.surface.Surface((256 * scale, 128 * scale))
        s.fill((0, 0, 0))
        s.set_alpha(128)

    if not pygame.mouse.get_pressed()[0]:
        pressed = False

    if pygame.mouse.get_pos()[0] <= 980 and pygame.mouse.get_pressed()[2]:
        for room in rooms:
            if pygame.Rect(room.rect.x * scale, room.rect.y * scale, room.rect.width * scale, room.rect.height * scale).collidepoint(((pygame.mouse.get_pos()[0] + scroll[0]), (pygame.mouse.get_pos()[1] + scroll[1]))):
                rooms.remove(room)
        for item in items:
            if pygame.Rect(item.rect.x * scale, item.rect.y * scale, item.rect.width * scale, item.rect.height * scale).collidepoint(((pygame.mouse.get_pos()[0] + scroll[0]), (pygame.mouse.get_pos()[1] + scroll[1]))):
                items.remove(item)


    for room in reversed(rooms):
        check_collision(room, rooms, scroll)
    for item in reversed(items):
        check_collision(item, items, scroll)

    scroll[0] += cam_movement[0] * 20
    scroll[1] += cam_movement[1] * 20

    screen.fill((255, 100, 100))

    for room in rooms:
        room.draw(screen, scroll, scale)
    for item in items:
        item.draw(screen, scroll, scale)
    if isinstance(s, pygame.surface.Surface):
        width = s.get_rect().width  # Multiply width by scale
        height = s.get_rect().height  # Multiply height by scale
        grid_x = (round(pygame.mouse.get_pos()[0]) / (32 * scale)) * (32 * scale) - scroll[0] % (32 * scale)
        grid_y = (round(pygame.mouse.get_pos()[1]) / (32 * scale)) * (32 * scale) - scroll[1] % (32 * scale)
        x = grid_x - width / 2
        y = grid_y - height / 2
        screen.blit(s, (x, y))


    pygame.draw.rect(screen, (0, 0, 0), (0 - scroll[0], 0 - scroll[1], 32 * scale, 32 * scale))

    grid_spacing = 32 * scale

    for i in range(int(1280 / grid_spacing) + 1):
        pygame.draw.line(screen, (0, 0, 0), (i * grid_spacing - scroll[0] % grid_spacing, 0), (i * grid_spacing - scroll[0] % grid_spacing, 720))
    for i in range(int(720 / grid_spacing) + 1):
        pygame.draw.line(screen, (0, 0, 0), (0, i * grid_spacing - scroll[1] % grid_spacing), (1280, i * grid_spacing - scroll[1] % grid_spacing))
    pygame.draw.rect(screen, (0, 0, 0), (980, 0, 300, 720))

    for button in buttons:
        if button.draw(screen):
            current_item = button.text

    pygame.display.update()
    clock.tick(60)

pygame.quit()
