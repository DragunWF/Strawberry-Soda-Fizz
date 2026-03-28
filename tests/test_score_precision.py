import unittest
import pygame
import os
from modules.core.score_manager import ScoreManager
from modules.constants import SCORE_PASSIVE_RATE

# Headless setup
os.environ['SDL_VIDEODRIVER'] = 'dummy'

class TestScorePrecision(unittest.TestCase):
    """
    Unit tests for the improved floating-point scoring and real-time high score updates.
    """

    def setUp(self) -> None:
        pygame.init()
        ScoreManager.reset_score()
        # Reset high score for clean test
        ScoreManager._high_score = 0.0

    def tearDown(self) -> None:
        pygame.quit()

    def test_passive_score_precision_over_time(self):
        """
        Verify that small frame-by-frame increments accumulate correctly over 1 second.
        """
        fps = 60
        dt = 1.0 / fps
        
        # Simulate 1 second of survival
        for _ in range(fps):
            ScoreManager.add_score(SCORE_PASSIVE_RATE * dt)
            
        # Should be exactly (or very near) SCORE_PASSIVE_RATE
        # Using 9 as a safe bound for rounding/float precision in this simple test
        self.assertGreaterEqual(ScoreManager.get_score(), int(SCORE_PASSIVE_RATE) - 1)
        self.assertLessEqual(ScoreManager.get_score(), int(SCORE_PASSIVE_RATE) + 1)

    def test_real_time_high_score_update(self):
        """
        Verify that the high score updates immediately when the current score exceeds it.
        """
        ScoreManager.add_score(100.0)
        self.assertEqual(ScoreManager.get_high_score(), 100)
        
        ScoreManager.add_score(50.0)
        self.assertEqual(ScoreManager.get_high_score(), 150)
        
        # Verify it doesn't drop
        ScoreManager.reset_score()
        self.assertEqual(ScoreManager.get_high_score(), 150)
        self.assertEqual(ScoreManager.get_score(), 0)

if __name__ == '__main__':
    unittest.main()
