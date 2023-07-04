import pygame
import math
import random

import assets.scripts.entity as entity

class Enemy(entity.Entity):
    def __init__(self, x, y, width, height, speed, health, img):
        super().__init__(x, y, width, height, speed, health, img)
        self.immune = False
        self.immune_timer = 15
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
        if self.rect.colliderect(player.sword.rect) and player.attack and not self.immune:
            self.health -= random.randint(20, 40)
            self.movement = [0, 0]
            if player.direction == "left":
                self.rect.x -= 100
            elif player.direction == "right":
                self.rect.x += 100
            elif player.direction == "up":
                self.rect.y -= 100
            else:
                self.rect.y += 100
            self.immune = True
            self.immune_timer = 15
        if self.immune:
            self.immune_timer -= 1
            if self.immune_timer <= 0:
                self.immune = False
        if self.health <= 0:
            self.alive = False
