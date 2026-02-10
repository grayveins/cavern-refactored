# Cavern - Constants
# Extracted from original cavern.py for better organization

# Window settings
WIDTH = 800
HEIGHT = 480
TITLE = "Cavern"

# Grid settings
NUM_ROWS = 18
NUM_COLUMNS = 28
LEVEL_X_OFFSET = 50
GRID_BLOCK_SIZE = 25

# Actor anchors
ANCHOR_CENTRE = ("center", "center")
ANCHOR_CENTRE_BOTTOM = ("center", "bottom")

# Level layouts - X marks blocks, spaces are empty
LEVELS = [
    ["XXXXX     XXXXXXXX     XXXXX",
     "", "", "", "",
     "   XXXXXXX        XXXXXXX   ",
     "", "", "",
     "   XXXXXXXXXXXXXXXXXXXXXX   ",
     "", "", "",
     "XXXXXXXXX          XXXXXXXXX",
     "", "", ""],

    ["XXXX    XXXXXXXXXXXX    XXXX",
     "", "", "", "",
     "    XXXXXXXXXXXXXXXXXXXX    ",
     "", "", "",
     "XXXXXX                XXXXXX",
     "      X              X      ",
     "       X            X       ",
     "        X          X        ",
     "         X        X         ",
     "", "", ""],

    ["XXXX    XXXX    XXXX    XXXX",
     "", "", "", "",
     "  XXXXXXXX        XXXXXXXX  ",
     "", "", "",
     "XXXX      XXXXXXXX      XXXX",
     "", "", "",
     "    XXXXXX        XXXXXX    ",
     "", "", ""]
]

# Font character widths (A-Z)
CHAR_WIDTH = [27, 26, 25, 26, 25, 25, 26, 25, 12, 26, 26, 25, 33, 25, 26,
              25, 27, 26, 26, 25, 26, 26, 38, 25, 25, 25]

# Status bar image widths
IMAGE_WIDTH = {"life": 44, "plus": 40, "health": 40}
