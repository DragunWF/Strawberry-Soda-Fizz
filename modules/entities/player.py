import pygame
from modules.entities.base_entity import BaseEntity
from modules.core.resource_manager import ResourceManager
from modules.constants import GRAVITY, PLAYER_SPEED, BOUNCE_POWER, WINDOW_WIDTH


class Player(BaseEntity):
    """
    The main character: a rebellious Strawberry Chunk.
    Handles gravity-based physics, horizontal movement, and dynamic shadows.
    """

    def __init__(self, x: float, y: float) -> None:
        super().__init__(x, y)
        self.width = 30
        self.height = 30
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        
        # Load Sprite (Crimson fallback)
        self.image = ResourceManager.get_image('player.png', (220, 20, 60), (self.width, self.height))
        
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
        Renders the player sprite to the screen with a dynamic contact shadow.
        """
        # --- Contact Shadow Generation ---
        # Shadow narrows as the player falls faster, simulating depth/distance
        # Max falling speed clamped roughly around 1000 for interpolation
        speed_factor = min(abs(self.vel_y) / 1000.0, 1.0)
        
        # As speed factor nears 1 (fast), shadow shrinks. Near 0 (resting), shadow is wide.
        shadow_width = max(int(self.width * (1.0 - speed_factor * 0.6)), 8)
        shadow_height = int(shadow_width * 0.35)
        
        if shadow_width > 0 and shadow_height > 0:
            shadow_surface = pygame.Surface((shadow_width, shadow_height), pygame.SRCALPHA)
            
            # Semi-transparent black oval shadow
            pygame.draw.ellipse(shadow_surface, (0, 0, 0, 100), shadow_surface.get_rect())
            
            # Position shadow slightly below the center-bottom of the player
            shadow_x = self.rect.centerx - (shadow_width // 2)
            shadow_y = self.rect.bottom + 5
            
            # Blit using multiplicative blending to naturally darken background sodas/bubbles
            screen.blit(shadow_surface, (shadow_x, shadow_y), special_flags=pygame.BLEND_RGBA_MULT)

        # --- Draw Player ---
        screen.blit(self.image, self.rect)
