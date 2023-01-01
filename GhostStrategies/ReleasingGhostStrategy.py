from GhostStrategies.GhostStrategy import GhostStrategy
import ConstantsForGame as CFG


class ReleasingGhostStrategy(GhostStrategy):


    def execute(self, ghost, game_board):
        exit_point = (13.5, 14)
        ghost.speed = CFG.GHOST_SPEED_NORMAL
        ghost_coords = (ghost.current_column, ghost.current_row)

        if ghost.ghost_type == CFG.ORANGE_GHOST:
            if (ghost_coords != exit_point):

                ghost.current_column = CFG.ORANGE_GHOST_ROUTE[ghost.release_state][0]
                ghost.current_row = CFG.ORANGE_GHOST_ROUTE[ghost.release_state][1]
                ghost.release_state += 1
            else:
                ghost.release_state = CFG.FULLY_RELEASED
                if ghost.IsFrightened:
                    ghost.strategy_index = CFG.GHOST_FRIGHTENED_STRATEGY
                    return

                ghost.strategy_index = CFG.GHOST_SCATTER_STRATEGY

        elif ghost.ghost_type == CFG.CYAN_GHOST:
            if (ghost_coords != exit_point):
                print("ВОООТ: ", ghost.release_state)
                ghost.current_column = CFG.CYAN_GHOST_ROUTE[ghost.release_state][0]
                ghost.current_row = CFG.CYAN_GHOST_ROUTE[ghost.release_state][1]
                ghost.release_state += 1
            else:
                ghost.release_state = CFG.FULLY_RELEASED
                if ghost.IsFrightened:
                    ghost.strategy_index = CFG.GHOST_FRIGHTENED_STRATEGY
                    return
                ghost.strategy_index = CFG.GHOST_SCATTER_STRATEGY

        elif ghost.ghost_type == CFG.PINK_GHOST:
            if (ghost_coords != exit_point):

                ghost.current_column = CFG.PINK_GHOST_ROUTE[ghost.release_state][0]
                ghost.current_row = CFG.PINK_GHOST_ROUTE[ghost.release_state][1]
                ghost.release_state += 1
            else:
                #print("ВОООТ: ", ghost.release_state)
                ghost.release_state = CFG.FULLY_RELEASED
                if ghost.IsFrightened:
                    ghost.strategy_index = CFG.GHOST_FRIGHTENED_STRATEGY
                    return
                ghost.strategy_index = CFG.GHOST_SCATTER_STRATEGY

        elif ghost.ghost_type == CFG.RED_GHOST:
            if (ghost_coords != exit_point):

                ghost.current_column = CFG.RED_GHOST_ROUTE[ghost.release_state][0]
                ghost.current_row = CFG.RED_GHOST_ROUTE[ghost.release_state][1]
                ghost.release_state += 1
            else:
                ghost.release_state = CFG.FULLY_RELEASED
                if ghost.IsFrightened:
                    ghost.strategy_index = CFG.GHOST_FRIGHTENED_STRATEGY
                    return
                ghost.strategy_index = CFG.GHOST_SCATTER_STRATEGY
