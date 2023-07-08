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
        self.dropped_items = []
        self.empty = False
        self.rect = pygame.Rect(x, y, 128, 64)
        self.color = (255, 175, 112)

    def generate_loot(self, player):
        if self.rect.colliderect(player.rect) and not self.empty:
            self.dropped_items.append(["sword", pygame.Rect(self.rect.centerx + random.randint(-32, 32), self.rect.centery + random.randint(-64, 64), 32, 32)])
            self.empty = True

    def draw(self, screen, scroll):
        pygame.draw.rect(screen, self.color, (self.rect.x - scroll[0], self.rect.y - scroll[1], self.rect.width, self.rect.height))
        for item in self.dropped_items:
            pygame.draw.rect(screen, (255, 255, 255), (item[1].x - scroll[0], item[1].y - scroll[1], item[1].width, item[1].height))


class End:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 128, 128)
        self.color = (255, 255, 0)

    def draw(self, screen, scroll):
        pygame.draw.rect(screen, self.color, (self.rect.x - scroll[0], self.rect.y - scroll[1], self.rect.width, self.rect.height))


def can_pass(self, current_room, rooms):
    pu, pd, pl, pr = [False, False, False, False]
    for room in rooms:
        if room != current_room:
            pu = (
                pu
                or self.rect.top - self.rect.height < room.rect.bottom
                and self.rect.top > room.rect.top
                and self.rect.left >= room.rect.left
                and self.rect.right <= room.rect.right
            )
            pd = (
                pd
                or self.rect.bottom + self.rect.height > room.rect.top
                and self.rect.bottom < room.rect.bottom
                and self.rect.left >= room.rect.left
                and self.rect.right <= room.rect.right
            )
            pl = (
                pl
                or self.rect.left - self.rect.width < room.rect.right
                and self.rect.left > room.rect.left
                and self.rect.top >= room.rect.top
                and self.rect.bottom <= room.rect.bottom
            )
            pr = (
                pr
                or self.rect.right + self.rect.width > room.rect.left
                and self.rect.right < room.rect.right
                and self.rect.top >= room.rect.top
                and self.rect.bottom <= room.rect.bottom
            )
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
