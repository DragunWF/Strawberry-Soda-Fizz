# Polish Implementation Plan: Visuals & Audio

This document outlines the next phase of development for **Strawberry Soda Fizz**, focusing on aesthetic "juice," kinetic feedback, and the game's audio architecture.

## 1. AudioManager System

A centralized `AudioManager` class will be created to manage sound effects (SFX) with graceful fallbacks.

- **Storage**: Sounds cached via `ResourceManager`.
- **Placeholders**:
  - `bubble_pop.wav` (Triggered on bounce)
  - `pickup_fizz.wav` (Triggered on collectible catch)
  - `game_over.wav` (Triggered on player fall)
- **Fail-safe**: If a `.wav` file is missing, the system will log a warning but continue running without a crash.

## 2. Aesthetic Overhaul (Premium Pygame Graphics)

Transition from flat shapes to stylized, 3D-effect organic assets using advanced `pygame.draw` techniques.

### Bubbles

- **Rim Lighting**: A slightly darker concentric circle for a thick "soapy" edge.
- **Surface Highlights**: A small, offset white circle near the top-left to simulate light reflection.
- **Shadows**: A faint, semi-transparent black circle rendered slightly behind and below the main bubble.

### Player (Strawberry Chunk)

- **Contact Shadow**: A dynamic drop shadow that scales slightly with the player's vertical velocity.

## 3. Advanced Particle Effects

Expanding the current particle system to handle specific gameplay rewards.

- **Collectible Burst**: When the player catches a `SodaFizzDrink`, a burst of golden/yellow bubbles will explode outward.
- **Fade Logic**: Implementing exponential decay for particle transparency to make them feel "fizzy."

## 4. Visual Depth

- **Parallax Background** (Optional Consideration): Subtle movement of background "fizz" layers to create depth.
- **Dynamic Shadows**: All interactive entities will cast shadows on the pink soda background to provide a sense of space.

---

**Next Steps:**

- Complete the architectural setup for `modules/core/audio_manager.py`.
- Refactor `modules/entities/bubbles.py` for the new draw logic.
- Implement the `fizz_glow` particle effect in `modules/scenes/game_scene.py`.
