import pygame
import random
from modules.entities.base_entity import BaseEntity


class Bubble(BaseEntity):
    """
    Carbonation bubbles that serve as rising platforms for the player.
    Utilizes advanced Pygame rendering to create a 3D glowing aesthetic.
    """

    def __init__(self, x: float, y: float) -> None:
        super().__init__(x, y)
        self.radius = random.randint(15, 35)
        self.speed = random.uniform(50.0, 150.0)
        
        # Collision rect centered on the bubble
        self.rect = pygame.Rect(
            self.x - self.radius,
            self.y - self.radius,
            self.radius * 2,
            self.radius * 2
        )

        # Basic bubble sizing and colors
        size = self.radius * 2
        base_color = (255, 182, 193, 200)       # Light pink, semi-transparent base
        rim_color = (255, 105, 180, 255)        # Hot pink, saturated rim light
        highlight_color = (255, 255, 255, 200)  # White highlight
        
        # 1. Base surface caching
        self.base_surface = pygame.Surface((size, size), pygame.SRCALPHA)
        pygame.draw.circle(self.base_surface, base_color, (self.radius, self.radius), self.radius)
        
        # 2. Rim surface caching (unfilled circle)
        self.rim_surface = pygame.Surface((size, size), pygame.SRCALPHA)
        pygame.draw.circle(self.rim_surface, rim_color, (self.radius, self.radius), self.radius, width=3)
        
        # 3. Highlight surface caching (small oval near top-left quadrant)
        self.highlight_surface = pygame.Surface((size, size), pygame.SRCALPHA)
        highlight_rect = pygame.Rect(self.radius * 0.4, self.radius * 0.3, self.radius * 0.5, self.radius * 0.3)
        # Draw slightly angled highlight using bounding rect oval
        pygame.draw.ellipse(self.highlight_surface, highlight_color, highlight_rect)

    def update(self, dt: float) -> None:
        """
        Moves the bubble upward and syncs its collision rect.
        """
        self.y -= self.speed * dt
        self.rect.x = int(self.x - self.radius)
        self.rect.y = int(self.y - self.radius)

    def draw(self, screen: pygame.Surface) -> None:
        """
        Renders the bubble using multiple blended layers to create surface luminosity.
        """
        pos = (int(self.rect.x), int(self.rect.y))
        
        # Blit base surface normally
        screen.blit(self.base_surface, pos)
        
        # Blit rim using additive blending for a luminous effect
        screen.blit(self.rim_surface, pos, special_flags=pygame.BLEND_RGBA_ADD)
        
        # Blit surface highlight using additive blending
        screen.blit(self.highlight_surface, pos, special_flags=pygame.BLEND_RGBA_ADD)
