import pygame
import math

class Tank:
    def update_from_flags(self, forward, left, right):
        if left:
            self.angle = (self.angle + self.rotation_speed) % 360
        if right:
            self.angle = (self.angle - self.rotation_speed) % 360
        if forward:
            self.x += self.speed * math.cos(math.radians(self.angle))
            self.y -= self.speed * math.sin(math.radians(self.angle))

    def __init__(self, x, y, angle=0, color=(0, 255, 0)):
        self.x = x
        self.y = y
        self.angle = angle  # en degrés
        self.speed = 2.0  # vitesse de déplacement
        self.rotation_speed = 3.0  # vitesse de rotation
        self.hp = 100
        self.fire_power = 10
        self.fire_delay = 500  # en millisecondes
        self.last_shot = pygame.time.get_ticks()
        self.color = color
        self.radius = 20

    def draw(self, surface):
        # Dessiner le tank
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.radius)
        end_x = self.x + self.radius * math.cos(math.radians(self.angle))
        end_y = self.y - self.radius * math.sin(math.radians(self.angle))
        pygame.draw.line(surface, (255, 255, 255), (self.x, self.y), (end_x, end_y), 2)

        # Affichage de la barre de vie
        pygame.draw.rect(surface, (255, 0, 0), (self.x - 20, self.y - 40, 100, 8))  # Barre rouge
        pygame.draw.rect(surface, (0, 255, 0), (self.x - 20, self.y - 40, self.hp, 8))  # Barre verte

    def update(self, keys, forward_key, left_key, right_key):
        if keys[left_key]:
            self.angle = (self.angle + self.rotation_speed) % 360
        if keys[right_key]:
            self.angle = (self.angle - self.rotation_speed) % 360
        if keys[forward_key]:
            self.x += self.speed * math.cos(math.radians(self.angle))
            self.y -= self.speed * math.sin(math.radians(self.angle))

    def can_shoot(self):
        current_time = pygame.time.get_ticks()
        return current_time - self.last_shot >= self.fire_delay

    def shoot(self):
        if self.can_shoot():
            self.last_shot = pygame.time.get_ticks()
            return Projectile(self.x, self.y, self.angle, self.fire_power, self)
        return None

    def get_rect(self):
        """ Retourne la hitbox du tank sous forme de rectangle """
        return pygame.Rect(self.x - self.radius, self.y - self.radius, self.radius * 2, self.radius * 2)

class Projectile:
    def __init__(self, x, y, angle, power, owner):
        self.x = x
        self.y = y
        self.angle = angle
        self.speed = 5.0
        self.power = power
        self.radius = 5
        self.owner = owner  # Tank qui a tiré

    def update(self):
        self.x += self.speed * math.cos(math.radians(self.angle))
        self.y -= self.speed * math.sin(math.radians(self.angle))

    def draw(self, surface):
        pygame.draw.circle(surface, (255, 0, 0), (int(self.x), int(self.y)), self.radius)

    def get_rect(self):
        """ Retourne la hitbox du projectile sous forme de rectangle """
        return pygame.Rect(self.x - self.radius, self.y - self.radius, self.radius * 2, self.radius * 2)
