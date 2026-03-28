import pygame
from typing import Dict, Tuple, Optional


class ResourceManager:
    """
    Centralized manager for loading and caching game assets.
    Provides graceful fallbacks if assets are missing.
    """
    _images: Dict[str, pygame.Surface] = {}
    _fonts: Dict[str, pygame.font.Font] = {}
    _sounds: Dict[str, pygame.mixer.Sound] = {}

    @classmethod
    def get_image(cls, name: str, fallback_color: Tuple[int, int, int], size: Tuple[int, int]) -> pygame.Surface:
        """
        Loads an image from assets/sprites/ or returns a fallback surface.
        """
        if name in cls._images:
            return cls._images[name]

        try:
            path = f"assets/sprites/{name}"
            image = pygame.image.load(path).convert_alpha()
            image = pygame.transform.scale(image, size)
            cls._images[name] = image
            return image
        except (pygame.error, FileNotFoundError, Exception):
            print(f"Warning: Resource '{name}' not found. Using fallback.")
            fallback = pygame.Surface(size)
            fallback.fill(fallback_color)
            cls._images[name] = fallback
            return fallback

    @classmethod
    def get_font(cls, name: Optional[str], size: int) -> pygame.font.Font:
        """
        Loads a font from assets/fonts/ or returns a default SysFont.
        """
        key = f"{name}_{size}"
        if key in cls._fonts:
            return cls._fonts[key]

        try:
            if name:
                font = pygame.font.Font(f"assets/fonts/{name}", size)
            else:
                font = pygame.font.SysFont(None, size)
            cls._fonts[key] = font
            return font
        except (pygame.error, FileNotFoundError, Exception):
            print(f"Warning: Font '{name}' not found. Using SysFont.")
            font = pygame.font.SysFont(None, size)
            cls._fonts[key] = font
            return font
