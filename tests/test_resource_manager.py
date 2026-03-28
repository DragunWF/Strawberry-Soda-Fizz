import unittest
import pygame
import os
from modules.core.resource_manager import ResourceManager

# Headless setup
os.environ['SDL_VIDEODRIVER'] = 'dummy'

class TestResourceManager(unittest.TestCase):
    """
    Unit tests for the ResourceManager asset loading and caching.
    """

    def setUp(self) -> None:
        pygame.init()
        # Initialize display for surface operations
        pygame.display.set_mode((1, 1))

    def tearDown(self) -> None:
        pygame.quit()

    def test_image_fallback_logic(self):
        """
        Verify that requesting a non-existent image returns a fallback surface.
        """
        name = "non_existent_sprite.png"
        color = (123, 123, 123)
        size = (50, 50)
        
        # This should print a warning but return a surface
        surface = ResourceManager.get_image(name, color, size)
        
        self.assertIsInstance(surface, pygame.Surface)
        self.assertEqual(surface.get_size(), size)
        # Check if filled with fallback color (at top-left)
        self.assertEqual(surface.get_at((0, 0))[:3], color)

    def test_image_caching(self):
        """
        Verify that requesting the same image twice returns the same object.
        """
        name = "cache_test_sprite.png"
        color = (255, 0, 0)
        size = (30, 30)
        
        surface1 = ResourceManager.get_image(name, color, size)
        surface2 = ResourceManager.get_image(name, color, size)
        
        self.assertIs(surface1, surface2, "ResourceManager should return the cached instance.")

if __name__ == '__main__':
    unittest.main()
