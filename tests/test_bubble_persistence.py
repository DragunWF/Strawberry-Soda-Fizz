import unittest
import pygame
import os
from modules.scenes.game_scene import GameScene
from modules.constants import INITIAL_BUBBLE_COUNT, WINDOW_HEIGHT

# Headless setup
os.environ['SDL_VIDEODRIVER'] = 'dummy'

class TestBubblePersistence(unittest.TestCase):
    """
    Verify that the bubble count remains constant after a bounce.
    """

    def setUp(self) -> None:
        pygame.init()
        pygame.display.set_mode((1, 1))
        self.scene = GameScene()

    def tearDown(self) -> None:
        pygame.quit()

    def test_bubble_count_constant_after_bounce(self):
        """
        Verify that the total number of bubbles does not decrease when the player bounces.
        """
        self.scene.enter()
        initial_count = len(self.scene.bubbles)
        self.assertEqual(initial_count, INITIAL_BUBBLE_COUNT)
        
        # 1. Setup a forced collision
        player = self.scene.player
        bubble = self.scene.bubbles[0]
        
        # Position player just above bubble center for a guaranteed bounce
        # Player bottom = y + height
        # Bubble center = y
        player.x = bubble.x - (player.width // 2)
        player.y = bubble.y - player.height + 2 # Slightly overlapping but bottom is near center
        player.vel_y = 10.0 # Slow falling
        
        # Sync rects manually for the test
        player.rect.x = int(player.x)
        player.rect.y = int(player.y)
        bubble.rect.x = int(bubble.x - bubble.radius)
        bubble.rect.y = int(bubble.y - bubble.radius)
        
        # Ensure grace period is over
        self.scene.grace_timer = 0
        
        # 2. Trigger update with very small dt to avoid missing the window
        dt = 0.001
        self.scene.update(dt)
        
        # 3. Verify count
        final_count = len(self.scene.bubbles)
        self.assertEqual(final_count, initial_count, "Bubble count should not decrease after a jump.")
        self.assertGreater(bubble.y, WINDOW_HEIGHT, f"Bubble should have been recycled below {WINDOW_HEIGHT}. Current Y: {bubble.y}")

if __name__ == '__main__':
    unittest.main()
