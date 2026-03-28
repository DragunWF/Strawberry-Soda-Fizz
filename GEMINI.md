# Strawberry Soda Fizz 🍓🥤

**Developer:** DragunWF  
**Tech Stack:** Python / Pygame (Powered by Google Antigravity)  
**Genre:** Endless Jumper / Casual Arcade

---

## Project Context

_Strawberry Soda Fizz_ is a bite-sized, kinetic arcade game where players control a rebellious Strawberry Chunk trapped inside a tall glass of freshly poured soda. The objective is to continuously ride rising carbonation bubbles to the top of the glass before the drink goes flat.

Designed with scalability in mind, the project utilizes a strict, SOLID-compliant Object-Oriented architecture. By leveraging an event-driven state machine and abstracted entity blueprints, the codebase remains modular, testable, and completely open for future feature expansions (like new flavor biomes or crazy straw hazards).

## Core Features

- **Carbonation Physics:** Fluid vertical platforming mechanics that rely on bouncing off procedurally generated, rising bubbles.
- **Cylindrical Screen Wrap:** Continuous horizontal movement where exiting one side of the screen seamlessly teleports the player to the opposite side.
- **Dual-Layered Scoring:** Players earn points passively by surviving the rising fizz, and actively by catching falling Soda Fizz drink collectibles.
- **Modular Scene Management:** A decoupled `StateMachine` that handles transitions between the Main Menu, Game Scene, and Game Over states without cluttering the main game loop.

## Architecture & Directory Structure

The project directory separates core engine logic from game-specific entities and static assets, ensuring a clean and manageable workspace.

```text
strawberry_soda_project/
├── assets/
│   ├── audio/
│   ├── fonts/
│   ├── sprites/
├── docs/
├── prototypes/
├── utils/
│   └── math_helpers.py
├── modules/
│   ├── core/
│   │   ├── engine.py
│   │   ├── state_machine.py
│   │   └── resource_manager.py
│   ├── scenes/
│   │   ├── base_scene.py
│   │   ├── main_menu.py
│   │   ├── game_scene.py
│   │   └── game_over.py
│   ├── entities/
│   │   ├── base_entity.py
│   │   ├── player.py
│   │   └── interactables.py
│   ├── ui/
│   │   ├── base_widget.py
│   │   └── text_button.py
│   └── constants.py
├── main.py
├── GEMINI.md
└── requirements.txt
```
