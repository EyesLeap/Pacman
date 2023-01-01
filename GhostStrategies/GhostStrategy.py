from abc import ABC, abstractmethod
import ConstantsForGame as CFG
from random import randint

## Strategy interface
class GhostStrategy(ABC):


    def __init__(self):
        self.next_strategy = None

    @abstractmethod
    def execute(self, ghost, game_board):
        pass

    def setNextStrategy(self, _next_strategy):
        self.next_strategy = _next_strategy






class ChaseStrategy(GhostStrategy):

    def __init__(self, _pacman):
        self.pacman = _pacman

    def execute(self, ghost, game_board):
        pass


class BlinkyChaseStrategy(ChaseStrategy):

    def __init__(self, _pacman):
        self.pacman = _pacman

    def execute(self, ghost, game_board):

        target = (self.pacman.current_column, self.pacman.current_row)
        ghost.chooseNewDirectionToMove(target, game_board)

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

        print("--------------------")
        print("ЦЕЛЬ:", target[0], target[1])
        print("PACMAN:", self.pacman.current_column, self.pacman.current_row)
        print("--------------------")
        print()
        ghost.chooseNewDirectionToMove(tuple(target), game_board)

        pass

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



class ScatterInCornersStrategy(GhostStrategy):


    def execute(self, ghost, game_board):


        target = ghost.chooseCornerToMove()
        ghost.chooseNewDirectionToMove(target, game_board)


class ChasePacmanStrategy(GhostStrategy):

    def __init__(self, _pacman):
        self.pacman = _pacman


    def execute(self, ghost, game_board):

        target = (self.pacman.current_column, self.pacman.current_row)
        ghost.chooseNewDirectionToMove(target, game_board)


class StartInCageStrategy(GhostStrategy):


    def execute(self, ghost, game_board):
        #ghost.calculateRoundedColumnRow()

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
