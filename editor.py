import pygame
import json

import assets.scripts.dungeon as dungeon
import assets.scripts.weapon as weapon
import assets.scripts.enemy as enemy
import assets.scripts.ui as ui

pygame.init()
pygame.mixer.init()

screen = pygame.display.set_mode((1280, 720))

def save(num, level, items):
    data = []
    for room in level:
        if isinstance(room, dungeon.DungeonRoom):
            l = "room"
        elif isinstance(room, dungeon.Corridor):
            l = "corridor"

        data.append({"type": l, "x": room.rect.x, "y": room.rect.y})

    for item in items:
        if isinstance(item, enemy.Zombie):
            l = "zombie"
        if isinstance(item, enemy.Archer):
            l = "archer"
        elif isinstance(item, dungeon.End):
            l = "end"
        if isinstance(item, dungeon.LevelEnter):
            data.append({"type": "level enter", "x": item.rect.x, "y": item.rect.y, "level": item.level})
        elif isinstance(item, dungeon.Lock):
            data.append({"type": "lock", "x": item.rect.x, "y": item.rect.y, "key": str(item.key)})
        elif isinstance(item, dungeon.Chest):
            data.append({"type": "chest", "x": item.rect.x, "y": item.rect.y, "space": item.items.space})
        else:
            data.append({"type": l, "x": item.rect.x, "y": item.rect.y})

    with open(f'assets/levels/{num}.json', 'w') as f:
        json.dump(data, f)

def load(num):
    with open(f'assets/levels/{num}.json', 'r') as f:
        data = json.load(f)

    level = []
    things = []
    for item in data:
        if item["type"] == "room":
            level.append(dungeon.DungeonRoom(item["x"], item["y"]))
        elif item["type"] == "corridor":
            level.append(dungeon.Corridor(item["x"], item["y"]))
        elif item["type"] == "chest":
            things.append(dungeon.Chest(item["x"], item["y"], item["space"]))
        elif item["type"] == "zombie":
            things.append(enemy.Zombie(item["x"], item["y"]))
        elif item["type"] == "archer":
            things.append(enemy.Archer(item["x"], item["y"]))
        elif item["type"] == "end":
            things.append(dungeon.End(item["x"], item["y"]))
        elif item["type"] == "level enter":
            things.append(dungeon.LevelEnter(item["x"], item["y"], item["level"]))
        elif item["type"] == "lock":
            things.append(dungeon.Lock(item["x"], item["y"], str(item["key"])))

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
    items = ["sword", "bow", "key", "empty", "empty", "empty", "empty", "empty", "empty"]
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
                if item != "key":
                    item_carrying = item
                else:
                    key_prompt.prompt()

        if mouse_pressed and trash.collidepoint(mouse_pos):
            item_carrying = "empty"

        screen.fill((117, 201, 151))
        for spot, item in enumerate(items):
            s = pygame.surface.Surface((75, 75))
            s.set_alpha(200)
            s.fill((127, 127, 127))
            screen.blit(s, (640 - 450 + spot * 100, 600, 75, 75))
            pygame.draw.rect(screen, (0, 0, 0), (640 - 450 + spot * 100, 600, 75, 75), 5)

            if item == "sword":
                pygame.draw.rect(screen, (255, 255, 255), (640 - 450 + 22 + spot * 100, 600 + 22, 32, 32))
            if item == "bow":
                pygame.draw.rect(screen, (0, 255, 0), (640 - 450 + 22 + spot * 100, 600 + 22, 32, 32))
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
    print(chest.items.space)
    return quitted

scroll = [0, 0]
cam_movement = [0, 0]

rooms = []
items = []
level = 0
level_enter_level = 0
s = 0

pressed = False

clock = pygame.time.Clock()

rooms_button = ui.Button("Rooms", 1130, 200, 200, 25, "large")
enemies_button = ui.Button("Enemies", 1130, 300, 200, 25, "large")
items_button = ui.Button("Items", 1130, 400, 200, 25, "large")

rooms_list = ["dungeon", "corridor"]
enemies_list = ["zombie", "archer"]
items_list = ["chest", "end", "lock", "level enter"]

current_list = rooms_list
current_item = 0

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

            if current_list[current_item] == "level enter":
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

        if event.type == pygame.MOUSEWHEEL:
            if event.y > 0:
                if len(current_list) - 1 == current_item:
                    current_item = 0
                else:
                    current_item += 1
            else:
                if current_item == 0:
                    current_item = len(current_list) - 1
                else:
                    current_item -= 1

    if pygame.mouse.get_pos()[0] <= 980 and lock_prompt.prompted:
        if pygame.mouse.get_pressed()[0]:
            s = 0
            if not pressed:
                pressed = True
                if current_list[current_item] == "dungeon":
                    rooms.append(dungeon.DungeonRoom(round((pygame.mouse.get_pos()[
                                0] + scroll[0] - 512) / 32) * 32, round((pygame.mouse.get_pos()[1] + scroll[1] - 512) / 32) * 32))
                elif current_list[current_item] == "corridor":
                    rooms.append(dungeon.Corridor(round((pygame.mouse.get_pos()[
                                0] + scroll[0] - 128) / 32) * 32, round((pygame.mouse.get_pos()[1] + scroll[1] - 64) / 32) * 32))
                elif current_list[current_item] == "zombie":
                    items.append(enemy.Zombie(round((pygame.mouse.get_pos()[0] + scroll[0] - 32) / 32) * 32, round((pygame.mouse.get_pos()[1] + scroll[1] - 32) / 32) * 32))
                elif current_list[current_item] == "archer":
                    items.append(enemy.Archer(round((pygame.mouse.get_pos()[0] + scroll[0] - 32) / 32) * 32, round((pygame.mouse.get_pos()[1] + scroll[1] - 32) / 32) * 32))
                elif current_list[current_item] == "chest":
                    items.append(dungeon.Chest(round((pygame.mouse.get_pos()[
                                0] + scroll[0] - 64) / 32) * 32, round((pygame.mouse.get_pos()[1] + scroll[1] - 32) / 32) * 32))
                elif current_list[current_item] == "end":
                    items.append(dungeon.End(round((pygame.mouse.get_pos()[0] + scroll[0] - 64) / 32) * 32, round((pygame.mouse.get_pos()[1] + scroll[1] - 64) / 32) * 32))
                elif current_list[current_item] == "level enter":
                    items.append(dungeon.LevelEnter(round((pygame.mouse.get_pos()[0] + scroll[0] - 128) / 32) * 32, round((pygame.mouse.get_pos()[1] + scroll[1] - 64) / 32) * 32, level_enter_level))
                elif current_list[current_item] == "lock":
                    pos = pygame.mouse.get_pos()
                    lock_prompt.prompt()
        else:

            if current_list[current_item] == "dungeon":
                s = pygame.surface.Surface((1024, 1024))
                pygame.draw.rect(s, (0, 0, 255), (0, 0, 1024, 1024))
            elif current_list[current_item] == "corridor":
                s = pygame.surface.Surface((256, 128))
                pygame.draw.rect(s, (0, 0, 255), (0, 0, 256, 228))
            elif current_list[current_item] == "zombie":
                s = pygame.surface.Surface((64, 64))
                enemy.Zombie(0, 0).draw(s, [0, 0])
            elif current_list[current_item] == "archer":
                s = pygame.surface.Surface((64, 64))
                enemy.Archer(0, 0).draw(s, [0, 0])
            elif current_list[current_item] == "chest":
                s = pygame.surface.Surface((128, 64))
                dungeon.Chest(0, 0).draw(s, [0, 0])
            elif current_list[current_item] == "end":
                s = pygame.surface.Surface((128, 128))
                dungeon.End(0, 0).draw(s, [0, 0])
            elif current_list[current_item] == "level enter":
                s = pygame.surface.Surface((256, 128))
                dungeon.LevelEnter(0, 0, "").draw(s, [0, 0])
            elif current_list[current_item] == "lock":
                s = pygame.surface.Surface((256, 64))
                dungeon.Lock(0, 0, None).draw(s, [0, 0])
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

    screen.fill((117, 201, 151))

    for room in rooms:
        room.draw(screen, scroll, True)
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

    if rooms_button.draw(screen, 0, pygame.mouse.get_pos()):
        current_list = rooms_list
        current_item = 0
    elif items_button.draw(screen, 0, pygame.mouse.get_pos()):
        current_list = items_list
        current_item = 0
    elif enemies_button.draw(screen, 0, pygame.mouse.get_pos()):
        current_list = enemies_list
        current_item = 0

    output = lock_prompt.draw(screen)
    if output:
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
