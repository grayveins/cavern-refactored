# Cavern - Game Over Screen
# Displayed when player loses all lives

from screens.base import BaseScreen
from utils import draw_status


class GameOverScreen(BaseScreen):
    """
    Game over screen.
    
    Shows the final game state with a "GAME OVER" overlay.
    Pressing SPACE returns to the menu.
    """
    
    def __init__(self, app, game):
        """
        Initialize the game over screen.
        
        Args:
            app: Reference to the App instance
            game: Reference to the finished Game (for displaying final state)
        """
        super().__init__(app)
        self.game = game
    
    def update(self, input_state):
        """
        Update game over state.
        
        Checks for SPACE press to return to menu.
        
        Args:
            input_state: InputState object
        """
        if input_state.fire_pressed:
            # Return to menu
            from screens.menu import MenuScreen
            self.app.change_screen(MenuScreen(self.app))
    
    def draw(self, screen):
        """
        Draw the game over screen.
        
        Shows the final game state with "GAME OVER" overlay.
        
        Args:
            screen: Pygame Zero screen object
        """
        # Draw the final game state
        self.game.draw(screen)
        
        # Draw status bar (shows final score)
        draw_status(screen, self.game.player, self.game.level)
        
        # Draw "GAME OVER" overlay
        screen.blit("over", (0, 0))
