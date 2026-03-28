import unittest
import pygame
import os
from modules.scenes.game_scene import GameScene
from modules.constants import GRACE_DURATION, INITIAL_BUBBLE_COUNT, PLAYER_START_X, PLAYER_START_Y

# Headless setup
os.environ['SDL_VIDEODRIVER'] = 'dummy'

class TestGameplayTuning(unittest.TestCase):
    """
    Unit tests for the new gameplay tuning, grace period, and starting platforms.
    """

    def setUp(self) -> None:
        pygame.init()
        pygame.display.set_mode((1, 1))
        self.scene = GameScene()

    def tearDown(self) -> None:
        pygame.quit()

    def test_grace_period_initialization(self):
        """
        Verify that grace_timer is initialized to the correct duration.
        """
        self.scene.enter()
        self.assertEqual(self.scene.grace_timer, GRACE_DURATION)

    def test_starting_bubble_exists(self):
        """
        Verify that a bubble is placed directly beneath the player's spawn point.
        """
        self.scene.enter()
        # Find if any bubble is within reasonable range of (PLAYER_START_X + 15, PLAYER_START_Y + 60)
        start_x, start_y = PLAYER_START_X + 15, PLAYER_START_Y + 60
        found = False
        for bubble in self.scene.bubbles:
            if abs(bubble.x - start_x) < 5 and abs(bubble.y - start_y) < 5:
                found = True
                break
        self.assertTrue(found, "Starting bubble not found under spawn point.")

    def test_bubble_count(self):
        """
        Verify bubble density matches the new INITIAL_BUBBLE_COUNT constant.
        """
        self.scene.enter()
        self.assertEqual(len(self.scene.bubbles), INITIAL_BUBBLE_COUNT)

    def test_grace_period_skips_gravity(self):
        """
        Verify that player's y-position doesn't change during grace period.
        """
        self.scene.enter()
        initial_y = self.scene.player.y
        # Simulate update with some dt (less than grace duration)
        self.scene.update(0.5)
        self.assertEqual(self.scene.player.y, initial_y, "Player should not move vertically during grace period.")

if __name__ == '__main__':
    unittest.main()
