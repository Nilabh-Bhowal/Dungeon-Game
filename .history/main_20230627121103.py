import pygame

# import other python files in project
import assets.scripts.dungeon as dungeon

pygame.init()
pygame.display.init()

# create window
WIDTH = 1280
HEIGHT = 720
display = pygame.display.set_mode((WIDTH, HEIGHT))
screen = pygame.Surface((1280, 720))


# player class
class Player:
    def __init__(self):
        self.rect = pygame.Rect(304, 164, 64, 64)
        self.speed = 10
        self.movement = [0, 0]
        self.color = (255, 255, 255)
        self.img = pygame.transform.scale2x(pygame.image.load("player.png"))
        self.direction = "down"
        self.sword = Sword(self)

    def move(self, rooms):
        self.rect.x += self.speed * self.movement[0]
        self.rect.y += self.speed * self.movement[1]
        collide(self, rooms)
        self.sword.update()

    def draw(self, screen, scroll):
        if self.direction == "left":
            screen.blit(pygame.transform.rotate(self.img, -90),
                        (self.rect.x - scroll[0], self.rect.y - scroll[1]))
        elif self.direction == "right":
            screen.blit(pygame.transform.rotate(self.img, 90),
                        (self.rect.x - scroll[0], self.rect.y - scroll[1]))
        elif self.direction == "up":
            screen.blit(pygame.transform.rotate(self.img, 180),
                        (self.rect.x - scroll[0], self.rect.y - scroll[1]))
        else:
            screen.blit(self.img, (self.rect.x -
                        scroll[0], self.rect.y - scroll[1]))
        self.sword.draw(screen, scroll)


class Enemy:
    def __init__(self):
        self.rect = pygame.Rect(304, 164, 64, 64)
        self.speed = 7
        self.movement = [0, 0]
        self.color = (255, 255, 255)

    def move(self, rooms):
        self.rect.x += self.speed * self.movement[0]
        self.rect.y += self.speed * self.movement[1]
        collide(self, rooms)

    def draw(self, screen, scroll):
        pygame.draw.rect(screen, ())


class Sword:
    def __init__(self, holder):
        self.holder = holder
        self.rect = pygame.Rect(self.holder.rect.x, self.holder.rect.y, 16, 32)

    def update(self):
        if self.holder.direction == "up":
            self.rect.x = self.holder.rect.x
            self.rect.y = self.holder.rect.y - self.rect.height
        elif self.holder.direction == "down":
            self.rect.x = self.holder.rect.x
            self.rect.y = self.holder.rect.y - self.rect.height
        elif self.holder.direction == "left":
            self.rect.x = self.holder.rect.x
            self.rect.y = self.holder.rect.y - self.rect.height
        else:
            self.rect.x = self.holder.rect.x
            self.rect.y = self.holder.rect.y - self.rect.height

    def draw(self, screen, scroll):
        pygame.draw.rect(screen, (255, 255, 255), (self.rect.x - scroll[0], self.rect.y - scroll[1], self.rect.width, self.rect.height))


# check if player can pass into other rooms
def can_pass(player, current_room, rooms):
    # sourcery skip: instance-method-first-arg-name
    pu, pd, pl, pr = [False, False, False, False]
    for room in rooms:
        if room != current_room:
            pu = pu or player.rect.top - player.rect.height < room.rect.bottom \
                and player.rect.top > room.rect.top \
                and player.rect.left >= room.rect.left \
                and player.rect.right <= room.rect.right
            pd = pd or player.rect.bottom + player.rect.height > room.rect.top \
                and player.rect.bottom < room.rect.bottom\
                and player.rect.left >= room.rect.left \
                and player.rect.right <= room.rect.right
            pl = pl or player.rect.left - player.rect.width < room.rect.right \
                and player.rect.left > room.rect.left \
                and player.rect.top >= room.rect.top \
                and player.rect.bottom <= room.rect.bottom
            pr = pr or player.rect.right + player.rect.width > room.rect.left \
                and player.rect.right < room.rect.right \
                and player.rect.top >= room.rect.top \
                and player.rect.bottom <= room.rect.bottom
    return pu, pd, pl, pr


# control player collision within room
def collide(player, rooms):
    for room in rooms:
        if player.rect.colliderect(room):
            pu, pd, pl, pr = can_pass(player, room, rooms)
            if not pl and player.rect.left <= room.rect.left + 5:
                player.rect.left = room.rect.left + 11
            elif not pr and player.rect.right >= room.rect.right - 5:
                player.rect.left = room.rect.right - player.rect.width - 11

            if not pu and player.rect.top < room.rect.top + 5:
                player.rect.top = room.rect.top + 11
            elif not pd and player.rect.bottom >= room.rect.bottom - 5:
                player.rect.top = room.rect.bottom - player.rect.height - 11


# allows to load levels from file
def load_level(level):
    with open(f"assets/levels/{level}.txt", "r") as f:
        items = (f.read().splitlines())
        items = [eval(item) for item in items]
        rooms = []
        chests = []
        for item in items:
            if item[0] == 0:
                rooms.append(dungeon.DungeonRoom(item[1], item[2]))
            elif item[0] == 1:
                rooms.append(dungeon.Corridor(item[1], item[2]))
            elif item[0] == 2:
                chests.append(dungeon.Chest(item[1], item[2]))

    return rooms, chests


# scroll for camera
true_scroll = [0, 0]
scroll = [0, 0]

# load level from file
dungeons, chests = load_level(0)

# initialize objects
player = Player()

# controls fps
clock = pygame.time.Clock()

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

        # check if key is released to set the movement variable based on that
        if event.type == pygame.KEYUP:
            if event.key in [pygame.K_LEFT, pygame.K_RIGHT]:
                player.movement[0] = 0
            if event.key in [pygame.K_UP, pygame.K_DOWN]:
                player.movement[1] = 0

    # sets the scroll value
    true_scroll[0] += (player.rect.x - (1280 / 2 - player.rect.width / 2)
                       - true_scroll[0]) / 25
    true_scroll[1] += (player.rect.y - (720 / 2 - player.rect.height / 2)
                       - true_scroll[1]) / 25
    scroll = true_scroll.copy()
    scroll[0] = int(scroll[0])
    scroll[1] = int(scroll[1])

    # moves objects
    player.move(dungeons)

    # draws to the screen
    screen.fill((255, 100, 100))
    for dungeon in dungeons:
        dungeon.draw(screen, scroll)
    for chest in chests:
        chest.draw(screen, scroll)
    player.draw(screen, scroll)

    # updates display
    display.blit(pygame.transform.scale(screen, (WIDTH, HEIGHT)), (0, 0))
    pygame.display.update()
    clock.tick(60)

pygame.quit()
