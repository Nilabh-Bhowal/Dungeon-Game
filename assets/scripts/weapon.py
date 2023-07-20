import pygame
import math

class Weapon:
    def __init__(self, holder, damage, reload_time, size):
        self.holder = holder
        self.damage = damage
        self.mode = "held"
        self.reload = reload_time
        self.timer = self.reload
        self.rect = pygame.Rect(self.holder.rect.x, self.holder.rect.y, size, size)

    def update(self, dt):
        self.update_mode(dt)

        if self.holder.direction == "up":
            self.rect = pygame.Rect(self.holder.rect.left, self.holder.rect.top - self.rect.height, self.holder.rect.width, self.rect.height)
        elif self.holder.direction == "down":
            self.rect = pygame.Rect(self.holder.rect.left, self.holder.rect.bottom, self.holder.rect.width, self.rect.height)
        elif self.holder.direction == "left":
            self.rect = pygame.Rect(self.holder.rect.left - self.rect.width, self.holder.rect.top, self.rect.width, self.holder.rect.height)
        else:
            self.rect = pygame.Rect(self.holder.rect.right, self.holder.rect.top, self.rect.width, self.holder.rect.height)

        # allows the ability to check if holder attacked
        return self.mode == "attack"

    def update_mode(self, dt):
        # updates mode from held to attack to cooldown
        if self.mode != "held":
            if 0 < self.timer * dt <= (self.reload - 1) * dt:
                self.mode = "cooldown"
            elif self.timer <= 0:
                self.mode = "held"
            self.timer -= 1 * dt
        else:
            self.timer = (self.reload) * dt

    def draw(self, screen, scroll):
        pygame.draw.rect(screen, (255, 255, 255), (self.rect.x - scroll[0], self.rect.y - scroll[1], self.rect.width, self.rect.height))


class Sword(Weapon):
    def __init__(self, holder, damage, size):
        super().__init__(holder, damage, 15, size)


class Bow(Weapon):
    def __init__(self, holder, damage, speed):
        super().__init__(holder, damage, 15, 5)
        self.speed = speed
        self.arrows = []

    def target(self, target_x, target_y):
        dx = target_x - self.holder.rect.centerx
        dy = target_y - self.holder.rect.centery
        return math.atan2(dy, dx)


    def update(self, target_x, target_y, opponents, dt):
        angle = self.target(target_x, target_y)
        if self.mode == "attack":
            self.arrows.append(Arrow(self.holder.rect.centerx, self.holder.rect.centery, angle, self.speed))
            self.mode = "cooldown"
        arrows_to_remove = []
        for arrow in self.arrows:
            arrow.aim(dt)
            if arrow.timer <= 0:
                arrows_to_remove.append(arrow)
        for arrow in self.arrows:
            for opponent in opponents:
                if arrow.rect.colliderect(opponent.rect):
                    opponent.health -= self.damage
                    arrows_to_remove.append(arrow)
        for arrow in arrows_to_remove:
            self.arrows.remove(arrow)
            arrows_to_remove.remove(arrow)

        super().update(dt)

    def draw(self, screen, scroll):
        super().draw(screen, scroll)
        for arrow in self.arrows:
            arrow.draw(screen, scroll)

class Arrow:
    def __init__(self, x, y, angle, speed):
        self.rect = pygame.Rect(x, y, 5, 5)
        self.speed = speed
        self.angle = angle
        self.timer = 120

    def aim(self, dt):
        dx = math.cos(self.angle)
        dy = math.sin(self.angle)
        self.rect.x += (dx * self.speed * dt)
        self.rect.y += (dy * self.speed * dt)
        self.timer -= 1 * dt

    def draw(self, screen, scroll):
        pygame.draw.rect(screen, (255, 255, 255), (self.rect.x - scroll[0], self.rect.y - scroll[1], self.rect.width, self.rect.height))
