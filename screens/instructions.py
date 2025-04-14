import pygame
import math

STATE_MENU = 'menu'

def draw_tank(surface, x, y, color, angle=0, scale=1.0):
    """Dessine un tank à la position spécifiée"""
    radius = 15 * scale
    pygame.draw.circle(surface, color, (int(x), int(y)), int(radius))
    
   
    end_x = x + radius * 1.2 * math.cos(math.radians(angle))
    end_y = y - radius * 1.2 * math.sin(math.radians(angle))
    pygame.draw.line(surface, (255, 255, 255), (x, y), (end_x, end_y), max(2, int(3 * scale)))
    
   
    track_width = radius * 2.2
    track_height = radius * 0.8
    track_x = x - track_width / 2
    track_y = y - track_height / 2
    pygame.draw.rect(surface, (100, 100, 100), 
                   (track_x, track_y, track_width, track_height), 
                   border_radius=int(track_height/2))

def draw_key(surface, x, y, width, height, text, is_pressed=False):
    """Dessine une touche de clavier"""
    if is_pressed:
        color = (200, 200, 200)
        border_color = (255, 255, 255)
    else:
        color = (80, 80, 80)
        border_color = (150, 150, 150)
    
    pygame.draw.rect(surface, color, (x, y, width, height), border_radius=5)
    pygame.draw.rect(surface, border_color, (x, y, width, height), 2, border_radius=5)
    
    font = pygame.font.SysFont("Arial", 16)
    text_surf = font.render(text, True, (255, 255, 255))
    text_rect = text_surf.get_rect(center=(x + width/2, y + height/2))
    surface.blit(text_surf, text_rect)

def draw_control_section(surface, title, x, y, width, height, controls, color):
    """Dessine une section de contrôles"""
  
    pygame.draw.rect(surface, (50, 50, 50), (x, y, width, height), border_radius=10)
    pygame.draw.rect(surface, color, (x, y, width, height), 2, border_radius=10)
    
  
    font_title = pygame.font.SysFont("Arial", 24, bold=True)
    title_surf = font_title.render(title, True, color)
    title_rect = title_surf.get_rect(midtop=(x + width/2, y + 10))
    surface.blit(title_surf, title_rect)
    
  
    pygame.draw.line(surface, color, (x + 20, y + 45), (x + width - 20, y + 45), 2)
    

    font_controls = pygame.font.SysFont("Arial", 20)
    for i, (action, key) in enumerate(controls):
        text = f"{action}: {key}"
        text_surf = font_controls.render(text, True, (255, 255, 255))
        surface.blit(text_surf, (x + 20, y + 60 + i * 30))

def draw_arrow_keys(surface, x, y, pressed_keys):
    """Dessine les flèches directionnelles"""
    key_size = 40
    padding = 5
    
    up_pressed = pressed_keys.get(pygame.K_UP, False)
    draw_key(surface, x, y, key_size, key_size, "↑", up_pressed)
    
    left_pressed = pressed_keys.get(pygame.K_LEFT, False)
    draw_key(surface, x - key_size - padding, y + key_size + padding, key_size, key_size, "←", left_pressed)
    
    down_pressed = pressed_keys.get(pygame.K_DOWN, False)
    draw_key(surface, x, y + key_size + padding, key_size, key_size, "↓", down_pressed)
    
    right_pressed = pressed_keys.get(pygame.K_RIGHT, False)
    draw_key(surface, x + key_size + padding, y + key_size + padding, key_size, key_size, "→", right_pressed)
    
    space_pressed = pressed_keys.get(pygame.K_SPACE, False)
    draw_key(surface, x - key_size, y + 2*(key_size + padding), key_size*3, key_size, "ESPACE", space_pressed)

def draw_zqsd_keys(surface, x, y, pressed_keys):
    """Dessine les touches ZQSD"""
    key_size = 40
    padding = 5
    
    z_pressed = pressed_keys.get(pygame.K_z, False)
    draw_key(surface, x, y, key_size, key_size, "Z", z_pressed)
    

    q_pressed = pressed_keys.get(pygame.K_q, False)
    draw_key(surface, x - key_size - padding, y + key_size + padding, key_size, key_size, "Q", q_pressed)
    
    
    s_pressed = pressed_keys.get(pygame.K_s, False)
    draw_key(surface, x, y + key_size + padding, key_size, key_size, "S", s_pressed)
    
    
    d_pressed = pressed_keys.get(pygame.K_d, False)
    draw_key(surface, x + key_size + padding, y + key_size + padding, key_size, key_size, "D", d_pressed)

def run_instructions(screen):
    """Exécute l'écran d'instructions"""
    background_color = (30, 30, 30)
    clock = pygame.time.Clock()
    
    tank1_color = (0, 255, 0)  # Vert
    tank2_color = (0, 0, 255)  # Bleu
    
    tank1_angle = 0
    tank2_angle = 180
    animation_speed = 2
    
    pressed_keys = {}
    key_cycle = 0
    
    font_title = pygame.font.SysFont("Arial", 48, bold=True)
    font_subtitle = pygame.font.SysFont("Arial", 32)
    font_text = pygame.font.SysFont("Arial", 20)
    
    
    back_button = pygame.Rect(50, 520, 200, 50)
    back_button_hover = False
    
    running = True
    while running:
        mouse_pos = pygame.mouse.get_pos()
        mouse_clicked = False
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return None
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  
                    mouse_clicked = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return STATE_MENU
        
        back_button_hover = back_button.collidepoint(mouse_pos)
        if back_button_hover and mouse_clicked:
            return STATE_MENU
        
        key_cycle = (key_cycle + 1) % 120
        
        if key_cycle < 30:
            pressed_keys = {pygame.K_UP: True}
            tank1_angle = (tank1_angle + animation_speed) % 360
        elif key_cycle < 60:
            pressed_keys = {pygame.K_RIGHT: True}
            tank1_angle = (tank1_angle - animation_speed) % 360
        elif key_cycle < 90:
            pressed_keys = {pygame.K_z: True}
            tank2_angle = (tank2_angle + animation_speed) % 360
        else:
            pressed_keys = {pygame.K_d: True}
            tank2_angle = (tank2_angle - animation_speed) % 360
        
        screen.fill(background_color)
        
        title_text = font_title.render("COMMANDES", True, (255, 200, 0))
        title_shadow = font_title.render("COMMANDES", True, (150, 100, 0))
        screen.blit(title_shadow, (203, 33))  # Ombre
        screen.blit(title_text, (200, 30))
        
        subtitle = font_subtitle.render("Comment jouer", True, (200, 200, 200))
        screen.blit(subtitle, (50, 90))
        
        tank1_controls = [
            ("Avancer", "↑"),
            ("Tourner à gauche", "←"),
            ("Tourner à droite", "→"),
            ("Tirer", "ESPACE")
        ]
        
        tank2_controls = [
            ("Avancer", "Z"),
            ("Tourner à gauche", "Q"),
            ("Tourner à droite", "D"),
            ("Tirer", "S")
        ]
        
       
        draw_control_section(screen, "JOUEUR 1", 50, 140, 300, 170, tank1_controls, tank1_color)
        draw_tank(screen, 150, 350, tank1_color, tank1_angle, 1.5)
        draw_arrow_keys(screen, 150, 400, pressed_keys)
        
     
        draw_control_section(screen, "JOUEUR 2", 450, 140, 300, 170, tank2_controls, tank2_color)
        draw_tank(screen, 550, 350, tank2_color, tank2_angle, 1.5)
        draw_zqsd_keys(screen, 550, 400, pressed_keys)
        
        pygame.draw.rect(screen, (50, 50, 50), (50, 480, 700, 30), border_radius=5)
        objective = font_text.render("OBJECTIF: Détruire le tank adverse en lui tirant dessus pour réduire ses points de vie à zéro.", 
                                  True, (255, 255, 255))
        screen.blit(objective, (60, 485))
        
        # Bouton de retour
        button_color = (150, 150, 150) if back_button_hover else (100, 100, 100)
        pygame.draw.rect(screen, button_color, back_button, border_radius=10)
        pygame.draw.rect(screen, (255, 255, 255), back_button, 2, border_radius=10)
        back_text = font_subtitle.render("RETOUR", True, (255, 255, 255))
        back_rect = back_text.get_rect(center=back_button.center)
        screen.blit(back_text, back_rect)
        
        pygame.display.flip()
        clock.tick(60)
    
    return STATE_MENU