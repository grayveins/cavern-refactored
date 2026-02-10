#!/usr/bin/env python3
"""
Cavern - A PyGame Zero Bubble Bobble Clone

Refactored version with:
- Screen-based state management (State Pattern)
- Centralized input handling with edge detection (Command Pattern)
- Pause functionality

Run with: python main.py
"""

import sys
import pygame
import pgzero
import pgzrun

# Version checks from original
if sys.version_info < (3, 5):
    print("This game requires at least version 3.5 of Python.")
    print("Please download it from www.python.org")
    sys.exit()

pgzero_version = [int(s) if s.isnumeric() else s for s in pgzero.__version__.split('.')]
if pgzero_version < [1, 2]:
    print(f"This game requires at least version 1.2 of Pygame Zero.")
    print(f"You have version {pgzero.__version__}.")
    print("Please upgrade using: pip3 install --upgrade pgzero")
    sys.exit()

# Import our modules
from app import App
from input import InputManager
from screens.menu import MenuScreen

# Pygame Zero required globals
WIDTH = 800
HEIGHT = 480
TITLE = "Cavern"

# Application state
app = App()
input_manager = InputManager()


def init():
    """Initialize the game on startup."""
    # Setup audio
    try:
        pygame.mixer.quit()
        pygame.mixer.init(44100, -16, 2, 1024)
        music.play("theme")
        music.set_volume(0.3)
    except Exception as e:
        # If audio fails, continue without it
        print(f"Audio initialization warning: {e}")
    
    # Start at the menu screen
    app.change_screen(MenuScreen(app))


# Pygame Zero hook - called every frame
def update():
    """
    Main update function (Pygame Zero hook).
    
    Thin delegate: captures input and passes to app.
    """
    input_state = input_manager.capture(keyboard)
    app.update(input_state)


# Pygame Zero hook - called every frame after update
def draw():
    """
    Main draw function (Pygame Zero hook).
    
    Thin delegate: passes screen to app.
    """
    app.draw(screen)


# Initialize and run
init()
pgzrun.go()
