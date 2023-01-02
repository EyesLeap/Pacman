import ConstantsForGame as CFG
import math

class GameObject:

    def __init__(self, col, row):
        self.current_column = col
        self.current_row = row
        self.rounded_column = math.floor(self.current_column)
        self.rounded_row = math.floor(self.current_row)

    def calculateRoundedColumnRow(self):
        self.rounded_column = math.floor(self.current_column)
        self.rounded_row = math.floor(self.current_row)
        return (self.rounded_column, self.rounded_row)

    def calculateDistanceBetweenObjects(self, obj1_col, obj1_row, obj2_col, obj2_row):
        distanceX = (abs(obj1_col - obj2_col) ** 2)
        distanceY = (abs(obj1_row - obj2_row) ** 2)
        return math.sqrt(distanceX + distanceY)

