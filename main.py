import pygame
import asyncio
import math
import json
import time
import sys

# import other files in project
import assets.scripts.ui as ui
import assets.scripts.dungeon as dungeon
from assets.scripts.player import Player
import assets.scripts.enemy as enemy
import assets.scripts.boss as boss
import assets.scripts.weapon as weapon
import assets.scripts.particle as particle

# initialize pygame
pygame.init()
pygame.mixer.init()
pygame.display.init()

display_x = 1280
display_y = 720

volume = 1.0

controls = {"up": pygame.K_w, "down": pygame.K_s, "left": pygame.K_a, "right": pygame.K_d, "inventory": pygame.K_e}

# create window
display = pygame.display.set_mode((1280, 720))
icon = pygame.image.load("assets/images/icon.ico")
pygame.display.set_caption("Blob Quest")
pygame.display.set_icon(icon)
screen = pygame.Surface((display_x, display_y))


pygame.mixer.music.load("assets/sounds/music/gameplay.wav")


def load_level(level):
    with open(f"assets/levels/{level}.json", "r") as f:
        data = json.load(f)

    rooms = []
    level_enters = []
    locks = []
    chests = []
    enemies = []
    end = None
    bosses = None

    for item in data:
        if item["type"] == "room":
            rooms.append(dungeon.DungeonRoom(item["x"], item["y"]))
        elif item["type"] == "corridor":
            rooms.append(dungeon.Corridor(item["x"], item["y"]))
        elif item["type"] == "chest":
            chests.append(dungeon.Chest(item["x"], item["y"], item["space"]))
        elif item["type"] == "zombie":
            enemies.append(enemy.Zombie(item["x"], item["y"]))
        elif item["type"] == "archer":
            enemies.append(enemy.Archer(item["x"], item["y"]))
        elif item["type"] == "boss":
            bosses = boss.Boss(item["x"], item["y"])
        elif item["type"] == "end":
            end = dungeon.End(item["x"], item["y"])
        elif item["type"] == "level enter":
            level_enters.append(dungeon.LevelEnter(item["x"], item["y"], item["level"]))
        elif item["type"] == "lock":
            locks.append(dungeon.Lock(item["x"], item["y"], str(item["key"])))

    # spits out lists for level data
    return rooms, chests, enemies, bosses, end, level_enters, locks

# quit function
def quit():
    pygame.quit()
    sys.exit()

# main menu function
async def main_menu(state):
    play_button = ui.Button("Play", 640, 360, 500, 50, "large")
    quit_button = ui.Button("Quit", 640, 435, 500, 50, "large")

    cursor = pygame.image.load("assets/images/cursor.png")
    cursor.set_colorkey((255, 255, 255))
    pygame.mouse.set_visible(False)

    shade = pygame.Surface((1280, 720), pygame.SRCALPHA)
    shade.fill((0, 0, 0, 64))

    splash = pygame.image.load("assets/images/splash.png")

    clock = pygame.time.Clock()

    pygame.mixer.music.set_volume(0.125)
    pygame.mixer.music.play(-1)

    while state == "main menu":
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                state = "quit"

        scaled_mouse_pos = [pygame.mouse.get_pos()[0] * 1280 / display_x, pygame.mouse.get_pos()[1] * 720 / display_y]

        screen.fill((96, 178, 124))
        screen.blit(splash, (0, 0))
        screen.blit(shade, (0, 0))
        ui.title("Blob Quest", 640, 200, screen)
        if play_button.draw(screen, volume, scaled_mouse_pos):
            state = "lobby"
        if quit_button.draw(screen, volume, scaled_mouse_pos):
            state = "quit"
        screen.blit(cursor, (scaled_mouse_pos[0] - 16, scaled_mouse_pos[1] - 16))

        display.blit(pygame.transform.scale(screen, (display_x, display_y)), (0, 0))
        pygame.display.update()

        clock.tick(60)
        await asyncio.sleep(0)

    pygame.mixer.music.fadeout(1000)
    return state


async def settings_menu():
    return_button = ui.Button("Return", 640, 360, 500, 50, "large")
    volume_button = ui.Button("Volume", 640, 435, 500, 50, "large")
    size_button = ui.Button("Size", 640, 510, 500, 50, "large")

    cursor = pygame.image.load("assets/images/cursor.png")
    cursor.set_colorkey((255, 255, 255))
    pygame.mouse.set_visible(False)

    clock = pygame.time.Clock()

    in_settings = True
    quitted = False
    while in_settings:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                in_settings = False
                quitted = True

        scaled_mouse_pos = [pygame.mouse.get_pos()[0] * 1280 / display_x, pygame.mouse.get_pos()[1] * 720 / display_y]

        screen.fill((96, 178, 124))
        ui.title("Settings",  640, 200, screen)
        if return_button.draw(screen, volume, scaled_mouse_pos):
            in_settings = False
        if volume_button.draw(screen, volume, scaled_mouse_pos):
            volume_menu()
        if size_button.draw(screen, volume, scaled_mouse_pos):
            size_menu()
        screen.blit(cursor, (scaled_mouse_pos[0] - 16, scaled_mouse_pos[1] - 16))

        display.blit(pygame.transform.scale(screen, (display_x, display_y)), (0, 0))
        pygame.display.update()

        clock.tick(60)
        await asyncio.sleep(0)

    if quitted:
        quit()


async def volume_menu():
    global volume
    return_button = ui.Button("Return", 640, 360, 500, 50, "large")

    volume_slider = ui.Slider(640, 435, "idk", volume * 100, 100)

    cursor = pygame.image.load("assets/images/cursor.png")
    cursor.set_colorkey((255, 255, 255))
    pygame.mouse.set_visible(False)

    clock = pygame.time.Clock()

    in_menu = True
    quitted = False
    while in_menu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                in_menu = False
                quitted = True

        scaled_mouse_pos = [pygame.mouse.get_pos()[0] * 1280 / display_x, pygame.mouse.get_pos()[1] * 720 / display_y]

        screen.fill((96, 178, 124))
        ui.title("Volume",  640, 200, screen)
        if return_button.draw(screen, volume, scaled_mouse_pos):
            in_menu = False
        volume = volume_slider.draw(screen, scaled_mouse_pos) / 100
        screen.blit(cursor, (scaled_mouse_pos[0] - 16, scaled_mouse_pos[1] - 16))

        display.blit(pygame.transform.scale(screen, (display_x, display_y)), (0, 0))
        pygame.display.update()

        clock.tick(60)
        await asyncio.sleep(0)

    if quitted:
        quit()

async def size_menu():
    global display, display_x, display_y
    return_button = ui.Button("Return", 640, 360, 500, 50, "large")
    small_button = ui.Button("Small", 640, 435, 500, 50, "large")
    medium_button = ui.Button("Medium", 640, 510, 500, 50, "large")
    large_button = ui.Button("Large", 640, 585, 500, 50, "large")
    full_button = ui.Button("Fullscreen", 640, 660, 500, 50, "large")

    cursor = pygame.image.load("assets/images/cursor.png")
    cursor.set_colorkey((255, 255, 255))
    pygame.mouse.set_visible(False)

    click_timer = 15

    clock = pygame.time.Clock()

    in_menu = True
    quitted = False
    while in_menu:
        click_timer -= 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                in_menu = False
                quitted = True

        scaled_mouse_pos = [pygame.mouse.get_pos()[0] * 1280 / display_x, pygame.mouse.get_pos()[1] * 720 / display_y]

        screen.fill((96, 178, 124))
        ui.title("Settings",  640, 200, screen)
        if return_button.draw(screen, volume, scaled_mouse_pos):
            in_menu = False
        if click_timer <= 0:
            if small_button.draw(screen, volume, scaled_mouse_pos):
                display_x = 640
                display_y = 360
                display = pygame.display.set_mode((display_x, display_y))
                click_timer = 15
            if medium_button.draw(screen, volume, scaled_mouse_pos):
                display_x = 1280
                display_y = 720
                display = pygame.display.set_mode((display_x, display_y))
                click_timer = 15
            if large_button.draw(screen, volume, scaled_mouse_pos):
                display_x = 1920
                display_y = 1080
                display = pygame.display.set_mode((display_x, display_y))
                click_timer = 15
            if full_button.draw(screen, volume, scaled_mouse_pos):
                display = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                display_x = display.get_width()
                display_y = display.get_height()
                click_timer = 15
        screen.blit(cursor, (scaled_mouse_pos[0] - 16, scaled_mouse_pos[1] - 16))

        display.blit(pygame.transform.scale(screen, (display_x, display_y)), (0, 0))
        pygame.display.update()

        clock.tick(60)
        await asyncio.sleep(0)

    if quitted:
        quit()

async def game_over(state, level):
    play_button = ui.Button("Restart", 640, 360, 500, 50, "large")
    lobby_button = ui.Button("Lobby", 640, 435, 500, 50, "large")
    quit_button = ui.Button("Quit", 640, 510, 500, 50, "large")

    cursor = pygame.image.load("assets/images/cursor.png")
    cursor.set_colorkey((255, 255, 255))
    pygame.mouse.set_visible(False)

    clock = pygame.time.Clock()

    while state == "game over":
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                state = "quit"

        scaled_mouse_pos = [pygame.mouse.get_pos()[0] * 1280 / display_x, pygame.mouse.get_pos()[1] * 720 / display_y]

        screen.fill((96, 178, 124))
        ui.title("You Got Slain",  640, 200, screen)
        if play_button.draw(screen, volume, scaled_mouse_pos):
            state = f"level {level}"
        if lobby_button.draw(screen, volume, scaled_mouse_pos):
            state = "lobby"
        if quit_button.draw(screen, volume, scaled_mouse_pos):
            state = "quit"
        screen.blit(cursor, (scaled_mouse_pos[0] - 16, scaled_mouse_pos[1] - 16))

        display.blit(pygame.transform.scale(screen, (display_x, display_y)), (0, 0))
        pygame.display.update()

        clock.tick(60)
        await asyncio.sleep(0)

    return state


async def win(state, level):
    global keys
    keys.append(f"{level}0")
    lobby_button = ui.Button("Continue", 640, 360, 500, 50, "large")
    quit_button = ui.Button("Quit", 640, 435, 500, 50, "large")

    cursor = pygame.image.load("assets/images/cursor.png")
    cursor.set_colorkey((255, 255, 255))
    pygame.mouse.set_visible(False)

    clock = pygame.time.Clock()

    while state == "win":
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                state = "quit"

        scaled_mouse_pos = [pygame.mouse.get_pos()[0] * 1280 / display_x, pygame.mouse.get_pos()[1] * 720 / display_y]

        screen.fill((96, 178, 124))
        ui.title("Level Complete!",  640, 200, screen)
        if lobby_button.draw(screen, volume, scaled_mouse_pos):
            state = "lobby"
        if quit_button.draw(screen, volume, scaled_mouse_pos):
            state = "quit"
        screen.blit(cursor, (scaled_mouse_pos[0] - 16, scaled_mouse_pos[1] - 16))

        display.blit(pygame.transform.scale(screen, (display_x, display_y)), (0, 0))
        pygame.display.update()

        clock.tick(60)
        await asyncio.sleep(0)

    return state


async def paused(state):
    play_button = ui.Button("Continue", 640, 360, 500, 50, "large")
    restart_button = ui.Button("Restart", 640, 435, 500, 50, "large")
    settings_button = ui.Button("Settings", 640, 510, 500, 50, "large")
    quit_button = ui.Button("Exit", 640, 585, 500, 50, "large")

    cursor = pygame.image.load("assets/images/cursor.png")
    cursor.set_colorkey((255, 255, 255))
    pygame.mouse.set_visible(False)

    clock = pygame.time.Clock()

    pause = True
    restart = False
    while pause:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                state = "quit"
                pause = False

        scaled_mouse_pos = [pygame.mouse.get_pos()[0] * 1280 / display_x, pygame.mouse.get_pos()[1] * 720 / display_y]

        screen.fill((96, 178, 124))
        ui.title("Paused",  640, 200, screen)
        if play_button.draw(screen, volume, scaled_mouse_pos):
            pause = False
        if restart_button.draw(screen, volume, scaled_mouse_pos):
            pause = False
            restart = True
        if settings_button.draw(screen, volume, scaled_mouse_pos):
            settings_menu()
        if quit_button.draw(screen, volume, scaled_mouse_pos):
            state = "lobby"
            pause = False
        screen.blit(cursor, (scaled_mouse_pos[0] - 16, scaled_mouse_pos[1] - 16))

        display.blit(pygame.transform.scale(screen, (display_x, display_y)), (0, 0))
        pygame.display.update()

        clock.tick(60)
        await asyncio.sleep(0)

    return state, restart


async def lobby_pause(state):
    play_button = ui.Button("Continue", 640, 360, 500, 50, "large")
    settings_button = ui.Button("Settings", 640, 435, 500, 50, "large")
    quit_button = ui.Button("Exit", 640, 510, 500, 50, "large")

    cursor = pygame.image.load("assets/images/cursor.png")
    cursor.set_colorkey((255, 255, 255))
    pygame.mouse.set_visible(False)

    clock = pygame.time.Clock()

    pause = True
    while pause:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                state = "quit"
                pause = False

        scaled_mouse_pos = [pygame.mouse.get_pos()[0] * 1280 / display_x, pygame.mouse.get_pos()[1] * 720 / display_y]

        screen.fill((96, 178, 124))
        ui.title("Paused",  640, 200, screen)
        if play_button.draw(screen, volume, scaled_mouse_pos):
            pause = False
        if settings_button.draw(screen, volume, scaled_mouse_pos):
            settings_menu()
        if quit_button.draw(screen, volume, scaled_mouse_pos):
            state = "quit"
            pause = False
        screen.blit(cursor, (scaled_mouse_pos[0] - 16, scaled_mouse_pos[1] - 16))

        display.blit(pygame.transform.scale(screen, (display_x, display_y)), (0, 0))
        pygame.display.update()

        clock.tick(60)
        await asyncio.sleep(0)

    return state


async def open_chest(inventory, items):
    inventory_open = True

    item_carrying = "empty"

    cursor = pygame.image.load("assets/images/cursor.png")
    cursor.set_colorkey((255, 255, 255))


    clock = pygame.time.Clock()
    while inventory_open:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

            if event.type == pygame.KEYDOWN and event.key == controls["inventory"]:
                if item_carrying != "empty":
                    found_slot = False
                    counter = inventory.active_slot
                    while not found_slot:
                        if inventory.hotbar[counter] == "empty":
                            inventory.hotbar[counter] = item_carrying
                            found_slot = True
                        else:
                            counter += 1
                        if counter > 3:
                            counter = 0


                inventory_open = False

        scaled_mouse_pos = [pygame.mouse.get_pos()[0] * 1280 / display_x, pygame.mouse.get_pos()[1] * 720 / display_y]

        screen.fill((96, 178, 124))
        item_carrying = inventory.handle_mouse_interaction(item_carrying, scaled_mouse_pos)
        inventory.draw(screen, scaled_mouse_pos)
        item_carrying = items.draw(item_carrying, screen, scaled_mouse_pos)
        screen.blit(cursor, (scaled_mouse_pos[0] - 16, scaled_mouse_pos[1] - 16))

        display.blit(pygame.transform.scale(screen, (display_x, display_y)), (0, 0))
        pygame.display.update()
        clock.tick(60)
        await asyncio.sleep(0)

    return inventory, items


async def lobby(state):  # sourcery skip: low-code-quality

    cursor = pygame.image.load("assets/images/cursor.png")
    cursor.set_colorkey((255, 255, 255))
    pygame.mouse.set_visible(False)

    a = 0
    fade_surf = pygame.Surface((1280, 720))
    fade = False

    pause_button = ui.Button("", 20, 20, 32, 32, "pause")

    # load level from file
    rooms, _, enemies, _, _, level_enters, locks = load_level(0)
    for room in rooms:
        room.tiles.load_rooms(rooms)

    # initialize objects
    player = Player(state, keys)
    prev_pos = [0, 0]

    true_scroll = [-player.rect.x, -player.rect.y]
    scroll = [0, 0]

    level = None

    # controls fps
    clock = pygame.time.Clock()
    pt = time.time()
    dt = 1/60

    while state == "lobby":
        for event in pygame.event.get():
            # check if player quits
            if event.type == pygame.QUIT:
                state = "quit"

        # gets key inputs
        key_pressed = pygame.key.get_pressed()
        player.movement[0] = key_pressed[controls["right"]] - key_pressed[controls["left"]]
        player.movement[1] = key_pressed[controls["down"]] - key_pressed[controls["up"]]

        # sets the scroll value
        true_scroll[0] += (player.rect.x - (1280 / 2 - player.rect.width / 2)
                        - true_scroll[0]) / 25 * dt
        true_scroll[1] += (player.rect.y - (720 / 2 - player.rect.height / 2)
                        - true_scroll[1]) / 25 * dt
        scroll = [int(true_scroll[0]), int(true_scroll[1])]

        scaled_mouse_pos = [pygame.mouse.get_pos()[0] * 1280 / display_x, pygame.mouse.get_pos()[1] * 720 / display_y]

        # moves objects
        player.move(dt, rooms, enemies, scroll, scaled_mouse_pos, volume)
        in_room = False
        for room in rooms:
            if player.rect.colliderect(room.rect):
                in_room = True
        if (not in_room) or (math.hypot(player.rect.x - prev_pos[0], player.rect.y - prev_pos[1]) > player.speed * math.sqrt(2) * dt + 2):
            player.rect.topleft = prev_pos
        for lock in locks:
            lock.check_collision(player)
        if not fade:
            for level_enter in level_enters:
                level = level_enter.check_collision(player)
                if isinstance(level, int):
                    fade = True
                    break

        if fade:
            a += 5 * dt
        if a >= 250:
            state = f"level {level}"


        # draws to the screen
        fade_surf.set_alpha(a)
        fade_surf.fill((255, 255, 255))
        screen.fill((96, 178, 124))
        for room in rooms:
            room.draw(screen, scroll)
        for level_enter in level_enters:
            level_enter.draw(screen, scroll)
        for lock in locks:
            lock.draw(screen, scroll)
        player.draw(screen, scroll)

        if pause_button.draw(screen, volume, scaled_mouse_pos):
            state = await lobby_pause(state)
            pt = time.time()

        screen.blit(cursor, (scaled_mouse_pos[0] - 16, scaled_mouse_pos[1] - 16))
        screen.blit(fade_surf, (0, 0))

        # updates display
        display.blit(pygame.transform.scale(screen, (display_x, display_y)), (0, 0))
        pygame.display.update()

        # ensures everything is running smoothly
        clock.tick(60)
        prev_pos = player.rect.topleft
        now = time.time()
        dt = (now - pt) * 60
        pt = now
        await asyncio.sleep(0)

    return state


async def game_loop(state):
    cursor = pygame.image.load("assets/images/cursor.png")
    cursor.set_colorkey((255, 255, 255))
    pygame.mouse.set_visible(False)

    explosion_sound = pygame.mixer.Sound("assets/sounds/effects/explosion.wav")

    shake = False
    shake_timer = 0

    pause_button = ui.Button("", 20, 20, 32, 32, "pause")

    fade = False
    a = 0
    fade_surf = pygame.Surface((1280, 720))

    level = int(state[6])
    restart = False

    # load level from file
    rooms, chests, enemies, boss, end, _, locks = load_level(level)
    for room in rooms:
        room.tiles.load_rooms(rooms)

    # initialize objects
    player = Player(state, keys)
    prev_pos = [0, 0]

    pygame.mixer.music.play(-1)

    hold_timer = 0

    death_particles = particle.ParticleEmitter()

    true_scroll = [0, 0]
    scroll = [0, 0]

    # controls fps
    clock = pygame.time.Clock()
    pt = time.time()
    dt = 1/60

    # main loop
    while state == f"level {level}" and not restart:

        explosion_sound.set_volume(volume / 2)
        pygame.mixer.music.set_volume(volume / 4)

        for event in pygame.event.get():
            # check if player quits
            if event.type == pygame.QUIT:
                state = "quit"

            if event.type == pygame.KEYDOWN and event.key == controls["inventory"]:
                for chest in chests:
                    if player.rect.colliderect(chest.rect):
                        player.inventory, chest.items = await open_chest(player.inventory, chest.items)
                pt = time.time()

            if event.type == pygame.MOUSEBUTTONDOWN and issubclass(type(player.active_item), weapon.Weapon) and (player.active_item.mode == "held"):
                if isinstance(player.active_item, weapon.Sword):
                    player.active_item.mode = "attack"
                elif isinstance(player.active_item, weapon.Bow):
                    player.active_item.mode = "load"
                    hold_timer = 0

            if event.type == pygame.MOUSEBUTTONUP and (isinstance(player.active_item, weapon.Bow)) and (player.active_item.mode == "load"):
                player.active_item.mode = "attack"
                player.active_item.strength = min(hold_timer / 20, 3)

        # gets key inputs
        key_pressed = pygame.key.get_pressed()
        player.movement[0] = key_pressed[controls["right"]] - key_pressed[controls["left"]]
        player.movement[1] = key_pressed[controls["down"]] - key_pressed[controls["up"]]

        if key_pressed[pygame.K_1]:
            player.inventory.active_slot = 0
            player.switched = True
        elif key_pressed[pygame.K_2]:
            player.inventory.active_slot = 1
            player.switched = True
        elif key_pressed[pygame.K_3]:
            player.inventory.active_slot = 2
            player.switched = True
        elif key_pressed[pygame.K_4]:
            player.inventory.active_slot = 3

        # sets the scroll value
        true_scroll[0] += ((player.rect.x - (1280 / 2 - player.rect.width / 2)
                        - true_scroll[0]) / 25 * dt) + 10 * math.sin(5 * int(shake_timer))
        true_scroll[1] += ((player.rect.y - (720 / 2 - player.rect.height / 2)
                        - true_scroll[1]) / 25 * dt) + 2 * math.sin(5 * int(shake_timer))
        if boss and (boss.bossfight):
            if true_scroll[0] > boss.rect.centerx + 1024:
                true_scroll[0] = boss.rect.centerx + 1024
            elif true_scroll[0] < boss.rect.centerx - 1024:
                true_scroll[0] = boss.rect.centerx - 1024
            if true_scroll[1] > boss.rect.centery + 1024:
                true_scroll[1] = boss.rect.centery + 1024
            elif true_scroll[1] < boss.rect.centery - 1024:
                true_scroll[1] = boss.rect.centery - 1024

        scroll = [int(true_scroll[0]), int(true_scroll[1])]

        scaled_mouse_pos = [pygame.mouse.get_pos()[0] * 1280 / display_x, pygame.mouse.get_pos()[1] * 720 / display_y]

        # moves objects
        player.move(dt, rooms, enemies, scroll, scaled_mouse_pos, volume)
        in_room = False
        for room in rooms:
            if player.rect.colliderect(room.rect):
                in_room = True
        if (not in_room) or (math.hypot(player.rect.x - prev_pos[0], player.rect.y - prev_pos[1]) > player.speed * math.sqrt(2) * dt + 2):
            player.rect.topleft = prev_pos
        hold_timer += 1
        for lock in locks:
            shake = shake or lock.check_collision(player)
        death_particles.update(dt)
        for i, e in sorted(enumerate(enemies), reverse=True):
            e.move(player, dt, rooms, volume)
            if e.health <= 0:
                enemies.pop(i)
                death_particles.add_burst(e.rect.centerx, e.rect.centery, (200, 200, 200), 20, 10, 1, 500)
                shake = True
        for e in enemies:
            half_width = e.rect.width / 5
            half_height = e.rect.height / 5
            new_e_rect = pygame.Rect(e.rect.centerx - half_width, e.rect.centery - half_height, half_width * 2, half_height * 2)
            if new_e_rect.colliderect(player.rect):
                player.stun(e.angle)
                e.stun(-e.angle)
                break

        if boss:
            boss_shake, boss_enemies, boss_dead = boss.update(player, rooms, volume, dt)
            shake = shake or boss_shake
            for e in boss_enemies:
                enemies.append(e)
            if boss_dead:
                shake = True
                fade = True

        if end:
            end.update(dt)

        if player.state == "stunned" and shake_timer == 0 and not shake:
            shake = True
        if not player.alive and not fade:
            fade = True
        if end and (player.rect.colliderect(end.rect)):
            fade = True

        if fade:
            a += 5 * dt
        if a >= 255:
            if player.alive:
                state = "win"
                keys.append(f"{level + 1}0")
            else:
                state = "game over"


        if shake:
            explosion_sound.play()
            shake_timer = 15
            shake = False
        shake_timer -= 1
        if shake_timer <= 0:
            shake_timer = 0


        # draws to the screen
        screen.fill((96, 178, 124))
        for room in rooms:
            room.draw(screen, scroll)
        for chest in chests:
            chest.draw(screen, scroll)
        if end:
            end.draw(screen, scroll)
        for lock in locks:
            lock.draw(screen, scroll)
        player.draw(screen, scroll)
        for e in enemies:
            e.draw(screen, scroll)
        if boss:
            boss.draw(screen, scroll)
        death_particles.draw(screen, scroll)


        player.inventory.draw_hotbar(screen)
        pygame.draw.rect(screen, (255, 0, 0), (390, 525, 500, 35))
        pygame.draw.rect(screen, (0, 255, 0), (390, 525, player.health * 5, 35))
        if pause_button.draw(screen, volume, scaled_mouse_pos):
            state, restart = await paused(state)
            pt = time.time()
        screen.blit(cursor, (scaled_mouse_pos[0] - 16, scaled_mouse_pos[1] - 16))

        fade_surf.set_alpha(a)
        fade_surf.fill((255, 255, 255))
        screen.blit(fade_surf, (0, 0))

        # updates display
        display.blit(pygame.transform.scale(screen, (display_x, display_y)), (0, 0))
        pygame.display.update()

        # ensures everything is running smoothly
        clock.tick(60)
        prev_pos = player.rect.topleft
        now = time.time()
        dt = (now - pt) * 60
        pt = now
        await asyncio.sleep(0)

    pygame.mixer.music.fadeout(1000)
    return state, level

# set the state of the window
keys = []
async def main():
    global keys
    state = "main menu"
    running = True
    while running:
        if state == "main menu":
            state = await main_menu(state)
        elif state == "lobby":
            state = await lobby(state)
        elif state[:5] == "level":
            state, level = await game_loop(state)
        elif state == "win":
            state = await win(state, level)
        elif state == "game over":
            state = await game_over(state, level)
        if state == "quit":
            running = False

    quit()

asyncio.run(main())
