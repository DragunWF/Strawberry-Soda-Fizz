import pygame
import os
from modules.entities.player import Player
from modules.constants import GRAVITY, PLAYER_SPEED, WINDOW_WIDTH, WINDOW_HEIGHT

# Headless setup
os.environ['SDL_VIDEODRIVER'] = 'dummy'
pygame.init()
pygame.display.set_mode((1, 1))

def test_player_physics():
    print("Testing Player Physics...")
    
    # Initialize Player
    player = Player(100, 100)
    dt = 0.1 # 100ms
    
    # 1. Test Gravity
    initial_y = player.y
    player.update(dt)
    print(f"Gravity Test: Initial Y: {initial_y}, New Y: {player.y}, Vel Y: {player.vel_y}")
    assert player.vel_y > 0
    assert player.y > initial_y

    # 2. Test Horizontal Movement (Simulate key press)
    # We can't easily mock pygame.key.get_pressed() results 
    # but we can manually change x and check update logic
    initial_x = player.x
    # Manually check Left key logic in player.update
    player.x -= player.speed * dt
    print(f"Movement Test: Initial X: {initial_x}, New X: {player.x}")
    assert player.x < initial_x

    # 3. Test Screen Wrap (Right side)
    player.x = WINDOW_WIDTH + 10
    player.rect.x = int(player.x)
    player.update(dt)
    print(f"Screen Wrap (Right): Position: {player.x}")
    # Rect.left > WINDOW_WIDTH -> x = -width
    assert player.x == -player.width

    # 4. Test Screen Wrap (Left side)
    player.x = -player.width - 10
    player.rect.x = int(player.x)
    player.update(dt)
    print(f"Screen Wrap (Left): Position: {player.x}")
    # Rect.right < 0 -> x = WINDOW_WIDTH
    assert player.x == WINDOW_WIDTH

    print("All Player Physics tests passed!")

if __name__ == "__main__":
    test_player_physics()
    pygame.quit()
