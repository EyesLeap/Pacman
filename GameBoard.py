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

    #current_game_board = None
    def __init__(self):
        self.current_game_board = copy.deepcopy(CFG.original_game_board)
        self.pellets_count = 240

    def getTileValue(self, column, row):
        return self.current_game_board[row][column]

    def setTileValue(self, column, row, value):
        self.current_game_board[row][column] = value

    def restartGameBoard(self):
        self.pellets_count = 240
        self.current_game_board = copy.deepcopy(CFG.original_game_board)



