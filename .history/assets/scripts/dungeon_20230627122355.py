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


def can_pass(entity, current_room, rooms):
    # sourcery skip: instance-method-first-arg-name
    pu, pd, pl, pr = [False, False, False, False]
    for room in rooms:
        if room != current_room:
            pu = pu or entity.rect.top - entity.rect.height < room.rect.bottom \
                and entity.rect.top > room.rect.top \
                and entity.rect.left >= room.rect.left \
                and entity.rect.right <= room.rect.right
            pd = pd or entity.rect.bottom + entity.rect.height > room.rect.top \
                and entity.rect.bottom < room.rect.bottom\
                and entity.rect.left >= room.rect.left \
                and entity.rect.right <= room.rect.right
            pl = pl or entity.rect.left - entity.rect.width < room.rect.right \
                and entity.rect.left > room.rect.left \
                and entity.rect.top >= room.rect.top \
                and entity.rect.bottom <= room.rect.bottom
            pr = pr or entity.rect.right + entity.rect.width > room.rect.left \
                and entity.rect.right < room.rect.right \
                and entity.rect.top >= room.rect.top \
                and entity.rect.bottom <= room.rect.bottom
    return pu, pd, pl, pr


# control player collision within room
def collide(entity, rooms):
    for room in rooms:
        if entity.rect.colliderect(room):
            pu, pd, pl, pr = can_pass(entity, room, rooms)
            if not pl and entity.rect.left <= room.rect.left + 5:
                entity.rect.left = room.rect.left + 11
            elif not pr and entity.rect.right >= room.rect.right - 5:
                entity.rect.left = room.rect.right - entity.rect.width - 11

            if not pu and entity.rect.top < room.rect.top + 5:
                entity.rect.top = room.rect.top + 11
            elif not pd and entity.rect.bottom >= room.rect.bottom - 5:
                entity.rect.top = room.rect.bottom - entity.rect.height - 11
