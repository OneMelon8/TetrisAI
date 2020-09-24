import json
import time

import TetrisGame
import TetrisUtils
from TetrisSettings import *

# Delay between each action (seconds)
STEP_DELAY = 0.01


def get_best_actions(board, curr_tile, next_tile, offsets):
    """
    Use heuristics to obtain best possible step
      - Tiles: [curr_tile, next_tile]
      - Rotations: [rot0, rot1, rot2, rot3]
      - X coord(s): [TileX 0, ..., TileX N]
    """
    best_fitness = -9999
    best_tile_index = -1
    best_rotation = -1
    best_x = -1

    tiles = [curr_tile, next_tile]
    # 2 tiles: current and next
    for tile_index in range(len(tiles)):
        tile = tiles[tile_index]
        # Rotation: 0-3 times (4x is the same as 0x)
        for rotation_count in range(0, 4):
            # X movement
            for x in range(0, GRID_COL_COUNT - len(tile[0]) + 1):
                new_board = TetrisUtils.get_future_board_with_tile(board, tile, (x, offsets[1]), True)
                fitness = TetrisUtils.get_fitness_score(new_board)
                if fitness > best_fitness:
                    best_fitness = fitness
                    best_tile_index = tile_index
                    best_rotation = rotation_count
                    best_x = x
            # Rotate tile (prep for next iteration)
            tile = TetrisUtils.get_rotated_tile(tile)

    # Obtained best stats, now convert them into sequences of actions
    # Action = index of { NOTHING, L, R, 2L, 2R, ROTATE, SWAP, FAST_FALL, INSTA_FALL }
    actions = []
    if tiles[best_tile_index] != curr_tile:
        actions.append(ACTIONS.index("SWAP"))
    for _ in range(best_rotation):
        actions.append(ACTIONS.index("ROTATE"))
    temp_x = offsets[0]
    while temp_x != best_x:
        direction = 1 if temp_x < best_x else -1
        magnitude = 1 if abs(temp_x - best_x) == 1 else 2
        temp_x += direction * magnitude
        actions.append(ACTIONS.index(("" if magnitude == 1 else "2") + ("R" if direction == 1 else "L")))
    actions.append(ACTIONS.index("INSTA_FALL"))
    return actions


if __name__ == "__main__":
    game = TetrisGame.TetrisGame()
    while True:
        # Reset game if game over
        if not game.active:
            game.reset()
        # Game is active, take best action
        actions = get_best_actions(board=game.board, curr_tile=game.tile_shape, next_tile=TILE_SHAPES[game.get_next_tile()], offsets=(game.tile_x, game.tile_y))
        # Take the series of actions
        for action in actions:
            if STEP_DELAY > 0:
                time.sleep(STEP_DELAY)
            game.step(action, True)
