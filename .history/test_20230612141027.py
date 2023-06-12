import pygame

import dungeon

pygame.init()
pygame.display.init()

WIDTH = 1280
HEIGHT = 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))


class Player:
    def __init__(self):
        self.rect = pygame.Rect(608, 328, 64, 64)
        self.color = (255, 255, 255)

    def draw(self, screen, scroll):
        pygame.draw.rect(screen, self.color, (self.rect.x - scroll[0], self.rect.y - scroll[1], self.rect.width, self.rect.height))

def collide(player, rect):
    if player.rect.x < rect.x:
        player.rect.x = rect.x.copy()


input = [0, 0]

scroll = [0, 0]

player = Player()
dungeon = dungeon.DungeonRoom()

clock = pygame.time.Clock()

running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                input[0] = -1
            if event.key == pygame.K_RIGHT:
                input[0] = 1
            if event.key == pygame.K_UP:
                input[1] = -1
            if event.key == pygame.K_DOWN:
                input[1] = 1

        if event.type == pygame.KEYUP:
            if event.key in [pygame.K_LEFT, pygame.K_RIGHT]:
                input[0] = 0
            if event.key in [pygame.K_UP, pygame.K_DOWN]:
                input[1] = 0

    scroll[0] += (player.rect.x - (WIDTH / 2 - player.rect.width / 2) - scroll[0]) / 10
    scroll[1] += (player.rect.y - (HEIGHT / 2 - player.rect.height / 2) - scroll[1]) / 10

    player.rect.x += 10 * input[0]
    player.rect.y += 10 * input[1]


    screen.fill((255, 100, 100))
    dungeon.draw(screen, scroll)
    player.draw(screen, scroll)

    pygame.display.update()
    clock.tick(60)

pygame.quit()