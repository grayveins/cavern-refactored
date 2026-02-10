# Cavern - Play Screen
# Main gameplay screen with pause functionality

import pygame

from screens.base import BaseScreen
from game import Game
from actors import Player
from utils import draw_status, draw_text
from constants import WIDTH, HEIGHT


class PlayScreen(BaseScreen):
    """
    Main gameplay screen.
    
    Owns the Game and Player instances. Handles:
    - Normal gameplay updates
    - Pause toggling with P key
    - Transition to GameOverScreen when player dies
    
    Game and Player are created HERE, not in global scope.
    """
    
    def __init__(self, app):
        """
        Initialize the play screen.
        
        Creates a new Game with a new Player.
        
        Args:
            app: Reference to the App instance
        """
        super().__init__(app)
        
        # Create player first (game reference set after)
        self.player = Player(game=None)
        
        # Create game with the player
        self.game = Game(player=self.player)
        
        # Set the game reference on the player (back-reference)
        self.player.game = self.game
        
        # Initialize player state
        self.player.reset()
        
        # Pause state
        self.paused = False
    
    def update(self, input_state):
        """
        Update gameplay state.
        
        Handles pause toggling and game updates.
        
        Args:
            input_state: InputState object
        """
        # Toggle pause on P key
        if input_state.pause_pressed:
            self.paused = not self.paused
        
        # Don't update game while paused
        if self.paused:
            return
        
        # Check for game over
        if self.game.player.lives < 0:
            self.game.play_sound("over")
            from screens.game_over import GameOverScreen
            self.app.change_screen(GameOverScreen(self.app, self.game))
            return
        
        # Normal game update
        self.game.update(input_state)
    
    def draw(self, screen):
        """
        Draw the gameplay screen.
        
        Draws game state, status bar, and pause overlay if paused.
        
        Args:
            screen: Pygame Zero screen object
        """
        # Draw the game
        self.game.draw(screen)
        
        # Draw status bar (score, level, lives, health)
        draw_status(screen, self.game.player, self.game.level)
        
        # Draw pause overlay if paused
        if self.paused:
            self._draw_pause_overlay(screen)
    
    def _draw_pause_overlay(self, screen):
        """
        Draw a semi-transparent pause overlay.
        
        Shows "PAUSED" text centered on screen.
        
        Args:
            screen: Pygame Zero screen object
        """
        # Create semi-transparent overlay
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 128))  # Black with 50% transparency
        screen.surface.blit(overlay, (0, 0))
        
        # Draw "PAUSED" text centered
        draw_text(screen, "PAUSED", HEIGHT // 2 - 20)
