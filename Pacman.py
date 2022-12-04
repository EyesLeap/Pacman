#WASD
import math
import pygame
import ConstantsForGame as CFG
from MovingObject import MovingObject

class Pacman(MovingObject):

    def __init__(self):
        self.cur_dir = CFG.LEFT
        self.new_dir = CFG.LEFT
        #self.cur_pos_X = 350 #STARTPOS X
        #self.cur_pos_Y = 650 #STARTPOS Y
        self.cur_column = 13.5
        self.cur_row = 26
        self.pacman_sprite = pygame.image.load("ElementImages/pacman_start_sprite.png")
        self.pacman_sprite = pygame.transform.scale(self.pacman_sprite, (37, 37))
        self.pacman_arrow_sprite = pygame.image.load("ElementImages/pacman_arrow.png")
        self.current_score = 0


    def move(self):
        col, row = self.calculateColumnAndRow()
        if  self.cur_column >= CFG.BORDER_LEFT and self.cur_column < CFG.BORDER_RIGHT:
            if self.canChangeDirBeetweenWalls(col, row) is True:
                #(self.cur_column)
                #print(self.cur_row)
                self.cur_dir = self.new_dir

            ''''''
            if self.checkIfWallIsNext(col, row) == True:
                return


            if self.cur_dir == CFG.LEFT:
                self.cur_column -= CFG.PACMAN_SPEED
            elif self.cur_dir == CFG.RIGHT:
                self.cur_column += CFG.PACMAN_SPEED
            elif self.cur_dir == CFG.DOWN:
                self.cur_row += CFG.PACMAN_SPEED
            elif self.cur_dir == CFG.UP:
                self.cur_row -= CFG.PACMAN_SPEED

        elif self.cur_column < CFG.BORDER_LEFT:
            self.cur_column = 26.75
            return CFG.CROSSED_BORDER

        elif self.cur_column >= CFG.BORDER_RIGHT:
            self.cur_column = 0
            return CFG.CROSSED_BORDER

    def collectPellet(self, game_board):
        col, row = self.calculateColumnAndRow()
        if game_board.getTileValue(col,row) == CFG.PELLET:
            game_board.setTileValue(col,row,CFG.EMPTY_TILE)
            self.current_score += 10







