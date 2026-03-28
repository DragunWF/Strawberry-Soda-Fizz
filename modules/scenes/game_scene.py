import pygame
from typing import List, Optional
from modules.scenes.base_scene import BaseScene
from modules.entities.player import Player
from modules.constants import BG_COLOR, WINDOW_WIDTH, WINDOW_HEIGHT


class GameScene(BaseScene):
    """
    Main gameplay area for Strawberry Soda Fizz.
    Manages the player entity and handles failure conditions.
    """

    def __init__(self) -> None:
        super().__init__()
        # Spawn Strawberry Chunk in the top-middle segment
        self.player = Player(WINDOW_WIDTH // 2 - 15, 100)

    def enter(self) -> None:
        """
        Resets the next state and player position when entering the game.
        """
        self.next_state = None
        self.player.x = WINDOW_WIDTH // 2 - 15
        self.player.y = 100
        self.player.vel_y = 0

    def handle_events(self, events: List[pygame.event.Event]) -> None:
        """
        Processes keyboard inputs for the state machine.
        (Player movement keys are handled directly in the Player class via get_pressed).
        """
        for event in events:
            if event.type == pygame.KEYDOWN:
                # Debug override: Kill player manually
                if event.key == pygame.K_k:
                    self.next_state = "GAME_OVER"

    def update(self, dt: float) -> Optional[str]:
        """
        Updates the player physics and checks for "Fall-Off" failure.
        """
        # 1. Update Entities
        self.player.update(dt)
        
        # 2. Check Failure Condition: Falling off screen
        # Using player's rect top or center ensures some leeway
        if self.player.y > WINDOW_HEIGHT:
            self.next_state = "GAME_OVER"

        return self.next_state

    def draw(self, screen: pygame.Surface) -> None:
        """
        Renders the game environment and all entities.
        """
        # 1. Clear Screen
        screen.fill(BG_COLOR)

        # 2. Draw Entities
        self.player.draw(screen)
