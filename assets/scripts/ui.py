import pygame


def title(text, x, y, screen):
    font = pygame.font.Font("assets/fonts/PressStart2p.ttf", 40)
    text = font.render(text, True, (0, 0, 0))
    text_rect = text.get_rect()
    screen.blit(text, (x - text_rect.width // 2, y - text_rect.height // 2))



class Button:
    def __init__(self, text, x, y, width, height):
        self.text = text
        self.rect = pygame.Rect(0, 0, width, height)
        self.rect.centerx = x
        self.rect.centery = y
        self.clicked = True

    def draw(self, screen):
        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()[0]

        if self.rect.collidepoint(mouse_pos):
            if mouse_pressed:
                if not self.clicked:
                    return self.normal_draw(True, screen)
                self.clicked = True
            else:
                self.clicked = False
            return self.hover_draw(screen)
        else:
            self.clicked = bool(mouse_pressed)
            return self.normal_draw(False, screen)


    def hover_draw(self, screen):
        pygame.draw.rect(screen, (255, 255, 255), (self.rect.x - 15,
                         self.rect.y - 15, self.rect.width + 30, self.rect.height + 30))

        self.draw_text(screen)
        return False

    def normal_draw(self, pressed, screen):
        result = pressed
        pygame.draw.rect(screen, (255, 255, 255), self.rect)

        self.draw_text(screen)
        return(result)

    def draw_text(self, screen):
        font = pygame.font.Font("assets/fonts/PressStart2p.ttf", 20)
        text = font.render(self.text, True, (0, 0, 0))
        text_rect = text.get_rect()
        screen.blit(
            text,
            (
                self.rect.centerx - text_rect.width // 2,
                self.rect.centery - text_rect.height // 2,
            ),
        )
