import ConstantsForGame as CFG
import math
import GameObject
from GameObject import GameObject
class MovingObject(GameObject):

    def __init__(self, col, row):

        self.cur_dir = None
        self.new_dir = None
        self.cur_column = col
        self.cur_row = row

    def canChangeDirBeetweenWalls(self, col, row, game_board):

        IsWallAbove = game_board.getTileValue(col, row - 1) == CFG.WALL
        IsWallOnTheLeft = game_board.getTileValue(col - 1, row) == CFG.WALL
        IsWallBelow = game_board.getTileValue(col, row + 1) == CFG.WALL
        IsWallOnTheRight = game_board.getTileValue(col + 1, row) == CFG.WALL

        if self.new_dir == CFG.LEFT and IsWallOnTheLeft is False and (
                self.cur_row % 1.0 == 0):
            return True

        elif self.new_dir == CFG.RIGHT and IsWallOnTheRight is False and (
                self.cur_row % 1.0 == 0):
            return True

        elif self.new_dir == CFG.UP and IsWallAbove is False and (
                self.cur_column % 1.0 == 0):
            return True
        elif self.new_dir == CFG.DOWN and IsWallBelow is False and (
                self.cur_column % 1.0 == 0):
            return True
        else:
            return False


    def checkIfWallIsNext(self, col, row, game_board):
        IsWallAbove = game_board.getTileValue(col, row - 1) == CFG.WALL
        IsWallOnTheLeft = game_board.getTileValue(col - 1, row) == CFG.WALL
        IsWallBelow = game_board.getTileValue(col, row + 1) == CFG.WALL
        IsWallOnTheRight = game_board.getTileValue(col + 1, row) == CFG.WALL

        if self.cur_dir == CFG.LEFT and IsWallOnTheLeft and (
                self.cur_column % 1.0 == 0):
            return True

        elif self.cur_dir == CFG.RIGHT and IsWallOnTheRight and (
                self.cur_column % 1.0 == 0):
            return True

        elif self.cur_dir == CFG.UP and IsWallAbove and (
                self.cur_row % 1.0 == 0):
            return True
        elif self.cur_dir == CFG.DOWN and IsWallBelow and (
                self.cur_row % 1.0 == 0):
            return True
        else:
            return False
