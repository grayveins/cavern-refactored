# Cavern - Menu Screen
# Title screen with "Press SPACE" prompt

from screens.base import BaseScreen
from game import Game


class MenuScreen(BaseScreen):
    """
    Title/menu screen.
    
    Shows the game title and a "Press SPACE" animation.
    Runs a background game (without player) for visual interest.
    
    Pressing SPACE transitions to PlayScreen.
    """
    
    def __init__(self, app):
        """
        Initialize the menu screen.
        
        Args:
            app: Reference to the App instance
        """
        super().__init__(app)
        # Create a background game without a player for animations
        self.game = Game(player=None)
    
    def update(self, input_state):
        """
        Update menu state.
        
        Checks for SPACE press to start game, otherwise updates
        background animations.
        
        Args:
            input_state: InputState object
        """
        if input_state.fire_pressed:
            # Start the game - transition to PlayScreen
            from screens.play import PlayScreen
            self.app.change_screen(PlayScreen(self.app))
        else:
            # Update background game for animations
            self.game.update(None)
    
    def draw(self, screen):
        """
        Draw the menu screen.
        
        Args:
            screen: Pygame Zero screen object
        """
        # Draw background game
        self.game.draw(screen)
        
        # Draw title overlay
        screen.blit("title", (0, 0))
        
        # Draw "Press SPACE" animation
        # Animation has 10 frames (0-9), stays on frame 9 for most of the time
        anim_frame = min(((self.game.timer + 40) % 160) // 4, 9)
        screen.blit("space" + str(anim_frame), (130, 280))
