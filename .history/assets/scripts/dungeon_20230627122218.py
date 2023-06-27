import random

import pygame


class DungeonRoom:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 1024, 1024)
        self.color = (50, 0, 205)

    def draw(self, screen, scroll):
        pygame.draw.rect(screen, self.color,
                         (self.rect.x - scroll[0], self.rect.y - scroll[1], self.rect.width, self.rect.height))


class Corridor:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 256, 128)
        self.color = (50, 0, 205)

    def draw(self, screen, scroll):
        pygame.draw.rect(screen, self.color,
                         (self.rect.x - scroll[0], self.rect.y - scroll[1], self.rect.width, self.rect.height))


class Chest:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 128, 64)
        self.color = (255, 175, 112)

    def generate_loot():
        pass

    def draw(self, screen, scroll):
        pygame.draw.rect(screen, self.color,
                         (self.rect.x - scroll[0], self.rect.y - scroll[1], self.rect.width, self.rect.height))


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
