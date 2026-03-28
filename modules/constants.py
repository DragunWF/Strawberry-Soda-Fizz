"""
Global constants for Strawberry Soda Fizz.
"""

# Window settings
WINDOW_WIDTH = 400
WINDOW_HEIGHT = 600
FPS = 60
TITLE = "Strawberry Soda Fizz"

# Colors (RGB)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BG_COLOR = (255, 182, 193)  # Light Pink
RED = (255, 0, 0)           # Strawberry Chunk

# Physics constants
GRAVITY = 1200.0            # Pixels per second squared
PLAYER_SPEED = 300.0        # Horizontal pixels per second
BOUNCE_POWER = -600.0       # Vertical velocity on jump/bounce

# --- Gameplay Tuning ---
# Edit these to change the difficulty and feel of the game!
GRACE_DURATION = 2.0        # Seconds of "no-gravity" at the start
INITIAL_BUBBLE_COUNT = 6   # Number of bubbles in the screen at once
PLAYER_START_X = WINDOW_WIDTH // 2 - 15
PLAYER_START_Y = 100
