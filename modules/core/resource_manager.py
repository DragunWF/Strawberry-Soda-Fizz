import pygame
import os
from typing import Dict, Tuple, Optional


class ResourceManager:
    """
    Centralized manager for loading and caching game assets.
    Provides robust pathing and graceful fallbacks if assets are missing.
    """
    _images: Dict[str, pygame.Surface] = {}
    _fonts: Dict[str, pygame.font.Font] = {}
    _sounds: Dict[str, pygame.mixer.Sound] = {}

    # Root directory of the project for absolute pathing
    _base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

    @classmethod
    def get_image(cls, name: str, fallback_color: Tuple[int, int, int], size: Tuple[int, int]) -> pygame.Surface:
        """
        Loads an image from assets/sprites/ or returns a fallback surface.
        """
        if name in cls._images:
            return cls._images[name]

        try:
            path = os.path.join(cls._base_dir, "assets", "sprites", name)
            image = pygame.image.load(path).convert_alpha()
            image = pygame.transform.scale(image, size)
            cls._images[name] = image
            return image
        except (pygame.error, FileNotFoundError, Exception):
            # Only print warning if it's not a generic fallback request
            if name != "player.png":
                print(f"Warning: Resource '{name}' not found at {path}. Using fallback.")
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
                path = os.path.join(cls._base_dir, "assets", "fonts", name)
                font = pygame.font.Font(path, size)
            else:
                font = pygame.font.SysFont(None, size)
            cls._fonts[key] = font
            return font
        except (pygame.error, FileNotFoundError, Exception):
            print(f"Warning: Font '{name}' not found. Using SysFont.")
            font = pygame.font.SysFont(None, size)
            cls._fonts[key] = font
            return font

    @classmethod
    def get_sound(cls, name: str) -> Optional[pygame.mixer.Sound]:
        """
        Loads a sound from assets/audio/ or returns None if missing.
        Ensures the mixer is initialized before attempting to load.
        """
        if name in cls._sounds:
            return cls._sounds[name]

        # Safety check for uninitialized mixer
        if not pygame.mixer or not pygame.mixer.get_init():
            return None

        try:
            path = os.path.join(cls._base_dir, "assets", "audio", name)
            if not os.path.exists(path):
                return None
                
            sound = pygame.mixer.Sound(path)
            cls._sounds[name] = sound
            return sound
        except (pygame.error, FileNotFoundError, Exception):
            print(f"Sound effect '{name}' not found!")
            # Returning None if the sound file is missing or mixer is uninitialized.
            # AudioManager handles this gracefully.
            return None
