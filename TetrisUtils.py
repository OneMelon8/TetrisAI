# Util function for the TetrisGame.py

from copy import deepcopy
from TetrisSettings import *


###########################
# Board Helper Algorithms #
###########################
def check_collision(board, tile_shape, offsets):
    for cy, row in enumerate(tile_shape):
        for cx, val in enumerate(row):
            if val == 0:
                continue
            try:
                if board[cy + offsets[1]][cx + offsets[0]]:
                    return True
            except IndexError:
                return True
    return False


def get_effective_height(board, tile, offsets):
    offset_x, offset_y = offsets
    while not check_collision(board, tile, (offset_x, offset_y)):
        offset_y += 1
    return offset_y - 1


def get_board_with_tile(board, tile, offsets, flattened=False):
    # Make a copy
    board = deepcopy(board)
    # If flatten, change all numbers to 0/1
    if flattened:
        board = [[int(bool(val)) for val in row] for row in board]
    # Add current tile (do not flatten)
    for y, row in enumerate(tile):
        for x, val in enumerate(row):
            if val != 0:
                board[y + offsets[1]][x + offsets[0]] = val
    return board


def get_future_board_with_tile(board, tile, offsets, flattened=False):
    return get_board_with_tile(board, tile, (offsets[0], get_effective_height(board, tile, offsets)), flattened)


################
# Misc Helpers #
################
def print_board(board):
    print("Printing debug board")
    for i, row in enumerate(board):
        print("{:02d}".format(i), row)


def get_rotated_tile(tile):
    return list(zip(*reversed(tile)))


def get_color_tuple(color_hex):
    if color_hex is None:
        color_hex = "11c5bf"
    color_hex = color_hex.replace("#", "")
    return tuple(int(color_hex[i:i + 2], 16) for i in (0, 2, 4))


###########################
# Lee's Fitness Algorithm #
###########################
# Reference to https://codemyroad.wordpress.com/2013/04/14/tetris-ai-the-near-perfect-player/
def get_fitness_score(board):
    board, score_count = get_board_and_lines_cleared(board)
    score = WEIGHT_LINE_CLEARED * score_count
    score += WEIGHT_AGGREGATE_HEIGHT * sum(get_col_heights(board))
    score += WEIGHT_HOLES * get_hole_count(board)
    score += WEIGHT_BUMPINESS * get_bumpiness(board)
    return score


# Get height of each column
def get_col_heights(board):
    heights = [0] * GRID_COL_COUNT
    cols = list(range(GRID_COL_COUNT))
    for neg_height, row in enumerate(board):
        for i, val in enumerate(row):
            if val == 0 or i not in cols:
                continue
            heights[i] = GRID_ROW_COUNT - neg_height
            cols.remove(i)
    return heights


# Count of empty spaces below covers
def get_hole_count(board):
    holes = 0
    cols = [0] * GRID_COL_COUNT
    for neg_height, row in enumerate(board):
        height = GRID_ROW_COUNT - neg_height
        for i, val in enumerate(row):
            if val == 0 and cols[i] > height:
                holes += 1
                continue
            if val != 0 and cols[i] == 0:
                cols[i] = height
    return holes


# Get the unevenness of the board
def get_bumpiness(board):
    bumpiness = 0
    heights = get_col_heights(board)
    for i in range(1, GRID_COL_COUNT):
        bumpiness += abs(heights[i - 1] - heights[i])
    return bumpiness


# Get potential lines cleared
# WARNING: MODIFIES BOARD!!!
def get_board_and_lines_cleared(board):
    score_count = 0
    row = 0
    while True:
        if row >= len(board):
            break
        if 0 in board[row]:
            row += 1
            continue
        # Delete the "filled" row
        del board[row]
        # Insert empty row at top
        board.insert(0, [0] * GRID_COL_COUNT)
        score_count += 1
    return board, score_count
