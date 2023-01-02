from GhostStrategies.ChaseStrategy import ChaseStrategy
import ConstantsForGame as CFG

class ClydeChaseStrategy(ChaseStrategy):

    def __init__(self, _pacman):
        self.pacman = _pacman

    def execute(self, ghost, game_board):
        distanceBetweenGhostPacman = ghost.calculateDistanceBetweenObjects(ghost.current_column,
                                                                           ghost.current_row,
                                                                           self.pacman.current_column,
                                                                           self.pacman.current_row)

        # 8 tiles distance from pacman
        if distanceBetweenGhostPacman > 8:
            target = (self.pacman.current_column, self.pacman.current_row)
        else:
            target = ghost.chooseCornerToMove()

        ghost.chooseNewDirectionToMove(target, game_board)
