import pygame
import math
import random

import assets.scripts.entity as entity
import assets.scripts.enemy as enemy
import assets.scripts.weapon as weapon

class Boss(entity.Entity):
    def __init__(self, x, y):
        super().__init__(x, y, 256, 256, 0, 500, "boss.py")
        self.attack = "none"
        self.enemies = []
        self.fireballs = []

    def attack(self):
        if self.attack == "monsters":
            for _ in range(random.randint(3, 5)):
                angle = random.randint(0, 360)
                dx = math.cos(angle)
                dy = math.sin(angle)
                self.self.enemies.append(enemy.Zombie(dx * self.rect.width, dy * self.rect.height))
            for _ in range(random.randint(3, 5)):
                angle = random.randint(0, 360)
                dx = math.cos(angle)
                dy = math.sin(angle)
                self.self.enemies.append(enemy.Archer(dx * self.rect.width, dy * self.rect.height))
            self.attack = "none"
        elif self.attack == "fireball":
            self.attack = "none"
            self.fireballs.append(weapon.Fireball(self.rect.centerx, self.rect.centery, self.angle))

    def update(self, player, rooms, volume, death_particles, dt):
        x = self.rect.x
        y = self.rect.y
        super().move(dt, rooms)
        self.rect.x = x
        self.rect.y = y
        if player.attack and not self.immune and self.rect.colliderect(player.active_item.rect):
            self.hurt_sound.set_volume(volume * 0.2)
            self.hurt_sound.play()
            self.health -= random.randint(20, 40)
            self.stun(player.angle)
        for i, e in sorted(enumerate(self.enemies), reverse=True):
            e.move(player, dt, rooms, volume)
            if e.health <= 0:
                self.enemies.pop(i)
                death_particles.add_burst(e.rect.centerx, e.rect.centery, (200, 200, 200), 20, 10, 1, 500)
                shake = True
        for e in self.enemies:
            half_width = e.rect.width / 5
            half_height = e.rect.height / 5
            new_e_rect = pygame.Rect(e.rect.centerx - half_width, e.rect.centery - half_height, half_width * 2, half_height * 2)
            if new_e_rect.colliderect(player.rect):
                player.stun(e.angle)
                e.stun(-e.angle)
                break

        return shake
