import assets.scripts.

class Enemy(entity.Entity):
    def __init__(self):
        super().__init__(404, 264, 64, 64, 5, "player.png")
        self.near_player = False

    def move(self, player, rooms):
        super().move(rooms)

        if not self.near_player:
            for room in rooms:
                if player.rect.colliderect(room.rect) and self.rect.colliderect(room.rect):
                    self.near_player = True
            self.movement = [0, 0]
            return True

        dx = self.rect.centerx - player.rect.centerx
        dy = self.rect.centery - player.rect.centery
        angle = math.atan2(dy, dx)
        self.movement[0] = -math.cos(angle)
        self.movement[1] = -math.sin(angle)

        self.direction = "right" if self.movement[0] > 0 else "left"
