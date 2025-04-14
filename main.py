import pygame
import sys
from screens.menu import run_menu
from screens.game import run_game
from screens.options import run_options
from screens.instructions import run_instructions
from screens.endgame import run_endgame

# Définir des constantes d'état
STATE_MENU = 'menu'
STATE_GAME = 'game'
STATE_OPTIONS = 'options'
STATE_INSTRUCTIONS = 'instructions'
STATE_ENDGAME = 'endgame'

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Tank Duel")
    clock = pygame.time.Clock()
    
    state = STATE_MENU  # État initial
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
        # Navigation entre les écrans en fonction de l'état courant
        if state == STATE_MENU:
            state = run_menu(screen)
        elif state == STATE_GAME:
            state = run_game(screen)
        elif state == STATE_OPTIONS:
            state = run_options(screen)
        elif state == STATE_INSTRUCTIONS:
            state = run_instructions(screen)
        elif state == STATE_ENDGAME:
            state = run_endgame(screen)
        
        pygame.display.flip()
        clock.tick(60)

if __name__ == '__main__':
    main()
