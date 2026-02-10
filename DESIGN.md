# Design Document

## Screens Architecture

The game uses the **State Pattern** to manage different screens:

```
App
 └── current_screen
      ├── MenuScreen      # Title with "Press SPACE"
      ├── PlayScreen      # Main gameplay + pause
      └── GameOverScreen  # Final score display
```

### Screen Transitions

| From | To | Trigger |
|------|-----|---------|
| MenuScreen | PlayScreen | `fire_pressed` (SPACE) |
| PlayScreen | GameOverScreen | `player.lives < 0` |
| GameOverScreen | MenuScreen | `fire_pressed` (SPACE) |

### Key Design Decisions

- **Game creation in screens**: Each PlayScreen creates its own Game/Player
- **Single transition method**: `app.change_screen(new_screen)`
- **No global state variable**: Replaced with polymorphic screen objects

## Input Design

The **Command Pattern** centralizes all input handling:

```python
@dataclass
class InputState:
    left: bool          # Level (held)
    right: bool         # Level (held)
    up: bool            # Level (held)
    jump_pressed: bool  # Edge (just pressed)
    fire_pressed: bool  # Edge (just pressed)
    fire_held: bool     # Level (held)
    pause_pressed: bool # Edge (just pressed)
```

### Edge Detection

Edge detection distinguishes "just pressed" from "being held":

```
pressed = current AND NOT previous
```

This ensures:
- Menu starts only on fresh SPACE press
- Orbs fire only once per SPACE press
- Pause toggles only once per P press

### Input Flow

```
keyboard → InputManager.capture() → InputState → Screen.update()
```

## Pause Implementation

Pause is internal to `PlayScreen`:

```python
class PlayScreen:
    def __init__(self):
        self.paused = False
    
    def update(self, input_state):
        if input_state.pause_pressed:
            self.paused = not self.paused
        
        if self.paused:
            return  # Skip game update
        
        self.game.update(input_state)
    
    def draw(self, screen):
        self.game.draw(screen)
        if self.paused:
            self._draw_pause_overlay(screen)
```

### Why Internal Flag vs Separate Screen

- Simpler: No need to preserve/restore game state
- Faster: Avoids screen transition overhead
- Intuitive: Pause is a mode within gameplay, not a separate state
