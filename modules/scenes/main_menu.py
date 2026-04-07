import pygame
import math
import random
from typing import List, Optional
from modules.scenes.base_scene import BaseScene
from modules.ui.text_button import TextButton
from modules.entities.bubbles import Bubble
from modules.core.score_manager import ScoreManager
from modules.constants import BG_COLOR, TITLE, WINDOW_WIDTH, WINDOW_HEIGHT


class MainMenuScene(BaseScene):
    """
    The initial scene for the game, featuring the title, a start button, 
    and a rising background bubble aesthetic.
    """

    def __init__(self) -> None:
        super().__init__()
        self.title_font = pygame.font.SysFont(None, 42)   # Increased size for the glowing title
        self.score_font = pygame.font.SysFont(None, 36)
        
        # Instantiate the Start Game button
        button_width = 200
        button_height = 50
        x = (WINDOW_WIDTH - button_width) // 2
        y = (WINDOW_HEIGHT - button_height) // 2
        self.start_button = TextButton(x, y + 100, button_width, button_height, "Start Game")

        # Background procedural bubbles
        self.bubbles: List[Bubble] = []
        self._spawn_initial_bubbles()
        
        # Timing variable for the floating sine wave
        self.time_elapsed = 0.0

    def _spawn_initial_bubbles(self) -> None:
        """
        Fills the background with an initial set of bubbles.
        """
        for _ in range(8):  # A nice dense aesthetic
            x = random.randint(20, WINDOW_WIDTH - 20)
            y = random.randint(0, WINDOW_HEIGHT)
            self.bubbles.append(Bubble(x, y))

    def enter(self) -> None:
        """
        Resets the next state target when entering the menu.
        """
        self.next_state = None

    def handle_events(self, events: List[pygame.event.Event]) -> None:
        """
        Checks for button clicks to transition to the Game Scene.
        """
        for event in events:
            if self.start_button.handle_event(event):
                self.next_state = "GAME"

    def update(self, dt: float) -> Optional[str]:
        """
        Updates background elements, animations, and returns the next state target.
        """
        self.time_elapsed += dt
        
        # Update background bubbles
        for bubble in self.bubbles:
            bubble.update(dt)
            # Recycle bubbles to the bottom when they go off screen
            if bubble.y + bubble.radius < 0:
                bubble.y = WINDOW_HEIGHT + random.randint(50, 150)
                bubble.x = random.randint(20, WINDOW_WIDTH - 20)

        return self.next_state

    def draw(self, screen: pygame.Surface) -> None:
        """
        Renders the animated title, best score, bubbles, and the start button.
        """
        # 1. Background
        screen.fill(BG_COLOR)

        # 2. Background Bubbles Layer
        for bubble in self.bubbles:
            bubble.draw(screen)

        # 3. Floating and Glowing Title
        # Calculate sine wave bounce offset
        bounce_offset = math.sin(self.time_elapsed * 3.0) * 15.0
        title_center_y = (WINDOW_HEIGHT // 3) + bounce_offset

        # Create base title surfaces
        # We use a multi-pass offset method for the glow instead of scaling/blending
        # which can sometimes cause rectangular artifacts with standard fonts.
        glow_color = (255, 105, 180) # Hot Pink glow
        glow_surf = self.title_font.render(TITLE, True, glow_color)
        title_surf = self.title_font.render(TITLE, True, (255, 255, 255))
        
        title_rect = title_surf.get_rect(center=(WINDOW_WIDTH // 2, int(title_center_y)))
        
        # Draw the "glow" by blitting the pink text with small offsets
        for dx, dy in [(-2, -2), (2, -2), (-2, 2), (2, 2), (0, -3), (0, 3), (-3, 0), (3, 0)]:
            screen.blit(glow_surf, (title_rect.x + dx, title_rect.y + dy))
            
        # Then blit the crisp white text over it centered
        screen.blit(title_surf, title_rect)

        # 4. Draw Start Button
        self.start_button.draw(screen)

        # 5. Draw High Score HUD
        best_score = ScoreManager.get_high_score()
        score_surf = self.score_font.render(f"Best Run: {best_score}", True, (255, 255, 255))
        
        # Render a soft black shadow behind the score for readability
        shadow_surf = self.score_font.render(f"Best Run: {best_score}", True, (0, 0, 0))
        screen.blit(shadow_surf, (12, WINDOW_HEIGHT - 48))
        screen.blit(score_surf, (10, WINDOW_HEIGHT - 50))
