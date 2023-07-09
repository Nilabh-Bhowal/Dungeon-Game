import pygame

class Sword:
    def __init__(self, holder, damage, size):
        self.holder = holder
        self.damage = damage
        self.rect = pygame.Rect(self.holder.rect.x, self.holder.rect.y, size, size)
        self.mode = "held"
        self.timer = 15

    def update(self, dt):
        self.update_mode(dt)

        # put sword hitbox in right spot
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
            self.timer -= 1 * dt
            if 0 < self.timer <= 10 * dt:
                self.mode = "cooldown"
            elif self.timer <= 0:
                self.mode = "held"
        else:
            self.timer = 15 * dt


    def draw(self, screen, scroll):
        pygame.draw.rect(screen, (255, 255, 255), (self.rect.x - scroll[0], self.rect.y - scroll[1], self.rect.width, self.rect.height))
