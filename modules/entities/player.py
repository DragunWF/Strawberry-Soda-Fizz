import pygame
from modules.entities.base_entity import BaseEntity
from modules.constants import GRAVITY, PLAYER_SPEED, BOUNCE_POWER, WINDOW_WIDTH, RED


class Player(BaseEntity):
    """
    The main character: a rebellious Strawberry Chunk.
    Handles gravity-based physics and horizontal movement.
    """

    def __init__(self, x: float, y: float) -> None:
        super().__init__(x, y)
        self.width = 30
        self.height = 30
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        
        # Physics state
        self.vel_y = 0.0
        self.speed = PLAYER_SPEED
        self.gravity = GRAVITY
        self.bounce_power = BOUNCE_POWER

    def bounce(self) -> None:
        """
        Forcefully sets vertical velocity to trigger a bounce/jump.
        """
        self.vel_y = self.bounce_power

    def update(self, dt: float) -> None:
        """
        Updates player position based on gravity and user input.
        Also handles cylindrical screen wrapping.
        """
        # 1. Apply Gravity
        self.vel_y += self.gravity * dt
        self.y += self.vel_y * dt

        # 2. Handle Horizontal Input
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.x -= self.speed * dt
        if keys[pygame.K_RIGHT]:
            self.x += self.speed * dt

        # 3. Cylindrical Screen Wrap
        if self.rect.left > WINDOW_WIDTH:
            self.x = -self.width
        elif self.rect.right < 0:
            self.x = WINDOW_WIDTH

        # 4. Sync Rect with float positions
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)

    def draw(self, screen: pygame.Surface) -> None:
        """
        Renders the player as a red square (Strawberry Chunk).
        """
        pygame.draw.rect(screen, RED, self.rect)
        # Optional: Add a simple black border
        pygame.draw.rect(screen, (0, 0, 0), self.rect, 2)
