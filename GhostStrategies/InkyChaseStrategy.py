from GhostStrategies.GhostStrategy import GhostStrategy
from GhostStrategies.ChaseStrategy import ChaseStrategy
import ConstantsForGame as CFG

class InkyChaseStrategy(ChaseStrategy):

    def __init__(self, _pacman, _red_ghost):
        self.pacman = _pacman
        self.red_ghost = _red_ghost

    def execute(self, ghost, game_board):

        intermediate_tile = [self.pacman.current_column, self.pacman.current_row]

        if self.pacman.current_direction == CFG.UP:
            intermediate_tile[1] -= 2
        elif self.pacman.current_direction == CFG.LEFT:
            intermediate_tile[0] -= 2
        elif self.pacman.current_direction == CFG.DOWN:
            intermediate_tile[1] += 2
        elif self.pacman.current_direction == CFG.RIGHT:
            intermediate_tile[0] += 2

        target = [2 * intermediate_tile[0] - self.red_ghost.current_column,
                  2 * intermediate_tile[1] - self.red_ghost.current_row]

        if target[0] > CFG.GAME_BOARD_WIDTH - 1:
            target[0] = CFG.GAME_BOARD_WIDTH - 1
        elif target[1] > CFG.GAME_BOARD_HEIGHT - 1:
            target[1] = CFG.GAME_BOARD_HEIGHT

        ghost.chooseNewDirectionToMove(tuple(target), game_board)

