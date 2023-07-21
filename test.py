import pygame
import os
import assets.scripts.dungeon as dungeon

pygame.init()

screen = pygame.display.set_mode((800, 600))

player = pygame.image.load("assets/images/entity/player.png")

room = dungeon.Corridor(0, 0)
room2 = dungeon.Corridor(256, 0)

rooms = [room, room2]

running = True
while running:
    screen.fill((255, 255, 255))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    room.draw(screen, [0, 0], rooms)
    room2.draw(screen, [0, 0], rooms)
    screen.blit(player, (0, 0))
    pygame.display.update()

pygame.quit()
