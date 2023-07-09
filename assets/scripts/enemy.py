import pygame
import math
import random

import assets.scripts.entity as entity
import assets.scripts.weapon as weapon

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

        if self.state == "target":
            self.target_player(player)
        elif self.state == "stunned":
            self.movement = [0, 0]


        if math.hypot(self.rect.centerx - player.rect.centerx, self.rect.centery - player.rect.centery) < self.range and self.state not in ["stunned", "attack"]:
            self.state = "target"

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

        if player.attack and not self.immune and self.rect.colliderect(player.active_item.rect):
            self.health -= random.randint(20, 40)
            self.state = "stunned"
            self.knockback_direction = player.direction
            self.immune = True
            self.immune_timer = 15

        if self.health <= 0:
            self.alive = False


class Zombie(Enemy):
    def __init__(self, x, y):
        super().__init__(x, y, 64, 64, 4, 70, "player.png")
        self.weapon = weapon.Sword(self, 10, 16)
        self.attack = False

    def move(self, player, dt, rooms):
        if self.weapon.rect.colliderect(player.rect):
            self.strike()

        super().move(player, dt, rooms)
        self.attack = self.weapon.update(dt)

    def strike(self):
        if self.weapon.mode == "held" and random.randint(0, 15) == 15:
            self.weapon.mode = "attack"

    def draw(self, screen, scroll):
        self.weapon.draw(screen, scroll)
        super().draw(screen, scroll)
