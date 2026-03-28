import unittest
import pygame
import os
from modules.entities.bubbles import Bubble

# Headless setup
os.environ['SDL_VIDEODRIVER'] = 'dummy'

class TestBubbleRecycleSync(unittest.TestCase):
    """
    Verify that updating a bubble's coordinates correctly syncs its collision rect.
    """

    def setUp(self) -> None:
        pygame.init()

    def tearDown(self) -> None:
        pygame.quit()

    def test_rect_sync_on_update(self):
        """
        Changing x/y coordinates and calling update should sync the rect.
        """
        bubble = Bubble(100, 100)
        
        # Simulate recycling: New x and y
        new_x, new_y = 300, 500
        bubble.x = new_x
        bubble.y = new_y
        
        # Update with 0 dt to trigger sync logic without movement
        bubble.update(0)
        
        # Check alignment
        self.assertEqual(bubble.rect.centerx, new_x)
        self.assertEqual(bubble.rect.centery, new_y)
        print(f"Sync Test: New X/Y: ({new_x}, {new_y}), Rect Center: {bubble.rect.center}")

if __name__ == '__main__':
    unittest.main()
