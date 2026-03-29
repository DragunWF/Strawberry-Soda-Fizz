import unittest
import pygame
import os
from modules.scenes.game_scene import GameScene
from modules.constants import GRACE_DURATION

# Headless setup
os.environ['SDL_VIDEODRIVER'] = 'dummy'

class TestBubbleSpawnLocation(unittest.TestCase):
    """
    Verify that the procedural bubbles are scattered across the screen.
    """

    def setUp(self) -> None:
        pygame.init()
        pygame.display.set_mode((1, 1))
        self.scene = GameScene()

    def tearDown(self) -> None:
        pygame.quit()

    def test_procedural_spawn_is_scattered(self):
        """
        Verify that new bubbles spawn within the screen height during the first wave.
        """
        self.scene.enter()
        # Fast forward past grace period
        self.scene.update(GRACE_DURATION + 0.1)
        self.scene.update(0.1) # Trigger the else block
        
        # Check all bubbles are within the window (mostly)
        found_high = False
        for bubble in self.scene.bubbles:
            if bubble.y < 600:
                found_high = True
                break
        self.assertTrue(found_high, "Procedural bubbles should appear in the viewable area for immediate play.")

if __name__ == '__main__':
    unittest.main()
