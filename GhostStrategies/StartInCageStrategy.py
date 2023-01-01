from GhostStrategies.GhostStrategy import GhostStrategy
import ConstantsForGame as CFG


class StartInCageStrategy(GhostStrategy):

    def execute(self, ghost, game_board):

        if ghost.current_direction == CFG.UP:
            ghost.current_row -= ghost.speed
            ghost.calculateRoundedColumnRow()

            if ghost.checkIfWallInFront(ghost.rounded_column, ghost.rounded_row, game_board):
                ghost.current_direction *= CFG.OPPOSITE_DIRECTION  # OPPOSITE DIRECTION

            ghost.current_row += ghost.speed

        elif ghost.current_direction == CFG.DOWN:

            ghost.current_row += ghost.speed
            ghost.calculateRoundedColumnRow()

            if ghost.checkIfWallInFront(ghost.rounded_column, ghost.rounded_row, game_board):
                ghost.current_direction *= CFG.OPPOSITE_DIRECTION  # OPPOSITE DIRECTION

            ghost.current_row -= ghost.speed

        ghost.changePositionBySpeed(CFG.GHOST_SPEED_NORMAL)