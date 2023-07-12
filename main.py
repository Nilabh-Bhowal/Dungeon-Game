import random
import pygame
import time
import sys

# import other files in project
import assets.scripts.ui as ui
import assets.scripts.inventory as inventory
import assets.scripts.dungeon as dungeon
import assets.scripts.entity as entity
import assets.scripts.enemy as enemy
import assets.scripts.weapon as weapon
import assets.scripts.particle as particle

# initialize pygame
pygame.init()
pygame.display.init()

# create window
display = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Goofy Ahh Dungeon Game")
pygame.display.set_icon(pygame.image.load("assets/images/entity/player.png"))
screen = pygame.Surface((1280, 720))

# set the state of the window
state = "main menu"

# player class
class Player(entity.Entity):
    def __init__(self, state):
        super().__init__(0, 0, 64, 64, 10, 100, "player.png")
        self.state = "active"
        self.attack = False
        self.pickup = False
        self.inventory = inventory.Inventory(640, 600)
        if state != "lobby":
            self.inventory.hotbar[self.inventory.active_slot] = weapon.Sword(self, 30, 64)
        self.active_item = self.inventory.hotbar[self.inventory.active_slot]
        self.item_picked_up = "empty"

    def move(self, dt, rooms, enemies):
        super().move(dt, rooms)
        self.active_item = self.inventory.hotbar[self.inventory.active_slot]
        if self.health < 100:
            self.health += 0.01
        self.check_damaged(enemies)
        self.handle_pickups()
        if isinstance(self.active_item, weapon.Sword):
            self.attack = self.active_item.update(dt)

    def check_damaged(self, enemies):
        if self.immune:
            self.immune_timer -= 1
        if self.immune_timer <= 0 and self.immune:
            self.immune = False
            self.state = "active"
        for enemy in enemies:
            if self.rect.colliderect(enemy.weapon.rect) and enemy.attack and not self.immune:
                self.health -= enemy.weapon.damage
                self.state = "stunned"
                self.knockback_direction = enemy.direction
                self.immune = True
                self.immune_timer = 15

        if self.health <= 0:
            self.alive = False

    def handle_pickups(self):
        if self.item_picked_up == "empty":
            return

        for i, slot in enumerate(self.inventory.hotbar):
            if slot == "empty" and self.item_picked_up != "empty":
                if self.item_picked_up == "sword":
                    self.inventory.hotbar[i] = weapon.Sword(self, 30, 64)
                self.item_picked_up = "empty"
                return
        for spot, row in enumerate(self.inventory.space):
            for i, slot in enumerate(row):
                if slot == "empty" and self.item_picked_up != "empty":
                    if self.item_picked_up == "sword":
                        self.inventory.space[spot][i] = weapon.Sword(self, 30, 64)
                    self.item_picked_up = "empty"
                    return


    def draw(self, screen, scroll):
        super().draw(screen, scroll)
        if self.active_item != "empty":
            self.active_item.draw(screen, scroll)


# allows to load levels from file
def load_level(level):
    with open(f"assets/levels/{level}.txt", "r") as f:
        items = (f.read().splitlines())
        items = [eval(item) for item in items]
        rooms = []
        level_enters = []
        chests = []
        enemies = []
        end = None
        for item in items:
            if item[0] == 0:
                rooms.append(dungeon.DungeonRoom(item[1], item[2]))
            elif item[0] == 1:
                rooms.append(dungeon.Corridor(item[1], item[2]))
            elif item[0] == 2:
                chests.append(dungeon.Chest(item[1], item[2]))
            elif item[0] == 3:
                enemies.append(enemy.Zombie(item[1], item[2]))
            elif item[0] == 4:
                end = dungeon.End(item[1], item[2])
            elif item[0] == 5:
                level_enters.append(dungeon.LevelEnter(item[1], item[2], item[3]))

    # spits out list for level data
    return rooms, chests, enemies, end, level_enters


# quit function
def quit():
    pygame.quit()
    sys.exit()

# main menu function
def main_menu(state, screen, display):
    play_button = ui.Button("Play", 640, 360, 500, 100)
    quit_button = ui.Button("Quit", 640, 510, 500, 100)

    cursor = pygame.image.load("assets/images/cursor.png")
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
        if quit_button.draw(screen):
            state = "quit"
        screen.blit(cursor, (pygame.mouse.get_pos()[0] - 16, pygame.mouse.get_pos()[1] - 16))

        display.blit(pygame.transform.scale(screen, (1280, 720)), (0, 0))
        pygame.display.update()

        clock.tick(60)

    if state == "quit":
        quit()

    elif state == "lobby":
        lobby(state, screen, display)


def game_over(state, screen, display, level):
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

    if state == "quit":
        quit()
    elif state == f"level {level}":
        main_loop(level, state, screen, display)
    elif state == "lobby":
        lobby(state, screen, display)


def win(state, screen, display, level):
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

    if state == "lobby":
        lobby(state, screen, display)
    elif state == "quit":
        quit()


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

    if state == "quit":
        quit()
    elif state == f"level {level}" and restart:
        main_loop(level, state, screen, display)
    elif state == "lobby":
        lobby(state, screen, display)


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


def lobby(state, screen, display):

    pressed = False

    cursor = pygame.image.load("assets/images/cursor.png")
    cursor.set_colorkey((255, 255, 255))
    pygame.mouse.set_visible(False)

    # load level from file
    rooms, _, enemies, _, level_enters = load_level(0)
    particles = []

    # initialize objects
    player = Player(state)

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
        player.movement[0] = key_pressed[pygame.K_RIGHT] - key_pressed[pygame.K_LEFT]
        player.movement[1] = key_pressed[pygame.K_DOWN] - key_pressed[pygame.K_UP]
        if key_pressed[pygame.K_SPACE]:
            if player.active_item.mode == "held" and not pressed and isinstance(player.active_item, weapon.Sword):
                player.active_item.mode = "attack"
                pressed = True
        else:
            pressed = False

        if key_pressed[pygame.K_LEFT]:
            player.direction = "left"
            particles.append(particle.Particle(player.rect.right, player.rect.centery + random.randint(-16, 16), (71, 63, 49, 128), 10, 1000, random.uniform(-0.7, 0.7), 0.001, random.randint(1, 3)))
        elif key_pressed[pygame.K_RIGHT]:
            player.direction = "right"
            particles.append(particle.Particle(player.rect.left, player.rect.centery + random.randint(-16, 16), (71, 63, 49, 128), 10, -1000, random.uniform(-0.7, 0.7), 0.001, random.randint(1, 3)))
        elif key_pressed[pygame.K_UP]:
            player.direction = "up"
            particles.append(particle.Particle(player.rect.centerx + random.randint(-16, 16), player.rect.bottom, (71, 63, 49, 128), 10, random.uniform(-0.7, 0.7), 1000, 0.001, random.randint(1, 3)))
        elif key_pressed[pygame.K_DOWN]:
            player.direction = "down"
            particles.append(particle.Particle(player.rect.centerx + random.randint(-16, 16), player.rect.top, (71, 63, 49, 128), 10, random.uniform(-0.7, 0.7), -1000, 0.001, random.randint(1, 3)))


        # sets the scroll value
        true_scroll[0] += (player.rect.x - (1280 / 2 - player.rect.width / 2)
                        - true_scroll[0]) / 25 * dt
        true_scroll[1] += (player.rect.y - (720 / 2 - player.rect.height / 2)
                        - true_scroll[1]) / 25 * dt
        scroll = true_scroll.copy()
        scroll[0] = int(scroll[0])
        scroll[1] = int(scroll[1])

        # moves objects
        player.move(dt, rooms, enemies)
        for level_enter in level_enters:
            level = level_enter.check_collision(player)
            if isinstance(level, int):
                state = f"level {level}"
                break

        for p in particles:
            p.update(dt)
            if p.size <= 0:
                particles.remove(p)


        # draws to the screen
        screen.fill((255, 100, 100))
        for room in rooms:
            room.draw(screen, scroll)
        for level_enter in level_enters:
            level_enter.draw(screen, scroll)
        player.draw(screen, scroll)

        for p in particles:
            p.draw(screen, scroll)

        screen.blit(cursor, (pygame.mouse.get_pos()[0] - 16, pygame.mouse.get_pos()[1] - 16))

        # updates display
        display.blit(pygame.transform.scale(screen, (1280, 720)), (0, 0))
        pygame.display.update()

        # ensures everything is running smoothly
        clock.tick(60)
        now = time.time()
        dt = (now - pt) * 60
        pt = now

    if state == "quit":
        quit()

    main_loop(level, state, screen, display)




def main_loop(level, state, screen, display):  # sourcery skip: low-code-quality
    # scroll for camera
    pressed = False

    cursor = pygame.image.load("assets/images/cursor.png")
    cursor.set_colorkey((255, 255, 255))
    pygame.mouse.set_visible(False)

    # load level from file
    rooms, chests, enemies, end, level_enters = load_level(level)
    particles = []

    # initialize objects
    player = Player(state)

    true_scroll = [-player.rect.x, -player.rect.y]
    scroll = [0, 0]

    # controls fps
    clock = pygame.time.Clock()
    pt = time.time()
    dt = 1/60

    # main loop
    while state == f"level {level}":

        for event in pygame.event.get():
            # check if player quits
            if event.type == pygame.QUIT:
                state = "quit"

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e:
                    open_inventory(screen, display, player.inventory)
                    pt = time.time()
                elif event.key == pygame.K_p:
                    paused(state, screen, display, level)
                    pt = time.time()


        # gets key inputs
        key_pressed = pygame.key.get_pressed()
        player.movement[0] = key_pressed[pygame.K_RIGHT] - key_pressed[pygame.K_LEFT]
        player.movement[1] = key_pressed[pygame.K_DOWN] - key_pressed[pygame.K_UP]
        if key_pressed[pygame.K_SPACE]:
            if player.active_item.mode == "held" and not pressed and isinstance(player.active_item, weapon.Sword):
                player.active_item.mode = "attack"
                pressed = True
        else:
            pressed = False

        if key_pressed[pygame.K_LEFT]:
            player.direction = "left"
            particles.append(particle.Particle(player.rect.right, player.rect.centery + random.randint(-16, 16), (71, 63, 49, 128), 10, 1000, random.uniform(-0.7, 0.7), 0.001, random.randint(1, 3)))
        elif key_pressed[pygame.K_RIGHT]:
            player.direction = "right"
            particles.append(particle.Particle(player.rect.left, player.rect.centery + random.randint(-16, 16), (71, 63, 49, 128), 10, -1000, random.uniform(-0.7, 0.7), 0.001, random.randint(1, 3)))
        elif key_pressed[pygame.K_UP]:
            player.direction = "up"
            particles.append(particle.Particle(player.rect.centerx + random.randint(-16, 16), player.rect.bottom, (71, 63, 49, 128), 10, random.uniform(-0.7, 0.7), 1000, 0.001, random.randint(1, 3)))
        elif key_pressed[pygame.K_DOWN]:
            player.direction = "down"
            particles.append(particle.Particle(player.rect.centerx + random.randint(-16, 16), player.rect.top, (71, 63, 49, 128), 10, random.uniform(-0.7, 0.7), -1000, 0.001, random.randint(1, 3)))

        player.pickup = bool(key_pressed[pygame.K_q])

        if key_pressed[pygame.K_1]:
            player.inventory.active_slot = 0
        elif key_pressed[pygame.K_2]:
            player.inventory.active_slot = 1
        elif key_pressed[pygame.K_3]:
            player.inventory.active_slot = 2
        elif key_pressed[pygame.K_4]:
            player.inventory.active_slot = 3
        elif key_pressed[pygame.K_5]:
            player.inventory.active_slot = 4
        elif key_pressed[pygame.K_6]:
            player.inventory.active_slot = 5
        elif key_pressed[pygame.K_7]:
            player.inventory.active_slot = 6
        elif key_pressed[pygame.K_8]:
            player.inventory.active_slot = 7
        elif key_pressed[pygame.K_9]:
            player.inventory.active_slot = 8

        # sets the scroll value
        true_scroll[0] += (player.rect.x - (1280 / 2 - player.rect.width / 2)
                        - true_scroll[0]) / 25 * dt
        true_scroll[1] += (player.rect.y - (720 / 2 - player.rect.height / 2)
                        - true_scroll[1]) / 25 * dt
        scroll = true_scroll.copy()
        scroll[0] = int(scroll[0])
        scroll[1] = int(scroll[1])

        # moves objects
        player.move(dt, rooms, enemies)
        for p in particles:
            p.update(dt)
            if p.size <= 0:
                particles.remove(p)
        for enemy in enemies:
            enemy.move(player, dt, rooms)
            if not enemy.alive:
                enemies.remove(enemy)

        if player.health <= 0:
            state = "game over"
        if player.rect.colliderect(end.rect):
            state = "win"


        # draws to the screen
        screen.fill((255, 100, 100))
        for room in rooms:
            room.draw(screen, scroll)
        for chest in chests:
            chest.generate_loot(player)
            chest.draw(screen, scroll)
        end.draw(screen, scroll)
        player.draw(screen, scroll)
        for enemy in enemies:
            enemy.draw(screen, scroll)

        for p in particles:
            p.draw(screen, scroll)


        player.inventory.draw_hotbar(screen)
        pygame.draw.rect(screen, (255, 0, 0), (390, 525, 500, 35))

        pygame.draw.rect(screen, (0, 255, 0), (390, 525, player.health * 5, 35))
        screen.blit(cursor, (pygame.mouse.get_pos()[0] - 16, pygame.mouse.get_pos()[1] - 16))

        # updates display
        display.blit(pygame.transform.scale(screen, (1280, 720)), (0, 0))
        pygame.display.update()

        # ensures everything is running smoothly
        clock.tick(60)
        now = time.time()
        dt = (now - pt) * 60
        pt = now


    if state == "quit":
        quit()
    elif state == "game over":
        game_over(state, screen, display, level)
    elif state == "win":
        win(state, screen, display, level)

main_menu(state, screen, display)
