# Cavern - Input System
# Centralized input handling with edge detection (Command Pattern)

from dataclasses import dataclass


@dataclass
class InputState:
    """
    Snapshot of input state for a single frame.
    
    Contains both level (held) and edge (just pressed) input states.
    This replaces direct keyboard access throughout the codebase.
    
    Attributes:
        left: True if left arrow is held
        right: True if right arrow is held
        up: True if up arrow is held
        jump_pressed: True only on the frame up was first pressed (edge)
        fire_pressed: True only on the frame space was first pressed (edge)
        fire_held: True while space is held (level)
        pause_pressed: True only on the frame P was first pressed (edge)
    """
    left: bool = False
    right: bool = False
    up: bool = False
    jump_pressed: bool = False
    fire_pressed: bool = False
    fire_held: bool = False
    pause_pressed: bool = False


class InputManager:
    """
    Manages input state capture with edge detection.
    
    Edge detection allows distinguishing between a key being held
    and a key being newly pressed this frame. This is essential for
    actions that should only trigger once per keypress (like firing).
    
    Usage:
        input_manager = InputManager()
        
        # In update loop:
        input_state = input_manager.capture(keyboard)
        game.update(input_state)
    """
    
    def __init__(self):
        """Initialize with all previous states as False."""
        self._prev_space = False
        self._prev_up = False
        self._prev_pause = False
    
    def capture(self, keyboard) -> InputState:
        """
        Capture the current keyboard state and compute edge detection.
        
        Args:
            keyboard: Pygame Zero keyboard object
        
        Returns:
            InputState with current level and edge states
        """
        # Read current key states
        curr_space = keyboard.space
        curr_up = keyboard.up
        curr_pause = keyboard.p
        
        # Build input state with edge detection
        # Edge = current AND NOT previous (just pressed this frame)
        state = InputState(
            left=keyboard.left,
            right=keyboard.right,
            up=curr_up,
            jump_pressed=curr_up and not self._prev_up,
            fire_pressed=curr_space and not self._prev_space,
            fire_held=curr_space,
            pause_pressed=curr_pause and not self._prev_pause
        )
        
        # Store current state for next frame's edge detection
        self._prev_space = curr_space
        self._prev_up = curr_up
        self._prev_pause = curr_pause
        
        return state
