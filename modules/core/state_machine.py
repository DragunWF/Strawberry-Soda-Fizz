import pygame
from typing import Dict, Optional, List
from modules.scenes.base_scene import BaseScene


class StateMachine:
    """
    Manages the transitions between different scenes (states) of the game.
    Delegates event handling, updates, and rendering to the active scene.
    """

    def __init__(self) -> None:
        self.states: Dict[str, BaseScene] = {}
        self.current_state_name: Optional[str] = None
        self.current_state_obj: Optional[BaseScene] = None

    def setup(self, states_dict: Dict[str, BaseScene], start_state_name: str) -> None:
        """
        Initializes the state machine with available scenes and the starting scene.
        """
        self.states = states_dict
        self.current_state_name = start_state_name
        self.current_state_obj = self.states[start_state_name]
        self.current_state_obj.enter()

    def handle_events(self, events: List[pygame.event.Event]) -> None:
        """
        Passes events down to the current scene.
        """
        if self.current_state_obj:
            self.current_state_obj.handle_events(events)

    def update(self, dt: float) -> None:
        """
        Updates the current scene and handles scene transitions.
        """
        if self.current_state_obj:
            new_state_name = self.current_state_obj.update(dt)
            if new_state_name and new_state_name in self.states:
                self.flip_state(new_state_name)

    def draw(self, screen: pygame.Surface) -> None:
        """
        Renders the current scene to the screen.
        """
        if self.current_state_obj:
            self.current_state_obj.draw(screen)

    def flip_state(self, new_state_name: str) -> None:
        """
        Transitions to a new state and calls its enter() method.
        """
        print(f"State transition: {self.current_state_name} -> {new_state_name}")
        self.current_state_name = new_state_name
        self.current_state_obj = self.states[new_state_name]
        self.current_state_obj.enter()
