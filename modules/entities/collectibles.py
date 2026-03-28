import pygame
import random
from modules.entities.base_entity import BaseEntity


class SodaFizzDrink(BaseEntity):
    """
    A falling collectible that provides a significant score boost.
    """

    def __init__(self, x: float, y: float) -> None:
        super().__init__(x, y)
        self.width = 20
        self.height = 30
        self.speed = random.uniform(150.0, 250.0)
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        # Color: Bright Yellow for the "Soda Fizz" logo/drink
        self.color = (255, 255, 0)

    def update(self, dt: float) -> None:
        """
        Moves the collectible downward toward the player.
        """
        self.y += self.speed * dt
        self.rect.y = int(self.y)

    def draw(self, screen: pygame.Surface) -> None:
        """
        Renders the collectible as a distinct yellow rectangle.
        """
        pygame.draw.rect(screen, self.color, self.rect)
        # Add a "label" effect
        pygame.draw.rect(screen, (0, 0, 0), self.rect, 1)
        # Small white highlight to make it pop
        pygame.draw.line(screen, (255, 255, 255), 
                         (self.rect.left + 4, self.rect.top + 4), 
                         (self.rect.left + 4, self.rect.bottom - 4), 2)
