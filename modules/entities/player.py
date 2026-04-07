import pygame
from modules.entities.base_entity import BaseEntity
from modules.constants import GRAVITY, PLAYER_SPEED, BOUNCE_POWER, WINDOW_WIDTH


class Player(BaseEntity):
    """
    The main character: a rebellious Strawberry Chunk.
    Handles gravity-based physics, horizontal movement, and dynamic shadows.
    Now utilizes purely procedural graphics to fit the "fizzy" aesthetic.
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
        Renders a procedurally generated Strawberry Chunk with a dynamic shadow.
        """
        # --- 1. Dynamic Contact Shadow ---
        speed_factor = min(abs(self.vel_y) / 1000.0, 1.0)
        shadow_width = max(int(self.width * (1.0 - speed_factor * 0.6)), 8)
        shadow_height = int(shadow_width * 0.35)
        
        if shadow_width > 0 and shadow_height > 0:
            shadow_surface = pygame.Surface((shadow_width, shadow_height), pygame.SRCALPHA)
            pygame.draw.ellipse(shadow_surface, (0, 0, 0, 80), (0, 0, shadow_width, shadow_height))
            shadow_x = self.rect.centerx - (shadow_width // 2)
            shadow_y = self.rect.bottom + 5
            screen.blit(shadow_surface, (shadow_x, shadow_y), special_flags=pygame.BLEND_RGBA_MULT)

        # --- 2. Procedural Strawberry Body ---
        # Draw the main red body (slightly tapered at the bottom)
        body_rect = self.rect.inflate(-2, -4)
        pygame.draw.ellipse(screen, (220, 20, 60), body_rect) # Crimson body
        # Overlay a slightly brighter red highlight on top
        highlight_rect = pygame.Rect(self.rect.x + 5, self.rect.y + 5, 10, 8)
        pygame.draw.ellipse(screen, (255, 69, 0), highlight_rect) # Red-orange highlight

        # --- 3. Green Leaves/Stem ---
        leaf_points = [
            (self.rect.centerx, self.rect.top),           # Middle top
            (self.rect.left + 5, self.rect.top - 5),      # Left tip
            (self.rect.centerx, self.rect.top + 5),       # Middle anchor
            (self.rect.right - 5, self.rect.top - 5)      # Right tip
        ]
        pygame.draw.polygon(screen, (34, 139, 34), leaf_points) # Forest Green

        # --- 4. Yellow Seeds ---
        seed_color = (255, 255, 224) # Light yellow
        seeds = [
            (self.rect.x + 8, self.rect.y + 15),
            (self.rect.x + 22, self.rect.y + 15),
            (self.rect.centerx, self.rect.y + 22),
            (self.rect.x + 10, self.rect.y + 25),
            (self.rect.x + 20, self.rect.y + 25)
        ]
        for sx, sy in seeds:
            pygame.draw.circle(screen, seed_color, (sx, sy), 1)
