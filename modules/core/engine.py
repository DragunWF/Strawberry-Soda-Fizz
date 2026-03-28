import pygame
import sys
from typing import List, Optional, Dict

from modules.constants import WINDOW_WIDTH, WINDOW_HEIGHT, FPS, TITLE, BG_COLOR
from modules.core.state_machine import StateMachine

from modules.scenes.base_scene import BaseScene
from modules.scenes.main_menu import MainMenuScene
from modules.scenes.game_scene import GameScene
from modules.scenes.game_over import GameOverScene


class PlaceholderScene(BaseScene):
    """
    Temporary scene used to test the Engine and StateMachine.
    """

    def __init__(self) -> None:
        super().__init__()

    def enter(self) -> None:
        print("PlaceholderScene entered.")

    def handle_events(self, events: List[pygame.event.Event]) -> None:
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    print("Space pressed in PlaceholderScene!")

    def update(self, dt: float) -> Optional[str]:
        # Logic update here...
        return None

    def draw(self, screen: pygame.Surface) -> None:
        # Drawing is handled by the engine filling the screen, 
        # but scenes can add more.
        pass

class Engine:
    """
    Main Pygame engine that handles the system lifecycle, event loop,
    and state delegation.
    """

    def __init__(self) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.is_running = True
        self.state_machine = StateMachine()

        # Initialize and setup scenes
        states: Dict[str, BaseScene] = {
            "MENU": MainMenuScene(),
            "GAME": GameScene(),
            "GAME_OVER": GameOverScene()
        }
        self.state_machine.setup(states, "MENU")

    def run(self) -> None:
        """
        Primary game loop.
        """
        while self.is_running:
            # Calculate delta time in seconds
            dt = self.clock.tick(FPS) / 1000.0

            # Handle events
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.is_running = False
            
            self.state_machine.handle_events(events)

            # Update
            self.state_machine.update(dt)

            # Draw
            self.screen.fill(BG_COLOR)
            self.state_machine.draw(self.screen)
            pygame.display.flip()

        pygame.quit()
        sys.exit()
