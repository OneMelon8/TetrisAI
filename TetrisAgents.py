# Imports
import random
from typing import *
from Tetris import Tetris
import TetrisUtils as TUtils
from TetrisSettings import *


class BaseAgent:
    """ The framework of an agent class, all agents should inherit this class """

    def __init__(self):
        self.action_queue = []

    def get_action(self, tetris: Tetris) -> int:
        if len(self.action_queue) == 0:
            self.action_queue = self.calculate_actions(tetris.board, tetris.tile_shape, TILE_SHAPES[tetris.get_next_tile()], (tetris.tile_x, tetris.tile_y))
        return self.action_queue.pop(0)

    def calculate_actions(self, board, current_tile, next_tile, offsets) -> List[int]:
        """
        Get best actions from the current board and tile situation

        :param board: Tetris board matrix (2D list)
        :param current_tile: current tile shape (2D list)
        :param next_tile: next tile shape (2D list)
        :param offsets: x, y offsets of the current tile (int, int)
        :return: list of actions to take, actions will be executed in order
        """


class RandomAgent(BaseAgent):
    """ Agent that randomly picks actions """

    def calculate_actions(self, board, current_tile, next_tile, offsets):
        return [random.randint(0, 8) for _ in range(10)]


class HeuristicAgent(BaseAgent):
    """ Agent that uses heuristic to calculate the best action """

    def calculate_actions(self, board, current_tile, next_tile, offsets):
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

        tiles = [current_tile, next_tile]
        # 2 tiles: current and next
        for tile_index in range(len(tiles)):
            tile = tiles[tile_index]
            # Rotation: 0-3 times (4x is the same as 0x)
            for rotation_count in range(0, 4):
                # X movement
                for x in range(0, GRID_COL_COUNT - len(tile[0]) + 1):
                    new_board = TUtils.get_future_board_with_tile(board, tile, (x, offsets[1]), True)
                    fitness = TUtils.get_fitness_score(new_board)
                    if fitness > best_fitness:
                        best_fitness = fitness
                        best_tile_index = tile_index
                        best_rotation = rotation_count
                        best_x = x
                # Rotate tile (prep for next iteration)
                tile = TUtils.get_rotated_tile(tile)

        # Obtained best stats, now convert them into sequences of actions
        # Action = index of { NOTHING, L, R, 2L, 2R, ROTATE, SWAP, FAST_FALL, INSTA_FALL }
        actions = []
        if tiles[best_tile_index] != current_tile:
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
