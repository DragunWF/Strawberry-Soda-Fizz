# Implementation Plan: Strawberry Soda Fizz

**Methodology:** Iterative Development via Meta-Prompting
**Goal:** Build the game module by module, ensuring SOLID principles and architectural integrity at each step before moving on to the next.

## Workflow

For each phase, the developer will request a "Meta-Prompt" from the AI (e.g., _"Generate the implementation prompt for Phase 1"_). The AI will output a highly specific, context-rich prompt that the developer can use to generate the actual Python code for those specific files.

---

### Phase 1: Core Architecture & Game Loop

**Objective:** Establish the foundation of the game without any specific gameplay logic.

- **Files to Target:** `modules/constants.py`, `modules/core/engine.py`, `modules/core/state_machine.py`.
- **Tasks:** \* Define window dimensions, colors, and framerate in constants.
  - Create the main Pygame event loop and delta time (`dt`) calculation in the Engine.
  - Implement the State Machine to handle switching between scenes.
- **Milestone:** A blank window opens, runs at 60 FPS, and gracefully closes when the 'X' is clicked.

### Phase 2: Scene Scaffolding & UI Basics

**Objective:** Implement the abstract blueprints and get the menu states working.

- **Files to Target:** `modules/scenes/base_scene.py`, `modules/scenes/main_menu.py`, `modules/scenes/game_over.py`, `modules/ui/text_button.py`.
- **Tasks:**
  - Finalize the `BaseScene` abstract class.
  - Create a basic text button class for UI interaction.
  - Build the Main Menu (with a "Start" button) and Game Over (with a "Restart" button) scenes.
- **Milestone:** The game boots to a Main Menu, clicking start goes to an empty Game Scene (placeholder), and pressing a debug key triggers the Game Over scene, which can return to the menu.

### Phase 3: The Player Controller & Physics

**Objective:** Bring the Strawberry Chunk to life inside the Game Scene.

- **Files to Target:** `modules/scenes/game_scene.py`, `modules/entities/base_entity.py`, `modules/entities/player.py`.
- **Tasks:**
  - Create the base entity blueprint.
  - Implement the Player class with gravity, horizontal movement, and the cylindrical screen-wrap mechanic.
  - Integrate the player into the `GameScene` update and draw loops.
- **Milestone:** The player can move left/right, wrap around the screen, and falls continuously off the bottom of the screen.

### Phase 4: Procedural Environment (The Fizz)

**Objective:** Implement the rising carbonation platforms.

- **Files to Target:** `modules/entities/interactables.py` (or `bubbles.py`), update `modules/scenes/game_scene.py`.
- **Tasks:**
  - Create the `Bubble` class (moves upward, varies in size and speed).
  - Implement a spawn manager in the Game Scene to generate bubbles at the bottom and destroy them at the top.
  - Implement collision detection: if the player is falling and hits the top half of a bubble, trigger the player's bounce method.
- **Milestone:** The player can successfully survive by bouncing from bubble to bubble without falling.

### Phase 5: Collectibles, Scoring, and Game Over Logic

**Objective:** Complete the core gameplay loop with objectives and failure states.

- **Files to Target:** `modules/entities/interactables.py` (for Drinks), update `modules/scenes/game_scene.py`.
- **Tasks:**
  - Create the `SodaFizzDrink` collectible (spawns at top, falls downward).
  - Implement collision between the player and collectibles.
  - Add the passive time-based score and the active collectible bonus score to the Game Scene UI.
  - Implement the failure condition: if the player falls below the screen, trigger a state change to the Game Over scene.
- **Milestone:** A fully playable game loop with a working score and fail state.

### Phase 6: Polish & Resource Management

**Objective:** Replace placeholder shapes with actual graphics and sound.

- **Files to Target:** `modules/core/resource_manager.py`, updates to all entity drawing methods.
- **Tasks:**
  - Build the Resource Manager to load and cache sprites and fonts.
  - Swap the `pygame.draw.rect/circle` calls in entities with `screen.blit()` using the cached images.
- **Milestone:** The completed, visually polished game.
