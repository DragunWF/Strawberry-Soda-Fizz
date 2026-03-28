import pygame
import random
from modules.entities.base_entity import BaseEntity
from modules.core.resource_manager import ResourceManager


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
        
        # Load Sprite (Yellow fallback)
        self.image = ResourceManager.get_image('drink.png', (255, 255, 0), (self.width, self.height))

    def update(self, dt: float) -> None:
        """
        Moves the collectible downward toward the player.
        """
        self.y += self.speed * dt
        self.rect.y = int(self.y)

    def draw(self, screen: pygame.Surface) -> None:
        """
        Renders the collectible sprite or its fallback.
        """
        screen.blit(self.image, self.rect)
