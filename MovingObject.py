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

    def canChangeDirBeetweenWalls(self, col, row):

        if self.new_dir == CFG.LEFT and CFG.original_game_board[row][col - 1] != CFG.WALL and (self.cur_row % 1.0 == 0):
            # print("NOOOOOOOOOOOOO")
            return True

        elif self.new_dir == CFG.RIGHT and CFG.original_game_board[row][col + 1] != CFG.WALL and (
                self.cur_row % 1.0 == 0):
            # print("NOOOOOOOOOOOOO")
            return True

        elif self.new_dir == CFG.UP and CFG.original_game_board[row - 1][col] != CFG.WALL and (
                self.cur_column % 1.0 == 0):
            # print(original_game_board[row+3][col])
            # print("NOOOOOOOOOOOOO")
            return True
        elif self.new_dir == CFG.DOWN and CFG.original_game_board[row + 1][col] != CFG.WALL and (
                self.cur_column % 1.0 == 0):
            # print(original_game_board[row+3][col])
            # print("NOOOOOOOOOOOOO")
            return True
        else:
            return False


    def checkIfWallIsNext(self, col, row):
        if self.cur_dir == CFG.LEFT and CFG.original_game_board[row][col - 1] == CFG.WALL and (
                self.cur_column % 1.0 == 0):
            return True

        elif self.cur_dir == CFG.RIGHT and CFG.original_game_board[row][col + 1] == CFG.WALL and (
                self.cur_column % 1.0 == 0):
            return True

        elif self.cur_dir == CFG.UP and CFG.original_game_board[row - 1][col] == CFG.WALL and (self.cur_row % 1.0 == 0):
            return True
        elif self.cur_dir == CFG.DOWN and CFG.original_game_board[row + 1][col] == CFG.WALL and (
                self.cur_row % 1.0 == 0):
            return True
        else:
            return False
