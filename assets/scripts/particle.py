import pygame

class Particle:
    def __init__(self, x, y, color, size, dx, dy, speed, shrink):
        self.x = x
        self.y = y
        self.size = size
        self.color = color
        self.dx = dx
        self.dy = dy
        self.speed = speed
        self.shrink = shrink
        self.surf = pygame.Surface((self.size * 2, self.size * 2), pygame.SRCALPHA)

    def update(self, dt):
        self.x += self.dx * self.speed * dt
        self.y += self.dy * self.speed * dt
        self.size -= self.shrink

    def draw(self, screen, scroll):
        pygame.draw.circle(self.surf, self.color, (self.size, self.size), self.size)
        screen.blit(self.surf, (self.x - scroll[0], self.y - scroll[1]))
