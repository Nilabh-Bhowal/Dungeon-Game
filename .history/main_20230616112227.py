import pygame

# import other python files in project
import dungeon

pygame.init()
pygame.display.init()

# create window
WIDTH = 1280
HEIGHT = 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))


# player class
class Player:
    def __init__(self):
        self.rect = pygame.Rect(608, 328, 64, 64)
        self.speed = 10
        self.movement = [0, 0]
        self.color = (255, 255, 255)

    def move(self, rooms):
        self.rect.x += self.speed * self.movement[0]
        self.rect.y += self.speed * self.movement[1]
        collide(self, rooms)

    def draw(self, screen, scroll):
        pygame.draw.rect(screen, self.color,
                         (self.rect.x - scroll[0], self.rect.y - scroll[1], self.rect.width, self.rect.height))


# check if player can pass into other rooms
def can_pass(player, current_room, rooms):
    for room in rooms:
        if room != current_room:
            pu = player.rect.top - player.rect.height * 2 < room.rect.bottom \
                and player.rect.top > room.rect.top \
                and player.rect.left >= room.rect.left \
                and player.rect.right <= room.rect.right
            pd = player.rect.bottom + player.rect.height > room.rect.top \
                and player.rect.bottom < room.rect.bottom\
                and player.rect.left >= room.rect.left \
                and player.rect.right <= room.rect.right
            pl = player.rect.left - player.rect.width < room.rect.right \
                and player.rect.left > room.rect.left \
                and player.rect.top >= room.rect.top \
                and player.rect.bottom <= room.rect.bottom
            pr = player.rect.right + player.rect.width > room.rect.left \
                and player.rect.right < room.rect.right \
                and player.rect.top >= room.rect.top \
                and player.rect.bottom <= room.rect.bottom
            if pu or pd or pl or pr:
                return pu, pd, pl, pr
    return pu, pd, pl, pr


# control player collision within room
def collide(player, rooms):
    for room in rooms:
        if player.rect.colliderect(room):
            pu, pd, pl, pr = can_pass(player, room, rooms)
            print(can_pass(player, room, rooms))
            if not pl and player.rect.left <= room.rect.left + 5:
                player.rect.left = room.rect.left + 11
            elif not pr and player.rect.right >= room.rect.right - 5:
                player.rect.left = room.rect.right - player.rect.width - 11

            if not pu and player.rect.top <= room.rect.top + 5:
                player.rect.top = room.rect.top + 11
            elif not pd and player.rect.bottom >= room.rect.bottom - 5:
                player.rect.top = room.rect.bottom - player.rect.height - 11


# allows to load levels from file
def load_level(file):
    with open(file, "r") as f:
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
dungeons, chests = load_level("levels/0.txt")

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
            if event.key == pygame.K_RIGHT:
                player.movement[0] = 1
            if event.key == pygame.K_UP:
                player.movement[1] = -1
            if event.key == pygame.K_DOWN:
                player.movement[1] = 1

        # check if key is released to set the movement variable based on that
        if event.type == pygame.KEYUP:
            if event.key in [pygame.K_LEFT, pygame.K_RIGHT]:
                player.movement[0] = 0
            if event.key in [pygame.K_UP, pygame.K_DOWN]:
                player.movement[1] = 0

    # sets the scroll value
    true_scroll[0] += (player.rect.x - (WIDTH / 2 - player.rect.width / 2)
                       - true_scroll[0]) / 10
    true_scroll[1] += (player.rect.y - (HEIGHT / 2 - player.rect.height / 2)
                       - true_scroll[1]) / 10
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
    pygame.display.update()
    clock.tick(60)

pygame.quit()
