import itertools
import pygame
import os
import json

class TileManager:
    def __init__(self, rect):
        self.rect = rect
        self.tile_path = "assets/images/tiles"
        with open(f"{self.tile_path}/tile_types.json", "r") as f:
            tiles = json.load(f)
        self.tiles = {}
        for number, image in enumerate(os.listdir(self.tile_path)):
            if image.endswith("png"):
                self.tiles[f"{list(tiles.keys())[number]}"] = pygame.transform.scale(pygame.image.load(f"{self.tile_path}/{image}"), (32, 32))

        self.tiles_surround = {"top": False, "bottom": False, "left": False, "right": False}
        self.tile_map = [[{"type": "empty", "top": False, "bottom": False, "left": False, "right": False, } for _ in range(self.rect.width // 32)] for _ in range(self.rect.height // 32)]

    def load_rooms(self, rooms):
        for y, row in enumerate(self.tile_map):
            for x, tile in enumerate(row):
                tile_rect = pygame.Rect(self.rect.x + x * 32, self.rect.y + y * 32, 32, 32)
                for room in rooms:
                    if room.rect.collidepoint((tile_rect.left - 5, tile_rect.centery)) or x > 0:
                        tile["left"] = True
                    elif room.rect.collidepoint((tile_rect.right + 5, tile_rect.centery)) or x < self.rect.width // 32:
                        tile["right"] = True
                    elif room.rect.collidepoint((tile_rect.centerx, tile_rect.bottom + 5)) or y < self.rect.height // 32:
                        tile["bottom"] = True
                    elif room.rect.collidepoint((tile_rect.centerx, tile_rect.top - 5)) or y > 0:
                        tile["top"] = True

        self.add_to_map()

    def add_to_map(self):
        for row in self.tile_map:
            for tile in row:
                if tile["bottom"] and tile["top"] and tile["left"] and tile["right"]:
                    tile["type"] = "center"
                elif tile["top"]:
                    if tile["left"]:
                        tile["type"] = "topleft"
                    elif tile["right"]:
                        tile["type"] = "topright"
                    else:
                        tile["type"] = "top"
                elif tile["bottom"]:
                    if tile["left"]:
                        tile["type"] = "bottomleft"
                    elif tile["right"]:
                        tile["type"] = "bottomright"
                    else:
                        tile["type"] = "bottom"
                elif tile["left"]:
                    tile["type"] = "left"
                elif tile["right"]:
                    tile["type"] = "right"

    def draw(self, screen, scroll):

        for y, row in enumerate(self.tile_map):
            for x, tile in enumerate(row):
                screen.blit(self.tiles[tile["type"]], (self.rect.x + (x * 32) - scroll[0], self.rect.y + (y * 32) - scroll[1]))
