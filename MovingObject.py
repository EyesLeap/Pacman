import ConstantsForGame as CFG
import math
import GameObject
from GameObject import GameObject
class MovingObject(GameObject):

    def __init__(self, col, row):

        self.current_direction = None
        self.new_direction = None
        self.current_column = col
        self.current_row = row

    def invertedDirection(self):
        return self.current_direction * -1

    def canChangeDirBeetweenWalls(self, col, row, game_board):

        IsWallAbove = game_board.getTileValue(col, row - 1) == CFG.WALL
        IsWallOnTheLeft = game_board.getTileValue(col - 1, row) == CFG.WALL
        IsWallBelow = game_board.getTileValue(col, row + 1) == CFG.WALL
        IsWallOnTheRight = game_board.getTileValue(col + 1, row) == CFG.WALL

        if self.new_direction == CFG.LEFT and IsWallOnTheLeft is False and (
                self.current_row % 1.0 == 0):

            return True

        elif self.new_direction == CFG.RIGHT and IsWallOnTheRight is False and (
                self.current_row % 1.0 == 0):
            return True

        elif self.new_direction == CFG.UP and IsWallAbove is False and (
                self.current_column % 1.0 == 0):
            return True
        elif self.new_direction == CFG.DOWN and IsWallBelow is False and (
                self.current_column % 1.0 == 0):
            return True
        else:
            return False

    def checkIfWallInFront(self, col, row, game_board):
        IsWallAbove = game_board.getTileValue(col, row - 1) == CFG.WALL
        IsWallOnTheLeft = game_board.getTileValue(col - 1, row) == CFG.WALL
        IsWallBelow = game_board.getTileValue(col, row + 1) == CFG.WALL
        IsWallOnTheRight = game_board.getTileValue(col + 1, row) == CFG.WALL

        if self.current_direction == CFG.LEFT and IsWallOnTheLeft and (
                self.current_column % 1.0 == 0):
            return True

        elif self.current_direction == CFG.RIGHT and IsWallOnTheRight and (
                self.current_column % 1.0 == 0):
            return True

        elif self.current_direction == CFG.UP and IsWallAbove and (
                self.current_row % 1.0 == 0):
            return True
        elif self.current_direction == CFG.DOWN and IsWallBelow and (
                self.current_row % 1.0 == 0):
            return True
        else:
            return False

    def goesThroughTunnel(self):
        if self.current_column < CFG.BORDER_LEFT:
            self.current_column = 26.75
            return True

        elif self.current_column >= CFG.BORDER_RIGHT:
            self.current_column = 0
            return True

        else:
            return False

    def changePositionBySpeed(self, speed):
        if self.current_direction == CFG.LEFT:
            self.current_column -= speed
        elif self.current_direction == CFG.RIGHT:
            self.current_column += speed
        elif self.current_direction == CFG.DOWN:
            self.current_row += speed
        elif self.current_direction == CFG.UP:
            self.current_row -= speed