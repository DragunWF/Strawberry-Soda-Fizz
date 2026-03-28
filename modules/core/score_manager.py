class ScoreManager:
    """
    Handles global score tracking for Strawberry Soda Fizz.
    Implemented with class-level attributes to allow singleton-like access.
    """
    _current_score: int = 0
    _high_score: int = 0

    @classmethod
    def add_score(cls, amount: int) -> None:
        """
        Increments the current run's score.
        """
        cls._current_score += amount

    @classmethod
    def get_score(cls) -> int:
        """
        Returns the current score.
        """
        return cls._current_score

    @classmethod
    def reset_score(cls) -> None:
        """
        Resets the current score to zero for a new game run.
        """
        # Update high score if current run was better
        if cls._current_score > cls._high_score:
            cls._high_score = cls._current_score
        cls._current_score = 0

    @classmethod
    def get_high_score(cls) -> int:
        """
        Returns the highest score achieved in the current session.
        """
        return cls._high_score
