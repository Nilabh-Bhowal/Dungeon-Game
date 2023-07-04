import pygame
import math
import time
import sys

# import other files in project
import assets.scripts.ui as ui
import assets.scripts.dungeon as dungeon
import assets.scripts.entity as entity
import assets.scripts.enemy as enemy

pygame.init()
pygame.display.init()

# create window
WIDTH = 1280
HEIGHT = 720
display = pygame.display.set_mode((WIDTH, HEIGHT))
screen = pygame.Surface((1280, 720))

state = "main menu"


# player class
class Player(entity.Entity):
    def __init__(self):
        super().__init__(304, 164, 64, 64, 10, 100, "player.png")
        self.sword = Sword(self)
        self.attack = False

    def move(self, dt, rooms):
        super().move(dt, rooms)
        self.attack = self.sword.update()

    def draw(self, screen, scroll):
        super().draw(screen, scroll)
        self.sword.draw(screen, scroll)


class Sword:
    def __init__(self, holder):
        self.holder = holder
        self.rect = pygame.Rect(self.holder.rect.x, self.holder.rect.y, 32, 32)
        self.range_rect = pygame.Rect(self.rect.x, self.rect.y, self.rect.width, self.rect.height)
        self.mode = "held"
        self.timer = 15

    def update(self):

        self.update_mode()

        if self.holder.direction == "up":
            self.rect.right = self.holder.rect.right
            self.rect.top = self.holder.rect.top - self.rect.height + 16
        elif self.holder.direction == "down":
            self.rect.left = self.holder.rect.left
            self.rect.top = self.holder.rect.bottom - 16
        elif self.holder.direction == "left":
            self.rect.top = self.holder.rect.top
            self.rect.left = self.holder.rect.left - self.rect.width + 16
        else:
            self.rect.bottom = self.holder.rect.bottom
            self.rect.left = self.holder.rect.right - 16

        if self.holder.direction == "up":
            self.range_rect = pygame.Rect(self.holder.rect.left, self.holder.rect.top - self.rect.height, self.holder.rect.width, self.rect.height)
        elif self.holder.direction == "down":
            self.range_rect = pygame.Rect(self.holder.rect.left, self.holder.rect.bottom, self.holder.rect.width, self.rect.height)
        elif self.holder.direction == "left":
            self.range_rect = pygame.Rect(self.holder.rect.left - self.rect.width, self.holder.rect.top, self.rect.width, self.holder.rect.height)
        else:
            self.range_rect = pygame.Rect(self.holder.rect.right, self.holder.rect.top, self.rect.width, self.holder.rect.height)

        return self.mode == "attack"

    def update_mode(self):
        if self.mode != "held":
            self.timer -= 1
            if 0 < self.timer <= 13:
                self.mode = "cooldown"
            elif self.timer == 0:
                self.mode = "held"

        else:
            self.timer = 15

    def draw(self, screen, scroll):
        pygame.draw.rect(screen, (255, 255, 255), (self.rect.x - scroll[0], self.rect.y - scroll[1], self.rect.width, self.rect.height))


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
                enemies.append(enemy.Enemy(item[1], item[2], 64, 64, 3, 70, "player.png"))

    return rooms, chests, enemies


def quit():
    pygame.quit()
    sys.exit()

def main_menu(state, screen, display):
    play_button = ui.Button("Play", 640, 360, 500, 100)
    quit_button = ui.Button("Quit", 640, 510, 500, 100)

    clock = pygame.time.Clock()
    while state == "main menu":
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                state = "quit"

        screen.fill((255, 100, 100))
        ui.title("Goofy Ahh Dungeon Game ",  640, 200, screen)
        if play_button.draw(screen):
            state = "level 0"
        if quit_button.draw(screen):
            state = "quit"

        display.blit(pygame.transform.scale(screen, (WIDTH, HEIGHT)), (0, 0))
        pygame.display.update()

        clock.tick(60)

    if state == "quit":
        quit()

    elif state == "level 0":
        main_loop(0, state, screen, display)


def main_loop(level, state, screen, display):
    # scroll for camera
    true_scroll = [0, 0]
    scroll = [0, 0]

    # load level from file
    rooms, chests, enemies = load_level(level)

    # initialize objects
    player = Player()

    # controls fps
    clock = pygame.time.Clock()
    pt = time.time()
    dt = 1/60

    # main loop
    running = True
    while running:

        for event in pygame.event.get():
            # check if player quits
            if event.type == pygame.QUIT:
                running = False

            # check if key is pressed down, and sets the movement variable based on that
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player.movement[0] = -1
                    player.direction = "left"
                if event.key == pygame.K_RIGHT:
                    player.movement[0] = 1
                    player.direction = "right"
                if event.key == pygame.K_UP:
                    player.movement[1] = -1
                    player.direction = "up"
                if event.key == pygame.K_DOWN:
                    player.movement[1] = 1
                    player.direction = "down"
                if event.key == pygame.K_SPACE and player.sword.mode == "held":
                    player.sword.mode = "attack"

            # check if key is released to set the movement variable based on that
            if event.type == pygame.KEYUP:
                if event.key in [pygame.K_LEFT, pygame.K_RIGHT]:
                    player.movement[0] = 0
                if event.key in [pygame.K_UP, pygame.K_DOWN]:
                    player.movement[1] = 0

        # sets the scroll value
        true_scroll[0] += (player.rect.x - (1280 / 2 - player.rect.width / 2)
                        - true_scroll[0]) / 25 * dt
        true_scroll[1] += (player.rect.y - (720 / 2 - player.rect.height / 2)
                        - true_scroll[1]) / 25 * dt
        scroll = true_scroll.copy()
        scroll[0] = int(scroll[0])
        scroll[1] = int(scroll[1])

        # moves objects
        player.move(dt, rooms)
        for enemy in enemies:
            enemy.move(player, dt, rooms)
            if not enemy.alive:
                enemies.remove(enemy)

        # draws to the screen
        screen.fill((255, 100, 100))
        for room in rooms:
            room.draw(screen, scroll)
        for chest in chests:
            chest.draw(screen, scroll)
        player.draw(screen, scroll)
        for enemy in enemies:
            enemy.draw(screen, scroll)

        # updates display
        display.blit(pygame.transform.scale(screen, (WIDTH, HEIGHT)), (0, 0))
        pygame.display.update()

        clock.tick(60)
        now = time.time()
        dt = (now - pt) * 60
        pt = now

main_menu(state, screen, display)
