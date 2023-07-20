import pygame
import math

import assets.scripts.player as player

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
        dx = (math.cos(math.radians(self.holder.angle - 90)))
        dy = -(math.sin(math.radians(self.holder.angle - 90)))
        self.rect.centerx = self.holder.rect.x + (dx * self.rect.width * 2)
        self.rect.centery = self.holder.rect.y + (dy * self.rect.height * 2)

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
        draw_surf = pygame.Surface((self.rect.width, self.rect.height)).convert_alpha()
        draw_surf.fill((255, 255, 255))
        draw_surf = pygame.transform.rotate(draw_surf, self.holder.angle)
        dx = (math.cos(math.radians(self.holder.angle - 90)))
        dy = -(math.sin(math.radians(self.holder.angle - 90)))
        screen.blit(draw_surf, ((self.holder.rect.centerx - scroll[0]) - (draw_surf.get_width() / 2) + (dx * (self.rect.width + 16)), (self.holder.rect.centery - scroll[1]) - (draw_surf.get_height() / 2) + (dy * (self.rect.height + 16))))


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
                    opponent.stun(-math.degrees(arrow.angle) + 90)
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
