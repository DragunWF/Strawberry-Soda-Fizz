import pygame
import random
from typing import List, Optional
from modules.scenes.base_scene import BaseScene
from modules.entities.player import Player
from modules.entities.bubbles import Bubble
from modules.entities.collectibles import SodaFizzDrink
from modules.core.score_manager import ScoreManager
from modules.constants import BG_COLOR, WINDOW_WIDTH, WINDOW_HEIGHT


class GameScene(BaseScene):
    """
    Main gameplay area for Strawberry Soda Fizz.
    Manages the player entity, procedurally generated fizz bubbles,
    and falling collectibles for score collection.
    """

    def __init__(self) -> None:
        super().__init__()
        # Spawn Strawberry Chunk
        self.player = Player(WINDOW_WIDTH // 2 - 15, 100)
        self.bubbles: List[Bubble] = []
        self.collectibles: List[SodaFizzDrink] = []
        
        # HUD settings
        self.hud_font = pygame.font.SysFont(None, 36)
        
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
        Resets the next state, player position, bubbles, and score.
        """
        self.next_state = None
        self.player.x = WINDOW_WIDTH // 2 - 15
        self.player.y = 100
        self.player.vel_y = 0
        ScoreManager.reset_score()
        self.collectibles = []
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
        Updates player, bubbles, collectibles, and handles physics/scoring.
        """
        # 1. Update Player
        self.player.update(dt)
        
        # 2. Update Score Passively (10 points per survived second)
        ScoreManager.add_score(int(10 * dt))

        # 3. Update Bubbles & Handle Recycling
        for bubble in self.bubbles[:]:  # Use a copy to allow removal
            bubble.update(dt)
            if bubble.y + bubble.radius < 0:
                bubble.y = WINDOW_HEIGHT + random.randint(50, 150)
                bubble.x = random.randint(50, WINDOW_WIDTH - 50)
                # Position sync is now handled within bubble.update()

            # Collision Logic: Player landing on Bubble
            if self.player.vel_y > 0:
                if self.player.rect.colliderect(bubble.rect):
                    if self.player.rect.bottom <= bubble.rect.centery + 15:
                        self.player.bounce()
                        # Bug Fix: Pop the bubble on bounce
                        self.bubbles.remove(bubble)
                        continue

        # 4. Handle Collectibles: Spawning & Logic
        # ~1% chance to spawn per frame (at 60 FPS)
        if random.random() < 0.01:
            x = random.randint(20, WINDOW_WIDTH - 40)
            self.collectibles.append(SodaFizzDrink(x, -50))

        # Update and filter out-of-bounds collectibles
        for drink in self.collectibles[:]:
            drink.update(dt)
            if drink.y > WINDOW_HEIGHT:
                self.collectibles.remove(drink)
                continue

            # Collision Logic: Catching a drink
            if self.player.rect.colliderect(drink.rect):
                ScoreManager.add_score(500)
                self.collectibles.remove(drink)

        # 5. Check Failure Condition: Falling off screen
        if self.player.y > WINDOW_HEIGHT:
            self.next_state = "GAME_OVER"

        return self.next_state

    def draw(self, screen: pygame.Surface) -> None:
        """
        Renders the background, entities, and the HUD score.
        """
        # 1. Clear Screen
        screen.fill(BG_COLOR)

        # 2. Draw Bubbles & Collectibles (Background/Interactive Layers)
        for bubble in self.bubbles:
            bubble.draw(screen)
        
        for drink in self.collectibles:
            drink.draw(screen)

        # 3. Draw Player
        self.player.draw(screen)

        # 4. Draw HUD (Foreground Layer)
        score_text = self.hud_font.render(f"Fizzy Score: {ScoreManager.get_score()}", True, (0, 0, 0))
        screen.blit(score_text, (10, 10))
