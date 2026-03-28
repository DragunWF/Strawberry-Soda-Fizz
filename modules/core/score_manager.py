class ScoreManager:
    """
    Handles global score tracking for Strawberry Soda Fizz.
    Uses floating-point precision for smooth accumulation of points.
    """
    _current_score: float = 0.0
    _high_score: float = 0.0

    @classmethod
    def add_score(cls, amount: float) -> None:
        """
        Increments the current run's score and updates high score instantly.
        """
        cls._current_score += amount
        if cls._current_score > cls._high_score:
            cls._high_score = cls._current_score

    @classmethod
    def get_score(cls) -> int:
        """
        Returns the current score rounded to the nearest integer.
        """
        return int(round(cls._current_score))

    @classmethod
    def reset_score(cls) -> None:
        """
        Resets the current score to zero for a new game run.
        The high score is preserved.
        """
        cls._current_score = 0.0

    @classmethod
    def get_high_score(cls) -> int:
        """
        Returns the highest score achieved in the current session.
        """
        return int(round(cls._high_score))
