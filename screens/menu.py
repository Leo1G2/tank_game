import pygame
import math

STATE_MENU = 'menu'
STATE_GAME = 'game'
STATE_OPTIONS = 'options'
STATE_INSTRUCTIONS = 'instructions'

class Button:
    def __init__(self, x, y, width, height, text, color, hover_color, text_color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.text_color = text_color
        self.is_hovered = False
        
    def draw(self, surface, font):
        #change la couleur avec la souris
        current_color = self.hover_color if self.is_hovered else self.color
        
       
        pygame.draw.rect(surface, current_color, self.rect, border_radius=10)
        pygame.draw.rect(surface, (255, 255, 255), self.rect, 2, border_radius=10)
        
        
        text_surface = font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)
    
    def check_hover(self, mouse_pos):
        self.is_hovered = self.rect.collidepoint(mouse_pos)
        return self.is_hovered
    
    def is_clicked(self, mouse_pos, mouse_click):
        return self.rect.collidepoint(mouse_pos) and mouse_click

class TankAnimation:
    def __init__(self, x, y, color, direction=1):
        self.x = x
        self.y = y
        self.angle = 0
        self.color = color
        self.radius = 20
        self.direction = direction 
        self.speed = 1
        
    def update(self):
        self.x += self.speed * self.direction
        self.angle = (self.angle + 2) % 360
        
        
        if self.x > 750:
            self.direction = -1
        elif self.x < 50:
            self.direction = 1
    
    def draw(self, surface):
       
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.radius)
        end_x = self.x + self.radius * math.cos(math.radians(self.angle))
        end_y = self.y - self.radius * math.sin(math.radians(self.angle))
        pygame.draw.line(surface, (255, 255, 255), (self.x, self.y), (end_x, end_y), 3)

def run_menu(screen):
    clock = pygame.time.Clock()
    font_title = pygame.font.SysFont("Arial", 64, bold=True)
    font_buttons = pygame.font.SysFont("Arial", 32)
    font_credits = pygame.font.SysFont("Arial", 16)
    
    background_color = (30, 30, 30)
    button_color = (100, 100, 100)
    button_hover_color = (150, 150, 150)
    text_color = (255, 255, 255)
    

    buttons = [
        Button(300, 250, 200, 50, "JOUER", button_color, button_hover_color, text_color),
        Button(300, 320, 200, 50, "OPTIONS", button_color, button_hover_color, text_color),
        Button(300, 390, 200, 50, "COMMANDES", button_color, button_hover_color, text_color),
        Button(300, 460, 200, 50, "QUITTER", button_color, button_hover_color, text_color)
    ]
    
    tank1 = TankAnimation(100, 150, (0, 255, 0), 1)
    tank2 = TankAnimation(700, 150, (0, 0, 255), -1)
    
    pulse_size = 64
    pulse_direction = 1
    
    current_state = STATE_MENU
    
    running = True
    while running:
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = False
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return None
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_click = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return None
        
        
        tank1.update()
        tank2.update()
        
     
        pulse_size += 0.1 * pulse_direction
        if pulse_size > 68:
            pulse_direction = -1
        elif pulse_size < 64:
            pulse_direction = 1
        
        for button in buttons:
            button.check_hover(mouse_pos)
            
            if button.is_clicked(mouse_pos, mouse_click):
                if button.text == "JOUER":
                    return STATE_GAME
                elif button.text == "OPTIONS":
                    return STATE_OPTIONS
                elif button.text == "COMMANDES":
                    return STATE_INSTRUCTIONS
                elif button.text == "QUITTER":
                    pygame.quit()
                    return None
        
        screen.fill(background_color)
        
        tank1.draw(screen)
        tank2.draw(screen)
        
        font_title_pulse = pygame.font.SysFont("Arial", int(pulse_size), bold=True)
        title_text = "Israël vs Palestine"
        title = font_title_pulse.render(title_text, True, (255, 200, 0))
        title_shadow = font_title_pulse.render(title_text, True, (250, 100, 0))

        title_rect = title.get_rect(center=(400, 100))
        shadow_rect = title_shadow.get_rect(center=(403, 103))  

        screen.blit(title_shadow, shadow_rect)
        screen.blit(title, title_rect)

        
       
        for button in buttons:
            button.draw(screen, font_buttons)
        
        
        credits = font_credits.render("© 2025 - Gaspard & Léo (amis et amants) <3", True, (200, 200, 200))
        screen.blit(credits, (10, 580))
        
        pygame.display.flip()
        clock.tick(60)
    
    return current_state