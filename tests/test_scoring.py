import unittest
import pygame
import os
from modules.core.score_manager import ScoreManager
from modules.entities.collectibles import SodaFizzDrink
from modules.entities.player import Player

# Headless setup
os.environ['SDL_VIDEODRIVER'] = 'dummy'

class TestScoring(unittest.TestCase):
    """
    Unit tests for the ScoreManager and collectible collision logic.
    """

    def setUp(self) -> None:
        pygame.init()
        ScoreManager.reset_score()

    def tearDown(self) -> None:
        pygame.quit()

    def test_passive_score_accumulation(self):
        """
        Verify score increases passively over simulated time.
        """
        initial_score = ScoreManager.get_score()
        dt = 1.0 # 1 second
        # Simulate the logic from GameScene: 10 * dt
        ScoreManager.add_score(int(10 * dt))
        self.assertEqual(ScoreManager.get_score(), initial_score + 10)

    def test_collectible_collision_score(self):
        """
        Verify score increases by 500 when player collects a drink.
        """
        initial_score = ScoreManager.get_score()
        player = Player(100, 100)
        drink = SodaFizzDrink(100, 100) # Overlapping
        
        # Simulate collision check logic from GameScene
        if player.rect.colliderect(drink.rect):
            ScoreManager.add_score(500)
            
        self.assertEqual(ScoreManager.get_score(), initial_score + 500)

    def test_score_reset(self):
        """
        Verify score resets correctly for a new run.
        """
        ScoreManager.add_score(1000)
        self.assertEqual(ScoreManager.get_score(), 1000)
        
        ScoreManager.reset_score()
        self.assertEqual(ScoreManager.get_score(), 0)
        self.assertEqual(ScoreManager.get_high_score(), 1000)

if __name__ == '__main__':
    unittest.main()
