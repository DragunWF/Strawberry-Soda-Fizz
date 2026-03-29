import unittest
import pygame
import os
from modules.entities.particles import Particle

# Headless setup
os.environ['SDL_VIDEODRIVER'] = 'dummy'

class TestParticles(unittest.TestCase):
    """
    Unit tests for the particle system.
    """

    def setUp(self) -> None:
        pygame.init()
        # Initialize small surface for drawing tests (even if headless)
        pygame.display.set_mode((1, 1))

    def tearDown(self) -> None:
        pygame.quit()

    def test_particle_movement(self):
        """
        Verify that particles update their position based on velocity.
        """
        p = Particle(100, 100, 50, 50, (255, 255, 255), 1.0)
        dt = 0.5
        p.update(dt)
        # Expected new position: 100 + (50 * 0.5) = 125
        self.assertEqual(p.x, 125)
        self.assertEqual(p.y, 125)
        self.assertEqual(p.lifetime, 0.5)

    def test_particle_expiration(self):
        """
        Verify that particles correctly report their alive status.
        """
        p = Particle(100, 100, 0, 0, (255, 255, 255), 0.1)
        self.assertTrue(p.is_alive())
        p.update(0.2)
        self.assertFalse(p.is_alive())

    def test_particle_draw_no_crash(self):
        """
        Verify that particle drawing doesn't crash.
        """
        surface = pygame.Surface((200, 200))
        p = Particle(100, 100, 0, 0, (255, 255, 255), 0.5)
        try:
            p.draw(surface)
        except Exception as e:
            self.fail(f"Particle.draw raised an exception: {e}")

if __name__ == '__main__':
    unittest.main()
