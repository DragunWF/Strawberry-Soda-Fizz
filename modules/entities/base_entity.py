import pygame
from abc import ABC, abstractmethod


class BaseEntity(ABC):
    """
    Abstract blueprint for all interactable objects in Strawberry Soda Fizz.
    """

    def __init__(self, x: float, y: float) -> None:
        self.x = x
        self.y = y

    @abstractmethod
    def update(self, dt: float) -> None:
        """
        Handles time-based logic and physics for the entity.
        """
        pass

    @abstractmethod
    def draw(self, screen: pygame.Surface) -> None:
        """
        Renders the entity to the screen.
        """
        pass
