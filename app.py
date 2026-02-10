# Cavern - Application Controller
# Manages screen transitions and delegates update/draw

class App:
    """
    Main application controller.
    
    Implements the State pattern by owning the current screen
    and delegating update() and draw() calls to it.
    
    Screen transitions are handled via change_screen().
    """
    
    def __init__(self):
        """Initialize the app with no current screen."""
        self.current_screen = None
    
    def change_screen(self, screen):
        """
        Switch to a new screen.
        
        This is the single point for all screen transitions.
        
        Args:
            screen: The new screen to display (BaseScreen subclass)
        """
        self.current_screen = screen
    
    def update(self, input_state):
        """
        Update the current screen.
        
        Thin delegate - just passes the call to the current screen.
        
        Args:
            input_state: InputState object with current input
        """
        if self.current_screen:
            self.current_screen.update(input_state)
    
    def draw(self, screen):
        """
        Draw the current screen.
        
        Thin delegate - just passes the call to the current screen.
        
        Args:
            screen: Pygame Zero screen object
        """
        if self.current_screen:
            self.current_screen.draw(screen)
