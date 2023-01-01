from GhostStrategies.GhostStrategy import GhostStrategy
import ConstantsForGame as CFG
from random import randint

class FrightenedGhostStrategy(GhostStrategy):

    def execute(self, ghost, game_board):

        ghost.calculateRoundedColumnRow()
        ghost.frightenedModeInvertCheck(game_board)

        for i in range(4):
            random_direction = randint(1,4)
            random_direction = ghost.convertDirectionToConstant(random_direction)

            if random_direction != ghost.invertedDirection():
                ghost.new_direction = random_direction

        if ghost.canChangeDirBeetweenWalls(ghost.rounded_column, ghost.rounded_row, game_board):

            if ghost.new_direction != ghost.current_direction:
                ghost.changeSpriteState()

            ghost.current_direction = ghost.new_direction

        if ghost.checkIfWallInFront(ghost.rounded_column, ghost.rounded_row, game_board) is False:
            ghost.changePositionBySpeed(CFG.GHOST_SPEED)