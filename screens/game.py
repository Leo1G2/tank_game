import pygame
from player import Tank

STATE_ENDGAME = 'endgame'

def run_game(screen):
    tank1 = Tank(150, 300, angle=0, color=(0, 255, 0))
    tank2 = Tank(650, 300, angle=180, color=(0, 0, 255))
    projectiles = []

    clock = pygame.time.Clock()
    running = True
    while running:
        clock.tick(60) 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                running = False

        keys = pygame.key.get_pressed()
        tank1.update(keys, forward_key=pygame.K_UP, left_key=pygame.K_LEFT, right_key=pygame.K_RIGHT)
        tank2.update(keys, forward_key=pygame.K_z, left_key=pygame.K_q, right_key=pygame.K_d)

        
        if keys[pygame.K_SPACE]:
            proj = tank1.shoot()
            if proj:
                projectiles.append(proj)
        if keys[pygame.K_s]:
            proj = tank2.shoot()
            if proj:
                projectiles.append(proj)

        new_projectiles = []
        for proj in projectiles:
            proj.update()

            if proj.owner != tank1 and tank1.get_rect().colliderect(proj.get_rect()):
                tank1.hp -= proj.power
                continue  
            if proj.owner != tank2 and tank2.get_rect().colliderect(proj.get_rect()):
                tank2.hp -= proj.power
                continue

            new_projectiles.append(proj)

        projectiles = new_projectiles  

        
        screen.fill((30, 30, 30))
        tank1.draw(screen)
        tank2.draw(screen)
        for proj in projectiles:
            proj.draw(screen)

        pygame.display.flip()

        
        if tank1.hp <= 0 or tank2.hp <= 0:
            running = False

    return STATE_ENDGAME