# Cavern - Refactored

A PyGame Zero Bubble Bobble clone, refactored from the original [Code the Classics](https://github.com/Wireframe-Magazine/Code-the-Classics) project.

## How to Run

### Prerequisites
- Python 3.5+
- Pygame Zero 1.2+

### Installation

```bash
# Install dependencies
pip install pygame pgzero

# Run the game
python main.py
```

## Controls

| Key | Action |
|-----|--------|
| Left/Right Arrow | Move |
| Up Arrow | Jump |
| Space | Fire bubble (hold to blow further) |
| P | Pause/Resume (during gameplay) |

## How to Test

This is a manual testing process. Run the game and verify:

- [ ] Menu screen displays with "Press SPACE" animation
- [ ] Pressing SPACE starts the game
- [ ] Player can move left/right with arrow keys
- [ ] Player can jump with up arrow
- [ ] Player can fire bubbles with SPACE
- [ ] Holding SPACE blows bubbles further
- [ ] Enemies spawn and move around
- [ ] Enemies can be trapped in bubbles
- [ ] Popping bubbles with enemies creates fruit
- [ ] Collecting fruit increases score
- [ ] Player takes damage from enemy bolts
- [ ] Game over screen appears when lives reach 0
- [ ] Pressing SPACE on game over returns to menu
- [ ] **Pause: Pressing P pauses the game**
- [ ] **Pause: "PAUSED" overlay appears**
- [ ] **Pause: Pressing P resumes the game**
- [ ] **Pause: Game state is preserved after resume**

## Architectural Changes

### Original Structure
- Single `cavern.py` file (~700 lines)
- Global `state` enum with branching in `update()` and `draw()`
- Global `space_down` variable for input edge detection
- Direct `keyboard.*` access in Player class
- Global `game` variable accessed by actors

### Refactored Structure

```
cavern/
├── main.py          # Entry point (thin delegates)
├── app.py           # App controller (owns screens)
├── game.py          # Game logic
├── actors.py        # All actor classes
├── input.py         # InputState + InputManager
├── constants.py     # Game constants
├── utils.py         # Utility functions
├── screens/
│   ├── base.py      # BaseScreen abstract class
│   ├── menu.py      # MenuScreen
│   ├── play.py      # PlayScreen (with pause)
│   └── game_over.py # GameOverScreen
├── images/          # Game sprites
├── sounds/          # Sound effects
└── music/           # Background music
```

### Key Improvements

1. **State Pattern (Task A)**: Screen objects replace global state branching
2. **Command Pattern (Task B)**: Centralized input with edge detection
3. **Pause Feature (Task C)**: P key toggles pause during gameplay
4. **Dependency Injection**: Actors receive game reference in constructor
5. **Separation of Concerns**: Each module has a single responsibility

## Project Files

| File | Purpose |
|------|---------|
| `main.py` | Pygame Zero entry point, thin delegates |
| `app.py` | Screen management, transitions |
| `game.py` | Core game logic (levels, spawning, updates) |
| `actors.py` | Player, Robot, Orb, Bolt, Fruit, Pop classes |
| `input.py` | InputState dataclass, InputManager with edge detection |
| `constants.py` | WIDTH, HEIGHT, LEVELS, etc. |
| `utils.py` | draw_text, draw_status, block, sign |

## Credits

Original game by [Wireframe Magazine](https://github.com/Wireframe-Magazine/Code-the-Classics) from the book "Code the Classics".
