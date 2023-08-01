import pygame
import math
import random

import assets.scripts.entity as entity
import assets.scripts.enemy as enemy
import assets.scripts.weapon as weapon

class Boss(entity.Entity):
    def __init__(self, x, y):
        super().__init__(x, y, 256, 256, 0, 2500, "boss.png")
        self.img = pygame.transform.scale2x(self.img)
        self.attacks = "none"
        self.bossfight = False
        self.hurt_sound = pygame.mixer.Sound("assets/sounds/effects/enemy_hurt.wav")
        self.immune = True
        self.wave = 1
        self.attacks_used = 0
        self.wave_timer = 0
        self.enemies = []

    def attack(self):
        if self.attacks != "monsters":
            return
        self.attacks = "none"
        self.attacks_used += 1
        for _ in range(random.randint(0, 3)):
            angle = random.randint(0, 360)
            dx = math.cos(angle)
            dy = math.sin(angle)
            self.enemies.append(enemy.Zombie(dx * self.rect.width + self.rect.centerx, dy * self.rect.height + self.rect.centery))
        for _ in range(random.randint(0, 1)):
            angle = random.randint(0, 360)
            dx = math.cos(angle)
            dy = math.sin(angle)
            self.enemies.append(enemy.Archer(dx * self.rect.width + self.rect.centerx, dy * self.rect.height + self.rect.centery))

    def update(self, player, rooms, volume, death_particles, dt):
        self.enemies = []
        x = self.rect.x
        y = self.rect.y
        super().move(dt, rooms)
        self.rect.x = x
        self.rect.y = y
        self.wave_timer += 1 * dt
        self.angle = math.degrees(-math.atan2(player.rect.centery - self.rect.centery, player.rect.centerx - self.rect.centerx)) + 180
        if math.hypot(player.rect.y - self.rect.y, player.rect.x - self.rect.x) < 200 and self.immune:
            player.stun(-self.angle)
        if self.bossfight and math.hypot(player.rect.y - self.rect.y, player.rect.x - self.rect.x) > 1024:
            player.stun(self.angle)
        if self.immune and self.alive and math.hypot(player.rect.y - self.rect.y, player.rect.x - self.rect.x) < 1024 and self.health >= 0:
            self.bossfight = True
            if random.randint(0, 500) <= self.wave_timer / 5 and self.attacks_used <= 4:
                self.attacks = "monsters"
            self.attack()
            if self.wave_timer >= 1000:
                self.attacks_used = 0
                self.immune = False

        shake = False
        if player.attack and not self.immune and self.rect.colliderect(player.active_item.rect):
            self.hurt_sound.set_volume(volume * 0.4)
            self.hurt_sound.play()
            self.health -= player.active_item.damage
            if self.health % 500 > 460 and self.health < 2000:
                self.immune = True
                self.wave_timer = 0

        return shake, death_particles, self.enemies

    def draw(self, screen, scroll):
        super().draw(screen, scroll)
        if self.immune:
            pygame.draw.circle(screen, (120, 120, 255), (self.rect.centerx - scroll[0], self.rect.centery - scroll[1]), 200, 10)
        pygame.draw.rect(screen, (255, 0, 0), (self.rect.centerx - scroll[0] - 50, self.rect.y - scroll[1] - 10, 100, 15))
        pygame.draw.rect(screen, (0, 255, 0), (self.rect.centerx - scroll[0] - 50, self.rect.y - scroll[1] - 10, 100 / self.max_health * self.health, 15))
