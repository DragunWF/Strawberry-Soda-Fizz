# Strawberry Soda Fizz 🍓🥤

**Developer:** DragunWF  
**Tech Stack:** Python 3 / Pygame (Google Antigravity)  
**Genre:** Endless Jumper / Casual Arcade

## 📖 Game Context

_Strawberry Soda Fizz_ is a bite-sized, kinetic arcade game where you play as a rebellious Strawberry Chunk trapped inside a freshly poured glass of soda. Your goal is to survive as long as possible by continuously bouncing on rising carbonation bubbles before the drink goes flat.

Designed with a strict, SOLID-compliant Object-Oriented architecture, the game features a seamless cylindrical screen-wrap mechanic, fluid jumping physics, and a dual-layered scoring system (survive to earn passive points, and catch falling _Soda Fizz Drinks_ for massive bonuses).

## ✨ Key Features

- **Procedural Fizz Physics:** Bounce off dynamically generated carbonation platforms that rise from the bottom of the glass.
- **Cylindrical Screen Wrap:** Exiting the left side of the screen seamlessly teleports your character to the right side, keeping the action fast and continuous.
- **Modular Architecture:** Built using an event-driven state machine and abstracted entity blueprints housed entirely within the `modules/` directory.

---

## 🚀 Setup & Installation

This project uses `pipenv` to manage its virtual environment and dependencies cleanly.

### Prerequisites

- Python 3.8+ installed on your system.
- `pipenv` installed globally (`pip install pipenv`).

### 1. Clone the Repository

Navigate to your desired workspace and clone the project:

```bash
git clone [https://github.com/yourusername/strawberry-soda-fizz.git](https://github.com/yourusername/strawberry-soda-fizz.git)
cd strawberry-soda-fizz
```

### 2. Initialize the Virtual Environment

Use `pipenv` to create the environment and install Pygame.

```bash
pipenv install pygame
```

### 3. Activate the Shell

Enter the isolated virtual environment

```bash
pipenv shell
```

### 4. Run the Game

Activate the virtual environment and run the main entry point.

```bash
pipenv run python main.py
```

## 🎮 Controls

- Left Arrow: Move Left
- Right Arrow: Move Right
- Spacebar / Mouse Click: Interact with menus
