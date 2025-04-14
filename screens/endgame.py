import pygame
import math
import random

STATE_MENU = 'menu'
STATE_GAME = 'game'

class Particle:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.radius = random.uniform(2, 5)
        self.lifetime = random.uniform(0.5, 2.0) * 60  # en frames
        self.current_life = self.lifetime
        self.velocity = [random.uniform(-2, 2), random.uniform(-2, 2)]
    
    def update(self):
        self.x += self.velocity[0]
        self.y += self.velocity[1]
        self.velocity[1] += 0.05  # Gravité
        self.current_life -= 1
        self.radius *= 0.99
        return self.current_life > 0
    
    def draw(self, surface):
        alpha = int(255 * (self.current_life / self.lifetime))
        color = (self.color[0], self.color[1], self.color[2])
        pygame.draw.circle(surface, color, (int(self.x), int(self.y)), int(self.radius))

def run_endgame(screen):
    background_color = (20, 20, 50)
    clock = pygame.time.Clock()
    
    # Polices
    font_title = pygame.font.SysFont("Arial", 60, bold=True)
    font_subtitle = pygame.font.SysFont("Arial", 32)
    font_button = pygame.font.SysFont("Arial", 30)
    
    # Couleurs des joueurs
    tank1_color = (0, 255, 0)  # Vert
    tank2_color = (0, 0, 255)  # Bleu
    
    # Créer des boutons
    replay_button = pygame.Rect(250, 350, 150, 50)
    menu_button = pygame.Rect(450, 350, 150, 50)
    
    # État des boutons
    replay_hover = False
    menu_hover = False
    
    # Particules
    particles = []
    
    # Animation du titre
    title_scale = 0
    title_max_scale = 1.0
    
    running = True
    while running:
        mouse_pos = pygame.mouse.get_pos()
        mouse_clicked = False
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return None
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # clic gauche
                    mouse_clicked = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return STATE_MENU
                elif event.key == pygame.K_SPACE:
                    return STATE_GAME
        
        # Animation du titre
        if title_scale < title_max_scale:
            title_scale += 0.05
        
        # Créer de nouvelles particules aléatoirement
        if random.random() < 0.3:
            x = random.randint(100, 700)
            y = random.randint(100, 500)
            color_choice = random.choice([
                (255, 200, 0),  # Or
                (255, 100, 0),  # Orange
                (255, 50, 50)   # Rouge
            ])
            particles.append(Particle(x, y, color_choice))
        
        # Mise à jour des particules
        particles = [p for p in particles if p.update()]
        
        # Vérifier si la souris est sur les boutons
        replay_hover = replay_button.collidepoint(mouse_pos)
        menu_hover = menu_button.collidepoint(mouse_pos)
        
        # Gérer les clics de boutons
        if replay_hover and mouse_clicked:
            return STATE_GAME
        if menu_hover and mouse_clicked:
            return STATE_MENU
        
        # Vérifier les touches
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
            return STATE_MENU
        
        # Dessiner l'écran
        screen.fill(background_color)
        
        # Dessiner les particules en arrière-plan
        for particle in particles:
            particle.draw(screen)
        
        # Titre avec animation
        scaled_font_size = int(60 * title_scale)
        if scaled_font_size > 0:
            font_title_scaled = pygame.font.SysFont("Arial", scaled_font_size, bold=True)
            title_text = "FIN DE PARTIE"
            title_surface = font_title_scaled.render(title_text, True, (255, 200, 0))
            title_shadow = font_title_scaled.render(title_text, True, (150, 100, 0))
            
            title_rect = title_surface.get_rect(center=(400, 100))
            shadow_rect = title_shadow.get_rect(center=(403, 103))
            
            screen.blit(title_shadow, shadow_rect)
            screen.blit(title_surface, title_rect)
        
        # Sous-titre
        subtitle_text = "QUI SERA LE PROCHAIN VAINQUEUR ?"
        subtitle = font_subtitle.render(subtitle_text, True, (200, 200, 200))
        subtitle_rect = subtitle.get_rect(center=(400, 200))
        screen.blit(subtitle, subtitle_rect)
        
        # Dessiner les boutons
        replay_color = (100, 200, 100) if replay_hover else (50, 150, 50)
        menu_color = (100, 100, 200) if menu_hover else (50, 50, 150)
        
        pygame.draw.rect(screen, replay_color, replay_button, border_radius=10)
        pygame.draw.rect(screen, (255, 255, 255), replay_button, 2, border_radius=10)
        replay_text = font_button.render("REJOUER", True, (255, 255, 255))
        replay_rect = replay_text.get_rect(center=replay_button.center)
        screen.blit(replay_text, replay_rect)
        
        pygame.draw.rect(screen, menu_color, menu_button, border_radius=10)
        pygame.draw.rect(screen, (255, 255, 255), menu_button, 2, border_radius=10)
        menu_text = font_button.render("MENU", True, (255, 255, 255))
        menu_rect = menu_text.get_rect(center=menu_button.center)
        screen.blit(menu_text, menu_rect)
        
        # Afficher un texte d'aide en bas de l'écran
        help_text = font_subtitle.render("Appuyez sur ENTRÉE pour le menu ou ESPACE pour rejouer", True, (150, 150, 150))
        help_rect = help_text.get_rect(center=(400, 500))
        screen.blit(help_text, help_rect)
        
        pygame.display.flip()
        clock.tick(60)
    
    return 'endgame'