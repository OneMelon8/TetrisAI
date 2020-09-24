# Settings for the TetrisGame.py

# Configurations (USER)
SIZE_SCALE = 1
SPEED_DEFAULT = 750  # 750 MS
SPEED_SCALE_ENABLED = True  # game gets faster with more points?
SPEED_SCALE = 0.05  # speed = max(50, 750 - SCORE * SPEED_SCALE)
DISPLAY_PREDICTION = True
HAS_DISPLAY = True
MIN_DEBUG_LEVEL = 10

FONT_NAME = "Consolas"

COLORS = {
    # Display
    "BACKGROUND_BLACK": "000000",
    "BACKGROUND_DARK": "021c2d",
    "BACKGROUND_LIGHT": "00263f",
    "TRIANGLE_GRAY": "efe6ff",
    "WHITE": "ffffff",
    # Tetris pieces
    "TILE_LINE": "ffb900",
    "TILE_L": "2753f1",
    "TILE_L_REVERSED": "f7ff00",
    "TILE_S": "ff6728",
    "TILE_S_REVERSED": "11c5bf",
    "TILE_T": "ae81ff",
    "TILE_CUBE": "e94659",
}

MESSAGES = {
    # Display
    "TITLE": "Tetris",
    "CONTROLS": "Left/Right - Move tile\nUp - Rotate tile\nDown - Fast drop\nSpace - Insta-drop\nEscape - Play/Pause\nTab - Swap next tile",
    "HIGH_SCORE": "H.Score: {:.2f} (x{})",
    "SCORE": "Score: {:.2f} (x{})",
    "FITNESS": "Fitness: {:.2f}",
    "SPEED": "Speed: {}ms",
    "NEXT_TILE": "Next tile: {}",
}

# Configurations (SYSTEM)
GRID_ROW_COUNT = 20
GRID_COL_COUNT = 10

SCREEN_RATIO = 0.55
SCREEN_WIDTH = int(360 / SCREEN_RATIO * SIZE_SCALE)
SCREEN_HEIGHT = int(720 * SIZE_SCALE)
MAX_FPS = 30

########################
# Score Configurations #
########################
MULTI_SCORE_ALGORITHM = lambda lines_cleared: 5 ** lines_cleared
PER_STEP_SCORE_GAIN = 0.0

# Fitness function configuration
# https://luckytoilet.wordpress.com/2011/05/27/coding-a-tetris-ai-using-a-genetic-algorithm/
# https://codemyroad.wordpress.com/2013/04/14/tetris-ai-the-near-perfect-player/
WEIGHT_AGGREGATE_HEIGHT = -0.03
WEIGHT_HOLES = -7.5
WEIGHT_BUMPINESS = -0.1845
WEIGHT_LINE_CLEARED = 8

######################
# STEP Configuration #
######################
ALWAYS_DRAW = True
STEP_ACTION = True

ACTIONS = ["NOTHING", "L", "R", "2L", "2R", "ROTATE", "SWAP", "FAST_FALL", "INSTA_FALL"]

TILES = ["LINE", "L", "L_REVERSED", "S", "S_REVERSED", "T", "CUBE"]
TILE_SHAPES = {
    "LINE": [[1, 1, 1, 1]],
    "L": [[0, 0, 2],
          [2, 2, 2]],
    "L_REVERSED": [[3, 0, 0],
                   [3, 3, 3]],
    "S": [[0, 4, 4],
          [4, 4, 0]],
    "S_REVERSED": [[5, 5, 0],
                   [0, 5, 5]],
    "T": [[6, 6, 6],
          [0, 6, 0]],
    "CUBE": [[7, 7],
             [7, 7]]
}
