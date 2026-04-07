import random
import pygame
from typing import List, Optional
from modules.core.resource_manager import ResourceManager


class AudioManager:
    """
    Centralized manager for playing sound effects in the game.
    Implements lazy-loading to ensure the mixer is initialized before use.
    """
    _bubble_pops: List[pygame.mixer.Sound] = []
    _pickup: Optional[pygame.mixer.Sound] = None
    _gameover: Optional[pygame.mixer.Sound] = None
    _initialized: bool = False
    _ui_click: Optional[pygame.mixer.Sound] = None

    @classmethod
    def _initialize(cls) -> None:
        """
        Loads sounds if the mixer is ready. This is called on the first play request.
        """
        if cls._initialized or not pygame.mixer or not pygame.mixer.get_init():
            return

        # Load pop variants and filter out None if files are missing
        pop_names = ["bubble_pop_1.wav", "bubble_pop_2.wav", "bubble_pop_3.wav", "bubble_pop_4.wav"]
        cls._bubble_pops = [s for s in (ResourceManager.get_sound(n) for n in pop_names) if s is not None]
        
        # Load single sounds
        cls._pickup = ResourceManager.get_sound("pickup_fizz.wav")
        cls._gameover = ResourceManager.get_sound("gameover.wav")
        cls._ui_click = ResourceManager.get_sound("ui_click.wav")

        cls._initialized = True

    @classmethod
    def play_pop(cls) -> None:
        """
        Triggered when the player successfully bounces on a bubble.
        """
        cls._initialize()
        if cls._bubble_pops:
            random.choice(cls._bubble_pops).play()

    @classmethod
    def play_pickup(cls) -> None:
        """
        Triggered when the player catches a Soda Fizz collectible.
        """
        cls._initialize()
        if cls._pickup:
            cls._pickup.play()

    @classmethod
    def play_lose(cls) -> None:
        """
        Triggered when the player falls off the screen (Game Over).
        """
        cls._initialize()
        if cls._gameover:
            cls._gameover.play()

    @classmethod
    def play_ui_click(cls) -> None:
        """
        Triggered when the player clicks a button
        """
        cls._initialize()
        if cls._ui_click:
            cls._ui_click.play()