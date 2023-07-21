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

        print(os.listdir(self.tile_path))

        self.tiles = {}
        for number, image in enumerate(os.listdir(self.tile_path)):
            if image.endswith("png"):
                self.tiles[f"{list(tiles.keys())[number]}"] = pygame.transform.scale(pygame.image.load(f"{self.tile_path}/{image}"), (64, 64))
        print(self.tiles)

    def draw(self, screen, scroll, surrounding_tiles):
        tiles_surround = {"top": False, "bottom": False, "left": False, "right": False}
        for tile in surrounding_tiles:
            if tile.rect.left == self.rect.right:
                tiles_surround["right"] = True
            elif tile.rect.right == self.rect.left:
                tiles_surround["left"] = True
            elif tile.rect.bottom == self.rect.top:
                tiles_surround["top"] = True
            elif tile.rect.top == self.rect.bottom:
                tiles_surround["bottom"] = True
        for x, y in itertools.product(range(7), range(3)):
            if 6 > x > 0 or tiles_surround["right"] or tiles_surround["left"]:
                if 2 > y > 0:
                    curr_tile = self.tiles["center"]
                elif y == 2:
                    curr_tile = self.tiles["bottom"]
                elif y == 0:
                    curr_tile = self.tiles["top"]
            elif x == 6:
                if 2 > y > 0:
                    curr_tile = self.tiles["right"]
                elif y == 2:
                    curr_tile = self.tiles["bottomright"]
                elif y == 0:
                    curr_tile = self.tiles["topright"]
            elif x == 0:
                if 2 > y > 0:
                    curr_tile = self.tiles["left"]
                elif y == 2:
                    curr_tile = self.tiles["bottomleft"]
                elif y == 0:
                    curr_tile = self.tiles["topleft"]
            screen.blit(curr_tile, (self.rect.x + (x * 32), self.rect.y + (y * 32)))
