import pygame
from player import Tank
from joystick_input import JoystickReader  # <-- ajouter cette ligne

STATE_ENDGAME = 'endgame'

def run_game(screen):
    tank1 = Tank(150, 300, angle=0, color=(0, 255, 0))
    tank2 = Tank(650, 300, angle=180, color=(0, 0, 255))
    projectiles = []

    joystick = JoystickReader()  # <-- initialiser le joystick

    clock = pygame.time.Clock()
    running = True
    while running:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                running = False

        input_state = joystick.get_direction()

        # Contrôle par joystick pour tank1
        tank1.update_from_flags(
            forward=input_state["forward"],
            left=input_state["left"],
            right=input_state["right"]
        )

        # Tir joystick
        if input_state["shoot"]:
            proj = tank1.shoot()
            if proj:
                projectiles.append(proj)

        # Contrôle clavier pour tank2 (inchangé)
        keys = pygame.key.get_pressed()
        tank2.update(keys, forward_key=pygame.K_z, left_key=pygame.K_q, right_key=pygame.K_d)
        if keys[pygame.K_s]:
            proj = tank2.shoot()
            if proj:
                projectiles.append(proj)

        # MàJ des projectiles et collisions
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
