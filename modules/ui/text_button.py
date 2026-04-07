import pygame
from typing import Tuple, Dict, Optional


class TextButton:
    """
    A reusable UI button that displays text and handles hover/click events.
    Includes a scaling effect when hovered.
    Optimized: Caches text surfaces to prevent redundant font.render calls.
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

        # --- Performance Caching ---
        self._cached_surf: Optional[pygame.Surface] = None
        self._cached_surf_hover: Optional[pygame.Surface] = None
        self._pre_render()

    def _pre_render(self) -> None:
        """
        Renders and caches the text surfaces for both normal and hover states.
        """
        # Normal Text
        self._cached_surf = self.font.render(self.text, True, self.colors["text"])
        
        # Hover Text (1.1x scaled)
        hover_surf = self.font.render(self.text, True, self.colors["text"])
        sw, sh = hover_surf.get_width(), hover_surf.get_height()
        self._cached_surf_hover = pygame.transform.scale(hover_surf, (int(sw * 1.1), int(sh * 1.1)))

    def handle_event(self, event: pygame.event.Event) -> bool:
        """
        Processes a single Pygame event.
        Returns True if the button was clicked.
        """
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.render_rect.collidepoint(event.pos):
                return True
        return False

    def update(self) -> None:
        """
        Updates the internal state (like hover detection).
        """
        mouse_pos = pygame.mouse.get_pos()
        self.is_hovered = self.base_rect.collidepoint(mouse_pos)

    def draw(self, screen: pygame.Surface) -> None:
        """
        Renders the button to the screen using cached surfaces.
        """
        self.update()
        
        scale = 1.1 if self.is_hovered else 1.0
        
        # Adjust background rect
        self.render_rect.width = int(self.base_rect.width * scale)
        self.render_rect.height = int(self.base_rect.height * scale)
        self.render_rect.center = self.base_rect.center

        # Draw background
        color = self.colors["hover"] if self.is_hovered else self.colors["normal"]
        pygame.draw.rect(screen, color, self.render_rect)
        pygame.draw.rect(screen, self.colors["text"], self.render_rect, 2)  # Border

        # Draw cached text surface
        text_surf = self._cached_surf_hover if self.is_hovered else self._cached_surf
        if text_surf:
            text_rect = text_surf.get_rect(center=self.render_rect.center)
            screen.blit(text_surf, text_rect)
