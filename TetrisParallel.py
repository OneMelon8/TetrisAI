""" This file runs multiple instances of Tetris classes in synchronization with a PyGame display """

# Imports
from time import sleep
import pygame
from Tetris import Tetris
import TetrisUtils as TUtils
from TetrisSettings import *
from TetrisAgents import *

###################
# Global Settings #
###################
# Parallel Tetris game count
ROW_COUNT = 2
COL_COUNT = 8
GAME_COUNT = ROW_COUNT * COL_COUNT

# Size of each Tetris display
GAME_WIDTH = 300
GAME_HEIGHT = GAME_WIDTH * 2
GAME_GRID_SIZE = GAME_WIDTH / GRID_COL_COUNT

# Size of padding
PADDING = 10
PADDING_STATS = 300

# Screen size (automatically calculated)
SCREEN_WIDTH = GAME_WIDTH * COL_COUNT + PADDING * (COL_COUNT + 1) + PADDING_STATS
SCREEN_HEIGHT = GAME_HEIGHT * ROW_COUNT + PADDING * (ROW_COUNT + 1)

####################
# Global Variables #
####################
# List of Tetris instances
TETRIS_GAMES = []
# List of agents
AGENTS = []


def update(screen):
    """ Called every frame by the runner, handles updates each frame """

    for a in range(GAME_COUNT):
        if TETRIS_GAMES[a].game_over:
            TETRIS_GAMES[a].reset_game()
        TETRIS_GAMES[a].step(AGENTS[a].get_action(TETRIS_GAMES[a]))

    draw(screen)
    pygame.event.get()


def draw(screen):
    """ Called by the update() function every frame, draws the PyGame GUI """
    # Background layer
    screen.fill(TUtils.get_color_tuple(COLORS.get("BACKGROUND_BLACK")))

    # Draw Tetris boards
    curr_x, curr_y = PADDING, PADDING
    for x in range(ROW_COUNT):
        for y in range(COL_COUNT):
            draw_board(screen, TETRIS_GAMES[x * COL_COUNT + y], curr_x, curr_y)
            curr_x += GAME_WIDTH + PADDING
        curr_x = PADDING
        curr_y += GAME_HEIGHT + PADDING

    # Draw statistics
    # TODO!

    # Update display
    pygame.display.update()


def draw_board(screen, tetris: Tetris, x_offset: int, y_offset: int):
    """
    Draws one Tetris board with offsets, called by draw() multiple times per frame

    :param screen: the screen to draw on
    :param tetris: Tetris instance
    :param x_offset: X offset (starting X)
    :param y_offset: Y offset (starting Y)
    """
    # [0] Striped background layer
    for a in range(GRID_COL_COUNT):
        color = TUtils.get_color_tuple(COLORS.get("BACKGROUND_DARK" if a % 2 == 0 else "BACKGROUND_LIGHT"))
        pygame.draw.rect(screen, color, (x_offset + a * GAME_GRID_SIZE, y_offset, GAME_GRID_SIZE, GAME_HEIGHT))

    # [1] Board tiles
    draw_tiles(screen, tetris.board, global_offsets=(x_offset, y_offset))
    # [1] Current tile
    draw_tiles(screen, tetris.tile_shape, offsets=(tetris.tile_x, tetris.tile_y), global_offsets=(x_offset, y_offset))


def draw_tiles(screen, matrix, offsets=(0, 0), global_offsets=(0, 0), outline_only=False):
    for y, row in enumerate(matrix):
        for x, val in enumerate(row):
            if val == 0:
                continue
            coord_x = global_offsets[0] + (offsets[0] + x) * GAME_GRID_SIZE
            coord_y = global_offsets[1] + (offsets[1] + y) * GAME_GRID_SIZE
            # Draw rectangle
            if not outline_only:
                pygame.draw.rect(screen,
                                 TUtils.get_color_tuple(COLORS.get("TILE_" + TILES[val - 1])),
                                 (coord_x, coord_y, GAME_GRID_SIZE, GAME_GRID_SIZE))
                pygame.draw.rect(screen,
                                 TUtils.get_color_tuple(COLORS.get("BACKGROUND_BLACK")),
                                 (coord_x, coord_y, GAME_GRID_SIZE, GAME_GRID_SIZE), 1)
                # Draw highlight triangle
                offset = int(GAME_GRID_SIZE / 10)
                pygame.draw.polygon(screen, TUtils.get_color_tuple(COLORS.get("TRIANGLE_GRAY")),
                                    ((coord_x + offset, coord_y + offset),
                                     (coord_x + 3 * offset, coord_y + offset),
                                     (coord_x + offset, coord_y + 3 * offset)))
            else:
                # Outline-only for prediction location
                pygame.draw.rect(screen,
                                 TUtils.get_color_tuple(COLORS.get("TILE_" + TILES[val - 1])),
                                 (coord_x + 1, coord_y + 1, GAME_GRID_SIZE - 2, GAME_GRID_SIZE - 2), 1)


if __name__ == "__main__":
    print(f"Hello world!")
    print(f">> Initializing {GAME_COUNT} Tetris games in parallel with a grid of {ROW_COUNT}×{COL_COUNT}...")

    # Initialize PyGame module
    pygame.init()
    pygame.font.init()
    display_screen = pygame.display.set_mode(size=(SCREEN_WIDTH, SCREEN_HEIGHT))
    print(f">> Screen size calculated to {SCREEN_WIDTH}×{SCREEN_HEIGHT}...")
    pygame.event.set_blocked(pygame.MOUSEMOTION)

    # Initialize Tetris modules
    for a in range(GAME_COUNT):
        TETRIS_GAMES.append(Tetris())

    # Initialize agents
    for a in range(GAME_COUNT):
        AGENTS.append(HeuristicAgent())

    while True:
        update(display_screen)
