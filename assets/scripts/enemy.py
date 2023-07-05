import pygame
import math
import random

import assets.scripts.entity as entity

class Enemy(entity.Entity):
    def __init__(self, x, y, width, height, speed, health, img):
        super().__init__(x, y, width, height, speed, health, img)
        self.immune = False
        self.immune_timer = 0
        self.knockback_direction = self.direction
        self.near_player = False
        self.state = "idle"
        self.range = random.randint(600, 800)

    def move(self, player, dt, rooms):
        super().move(dt, rooms)
        self.check_damaged(player)

        if self.state == "attack":
            self.target_player(player)
        if self.state == "stunned":

            self.movement = [0, 0]
            if self.knockback_direction == "left":
                self.rect.x -= 10
            elif self.knockback_direction == "right":
                self.rect.x += 10
            elif self.knockback_direction == "up":
                self.rect.y -= 10
            else:
                self.rect.y += 10

        if math.hypot(self.rect.centerx - player.rect.centerx, self.rect.centery - player.rect.centery) < self.range and self.state != "stunned":
            self.state = "attack"

        self.direction = "right" if self.movement[0] > 0 else "left"

    def target_player(self, player):
        dx = self.rect.centerx - player.rect.centerx
        dy = self.rect.centery - player.rect.centery
        angle = math.atan2(dy, dx)
        self.movement[0] = -math.cos(angle)
        self.movement[1] = -math.sin(angle)

    def check_damaged(self, player):
        if self.immune:
            self.immune_timer -= 1
        if self.immune_timer <= 0 and self.immune:
            self.immune = False
            self.state = "idle"

        if self.rect.colliderect(player.sword.rect) and player.attack and not self.immune:
            self.health -= random.randint(20, 40)
            self.state = "stunned"
            self.knockback_direction = player.direction
            self.immune = True
            self.immune_timer = 15

        if self.health <= 0:
            self.alive = False
