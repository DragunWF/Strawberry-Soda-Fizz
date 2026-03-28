import unittest
import pygame
import os
from modules.entities.bubbles import Bubble

# Headless setup to ensure tests run in any environment
os.environ['SDL_VIDEODRIVER'] = 'dummy'

class TestBubblePhysics(unittest.TestCase):
    """
    Unit tests for the Bubble entity's core logic and physics.
    """

    def setUp(self) -> None:
        """
        Initializes Pygame for headless operations.
        """
        pygame.init()

    def tearDown(self) -> None:
        """
        Cleans up Pygame state.
        """
        pygame.quit()

    def test_bubble_initialization(self):
        """
        Verify that giving a bubble an X/Y coordinate correctly sets its center.
        """
        x, y = 100, 200
        bubble = Bubble(x, y)
        
        # Check if the collision rect correctly encapsulates the bubble
        self.assertEqual(bubble.x, x)
        self.assertEqual(bubble.y, y)
        self.assertEqual(bubble.rect.centerx, int(x))
        self.assertEqual(bubble.rect.centery, int(y))

    def test_bubble_moves_upward(self):
        """
        Verify that a bubble's Y coordinate decreases over time.
        """
        x, y = 100, 500
        bubble = Bubble(x, y)
        initial_y = bubble.y
        
        # Simulate 1 second of movement
        dt = 1.0
        bubble.update(dt)
        
        # In Pygame, Y decreases as objects move UP
        self.assertLess(bubble.y, initial_y, "Bubble should move upward (decreasing Y).")
        self.assertLess(bubble.rect.y, initial_y - bubble.radius, "Rect should follow the bubble position.")

if __name__ == '__main__':
    unittest.main()
