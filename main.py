import random
import pygame
import json
import time
import sys

# import other files in project
import assets.scripts.ui as ui
import assets.scripts.dungeon as dungeon
from assets.scripts.player import Player
import assets.scripts.enemy as enemy
import assets.scripts.weapon as weapon
import assets.scripts.particle as particle

# initialize pygame
pygame.init()
pygame.mixer.init()
pygame.display.init()

# create window
display = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Goofy Ahh Dungeon Game")
pygame.display.set_icon(pygame.image.load("assets/images/entity/player.png").convert())
screen = pygame.Surface((1280, 720))



def load_level(level):
    with open(f"assets/levels/{level}.json", "r") as f:
        data = json.load(f)

    rooms = []
    level_enters = []
    locks = []
    chests = []
    enemies = []
    end = None

    for item in data:
        if item["type"] == 0:
            rooms.append(dungeon.DungeonRoom(item["x"], item["y"]))
        elif item["type"] == 1:
            rooms.append(dungeon.Corridor(item["x"], item["y"]))
        elif item["type"] == 2:
            chests.append(dungeon.Chest(item["x"], item["y"], item["space"]))
        elif item["type"] == 3:
            enemies.append(enemy.Zombie(item["x"], item["y"]))
        elif item["type"] == 4:
            end = dungeon.End(item["x"], item["y"])
        elif item["type"] == 5:
            level_enters.append(dungeon.LevelEnter(item["x"], item["y"], item["level"]))
        elif item["type"] == 6:
            locks.append(dungeon.Lock(item["x"], item["y"], str(item["key"])))

    # spits out lists for level data
    return rooms, chests, enemies, end, level_enters, locks

# quit function
def quit():
    pygame.quit()
    sys.exit()

# main menu function
def main_menu(state, screen, display):
    play_button = ui.Button("Play", 640, 360, 500, 100)
    quit_button = ui.Button("Quit", 640, 510, 500, 100)

    cursor = pygame.image.load("assets/images/cursor.png")
    click = pygame.mixer.Sound("assets/sounds/effects/click.wav")
    cursor.set_colorkey((255, 255, 255))
    pygame.mouse.set_visible(False)

    clock = pygame.time.Clock()

    while state == "main menu":
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                state = "quit"

        screen.fill((255, 100, 100))
        ui.title("Goofy Ahh Dungeon Game",  640, 200, screen)
        if play_button.draw(screen):
            state = "lobby"
            click.play()
        if quit_button.draw(screen):
            state = "quit"
        screen.blit(cursor, (pygame.mouse.get_pos()[0] - 16, pygame.mouse.get_pos()[1] - 16))

        display.blit(pygame.transform.scale(screen, (1280, 720)), (0, 0))
        pygame.display.update()

        clock.tick(60)

    return state


def game_over(state, level, screen, display):
    play_button = ui.Button("Restart", 640, 360, 400, 75)
    lobby_button = ui.Button("Lobby", 640, 460, 400, 75)
    quit_button = ui.Button("Quit", 640, 560, 400, 75)

    cursor = pygame.image.load("assets/images/cursor.png")
    cursor.set_colorkey((255, 255, 255))
    pygame.mouse.set_visible(False)

    clock = pygame.time.Clock()

    while state == "game over":
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                state = "quit"

        screen.fill((255, 100, 100))
        ui.title("You Ded",  640, 200, screen)
        if play_button.draw(screen):
            state = f"level {level}"
        if lobby_button.draw(screen):
            state = "lobby"
        if quit_button.draw(screen):
            state = "quit"
        screen.blit(cursor, (pygame.mouse.get_pos()[0] - 16, pygame.mouse.get_pos()[1] - 16))

        display.blit(pygame.transform.scale(screen, (1280, 720)), (0, 0))
        pygame.display.update()

        clock.tick(60)

    return state


def win(state, screen, display):
    global keys
    lobby_button = ui.Button("Continue", 640, 360, 400, 75)
    quit_button = ui.Button("Quit", 640, 460, 400, 75)

    cursor = pygame.image.load("assets/images/cursor.png")
    cursor.set_colorkey((255, 255, 255))
    pygame.mouse.set_visible(False)

    clock = pygame.time.Clock()

    while state == "win":
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                state = "quit"

        screen.fill((255, 100, 100))
        ui.title("levil complet",  640, 200, screen)
        if lobby_button.draw(screen):
            state = "lobby"
        if quit_button.draw(screen):
            state = "quit"
        screen.blit(cursor, (pygame.mouse.get_pos()[0] - 16, pygame.mouse.get_pos()[1] - 16))

        display.blit(pygame.transform.scale(screen, (1280, 720)), (0, 0))
        pygame.display.update()

        clock.tick(60)

    return state


def paused(state, screen, display, level):
    play_button = ui.Button("Continue", 640, 360, 400, 75)
    restart_button = ui.Button("Restart", 640, 460, 400, 75)
    lobby_button = ui.Button("Return To Lobby", 640, 560, 400, 75)
    quit_button = ui.Button("Quit", 640, 660, 400, 75)

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

        screen.fill((255, 100, 100))
        ui.title("Paused",  640, 200, screen)
        if play_button.draw(screen):
            pause = False
        if restart_button.draw(screen):
            state = f"level {level}"
            pause = False
            restart = True
        if lobby_button.draw(screen):
            state = "lobby"
            pause = False
        if quit_button.draw(screen):
            state = "quit"
            pause = False
        screen.blit(cursor, (pygame.mouse.get_pos()[0] - 16, pygame.mouse.get_pos()[1] - 16))

        display.blit(pygame.transform.scale(screen, (1280, 720)), (0, 0))
        pygame.display.update()

        clock.tick(60)
    return state, restart


def open_inventory(screen, display, inventory):
    inventory_open = True

    cursor = pygame.image.load("assets/images/cursor.png")
    cursor.set_colorkey((255, 255, 255))

    clock = pygame.time.Clock()
    while inventory_open:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

            if event.type == pygame.KEYDOWN and event.key == pygame.K_e:
                inventory_open = False

        screen.fill((255, 100, 100))
        inventory.draw(screen)
        screen.blit(cursor, (pygame.mouse.get_pos()[0] - 16, pygame.mouse.get_pos()[1] - 16))

        display.blit(pygame.transform.scale(screen, (1280, 720)), (0, 0))
        pygame.display.update()
        clock.tick(60)


def open_chest(screen, display, inventory, items):
    inventory_open = True

    item_carrying = "empty"

    cursor = pygame.image.load("assets/images/cursor.png")
    cursor.set_colorkey((255, 255, 255))

    clock = pygame.time.Clock()
    while inventory_open:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

            if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                inventory_open = False

        screen.fill((255, 100, 100))
        inventory.draw_hotbar(screen)
        item_carrying = inventory.handle_hotbar_mouse_interaction(item_carrying)
        item_carrying = items.draw(item_carrying, screen)
        screen.blit(cursor, (pygame.mouse.get_pos()[0] - 16, pygame.mouse.get_pos()[1] - 16))

        display.blit(pygame.transform.scale(screen, (1280, 720)), (0, 0))
        pygame.display.update()
        clock.tick(60)

    return inventory, items


def lobby(state, screen, display):  # sourcery skip: low-code-quality
    global keys

    pressed = False

    cursor = pygame.image.load("assets/images/cursor.png")
    cursor.set_colorkey((255, 255, 255))
    a = 0
    fade_surf = pygame.Surface((1280, 720))
    fade = False
    pygame.mouse.set_visible(False)

    # load level from file
    rooms, _, enemies, _, level_enters, locks = load_level(0)

    # initialize objects
    player = Player(state, keys)

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
        player.movement[0] = (key_pressed[pygame.K_RIGHT] or key_pressed[pygame.K_d]) - (key_pressed[pygame.K_LEFT] or key_pressed[pygame.K_a])
        player.movement[1] = (key_pressed[pygame.K_DOWN] or key_pressed[pygame.K_s]) - (key_pressed[pygame.K_UP] or key_pressed[pygame.K_w])
        if key_pressed[pygame.K_SPACE]:
            if isinstance(player.active_item, weapon.Sword) and (player.active_item.mode == "held" and not pressed):
                player.active_item.mode = "attack"
                pressed = True
        else:
            pressed = False


        # sets the scroll value
        true_scroll[0] += (player.rect.x - (1280 / 2 - player.rect.width / 2)
                        - true_scroll[0]) / 25 * dt
        true_scroll[1] += (player.rect.y - (720 / 2 - player.rect.height / 2)
                        - true_scroll[1]) / 25 * dt
        scroll = true_scroll.copy()
        scroll[0] = int(scroll[0])
        scroll[1] = int(scroll[1])

        # moves objects
        player.move(dt, rooms, enemies, scroll)
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
        screen.fill((255, 100, 100))
        for room in rooms:
            room.draw(screen, scroll)
        for level_enter in level_enters:
            level_enter.draw(screen, scroll)
        for lock in locks:
            lock.draw(screen, scroll)
        player.draw(screen, scroll)

        ui.title(f"f: {int(clock.get_fps())}", 1100, 50, screen)

        screen.blit(cursor, (pygame.mouse.get_pos()[0] - 16, pygame.mouse.get_pos()[1] - 16))
        screen.blit(fade_surf, (0, 0))

        # updates display
        display.blit(pygame.transform.scale(screen, (1280, 720)), (0, 0))
        pygame.display.update()

        # ensures everything is running smoothly
        clock.tick(5)
        now = time.time()
        dt = (now - pt) * 60
        dt = min(dt, 4)
        pt = now

    return state


def game_loop(state, screen, display):
    global keys  # sourcery skip: low-code-quality

    cursor = pygame.image.load("assets/images/cursor.png")
    cursor.set_colorkey((255, 255, 255))
    pygame.mouse.set_visible(False)

    fade = False
    a = 0
    fade_surf = pygame.Surface((1280, 720))

    level = int(state[6])
    restart = False

    # load level from file
    rooms, chests, enemies, end, _, locks = load_level(level)

    # initialize objects
    player = Player(state, keys)

    death_particles = particle.ParticleEmitter()

    true_scroll = [0, 0]
    scroll = [0, 0]

    # controls fps
    clock = pygame.time.Clock()
    pt = time.time()
    dt = 1/60

    # main loop
    while state == f"level {level}" and not restart:

        for event in pygame.event.get():
            # check if player quits
            if event.type == pygame.QUIT:
                state = "quit"

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e:
                    open_inventory(screen, display, player.inventory)
                    pt = time.time()
                elif event.key == pygame.K_p:
                    state, restart = paused(state, screen, display, level)
                    pt = time.time()
                elif event.key == pygame.K_q:
                    for chest in chests:
                        if player.rect.colliderect(chest.rect):
                            player.inventory, chest.items = open_chest(screen, display, player.inventory, chest.items)
                            pt = time.time()

            if event.type == pygame.MOUSEBUTTONDOWN and issubclass(type(player.active_item), weapon.Weapon) and (player.active_item.mode == "held"):
                player.active_item.mode = "attack"

        # gets key inputs
        key_pressed = pygame.key.get_pressed()
        player.movement[0] = (key_pressed[pygame.K_RIGHT] or key_pressed[pygame.K_d]) - (key_pressed[pygame.K_LEFT] or key_pressed[pygame.K_a])
        player.movement[1] = (key_pressed[pygame.K_DOWN] or key_pressed[pygame.K_s]) - (key_pressed[pygame.K_UP] or key_pressed[pygame.K_w])

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
            player.switched = True
        elif key_pressed[pygame.K_5]:
            player.inventory.active_slot = 4
            player.switched = True
        elif key_pressed[pygame.K_6]:
            player.inventory.active_slot = 5
            player.switched = True
        elif key_pressed[pygame.K_7]:
            player.inventory.active_slot = 6
            player.switched = True
        elif key_pressed[pygame.K_8]:
            player.inventory.active_slot = 7
            player.switched = True
        elif key_pressed[pygame.K_9]:
            player.inventory.active_slot = 8
            player.switched = True

        # sets the scroll value
        true_scroll[0] += (player.rect.x - (1280 / 2 - player.rect.width / 2)
                        - true_scroll[0]) / 25 * dt
        true_scroll[1] += (player.rect.y - (720 / 2 - player.rect.height / 2)
                        - true_scroll[1]) / 25 * dt

        scroll = [int(true_scroll[0]), int(true_scroll[1])]

        # moves objects
        player.move(dt, rooms, enemies, scroll)
        for lock in locks:
            lock.check_collision(player)
        death_particles.update(dt)
        removed_enemies = []
        for i, enemy in enumerate(enemies):
            if enemy.health <= 0:
                removed_enemies.append(i)
                death_particles.add_burst(enemy.rect.centerx, enemy.rect.centery, (200, 200, 200), 20, 5, 0.5, 10000)
            enemy.move(player, dt, rooms)
        for i in reversed(removed_enemies):
            enemies.pop(i)

        if player.health <= 0 and not fade:
            state = "game over"
        if player.rect.colliderect(end.rect):
            fade = True

        if fade:
            a += 5 * dt
        if a >= 255:
            state = "win"
            keys.append(f"{level + 1}0")


        # draws to the screen
        screen.fill((255, 100, 100))
        for room in rooms:
            room.draw(screen, scroll)
        for chest in chests:
            chest.draw(screen, scroll)
        end.draw(screen, scroll)
        for lock in locks:
            lock.draw(screen, scroll)
        player.draw(screen, scroll)
        for enemy in enemies:
            enemy.draw(screen, scroll)
        death_particles.draw(screen, scroll)


        player.inventory.draw_hotbar(screen)
        pygame.draw.rect(screen, (255, 0, 0), (390, 525, 500, 35))
        pygame.draw.rect(screen, (0, 255, 0), (390, 525, player.health * 5, 35))
        screen.blit(cursor, (pygame.mouse.get_pos()[0] - 16, pygame.mouse.get_pos()[1] - 16))
        ui.title(f"f: {int(clock.get_fps())}", 1100, 50, screen)

        fade_surf.set_alpha(a)
        fade_surf.fill((255, 255, 255))
        screen.blit(fade_surf, (0, 0))

        # updates display
        display.blit(pygame.transform.scale(screen, (1280, 720)), (0, 0))
        pygame.display.update()

        # ensures everything is running smoothly
        clock.tick(60)
        now = time.time()
        dt = (now - pt) * 60
        dt = min(dt, 4)
        pt = now

    return state, level

# set the state of the window
state = "main menu"
keys = []
running = True
while running:
    if state == "main menu":
        state = main_menu(state, screen, display)
    elif state == "lobby":
        state = lobby(state, screen, display)
    elif state[:5] == "level":
        state, level = game_loop(state, screen, display)
    elif state == "win":
        state = win(state, screen, display)
    elif state == "game over":
        state = game_over(state, level, screen, display)
    if state == "quit":
        running = False

quit()
