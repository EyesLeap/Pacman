from GhostStrategies.GhostStrategy import GhostStrategy
import ConstantsForGame as CFG

class EnteringCageStrategy(GhostStrategy):

    def execute(self, ghost, game_board):

        ghost_coords = (ghost.current_column, ghost.current_row)
        middle_cage_point = (13.5, 17)
        if ghost_coords != middle_cage_point:

            ghost.current_column = CFG.BACK_TO_CAGE_ROUTE[ghost.entering_cage_state][0]
            ghost.current_row = CFG.BACK_TO_CAGE_ROUTE[ghost.entering_cage_state][1]
            ghost.entering_cage_state += 1
        else:

            ghost.entering_cage_state = CFG.IN_CAGE_MODE
            ghost.IsFrightened = False
            ghost.strategy_index = CFG.GHOST_RELEASING_STRATEGY