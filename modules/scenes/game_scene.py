import pygame
import random
from typing import List, Optional
from modules.scenes.base_scene import BaseScene
from modules.entities.player import Player
from modules.entities.bubbles import Bubble
from modules.constants import BG_COLOR, WINDOW_WIDTH, WINDOW_HEIGHT


class GameScene(BaseScene):
    """
    Main gameplay area for Strawberry Soda Fizz.
    Manages the player entity and procedurally generated fizz bubbles.
    """

    def __init__(self) -> None:
        super().__init__()
        # Spawn Strawberry Chunk
        self.player = Player(WINDOW_WIDTH // 2 - 15, 100)
        self.bubbles: List[Bubble] = []
        
        # Initial procedural fizz setup
        self._spawn_initial_bubbles()

    def _spawn_initial_bubbles(self) -> None:
        """
        Creates 5-6 bubbles scattered across the height of the screen.
        """
        self.bubbles = []
        for i in range(6):
            x = random.randint(50, WINDOW_WIDTH - 50)
            y = (WINDOW_HEIGHT // 6) * i + random.randint(0, 50)
            self.bubbles.append(Bubble(x, y))

    def enter(self) -> None:
        """
        Resets the next state, player position, and bubbles when entering.
        """
        self.next_state = None
        self.player.x = WINDOW_WIDTH // 2 - 15
        self.player.y = 100
        self.player.vel_y = 0
        self._spawn_initial_bubbles()

    def handle_events(self, events: List[pygame.event.Event]) -> None:
        """
        Processes standard game inputs and debug triggers.
        """
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_k:
                    self.next_state = "GAME_OVER"

    def update(self, dt: float) -> Optional[str]:
        """
        Updates player, bubbles, and handles collision and recycling.
        """
        # 1. Update Player
        self.player.update(dt)
        
        # 2. Update Bubbles & Handle Recycling
        for bubble in self.bubbles:
            bubble.update(dt)
            # If bubble goes above screen top, move it below the screen
            if bubble.y + bubble.radius < 0:
                bubble.y = WINDOW_HEIGHT + random.randint(50, 150)
                bubble.x = random.randint(50, WINDOW_WIDTH - 50)
                # Ensure the collision rect is also updated immediately
                bubble.rect.y = int(bubble.y - bubble.radius)

            # 3. Collision Logic: Player landing on Bubble
            # Condition 1: Player is falling
            if self.player.vel_y > 0:
                # Condition 2: Player rect overlaps Bubble rect
                if self.player.rect.colliderect(bubble.rect):
                    # Condition 3: Player's bottom is within the top half of the bubble
                    # (Allow some tolerance for platforming feel)
                    if self.player.rect.bottom <= bubble.rect.centery + 15:
                        self.player.bounce()

        # 4. Check Failure Condition: Falling off screen
        if self.player.y > WINDOW_HEIGHT:
            self.next_state = "GAME_OVER"

        return self.next_state

    def draw(self, screen: pygame.Surface) -> None:
        """
        Renders the game background, fizz, and the player chunk.
        """
        # 1. Clear Screen
        screen.fill(BG_COLOR)

        # 2. Draw Bubbles FIRST (Layering: Bubbles are background)
        for bubble in self.bubbles:
            bubble.draw(screen)

        # 3. Draw Player on top (Layering: Player is foreground)
        self.player.draw(screen)
