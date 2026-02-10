# Cavern - Base Screen
# Abstract base class for all screen states

from abc import ABC, abstractmethod


class BaseScreen(ABC):
    """
    Abstract base class for all game screens.
    
    Implements the State pattern - each screen handles its own
    update and draw logic, and the App delegates to the current screen.
    
    Screens can trigger transitions by calling app.change_screen().
    """
    
    def __init__(self, app):
        """
        Initialize the screen.
        
        Args:
            app: Reference to the App instance for screen transitions
        """
        self.app = app
    
    @abstractmethod
    def update(self, input_state):
        """
        Update the screen state.
        
        Args:
            input_state: InputState object with current input
        """
        pass
    
    @abstractmethod
    def draw(self, screen):
        """
        Draw the screen.
        
        Args:
            screen: Pygame Zero screen object
        """
        pass
