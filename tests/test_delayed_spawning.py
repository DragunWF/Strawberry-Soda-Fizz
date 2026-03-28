import unittest
import pygame
import os
from modules.scenes.game_scene import GameScene
from modules.constants import GRACE_DURATION, INITIAL_BUBBLE_COUNT

# Headless setup
os.environ['SDL_VIDEODRIVER'] = 'dummy'

class TestDelayedSpawning(unittest.TestCase):
    """
    Unit tests for the delayed procedural bubble spawning.
    """

    def setUp(self) -> None:
        pygame.init()
        pygame.display.set_mode((1, 1))
        self.scene = GameScene()

    def tearDown(self) -> None:
        pygame.quit()

    def test_initial_state_empty(self):
        """
        Verify that no bubbles exist during the initial grace period.
        """
        self.scene.enter()
        self.assertEqual(len(self.scene.bubbles), 0, "Should have no bubbles initially.")
        self.assertFalse(self.scene.fizz_spawned)

    def test_spawning_after_grace_period(self):
        """
        Verify that the full bubble count is spawned only after the grace timer hits zero.
        """
        self.scene.enter()
        
        # 1. Update during grace period (dt < GRACE_DURATION)
        self.scene.update(GRACE_DURATION / 2)
        self.assertEqual(len(self.scene.bubbles), 0)
        
        # 2. Update to push past grace period
        self.scene.update(GRACE_DURATION)
        
        # 3. One more update to trigger the 'else' block
        self.scene.update(0.1)
        
        # 4. Verify procedural fizz spawned
        self.assertEqual(len(self.scene.bubbles), INITIAL_BUBBLE_COUNT, 
                         f"Should have {INITIAL_BUBBLE_COUNT} bubbles after grace period.")
        self.assertTrue(self.scene.fizz_spawned)

if __name__ == '__main__':
    unittest.main()
