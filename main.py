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
    def __init__(self):
        super().__init__(304, 164, 64, 64, 10, 100, "player.png")
        self.state = "active"
        self.attack = False
        self.inventory = inventory.Inventory(640, 600)
        self.inventory.hotbar[self.inventory.active_slot] = weapon.Sword(self, 30)
        self.active_item = self.inventory.hotbar[self.inventory.active_slot]

    def move(self, dt, rooms, enemies):
        super().move(dt, rooms)
        self.active_item = self.inventory.hotbar[self.inventory.active_slot]
        if self.health < 100:
            self.health += 0.01
        self.check_damaged(enemies)
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
        chests = []
        enemies = []
        for item in items:
            if item[0] == 0:
                rooms.append(dungeon.DungeonRoom(item[1], item[2]))
            elif item[0] == 1:
                rooms.append(dungeon.Corridor(item[1], item[2]))
            elif item[0] == 2:
                chests.append(dungeon.Chest(item[1], item[2]))
            elif item[0] == 3:
                enemies.append(enemy.Zombie(item[1], item[2]))

    # spits out list for level data
    return rooms, chests, enemies


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
            state = "level 0"
        if quit_button.draw(screen):
            state = "quit"
        screen.blit(cursor, (pygame.mouse.get_pos()[0] - 16, pygame.mouse.get_pos()[1] - 16))

        display.blit(pygame.transform.scale(screen, (1280, 720)), (0, 0))
        pygame.display.update()

        clock.tick(60)

    if state == "quit":
        quit()

    elif state == "level 0":
        main_loop(0, state, screen, display)


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


def main_loop(level, state, screen, display):  # sourcery skip: low-code-quality
    # scroll for camera
    true_scroll = [0, 0]
    scroll = [0, 0]
    pressed = False

    cursor = pygame.image.load("assets/images/cursor.png")
    cursor.set_colorkey((255, 255, 255))
    pygame.mouse.set_visible(False)

    # load level from file
    rooms, chests, enemies = load_level(level)

    # initialize objects
    player = Player()

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

            if event.type == pygame.KEYDOWN and event.key == pygame.K_e:
                open_inventory(screen, display, player.inventory)
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
        if key_pressed[pygame.K_RIGHT]:
            player.direction = "right"
        if key_pressed[pygame.K_UP]:
            player.direction = "up"
        if key_pressed[pygame.K_DOWN]:
            player.direction = "down"

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

        # moves objects
        player.move(dt, rooms, enemies)
        for enemy in enemies:
            enemy.move(player, dt, rooms)
            if not enemy.alive:
                enemies.remove(enemy)

        true_scroll[0] += (player.rect.x - (1280 / 2 - player.rect.width / 2)
                        - true_scroll[0]) / 25 * dt
        true_scroll[1] += (player.rect.y - (720 / 2 - player.rect.height / 2)
                        - true_scroll[1]) / 25 * dt
        scroll = true_scroll.copy()
        scroll[0] = int(scroll[0])
        scroll[1] = int(scroll[1])

        # draws to the screen
        screen.fill((255, 100, 100))
        for room in rooms:
            room.draw(screen, scroll)
        for chest in chests:
            chest.generate_loot(player)
            chest.draw(screen, scroll)
        player.draw(screen, scroll)
        for enemy in enemies:
            enemy.draw(screen, scroll)


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

main_menu(state, screen, display)
