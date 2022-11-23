#WASD
import math
import pygame
UP = 0
LEFT = 1
DOWN = 2
RIGHT = 3
square_size = 25
PACMAN_SPEED = 1/4
original_game_board = [
    [3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3],
    [3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3],
    [3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3],
    [3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3],
    [3,2,2,2,2,2,2,2,2,2,2,2,2,3,3,2,2,2,2,2,2,2,2,2,2,2,2,3],
    [3,2,3,3,3,3,2,3,3,3,3,3,2,3,3,2,3,3,3,3,3,2,3,3,3,3,2,3],
    [3,6,3,3,3,3,2,3,3,3,3,3,2,3,3,2,3,3,3,3,3,2,3,3,3,3,6,3],
    [3,2,3,3,3,3,2,3,3,3,3,3,2,3,3,2,3,3,3,3,3,2,3,3,3,3,2,3],
    [3,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,3],
    [3,2,3,3,3,3,2,3,3,2,3,3,3,3,3,3,3,3,2,3,3,2,3,3,3,3,2,3],
    [3,2,3,3,3,3,2,3,3,2,3,3,3,3,3,3,3,3,2,3,3,2,3,3,3,3,2,3],
    [3,2,2,2,2,2,2,3,3,2,2,2,2,3,3,2,2,2,2,3,3,2,2,2,2,2,2,3],
    [3,3,3,3,3,3,2,3,3,3,3,3,1,3,3,1,3,3,3,3,3,2,3,3,3,3,3,3],
    [3,3,3,3,3,3,2,3,3,3,3,3,1,3,3,1,3,3,3,3,3,2,3,3,3,3,3,3],
    [3,3,3,3,3,3,2,3,3,1,1,1,1,1,1,1,1,1,1,3,3,2,3,3,3,3,3,3],
    [3,3,3,3,3,3,2,3,3,1,3,3,3,3,3,3,3,3,1,3,3,2,3,3,3,3,3,3],
    [3,3,3,3,3,3,2,3,3,1,3,4,4,4,4,4,4,3,1,3,3,2,3,3,3,3,3,3],
    [1,1,1,1,1,1,2,1,1,1,3,4,4,4,4,4,4,3,1,1,1,2,1,1,1,1,1,1], # Middle Lane Row: 14
    [3,3,3,3,3,3,2,3,3,1,3,4,4,4,4,4,4,3,1,3,3,2,3,3,3,3,3,3],
    [3,3,3,3,3,3,2,3,3,1,3,3,3,3,3,3,3,3,1,3,3,2,3,3,3,3,3,3],
    [3,3,3,3,3,3,2,3,3,1,1,1,1,1,1,1,1,1,1,3,3,2,3,3,3,3,3,3],
    [3,3,3,3,3,3,2,3,3,1,3,3,3,3,3,3,3,3,1,3,3,2,3,3,3,3,3,3],
    [3,3,3,3,3,3,2,3,3,1,3,3,3,3,3,3,3,3,1,3,3,2,3,3,3,3,3,3],
    [3,2,2,2,2,2,2,2,2,2,2,2,2,3,3,2,2,2,2,2,2,2,2,2,2,2,2,3],
    [3,2,3,3,3,3,2,3,3,3,3,3,2,3,3,2,3,3,3,3,3,2,3,3,3,3,2,3],
    [3,2,3,3,3,3,2,3,3,3,3,3,2,3,3,2,3,3,3,3,3,2,3,3,3,3,2,3],
    [3,6,2,2,3,3,2,2,2,2,2,2,2,1,1,2,2,2,2,2,2,2,3,3,2,2,6,3],
    [3,3,3,2,3,3,2,3,3,2,3,3,3,3,3,3,3,3,2,3,3,2,3,3,2,3,3,3],
    [3,3,3,2,3,3,2,3,3,2,3,3,3,3,3,3,3,3,2,3,3,2,3,3,2,3,3,3],
    [3,2,2,2,2,2,2,3,3,2,2,2,2,3,3,2,2,2,2,3,3,2,2,2,2,2,2,3],
    [3,2,3,3,3,3,3,3,3,3,3,3,2,3,3,2,3,3,3,3,3,3,3,3,3,3,2,3],
    [3,2,3,3,3,3,3,3,3,3,3,3,2,3,3,2,3,3,3,3,3,3,3,3,3,3,2,3],
    [3,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,3],
    [3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3],
    [3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3],
    [3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3],
]
class Pacman:


    def __init__(self):
        self.cur_dir = LEFT
        self.new_dir = LEFT
        self.cur_pos_X = 350 #STARTPOS X
        self.cur_pos_Y = 650 #STARTPOS Y
        self.cur_column = 350/25
        self.cur_row =650/25
        self.pacman_sprite = pygame.image.load("ElementImages/pacman_start_sprite.png")
        self.pacman_sprite = pygame.transform.scale(self.pacman_sprite, (37.5, 37.5))
        self.pacman_arrow_sprite = pygame.image.load("ElementImages/pacman_arrow.png")
    def canChangeDir(self):

        col, row = self.calculateColumnAndRow()
        if self.new_dir == LEFT and original_game_board[row][col-1] != 3 and (self.cur_row % 1.0 == 0):
            #print("NOOOOOOOOOOOOO")
            return True

        elif self.new_dir == RIGHT and original_game_board[row][col+1] != 3 and (self.cur_row % 1.0 == 0):
            #print("NOOOOOOOOOOOOO")
            return True

        elif self.new_dir == UP and original_game_board[row-1][col] != 3 and (self.cur_column % 1.0 == 0):
            # print(original_game_board[row+3][col])
            #print("NOOOOOOOOOOOOO")
            return True
        elif self.new_dir == DOWN and original_game_board[row+1][col] != 3 and (self.cur_column % 1.0 == 0):
            # print(original_game_board[row+3][col])
            #print("NOOOOOOOOOOOOO")
            return True
        else:
            return False

    def move(self, pressed_button_buffer):
        #self.calculateColumnAndRow()
        #print(original_game_board[self.cur_row][self.cur_column])
        col, row = self.calculateColumnAndRow()
        if self.canChangeDir() is True:

            print(self.cur_column)
            print(self.cur_row)
            self.cur_dir = self.new_dir


        if self.cur_dir == LEFT and original_game_board[row][col-1] == 3 and (self.cur_column % 1.0 == 0):
            print("NOOOOOOOOOOOOO")
            return

        elif self.cur_dir == RIGHT and original_game_board[row][col+1] == 3 and (self.cur_column % 1.0 == 0):
            print("NOOOOOOOOOOOOO")
            return

        elif self.cur_dir == UP and original_game_board[row-1][col] == 3 and (self.cur_row % 1.0 == 0):
            #print(original_game_board[row+3][col])
            print("NOOOOOOOOOOOOO")
            return
        elif self.cur_dir == DOWN and original_game_board[row+1][col] == 3 and (self.cur_row % 1.0 == 0):
            #print(original_game_board[row+3][col])
            print("NOOOOOOOOOOOOO")
            return
        '''
        print(self.cur_column)
        print(self.cur_row)
        '''
        if self.cur_dir == LEFT:
            self.cur_column -= PACMAN_SPEED
        elif self.cur_dir == RIGHT:
            self.cur_column += PACMAN_SPEED
        elif self.cur_dir == DOWN:
            self.cur_row += PACMAN_SPEED
        elif self.cur_dir == UP:
            self.cur_row -= PACMAN_SPEED


    def calculateColumnAndRow(self):
       return (math.floor(self.cur_column), math.floor(self.cur_row))
