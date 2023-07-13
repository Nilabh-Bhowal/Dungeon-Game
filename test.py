import pygame
import assets.scripts.ui as ui

pygame.init()

screen = pygame.display.set_mode((1280, 720))

running = True

prompt = ui.PromptBox("Testing")

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        prompt.handle_input(event)



    screen.fill((255, 255, 255))
    prompt.draw(screen)

    pygame.display.update()

pygame.quit()
