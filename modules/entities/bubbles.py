import pygame
import random
from modules.entities.base_entity import BaseEntity


class Bubble(BaseEntity):
    """
    Carbonation bubbles that serve as rising platforms for the player.
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

    def update(self, dt: float) -> None:
        """
        Moves the bubble upward.
        """
        self.y -= self.speed * dt
        self.rect.y = int(self.y - self.radius)

    def draw(self, screen: pygame.Surface) -> None:
        """
        Renders the bubble as a white circle.
        """
        pygame.draw.circle(screen, (255, 255, 255), (int(self.x), int(self.y)), self.radius)
        # Subtle border for visibility
        pygame.draw.circle(screen, (200, 200, 200), (int(self.x), int(self.y)), self.radius, 1)
