import pygame
import math
import random

import assets.scripts.entity as entity

class Enemy(entity.Entity):
    def __init__(self, x, y, width, height, speed, health, img):
        super().__init__(x, y, width, height, speed, health, img)
        self.near_player = False
        self.range = random.randint(400, 600)

    def move(self, player, dt, rooms):
        super().move(dt, rooms)
        if math.hypot(self.rect.centerx - player.rect.centerx, self.rect.centery - player.rect.centery) < self.range:
            dx = self.rect.centerx - player.rect.centerx
            dy = self.rect.centery - player.rect.centery
            angle = math.atan2(dy, dx)
            self.movement[0] = -math.cos(angle)
            self.movement[1] = -math.sin(angle)

            self.direction = "right" if self.movement[0] > 0 else "left"

        self.check_damaged(player)

    def check_damaged(self, player):
        if self.rect.colliderect(player.sword.range_rect) and player.attack:
            self.health -= random.randint(20, 40)
        if self.health <= 0:
            self.alive = False
