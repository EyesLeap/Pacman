from GhostStrategies.GhostStrategy import GhostStrategy
from GhostStrategies.ChaseStrategy import ChaseStrategy
import ConstantsForGame as CFG


class BlinkyChaseStrategy(ChaseStrategy):

    def __init__(self, _pacman):
        self.pacman = _pacman

    def execute(self, ghost, game_board):

        target = (self.pacman.current_column, self.pacman.current_row)
        ghost.chooseNewDirectionToMove(target, game_board)