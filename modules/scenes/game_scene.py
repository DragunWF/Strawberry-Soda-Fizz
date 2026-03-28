import pygame
import random
from typing import List, Optional
from modules.scenes.base_scene import BaseScene
from modules.entities.player import Player
from modules.entities.bubbles import Bubble
from modules.entities.collectibles import SodaFizzDrink
from modules.core.score_manager import ScoreManager
from modules.constants import (
    BG_COLOR, WINDOW_WIDTH, WINDOW_HEIGHT, 
    INITIAL_BUBBLE_COUNT, GRACE_DURATION, 
    PLAYER_START_X, PLAYER_START_Y,
    SCORE_PASSIVE_RATE, SCORE_COLLECTIBLE_BONUS
)


class GameScene(BaseScene):
    """
    Main gameplay area for Strawberry Soda Fizz.
    Manages the player entity, procedural bubbles, and scoring.
    """

    def __init__(self) -> None:
        super().__init__()
        # Spawn Strawberry Chunk
        self.player = Player(PLAYER_START_X, PLAYER_START_Y)
        self.bubbles: List[Bubble] = []
        self.collectibles: List[SodaFizzDrink] = []
        
        # HUD and UI settings
        self.hud_font = pygame.font.SysFont(None, 36)
        self.grace_font = pygame.font.SysFont(None, 72)
        self.grace_timer = 0.0
        self.fizz_spawned = False
        
        # Initial starting platform
        self._spawn_starting_platform()

    def _spawn_starting_platform(self) -> None:
        """
        Clears the bubbles list. No initial platform is spawned.
        """
        self.bubbles = []
        self.fizz_spawned = False

    def _spawn_procedural_fizz(self) -> None:
        """
        Fills the screen with the remaining procedural bubbles.
        """
        for _ in range(INITIAL_BUBBLE_COUNT - len(self.bubbles)):
            x = random.randint(50, WINDOW_WIDTH - 50)
            y = random.randint(150, WINDOW_HEIGHT - 50)
            self.bubbles.append(Bubble(x, y))
        self.fizz_spawned = True

    def enter(self) -> None:
        """
        Resets the scene, player position, score, and starts the grace period.
        """
        self.next_state = None
        self.player.x = PLAYER_START_X
        self.player.y = PLAYER_START_Y
        self.player.vel_y = 0
        self.grace_timer = GRACE_DURATION
        
        ScoreManager.reset_score()
        self.collectibles = []
        self._spawn_starting_platform()

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
        Updates entities and handles physics/scoring.
        Triggers procedural fizz spawning after the grace period ends.
        """
        # --- Grace Period Update ---
        if self.grace_timer > 0:
            self.grace_timer -= dt
            # During grace period, don't update player gravity
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                self.player.x -= self.player.speed * dt
            if keys[pygame.K_RIGHT]:
                self.player.x += self.player.speed * dt
            self.player.rect.x = int(self.player.x)
            self.player.rect.y = int(self.player.y)
        else:
            # Check if we need to trigger the procedural fizz spawn
            if not self.fizz_spawned:
                self._spawn_procedural_fizz()
                
            # 1. Update Player (Full Physics)
            self.player.update(dt)
        
            # 2. Update Score Passively (Floating precision fix)
            ScoreManager.add_score(SCORE_PASSIVE_RATE * dt)

        # 3. Update Bubbles & Handle Recycling
        for bubble in self.bubbles[:]:
            bubble.update(dt)
            if bubble.y + bubble.radius < 0:
                bubble.y = WINDOW_HEIGHT + random.randint(50, 150)
                bubble.x = random.randint(50, WINDOW_WIDTH - 50)

            # Collision Logic: Player landing on Bubble (only if grace period over)
            if self.player.vel_y > 0 and self.grace_timer <= 0:
                if self.player.rect.colliderect(bubble.rect):
                    if self.player.rect.bottom <= bubble.rect.centery + 15:
                        self.player.bounce()
                        # Bug Fix: Recycle instead of removing to maintain density
                        bubble.y = WINDOW_HEIGHT + random.randint(50, 150)
                        bubble.x = random.randint(50, WINDOW_WIDTH - 50)
                        continue

        # 4. Handle Collectibles: Spawning & Logic
        if random.random() < 0.01:
            x = random.randint(20, WINDOW_WIDTH - 40)
            self.collectibles.append(SodaFizzDrink(x, -50))

        for drink in self.collectibles[:]:
            drink.update(dt)
            if drink.y > WINDOW_HEIGHT:
                self.collectibles.remove(drink)
                continue

            if self.player.rect.colliderect(drink.rect):
                ScoreManager.add_score(SCORE_COLLECTIBLE_BONUS)
                self.collectibles.remove(drink)

        # 5. Check Failure Condition: Only check after grace period
        if self.grace_timer <= 0:
            if self.player.y > WINDOW_HEIGHT:
                self.next_state = "GAME_OVER"

        return self.next_state

    def draw(self, screen: pygame.Surface) -> None:
        """
        Renders the background, entities, and the HUD.
        """
        # 1. Clear Screen
        screen.fill(BG_COLOR)

        # 2. Draw Bubbles & Collectibles
        for bubble in self.bubbles:
            bubble.draw(screen)
        
        for drink in self.collectibles:
            drink.draw(screen)

        # 3. Draw Player
        self.player.draw(screen)

        # 4. Draw HUD
        score_text = self.hud_font.render(f"Fizzy Score: {ScoreManager.get_score()}", True, (0, 0, 0))
        screen.blit(score_text, (10, 10))

        # 5. Draw "Ready?" during Grace Period
        if self.grace_timer > 0:
            ready_surf = self.grace_font.render("Fizzy Ready?", True, (255, 255, 255))
            ready_rect = ready_surf.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
            screen.blit(ready_surf, ready_rect)
