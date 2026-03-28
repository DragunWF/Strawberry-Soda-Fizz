### Project Requirements Document: Strawberry Soda Fizz

**Developer:** DragunWF  
**Genre:** Endless Jumper / Casual Arcade  
**Platform:** PC (Python/Pygame)

---

### 1. Game Overview

The player controls a rebellious Strawberry Chunk inside a glass of strawberry soda. The objective is to survive as long as possible by continually bouncing on rising carbonation bubbles to avoid sinking to the bottom of the glass. The player earns points passively over time and actively by catching falling Strawberry Soda Fizz drinks.

### 2. Core Mechanics

- **Movement:** The player can move left and right horizontally. The game features a "cylindrical" screen wrap; exiting the left side of the screen makes the player seamlessly appear on the right side, and vice versa.
- **Bouncing (Verticality):** The player automatically bounces upwards upon colliding with the top half of a rising carbonation bubble. Gravity constantly pulls the player downward.
- **Scoring System:** \* **Passive Score:** The player gains points continuously for every second they stay alive.
  - **Active Score:** Catching falling collectible drinks grants a burst of bonus points.
- **Failure Condition:** There are no enemies to kill the player. The only way to get a "Game Over" is if the player falls below the bottom edge of the screen (representing the soda going flat).

### 3. Game Entities

- **The Player (Strawberry Chunk):** The user-controlled avatar. Affected by gravity and horizontal inputs.
- **Platforms (Carbonation Bubbles):** Procedurally generated circles of varying sizes that continuously rise from the bottom of the screen to the top. They act as moving trampolines.
- **Collectibles (Soda Fizz Drinks):** Small items that spawn randomly at the top of the screen and fall downwards. They disappear when they hit the bottom edge or are collected by the player.

---

### 4. Scene Architecture

#### 4.1 Main Menu Scene

The initial screen the player sees upon launching the game.

- **Visuals:** A static or gently animating background of bubbly pink soda.
- **UI Elements:**
  - **Game Title:** Large, stylized text (e.g., "Strawberry Soda Fizz").
  - **Start Button / Prompt:** "Press SPACE to Jump In".
  - **Controls Tutorial:** Brief text explaining the left/right arrows and the screen-wrap mechanic.
- **Logic:** Waits for the player to press the designated start key, which then transitions the game state to the Game Scene.

#### 4.2 Game Scene

The active gameplay loop.

- **Visuals:** The background scrolls downward to simulate the player climbing higher up the glass.
- **UI Elements:**
  - **Score HUD:** A persistent counter in the top corner displaying the current Total Score.
- **Logic:**
  - Handles player input and physics (gravity, horizontal speed).
  - Manages the procedural generation, movement, and cleanup of Bubbles and Collectibles.
  - Calculates collisions between the Player, Bubbles, and Collectibles.
  - Updates the passive time-based score and adds bonus points upon collectible pickup.
  - Transitions to the Game Over Scene if the player's Y-coordinate exceeds the bottom screen boundary.

#### 4.3 Game Over Scene

The end-state screen after the player fails.

- **Visuals:** The game freezes, and a semi-transparent dark or red overlay is placed over the last frame of the Game Scene.
- **UI Elements:**
  - **Game Over Text:** Prominent text stating "The Soda Went Flat!"
  - **Final Score Display:** Shows the total points accumulated during the run.
  - **Restart Prompt:** "Press SPACE to Play Again".
  - **Menu Prompt:** "Press ESC to Return to Menu".
- **Logic:** Clears the previous run's variables (score, bubble positions, collectibles) and waits for input to either reload the Game Scene or load the Main Menu Scene.
