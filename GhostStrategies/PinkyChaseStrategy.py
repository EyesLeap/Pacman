from GhostStrategies.ChaseStrategy import ChaseStrategy
import ConstantsForGame as CFG

class PinkyChaseStrategy(ChaseStrategy):

    def __init__(self, _pacman):
        self.pacman = _pacman

    # 4 tiles from pacman's front
    def execute(self, ghost, game_board):

        target = [self.pacman.current_column, self.pacman.current_row]

        if self.pacman.current_direction == CFG.UP:
            target[1] -= 4
        elif self.pacman.current_direction == CFG.LEFT:
            target[0] -= 4
        elif self.pacman.current_direction == CFG.DOWN:
            target[1] += 4
        elif self.pacman.current_direction == CFG.RIGHT:
            target[0] += 4

        if target[0] > CFG.GAME_BOARD_WIDTH - 1:
            target[0] = CFG.GAME_BOARD_WIDTH - 1
        elif target[1] > CFG.GAME_BOARD_HEIGHT - 1:
            target[1] = CFG.GAME_BOARD_HEIGHT

        ghost.chooseNewDirectionToMove(tuple(target), game_board)