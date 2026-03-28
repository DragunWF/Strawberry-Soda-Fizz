import pygame
from typing import Tuple, Dict


class TextButton:
    """
    A reusable UI button that displays text and handles hover/click events.
    """

    def __init__(
        self,
        x: int,
        y: int,
        width: int,
        height: int,
        text: str,
        font_size: int = 32,
        colors: Dict[str, Tuple[int, int, int]] = None
    ) -> None:
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = pygame.font.SysFont(None, font_size)
        
        # Default colors if none provided
        if colors is None:
            colors = {
                "normal": (200, 200, 200),
                "hover": (255, 255, 255),
                "text": (0, 0, 0)
            }
        self.colors = colors
        self.is_hovered = False

    def handle_event(self, event: pygame.event.Event) -> bool:
        """
        Processes a single Pygame event.
        Returns True if the button was clicked.
        """
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                return True
        return False

    def draw(self, screen: pygame.Surface) -> None:
        """
        Renders the button to the screen, adjusting color for hover state.
        """
        # Update hover state
        mouse_pos = pygame.mouse.get_pos()
        self.is_hovered = self.rect.collidepoint(mouse_pos)

        # Draw background
        color = self.colors["hover"] if self.is_hovered else self.colors["normal"]
        pygame.draw.rect(screen, color, self.rect)
        pygame.draw.rect(screen, self.colors["text"], self.rect, 2)  # Border

        # Draw text
        text_surf = self.font.render(self.text, True, self.colors["text"])
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)
