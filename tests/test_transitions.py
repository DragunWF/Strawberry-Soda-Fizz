import pygame
import os

# Set environment variable to use dummy video driver for headless testing
os.environ['SDL_VIDEODRIVER'] = 'dummy'
pygame.init()
pygame.display.set_mode((1, 1))

from modules.scenes.main_menu import MainMenuScene
from modules.scenes.game_scene import GameScene
from modules.scenes.game_over import GameOverScene

def test_transitions():
    print("Testing Scene Transitions...")
    
    # Test MainMenu -> Game
    menu = MainMenuScene()
    menu.enter()
    # Simulate a click on the start button
    event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {"button": 1, "pos": menu.start_button.rect.center})
    menu.handle_events([event])
    res = menu.update(0.1)
    print(f"MainMenu update result after click: {res}")
    assert res == "GAME"

    # Test Game -> GameOver
    game = GameScene()
    game.enter()
    # Simulate 'K' key press
    event = pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_k})
    game.handle_events([event])
    res = game.update(0.1)
    print(f"Game update result after 'K' key: {res}")
    assert res == "GAME_OVER"

    # Test GameOver -> Game
    game_over = GameOverScene()
    game_over.enter()
    # Simulate click on Play Again
    event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {"button": 1, "pos": game_over.play_again_button.rect.center})
    game_over.handle_events([event])
    res = game_over.update(0.1)
    print(f"GameOver result after Play Again click: {res}")
    assert res == "GAME"

    # Test GameOver -> Menu
    game_over.enter()
    # Simulate click on Main Menu
    event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {"button": 1, "pos": game_over.main_menu_button.rect.center})
    game_over.handle_events([event])
    res = game_over.update(0.1)
    print(f"GameOver result after Main Menu click: {res}")
    assert res == "MENU"

    print("All transition tests passed!")

if __name__ == "__main__":
    test_transitions()
    pygame.quit()
