import pygame
from typing import List, Optional
from modules.scenes.base_scene import BaseScene
from modules.constants import WINDOW_WIDTH, WINDOW_HEIGHT


class GameScene(BaseScene):
    """
    A placeholder scene for the actual gameplay area.
    Transitions to Game Over state when 'K' is pressed.
    """

    def __init__(self) -> None:
        super().__init__()
        self.font = pygame.font.SysFont(None, 24)

    def enter(self) -> None:
        """
        Resets the next state target when entering.
        """
        self.next_state = None

    def handle_events(self, events: List[pygame.event.Event]) -> None:
        """
        Processes 'K' key to simulate a Game Over trigger.
        """
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_k:
                    self.next_state = "GAME_OVER"

    def update(self, dt: float) -> Optional[str]:
        """
        Returns the next state target.
        """
        return self.next_state

    def draw(self, screen: pygame.Surface) -> None:
        """
        Renders gameplay placeholder text.
        """
        text_surf = self.font.render("Game Running - Press 'K' to simulate Game Over", True, (0, 0, 0))
        text_rect = text_surf.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
        screen.blit(text_surf, text_rect)
