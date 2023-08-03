import pygame
import math
import random

import assets.scripts.entity as entity
import assets.scripts.weapon as weapon

class Enemy(entity.Entity):
    def __init__(self, x, y, width, height, speed, range, health, img):
        super().__init__(x, y, width, height, speed, health, img)
        self.immune = False
        self.hurt_sound = pygame.mixer.Sound("assets/sounds/effects/enemy_hurt.wav")
        self.immune_timer = 0
        self.near_player = False
        self.state = "idle"
        self.range = range

    def move(self, player, dt, rooms, volume):
        super().move(dt, rooms)
        self.check_damaged(player, volume)

        if self.state == "target":
            self.target_player(player)


        if math.hypot(self.rect.centerx - player.rect.centerx, self.rect.centery - player.rect.centery) < self.range and self.state not in ["stunned", "attack"]:
            self.state = "target"

    def target_player(self, player):
        dx = self.rect.centerx - player.rect.centerx
        dy = self.rect.centery - player.rect.centery
        angle = math.atan2(dy, dx)
        self.angle = -math.degrees(angle) - 90
        self.movement[0] = -math.cos(angle)
        self.movement[1] = -math.sin(angle)

    def check_damaged(self, player, volume):
        if self.immune:
            self.immune_timer -= 1
        if self.immune_timer <= 0 and self.immune:
            self.immune = False
            self.state = "idle"

        if player.attack and not self.immune and self.rect.colliderect(player.active_item.rect):
            self.hurt_sound.set_volume(volume * 0.2)
            self.hurt_sound.play()
            self.health -= player.active_item.damage
            self.stun(player.angle)

        if self.health <= 0:
            self.alive = False

    def draw(self, screen, scroll):
        super().draw(screen, scroll)
        if self.health < self.max_health:
            pygame.draw.rect(screen, (255, 0, 0), (self.rect.centerx - scroll[0], self.rect.y - scroll[1] + 10, 20, 5))
            pygame.draw.rect(screen, (0, 255, 0), (self.rect.centerx - scroll[0], self.rect.y - scroll[1] + 10, 20 / self.max_health * self.health, 5))


class Zombie(Enemy):
    def __init__(self, x, y):
        super().__init__(x, y, 64, 64, 4, 550, 70, "zombie.png")
        self.weapon = weapon.Sword(self, 7, 16)
        self.attack = False

    def move(self, player, dt, rooms, volume):
        if self.weapon.rect.inflate(10, 10).colliderect(player.rect):
            self.strike()

        super().move(player, dt, rooms, volume)
        self.attack = self.weapon.update(dt)

    def strike(self):
        if self.weapon.mode == "held" and random.randint(0, 1) == 0:
            self.weapon.mode = "attack"

    def draw(self, screen, scroll):
        self.weapon.draw(screen, scroll)
        super().draw(screen, scroll)


class Archer(Enemy):
    def __init__(self, x, y):
        super().__init__(x, y, 64, 64, 1, 600, 70, "archer.png")
        self.weapon = weapon.Bow(self, 2, 15)
        self.attack = False
        self.attack_timer = 0

    def move(self, player, dt, rooms, volume):
        if self.state == "target":
            self.strike()

        super().move(player, dt, rooms, volume)
        self.weapon.update(player.rect.centerx + random.randint(-32, 32), player.rect.centery + random.randint(-32, 32), [player], dt, rooms, volume)

    def strike(self):
        self.attack_timer += 1
        if self.attack_timer >= random.randint(60, 90):
            self.attack_timer = 0
        if self.weapon.mode == "held" and self.attack_timer == 0:
            self.weapon.mode = "attack"

    def draw(self, screen, scroll):
        self.weapon.draw(screen, scroll)
        super().draw(screen, scroll)
