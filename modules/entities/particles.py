import pygame
import random


class Particle:
    """
    A lightweight visual entity for fizzy pop effects.
    Fades out over its lifetime.
    """

    def __init__(self, x: float, y: float, vx: float, vy: float, color: tuple, lifetime: float) -> None:
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.color = color
        self.initial_lifetime = lifetime
        self.lifetime = lifetime
        self.radius = random.randint(2, 5)

    def update(self, dt: float) -> None:
        """
        Updates position based on velocity and handles lifetime.
        """
        self.x += self.vx * dt
        self.y += self.vy * dt
        self.lifetime -= dt

    def is_alive(self) -> bool:
        """
        Returns True if the particle still has lifetime.
        """
        return self.lifetime > 0

    def draw(self, screen: pygame.Surface) -> None:
        """
        Renders the particle as a circle that fades out.
        """
        # Calculate alpha (0 to 255) based on remaining lifetime
        alpha = int((self.lifetime / self.initial_lifetime) * 255)
        if alpha <= 0:
            return

        # Create a tiny surface with alpha support for the fade effect
        s = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
        # Combine the base color with the calculated alpha
        rgba_color = (*self.color, alpha)
        pygame.draw.circle(s, rgba_color, (self.radius, self.radius), self.radius)
        
        # Blit the particle surface to the main screen
        screen.blit(s, (int(self.x - self.radius), int(self.y - self.radius)))
