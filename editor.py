import pygame

import assets.scripts.dungeon as dungeon
import assets.scripts.weapon as weapon
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
            if isinstance(item, enemy.Zombie):
                l = 3
            elif isinstance(item, dungeon.End):
                l = 4
            if isinstance(item, dungeon.LevelEnter):
                f.write(f"[5, {item.rect.x}, {item.rect.y}, {item.level}]\n")
            elif isinstance(item, dungeon.Lock):
                f.write(f"[6, {item.rect.x}, {item.rect.y}, {item.key}]\n")
            elif isinstance(item, dungeon.Chest):
                f.write(f"[2, {item.rect.x}, {item.rect.y}, {item.items.space}]\n")
            else:
                f.write(f"[{l}, {item.rect.x}, {item.rect.y}]\n")

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
                things.append(dungeon.Chest(item[1], item[2], item[3]))
            elif item[0] == 3:
                things.append(enemy.Zombie(item[1], item[2]))
            elif item[0] == 4:
                things.append(dungeon.End(item[1], item[2]))
            elif item[0] == 5:
                things.append(dungeon.LevelEnter(item[1], item[2], item[3]))
            elif item[0] == 6:
                things.append(dungeon.Lock(item[1], item[2], str(item[3])))

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

def open_inventory(chest, screen):
    inventory_open = True
    quitted = False
    items = ["sword", "key", "empty", "empty", "empty", "empty", "empty", "empty", "empty"]
    trash = pygame.Rect(1165, 600, 75, 75)
    key_prompt = ui.PromptBox("Which lock is this for?")
    key_prompt.prompted = True
    item_carrying = "empty"
    while inventory_open:
        for event in pygame.event.get():
            key_prompt.handle_input(event)
            if event.type == pygame.QUIT:
                inventory_open = False
                quitted = True
            if event.type == pygame.KEYDOWN and event.key == pygame.K_e:
                inventory_open = False

        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()[0]

        for spot, item in enumerate(items):
            rect = pygame.Rect(640 - 450 + spot * 100, 600, 75, 75)
            if mouse_pressed and (rect.collidepoint(mouse_pos) and item_carrying == "empty"):
                if item == "sword":
                    item_carrying = item
                elif item == "key":
                    key_prompt.prompt()

        if mouse_pressed and trash.collidepoint(mouse_pos):
            item_carrying = "empty"

        screen.fill((255, 100, 100))
        for spot, item in enumerate(items):
            s = pygame.surface.Surface((75, 75))
            s.set_alpha(200)
            s.fill((127, 127, 127))
            screen.blit(s, (640 - 450 + spot * 100, 600, 75, 75))
            pygame.draw.rect(screen, (0, 0, 0), (640 - 450 + spot * 100, 600, 75, 75), 5)

            if item == "sword":
                pygame.draw.rect(screen, (255, 255, 255), (640 - 450 + 22 + spot * 100, 600 + 22, 32, 32))
            if item == "key":
                pygame.draw.rect(screen, (255, 0, 0), (640 - 450 + 22 + spot * 100, 600 + 22, 32, 32))
        s = pygame.surface.Surface((75, 75))
        s.set_alpha(200)
        s.fill((127, 127, 127))
        screen.blit(s, trash)
        pygame.draw.rect(screen, (0, 0, 0), trash, 5)
        item_carrying = chest.draw_storage(item_carrying, screen)
        if output := key_prompt.draw(screen):
            item_carrying = ["key", str(output)]
            key_prompt.input = ""
        pygame.display.update()
    return quitted

scroll = [0, 0]
cam_movement = [0, 0]

rooms = []
items = []
current_item = "Room"
level = 0
level_enter_level = 0
s = 0

pressed = False

clock = pygame.time.Clock()
buttons = [ui.Button("Room", 1130, 200, 200, 25), ui.Button("Corridor", 1130, 250, 200, 25), ui.Button("Chest", 1130, 300, 200, 25), ui.Button("Zombie", 1130, 350, 200, 25), ui.Button("End", 1130, 400, 200, 25), ui.Button("Level Enter", 1130, 450, 200, 25), ui.Button("Lock", 1130, 500, 200, 25)]

lock_prompt = ui.PromptBox("What is the key?")
lock_prompt.prompted = True

running = True
while running:

    for event in pygame.event.get():
        lock_prompt.handle_input(event)
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN and lock_prompt.prompted:
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
            if event.key == pygame.K_e:
                for item in items:
                    if isinstance(item, dungeon.Chest) and item.rect.collidepoint((pygame.mouse.get_pos()[0] + scroll[0], pygame.mouse.get_pos()[1] + scroll[1])):
                        running = not open_inventory(item, screen)

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
                cam_movement[1] = 0

    if pygame.mouse.get_pos()[0] <= 980 and lock_prompt.prompted:
        if pygame.mouse.get_pressed()[0]:
            s = 0
            if not pressed:
                pressed = True
                if current_item == "Room":
                    rooms.append(dungeon.DungeonRoom(round((pygame.mouse.get_pos()[
                                0] + scroll[0] - 512) / 32) * 32, round((pygame.mouse.get_pos()[1] + scroll[1] - 512) / 32) * 32))
                elif current_item == "Corridor":
                    rooms.append(dungeon.Corridor(round((pygame.mouse.get_pos()[
                                0] + scroll[0] - 128) / 32) * 32, round((pygame.mouse.get_pos()[1] + scroll[1] - 64) / 32) * 32))
                elif current_item == "Chest":
                    items.append(dungeon.Chest(round((pygame.mouse.get_pos()[
                                0] + scroll[0] - 64) / 32) * 32, round((pygame.mouse.get_pos()[1] + scroll[1] - 32) / 32) * 32))
                elif current_item == "Zombie":
                    items.append(enemy.Zombie(round((pygame.mouse.get_pos()[0] + scroll[0] - 32) / 32) * 32, round((pygame.mouse.get_pos()[1] + scroll[1] - 32) / 32) * 32))
                elif current_item == "End":
                    items.append(dungeon.End(round((pygame.mouse.get_pos()[0] + scroll[0] - 64) / 32) * 32, round((pygame.mouse.get_pos()[1] + scroll[1] - 64) / 32) * 32))
                elif current_item == "Level Enter":
                    items.append(dungeon.LevelEnter(round((pygame.mouse.get_pos()[0] + scroll[0] - 128) / 32) * 32, round((pygame.mouse.get_pos()[1] + scroll[1] - 64) / 32) * 32, level_enter_level))
                elif current_item == "Lock":
                    pos = pygame.mouse.get_pos()
                    lock_prompt.prompt()
        else:

            if current_item == "Room":
                s = pygame.surface.Surface((1024, 1024))
            elif current_item == "Corridor":
                s = pygame.surface.Surface((256, 128))
            elif current_item == "Chest":
                s = pygame.surface.Surface((128, 64))
            elif current_item == "Zombie":
                s = pygame.surface.Surface((64, 64))
            elif current_item == "End":
                s = pygame.surface.Surface((128, 128))
            elif current_item == "Level Enter":
                s = pygame.surface.Surface((256, 128))
            elif current_item == "Lock":
                s = pygame.surface.Surface((256, 64))
            s.fill((0, 0, 0))
            s.set_alpha(128)


    if not pygame.mouse.get_pressed()[0]:
        pressed = False

    if pygame.mouse.get_pos()[0] <= 980 and pygame.mouse.get_pressed()[2]:
        for room in rooms:
            if room.rect.collidepoint((pygame.mouse.get_pos()[0] + scroll[0], pygame.mouse.get_pos()[1] + scroll[1])):
                rooms.remove(room)
        for item in items:
            if item.rect.collidepoint((pygame.mouse.get_pos()[0] + scroll[0], pygame.mouse.get_pos()[1] + scroll[1])):
                items.remove(item)


    for room in reversed(rooms):
        check_collision(room, rooms, scroll)
    for item in reversed(items):
        check_collision(item, items, scroll)

    scroll[0] += cam_movement[0] * 20
    scroll[1] += cam_movement[1] * 20

    screen.fill((255, 100, 100))

    for room in rooms:
        room.draw(screen, scroll)
    for item in items:
        if isinstance(item, dungeon.Lock):
            item.draw(screen, scroll, True)
        else:
            item.draw(screen, scroll)

    if isinstance(s, pygame.surface.Surface):
        width = s.get_rect().width
        height = s.get_rect().height
        grid_x = round((pygame.mouse.get_pos()[0] + scroll[0]) / 32) * 32
        grid_y = round((pygame.mouse.get_pos()[1] + scroll[1]) / 32) * 32
        surface_x = grid_x - scroll[0] - width // 2
        surface_y = grid_y - scroll[1] - height // 2
        screen.blit(s, (surface_x, surface_y))
    pygame.draw.rect(screen, (0, 0, 0),
                     (-scroll[0], -scroll[1], 32, 32))
    for i in range(34):
        pygame.draw.line(screen, (0, 0, 0), (i * 32 -
                         scroll[0] % 32, 0), (i * 32 - scroll[0] % 32, 720))
    for i in range(26):
        pygame.draw.line(screen, (0, 0, 0), (0, i * 32 -
                         scroll[1] % 32), (980, i * 32 - scroll[1] % 32))
    pygame.draw.rect(screen, (0, 0, 0), (980, 0, 300, 720))

    for button in buttons:
        if button.draw(screen):
            current_item = button.text

    output = lock_prompt.draw(screen)
    if output and current_item == "Lock":
        lock_prompt.prompted = True
        lock_item = dungeon.Lock(round(((pos[0] + scroll[0]) - (256 / 2)) / 32) * 32,
                                 round(((pos[1] + scroll[1]) - (64 / 2)) / 32) * 32,
                                 output)
        items.append(lock_item)
        lock_prompt.input = ""

    lock_prompt.draw(screen)

    pygame.display.update()
    clock.tick(60)

pygame.quit()
