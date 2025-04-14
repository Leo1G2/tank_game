import pygame

# Initialisation de Pygame
pygame.init()

# Création de la fenêtre de jeu
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Tank Game")

running = True
while running:
    # Gestion des événements
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Remplir l'écran avec une couleur (noir)
    screen.fill((32, 49, 203))
    pygame.display.flip()

pygame.quit()
