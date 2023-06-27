import pygame

# import other python files in project
import assets.scripts.dungeon as dungeon
import assets.scripts.entity as entity

pygame.init()
pygame.display.init()

# create window
WIDTH = 1280
HEIGHT = 720
display = pygame.display.set_mode((WIDTH, HEIGHT))
screen = pygame.Surface((1280, 720))


# player class
class Player(entity.Entity):
    def __init__(self):
        super().__init__(304, 164, 64, 64, 10, "player.png")
        self.sword = Sword(self)

    def move(self, rooms):
        super().move(rooms)
        self.sword.update()

    def draw(self, screen, scroll):
        super().draw(screen, scroll)
        self.sword.draw(screen, scroll)


class Enemy(entity.Entity):
    def __init__(self):
        super().__init__(404, 264, 64, 64, 7, "player.png")

    def move(self, player, rooms):
        super().move(rooms)
        for room in rooms:
            if player.rect.colliderect(room.rect) and self.rect.colliderect(room.rect):
                if player.rect.left < self.rect.left:
                    self.movement[0] = -1
                elif player.rect.right < self.rect.right:
                    self.movement[0] = 1
                elif player.rect.top < self.rect.top:
                    self.movement[1] = -1
                elif player.rect.bottom < self.rect.bottom:
                    self.movement[1] = 1
            else:
                self.movement = [0, 0]


class Sword:
    def __init__(self, holder):
        self.holder = holder
        self.rect = pygame.Rect(self.holder.rect.x, self.holder.rect.y, 16, 32)

    def update(self):
        # sourcery skip: hoist-statement-from-if, merge-duplicate-blocks, remove-redundant-if, switch
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
enemies = [Enemy()]

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
    for enemy in e

    # draws to the screen
    screen.fill((255, 100, 100))
    for room in dungeons:
        room.draw(screen, scroll)
    for chest in chests:
        chest.draw(screen, scroll)
    player.draw(screen, scroll)

    # updates display
    display.blit(pygame.transform.scale(screen, (WIDTH, HEIGHT)), (0, 0))
    pygame.display.update()
    clock.tick(60)

pygame.quit()
