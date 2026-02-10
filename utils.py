# Cavern - Utility Functions
# Helper functions extracted from original cavern.py

from constants import (
    WIDTH, HEIGHT, NUM_ROWS, NUM_COLUMNS,
    LEVEL_X_OFFSET, GRID_BLOCK_SIZE, CHAR_WIDTH, IMAGE_WIDTH
)


def block(x, y, grid):
    """
    Check if there's a level grid block at the given coordinates.
    
    Args:
        x: X coordinate in pixels
        y: Y coordinate in pixels
        grid: The current level grid (list of strings)
    
    Returns:
        True if there's a block at this position, False otherwise
    """
    grid_x = (x - LEVEL_X_OFFSET) // GRID_BLOCK_SIZE
    grid_y = y // GRID_BLOCK_SIZE
    
    if grid_y > 0 and grid_y < NUM_ROWS:
        row = grid[grid_y]
        return (grid_x >= 0 and 
                grid_x < NUM_COLUMNS and 
                len(row) > 0 and 
                row[grid_x] != " ")
    else:
        return False


def sign(x):
    """
    Return the sign of a number.
    
    Args:
        x: A number
    
    Returns:
        -1 if x is negative, 1 otherwise
    """
    return -1 if x < 0 else 1


def char_width(char):
    """
    Return the width of a character in the game font.
    
    For letters A-Z, returns the specific width.
    For other characters (space, digits), returns the width of 'A'.
    
    Args:
        char: A single character string
    
    Returns:
        Width in pixels
    """
    index = max(0, ord(char) - 65)  # 65 is ASCII for 'A'
    if index < len(CHAR_WIDTH):
        return CHAR_WIDTH[index]
    return CHAR_WIDTH[0]


def draw_text(screen, text, y, x=None):
    """
    Draw text on screen using the game's bitmap font.
    
    Args:
        screen: Pygame Zero screen object
        text: String to draw
        y: Y coordinate
        x: X coordinate (if None, text is centered)
    """
    if x is None:
        # Center text horizontally
        total_width = sum(char_width(c) for c in text)
        x = (WIDTH - total_width) // 2
    
    for char in text:
        # Font images are named font0XX where XX is the ASCII code
        screen.blit("font0" + str(ord(char)), (x, y))
        x += char_width(char)


def draw_status(screen, player, level):
    """
    Draw the status bar showing score, level, lives, and health.
    
    Args:
        screen: Pygame Zero screen object
        player: Player object with score, lives, health attributes
        level: Current level number
    """
    # Display score, right-justified at edge of screen
    number_width = CHAR_WIDTH[0]
    score_str = str(player.score)
    draw_text(screen, score_str, 451, WIDTH - 2 - (number_width * len(score_str)))
    
    # Display level number
    draw_text(screen, "LEVEL " + str(level + 1), 451)
    
    # Display lives and health icons
    # Only display a maximum of two lives - if there are more, show a plus symbol
    lives_health = ["life"] * min(2, player.lives)
    if player.lives > 2:
        lives_health.append("plus")
    if player.lives >= 0:
        lives_health += ["health"] * player.health
    
    x = 0
    for image in lives_health:
        screen.blit(image, (x, 450))
        x += IMAGE_WIDTH[image]
