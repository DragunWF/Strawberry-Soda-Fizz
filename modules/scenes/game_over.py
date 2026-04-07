import pygame
from typing import List, Optional
from modules.scenes.base_scene import BaseScene
from modules.ui.text_button import TextButton
from modules.core.score_manager import ScoreManager
from modules.core.audio_manager import AudioManager
from modules.constants import WINDOW_WIDTH, WINDOW_HEIGHT


class GameOverScene(BaseScene):
    """
    The end-game scene, triggered when the soda goes flat.
    Displays the final score and allows for restarting or returning to the main menu.
    """

    def __init__(self) -> None:
        super().__init__()
        self.msg_font = pygame.font.SysFont(None, 40)
        self.score_font = pygame.font.SysFont(None, 32)
        
        # Instantiate Play Again and Main Menu buttons
        button_width = 180
        button_height = 40
        x = (WINDOW_WIDTH - button_width) // 2
        y_start = (WINDOW_HEIGHT // 2) + 60
        
        self.play_again_button = TextButton(x, y_start, button_width, button_height, "Play Again")
        self.main_menu_button = TextButton(x, y_start + 60, button_width, button_height, "Main Menu")

    def enter(self) -> None:
        """
        Resets the next state target when entering.
        """
        self.next_state = None

    def handle_events(self, events: List[pygame.event.Event]) -> None:
        """
        Checks for button clicks to navigate to Game or Menu scenes.
        """
        for event in events:
            if self.play_again_button.handle_event(event):
                AudioManager.play_ui_click()
                self.next_state = "GAME"
            elif self.main_menu_button.handle_event(event):
                AudioManager.play_ui_click()
                self.next_state = "MENU"

    def update(self, dt: float) -> Optional[str]:
        """
        Returns the next state target.
        """
        return self.next_state

    def draw(self, screen: pygame.Surface) -> None:
        """
        Renders the Game Over message, final score, and choice buttons.
        """
        # Draw Message
        msg_surf = self.msg_font.render("The Soda Went Flat!", True, (0, 0, 0))
        msg_rect = msg_surf.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 60))
        screen.blit(msg_surf, msg_rect)

        # Draw Final Score
        score_val = ScoreManager.get_score()
        score_surf = self.score_font.render(f"Final Fizz Level: {score_val}", True, (200, 0, 0))
        score_rect = score_surf.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 10))
        screen.blit(score_surf, score_rect)

        # Draw High Score
        high_score_surf = self.score_font.render(f"Best: {ScoreManager.get_high_score()}", True, (0, 0, 0))
        high_score_rect = high_score_surf.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 20))
        screen.blit(high_score_surf, high_score_rect)

        # Draw Buttons
        self.play_again_button.draw(screen)
        self.main_menu_button.draw(screen)
