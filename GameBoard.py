import pygame
import math
from random import randrange
import random
import copy
import sys
from RenderSystem import RenderSystem
from Pacman import Pacman
import ConstantsForGame as CFG
class GameBoard:

    current_game_board = copy.deepcopy(CFG.original_game_board)
    def __init__(self):

        pass

    def getTileValue(self, column, row):
        return self.current_game_board[row][column]


    def setTileValue(self, column, row, value):
        self.current_game_board[row][column] = value

