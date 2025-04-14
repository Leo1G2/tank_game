import pygame

STATE_MENU = 'menu'

class Slider:
    def __init__(self, x, y, width, min_val, max_val, init_val, label, value_format="{:.0f}"):
        self.rect = pygame.Rect(x, y, width, 10)
        self.knob = pygame.Rect(0, 0, 20, 20)
        self.min_val = min_val
        self.max_val = max_val
        self.value = init_val
        self.label = label
        self.value_format = value_format
        self.dragging = False
        self.update_knob_pos()
    
    def update_knob_pos(self):
        val_range = self.max_val - self.min_val
        pos_range = self.rect.width - self.knob.width
        rel_val = (self.value - self.min_val) / val_range
        knob_x = self.rect.x + rel_val * pos_range
        self.knob.x = knob_x
        self.knob.y = self.rect.y - 5  # Centre le bouton verticalement
    
    def draw(self, surface, font):
        # Dessiner le rail du slider
        pygame.draw.rect(surface, (100, 100, 100), self.rect, border_radius=5)
        
        # Dessiner la partie remplie du slider
        fill_width = self.knob.centerx - self.rect.x
        fill_rect = pygame.Rect(self.rect.x, self.rect.y, fill_width, self.rect.height)
        pygame.draw.rect(surface, (150, 150, 150), fill_rect, border_radius=5)
        
        # Dessiner le bouton du slider
        pygame.draw.rect(surface, (200, 200, 200), self.knob, border_radius=10)
        pygame.draw.rect(surface, (255, 255, 255), self.knob, 2, border_radius=10)
        
        # Afficher l'étiquette
        label_text = font.render(self.label, True, (255, 255, 255))
        surface.blit(label_text, (self.rect.x, self.rect.y - 30))
        
        # Afficher la valeur
        value_text = font.render(self.value_format.format(self.value), True, (255, 255, 255))
        surface.blit(value_text, (self.rect.right + 10, self.rect.y - 5))
    
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.knob.collidepoint(event.pos):
                self.dragging = True
        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False
        elif event.type == pygame.MOUSEMOTION and self.dragging:
            rel_x = event.pos[0] - self.rect.x
            rel_x = max(0, min(rel_x, self.rect.width))
            val_range = self.max_val - self.min_val
            pos_range = self.rect.width
            self.value = self.min_val + (rel_x / pos_range) * val_range
            self.update_knob_pos()
            return True
        return False

class Toggle:
    def __init__(self, x, y, label, initial_state=False):
        self.rect = pygame.Rect(x, y, 60, 30)
        self.label = label
        self.state = initial_state
        self.hover = False
    
    def draw(self, surface, font):
        # Fond du toggle
        if self.state:
            bg_color = (0, 200, 100)  # Vert quand activé
        else:
            bg_color = (100, 100, 100)  # Gris quand désactivé
        
        # Ajout d'effet de survol
        if self.hover:
            bg_color = (min(bg_color[0] + 30, 255), min(bg_color[1] + 30, 255), min(bg_color[2] + 30, 255))
        
        pygame.draw.rect(surface, bg_color, self.rect, border_radius=15)
        pygame.draw.rect(surface, (255, 255, 255), self.rect, 2, border_radius=15)
        
        # Bouton du toggle
        knob_radius = self.rect.height - 6
        if self.state:
            knob_x = self.rect.right - knob_radius - 3
        else:
            knob_x = self.rect.left + 3
        knob_y = self.rect.centery
        
        pygame.draw.circle(surface, (240, 240, 240), (knob_x, knob_y), knob_radius)
        
        # Afficher l'étiquette
        label_text = font.render(self.label, True, (255, 255, 255))
        surface.blit(label_text, (self.rect.x, self.rect.y - 30))
    
    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.hover = self.rect.collidepoint(event.pos)
        
        if event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos):
            self.state = not self.state
            return True
        return False

class Button:
    def __init__(self, x, y, width, height, text, color, hover_color, text_color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.text_color = text_color
        self.is_hovered = False
        
    def draw(self, surface, font):
        # Choisir la couleur en fonction de si la souris est sur le bouton
        current_color = self.hover_color if self.is_hovered else self.color
        
        # Dessiner le rectangle du bouton
        pygame.draw.rect(surface, current_color, self.rect, border_radius=10)
        pygame.draw.rect(surface, (255, 255, 255), self.rect, 2, border_radius=10)  # Bordure
        
        # Centrer le texte sur le bouton
        text_surface = font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)
    
    def check_hover(self, mouse_pos):
        self.is_hovered = self.rect.collidepoint(mouse_pos)
        return self.is_hovered
    
    def is_clicked(self, mouse_pos, mouse_click):
        return self.rect.collidepoint(mouse_pos) and mouse_click

def run_options(screen):
    # Configuration
    background_color = (30, 30, 30)
    clock = pygame.time.Clock()
    
    # Polices
    font_title = pygame.font.SysFont("Arial", 48, bold=True)
    font_subtitle = pygame.font.SysFont("Arial", 32)
    font_regular = pygame.font.SysFont("Arial", 20)
    
    # Paramètres initiaux - à adapter selon votre jeu
    game_options = {
        "tank_speed": 2.0,
        "rotation_speed": 3.0,
        "projectile_speed": 5.0,
        "fire_power": 10,
        "sound_volume": 80,
        "music_volume": 60,
        "show_hp": True,
        "friendly_fire": False
    }
    
    # Créer les contrôles d'interface
    sliders = [
        Slider(200, 150, 300, 1.0, 5.0, game_options["tank_speed"], "Vitesse des tanks"),
        Slider(200, 220, 300, 1.0, 10.0, game_options["rotation_speed"], "Vitesse de rotation"),
        Slider(200, 290, 300, 2.0, 10.0, game_options["projectile_speed"], "Vitesse des projectiles"),
        Slider(200, 360, 300, 5, 30, game_options["fire_power"], "Puissance de tir"),
        Slider(200, 430, 300, 0, 100, game_options["sound_volume"], "Volume des effets", "{:.0f}%"),
        Slider(200, 500, 300, 0, 100, game_options["music_volume"], "Volume de la musique", "{:.0f}%")
    ]
    
    toggles = [
        Toggle(600, 150, "Afficher les barres de vie", game_options["show_hp"]),
        Toggle(600, 220, "Tir ami", game_options["friendly_fire"])
    ]
    
    # Boutons
    save_button = Button(250, 570, 150, 50, "SAUVEGARDER", (100, 100, 100), (150, 150, 150), (255, 255, 255))
    back_button = Button(450, 570, 150, 50, "RETOUR", (100, 100, 100), (150, 150, 150), (255, 255, 255))
    
    # Message de confirmation
    save_message = ""
    save_message_time = 0
    
    running = True
    while running:
        mouse_pos = pygame.mouse.get_pos()
        mouse_clicked = False
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return None
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_clicked = True
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return STATE_MENU
            
            # Gérer les événements des sliders
            for slider in sliders:
                if slider.handle_event(event):
                    # Mettre à jour les options correspondantes
                    if slider.label == "Vitesse des tanks":
                        game_options["tank_speed"] = slider.value
                    elif slider.label == "Vitesse de rotation":
                        game_options["rotation_speed"] = slider.value
                    elif slider.label == "Vitesse des projectiles":
                        game_options["projectile_speed"] = slider.value
                    elif slider.label == "Puissance de tir":
                        game_options["fire_power"] = slider.value
                    elif slider.label == "Volume des effets":
                        game_options["sound_volume"] = slider.value
                    elif slider.label == "Volume de la musique":
                        game_options["music_volume"] = slider.value
            
            # Gérer les événements des toggles
            for toggle in toggles:
                if toggle.handle_event(event):
                    if toggle.label == "Afficher les barres de vie":
                        game_options["show_hp"] = toggle.state
                    elif toggle.label == "Tir ami":
                        game_options["friendly_fire"] = toggle.state
        
        # Vérifier les survols et clics de boutons
        save_button.check_hover(mouse_pos)
        back_button.check_hover(mouse_pos)
        
        if save_button.is_clicked(mouse_pos, mouse_clicked):
            # Ici, vous pourriez sauvegarder les options dans un fichier
            save_message = "Options sauvegardées!"
            save_message_time = pygame.time.get_ticks()
        
        if back_button.is_clicked(mouse_pos, mouse_clicked):
            return STATE_MENU
        
        # Dessiner l'écran
        screen.fill(background_color)
        
        # Titre
        title_text = font_title.render("OPTIONS", True, (255, 200, 0))
        title_shadow = font_title.render("OPTIONS", True, (150, 100, 0))
        screen.blit(title_shadow, (253, 33))  # Ombre
        screen.blit(title_text, (250, 30))
        
        # Section des réglages
        pygame.draw.rect(screen, (40, 40, 40), (150, 100, 500, 450), border_radius=10)
        pygame.draw.rect(screen, (100, 100, 100), (150, 100, 500, 450), 2, border_radius=10)
        
        # Dessiner les sliders
        for slider in sliders:
            slider.draw(screen, font_regular)
        
        # Dessiner les toggles
        for toggle in toggles:
            toggle.draw(screen, font_regular)
        
        # Dessiner les boutons
        save_button.draw(screen, font_subtitle)
        back_button.draw(screen, font_subtitle)
        
        # Afficher le message de confirmation si nécessaire
        if save_message:
            current_time = pygame.time.get_ticks()
            if current_time - save_message_time < 3000:  # Afficher pendant 3 secondes
                message_surf = font_subtitle.render(save_message, True, (0, 255, 0))
                message_rect = message_surf.get_rect(center=(400, 650))
                screen.blit(message_surf, message_rect)
            else:
                save_message = ""
        
        pygame.display.flip()
        clock.tick(60)
    
    return STATE_MENU