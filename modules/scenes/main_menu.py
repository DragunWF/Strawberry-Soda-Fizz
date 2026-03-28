import pygame
from typing import List, Optional
from modules.scenes.base_scene import BaseScene
from modules.ui.text_button import TextButton
from modules.constants import BG_COLOR, TITLE, WINDOW_WIDTH, WINDOW_HEIGHT


class MainMenuScene(BaseScene):
    """
    The initial scene for the game, featuring the title and a start button.
    """

    def __init__(self) -> None:
        super().__init__()
        self.title_font = pygame.font.SysFont(None, 48)
        
        # Instantiate the Start Game button
        button_width = 200
        button_height = 50
        x = (WINDOW_WIDTH - button_width) // 2
        y = (WINDOW_HEIGHT - button_height) // 2
        self.start_button = TextButton(x, y + 50, button_width, button_height, "Start Game")

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
        Returns the next state target.
        """
        return self.next_state

    def draw(self, screen: pygame.Surface) -> None:
        """
        Renders the title and the start button.
        """
        # Draw Title
        title_surf = self.title_font.render(TITLE, True, (0, 0, 0))
        title_rect = title_surf.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 3))
        screen.blit(title_surf, title_rect)

        # Draw Start Button
        self.start_button.draw(screen)
