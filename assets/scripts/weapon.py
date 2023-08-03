import pygame
import math

import assets.scripts.dungeon as dungeon
import assets.scripts.animation as animation

class Weapon:
    def __init__(self, holder, damage, reload_time, size, img):
        self.holder = holder
        self.damage = damage
        self.mode = "held"
        self.animation = animation.Animation(img)
        self.reload = reload_time
        self.timer = self.reload
        self.rect = pygame.Rect(self.holder.rect.x, self.holder.rect.y, size, size)

    def update(self, dt):
        self.animation.update()
        self.update_mode(dt)
        if self.mode == "attack":
            self.animation.change_animation("attack")
        elif self.mode == "load":
            self.animation.change_animation("load")
        elif self.mode == "held":
            self.animation.change_animation("idle")
        dx = (math.cos(math.radians(self.holder.angle - 90)))
        dy = -(math.sin(math.radians(self.holder.angle - 90)))
        self.rect.centerx = self.holder.rect.centerx + (dx * (16 + self.rect.height / 2))
        self.rect.centery = self.holder.rect.centery + (dy * (16 + self.rect.height / 2))

        # allows the ability to check if holder attacked
        return self.mode == "attack"

    def update_mode(self, dt):
        # updates mode from held to attack to cooldown
        if self.mode not in ["held", "load"]:
            if 0 < self.timer * dt <= (self.reload - 1) * dt:
                self.mode = "cooldown"
            elif self.timer <= 0:
                self.mode = "held"
            self.timer -= 1 * dt
        else:
            self.timer = (self.reload) * dt

    def draw(self, screen, scroll):
        draw_surf = pygame.transform.rotate(self.animation.get_image(), self.holder.angle + 180)
        dx = (math.cos(math.radians(self.holder.angle - 90)))
        dy = -(math.sin(math.radians(self.holder.angle - 90)))
        screen.blit(draw_surf, ((self.holder.rect.centerx - scroll[0]) - (draw_surf.get_width() / 2) + (dx * (self.rect.width + 16)), (self.holder.rect.centery - scroll[1]) - (draw_surf.get_height() / 2) + (dy * (self.rect.height + 16))))


class Sword(Weapon):
    def __init__(self, holder, damage, size):
        super().__init__(holder, damage, 7, size, "sword")


class Bow(Weapon):
    def __init__(self, holder, damage, speed):
        super().__init__(holder, damage, 5, 15, "bow")
        self.sound = pygame.mixer.Sound("assets/sounds/effects/shoot.wav")
        self.speed = speed
        self.strength = 5
        self.arrows = []

    def target(self, target_x, target_y):
        dx = target_x - self.holder.rect.centerx
        dy = target_y - self.holder.rect.centery
        return math.atan2(dy, dx)


    def update(self, target_x, target_y, opponents, dt, rooms, volume):
        self.sound.set_volume(volume)
        angle = self.target(target_x, target_y)
        if self.mode == "attack":
            self.sound.play()
            self.arrows.append(Arrow(self.holder.rect.centerx, self.holder.rect.centery, angle, max(self.holder.speed, self.speed * (self.strength / 3)), self.damage * self.strength / 2))
            self.mode = "cooldown"

        for i, arrow in sorted(enumerate(self.arrows), reverse=True):
            arrow.aim(dt, rooms)
            arrow_removed = False
            if (arrow.timer <= 0 or arrow.collided) and not arrow_removed:
                self.arrows.pop(i)
                arrow_removed = True
            for opponent in opponents:
                if arrow.rect.colliderect(opponent.rect) and not arrow_removed:
                    opponent.health -= arrow.damage
                    opponent.stun(-math.degrees(math.atan2(arrow.movement[1], arrow.movement[0])) + 90)
                    self.arrows.pop(i)
                    arrow_removed = True
                    break

        super().update(dt)

    def draw(self, screen, scroll):
        super().draw(screen, scroll)
        for arrow in self.arrows:
            arrow.draw(screen, scroll)

class Arrow:
    def __init__(self, x, y, angle, speed, damage):
        self.rect = pygame.Rect(x, y, 15, 15)
        self.speed = speed
        self.damage = damage
        self.animation = animation.Animation("arrow")
        self.collided = False
        self.angle = math.degrees(angle)
        self.movement = [math.cos(angle), math.sin(angle)]
        self.timer = 120

    def aim(self, dt, rooms):
        self.animation.update()
        self.collided = dungeon.collide(self, rooms, dt)
        self.rect.x += (self.movement[0] * self.speed * dt)
        self.rect.y += (self.movement[1] * self.speed * dt)
        self.timer -= 1 * dt

    def draw(self, screen, scroll):
        draw_surf = pygame.transform.rotate(self.animation.get_image(), -self.angle - 90)
        screen.blit(draw_surf, ((self.rect.centerx - scroll[0]) - (draw_surf.get_width() / 2), (self.rect.centery - scroll[1]) - (draw_surf.get_height() / 2)))
