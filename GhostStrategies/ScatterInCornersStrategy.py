from GhostStrategies.GhostStrategy import GhostStrategy
import ConstantsForGame as CFG


class ScatterInCornersStrategy(GhostStrategy):


    def execute(self, ghost, game_board):


        target = ghost.chooseCornerToMove()
        ghost.chooseNewDirectionToMove(target, game_board)