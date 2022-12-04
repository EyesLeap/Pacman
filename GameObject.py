import ConstantsForGame as CFG
import math

class GameObject:

    def __init__(self, col, row):
        self.cur_column = col
        self.cur_row = row

    def calculateColumnAndRow(self):
        return (math.floor(self.cur_column), math.floor(self.cur_row))