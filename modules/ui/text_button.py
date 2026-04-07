import pygame
from typing import Tuple, Dict


class TextButton:
    """
    A reusable UI button that displays text and handles hover/click events.
    Includes a scaling effect when hovered.
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
        self.base_rect = pygame.Rect(x, y, width, height)
        self.render_rect = self.base_rect.copy()
        
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
            # We check collision against the rendered (potentially scaled) rect
            if self.render_rect.collidepoint(event.pos):
                return True
        return False

    def update(self) -> None:
        """
        Updates the internal state (like hover detection).
        Designed to be called once per frame before drawing.
        """
        mouse_pos = pygame.mouse.get_pos()
        # We detect hover using the base rect to prevent flickering at the edges
        self.is_hovered = self.base_rect.collidepoint(mouse_pos)

    def draw(self, screen: pygame.Surface) -> None:
        """
        Renders the button to the screen, adjusting color and scale for hover state.
        """
        self.update()
        
        scale = 1.1 if self.is_hovered else 1.0
        
        current_width = int(self.base_rect.width * scale)
        current_height = int(self.base_rect.height * scale)
        self.render_rect.width = current_width
        self.render_rect.height = current_height
        self.render_rect.center = self.base_rect.center

        # Draw background
        color = self.colors["hover"] if self.is_hovered else self.colors["normal"]
        pygame.draw.rect(screen, color, self.render_rect)
        pygame.draw.rect(screen, self.colors["text"], self.render_rect, 2)  # Border

        # Draw text
        text_surf = self.font.render(self.text, True, self.colors["text"])
        if scale != 1.0:
            text_surf = pygame.transform.scale(
                text_surf, 
                (int(text_surf.get_width() * scale), int(text_surf.get_height() * scale))
            )
            
        text_rect = text_surf.get_rect(center=self.render_rect.center)
        screen.blit(text_surf, text_rect)
