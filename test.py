import pygame


pygame.init()


screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Tank Game")

running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

  
    screen.fill((32, 49, 203))
    pygame.display.flip()

pygame.quit()
