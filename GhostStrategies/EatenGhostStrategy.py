from GhostStrategies.GhostStrategy import GhostStrategy
import ConstantsForGame as CFG


class EatenGhostStrategy(GhostStrategy):

    def execute(self, ghost, game_board):
        ghost.speed = CFG.GHOST_SPEED_EATEN
        cage_enter = (13.5, 14)
        #ghost_coords = (ghost.cur_column, ghost.cur_row)
        ghost.chooseNewDirectionToMove(cage_enter, game_board)

        distanceBetweenGhostAndCage = ghost.calculateDistanceBetweenObjects(ghost.current_column,
                                                                             ghost.current_row,
                                                                             cage_enter[0],
                                                                             cage_enter[1])

        if distanceBetweenGhostAndCage <= 1:
            ghost.strategy_index = CFG.GHOST_ENTERING_CAGE_STRATEGY