import pygame
import random
from modules.entities.base_entity import BaseEntity


class SodaFizzDrink(BaseEntity):
    """
    A falling collectible that provides a significant score boost.
    Utilizes advanced Pygame rendering for a glowing, golden energy aesthetic.
    """

    def __init__(self, x: float, y: float) -> None:
        super().__init__(x, y)
        self.width = 20
        self.height = 30
        self.speed = random.uniform(150.0, 250.0)
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        
        # Caching the Golden Glow
        # We make the surface slightly larger than the rect to allow for the glow bleed
        size_x = int(self.width * 1.5)
        size_y = int(self.height * 1.5)
        
        # 1. Outer glow (soft yellow/gold)
        self.glow_surface = pygame.Surface((size_x, size_y), pygame.SRCALPHA)
        pygame.draw.ellipse(self.glow_surface, (255, 215, 0, 100), (0, 0, size_x, size_y))
        
        # 2. Inner core (bright white/yellow)
        self.core_surface = pygame.Surface((size_x, size_y), pygame.SRCALPHA)
        # Position the core in the center of the surface
        core_rect = pygame.Rect(size_x * 0.25, size_y * 0.25, size_x * 0.5, size_y * 0.5)
        pygame.draw.ellipse(self.core_surface, (255, 255, 200, 200), core_rect)

    def update(self, dt: float) -> None:
        """
        Moves the collectible downward toward the player.
        """
        self.y += self.speed * dt
        self.rect.y = int(self.y)

    def draw(self, screen: pygame.Surface) -> None:
        """
        Renders the collectible with glowing effects and a contact shadow.
        """
        # --- Contact Shadow ---
        shadow_width = int(self.width * 1.2)
        shadow_height = int(shadow_width * 0.4)
        shadow_surface = pygame.Surface((shadow_width, shadow_height), pygame.SRCALPHA)
        pygame.draw.ellipse(shadow_surface, (0, 0, 0, 80), shadow_surface.get_rect())
        
        shadow_x = self.rect.centerx - (shadow_width // 2)
        shadow_y = self.rect.bottom + 5
        screen.blit(shadow_surface, (shadow_x, shadow_y), special_flags=pygame.BLEND_RGBA_MULT)
        
        # --- Glowing Collectible ---
        # Center the larger effect surfaces on the actual rect
        pos = (
            self.rect.centerx - (self.glow_surface.get_width() // 2), 
            self.rect.centery - (self.glow_surface.get_height() // 2)
        )
        
        # Blit the glow and inner core with additive blending
        screen.blit(self.glow_surface, pos, special_flags=pygame.BLEND_RGBA_ADD)
        screen.blit(self.core_surface, pos, special_flags=pygame.BLEND_RGBA_ADD)
