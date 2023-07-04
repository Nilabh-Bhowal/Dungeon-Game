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

    def draw(self, screen):

        if self.rect.collidepoint(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]):
            return (
                self.normal_draw(True, screen)
                if pygame.mouse.get_pressed()[0]
                else self.hover_draw(screen)
            )
        else:
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
