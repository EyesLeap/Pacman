#WASD
import math
import pygame
import ConstantsForGame as CFG
from MovingObject import MovingObject
from MusicSystem import MusicSystem
class Pacman(MovingObject):

    def __init__(self, game_board):
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
        self.sprite_state = CFG.PACMAN_MOUTH_CLOSED



    def move(self, game_board):
        col, row = self.calculateColumnAndRow()
        if  self.cur_column >= CFG.BORDER_LEFT and self.cur_column < CFG.BORDER_RIGHT:
            if self.canChangeDirBeetweenWalls(col, row, game_board) is True:

                self.cur_dir = self.new_dir

            ''''''
            if self.checkIfWallIsNext(col, row, game_board) == True:
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
            MusicSystem.playMunchSound()


    def changeCurrentSpriteState(self):

        if self.sprite_state == CFG.PACMAN_MOUTH_CLOSED:
            self.sprite_state = CFG.PACMAN_MOUTH_OPENED1

        elif self.sprite_state == CFG.PACMAN_MOUTH_OPENED1:
            self.sprite_state = CFG.PACMAN_MOUTH_OPENED2

        elif self.sprite_state == CFG.PACMAN_MOUTH_OPENED2:
            self.sprite_state = CFG.PACMAN_MOUTH_CLOSED

        self.changeCurrentSprite()
    def changeCurrentSprite(self):
        if self.sprite_state == CFG.PACMAN_MOUTH_CLOSED:
            self.pacman_sprite = pygame.image.load(f"Assets/PacmanSprites/pacman_mouth_closed.png")
            self.pacman_sprite = pygame.transform.scale(self.pacman_sprite, (CFG.SQUARE_SIZE*1.5, CFG.SQUARE_SIZE*1.5))
            return

        if self.cur_dir == CFG.UP:
            self.pacman_sprite = pygame.image.load(f"Assets/PacmanSprites/pacman_mouth_up{self.sprite_state}.png")
            self.pacman_sprite = pygame.transform.scale(self.pacman_sprite, (CFG.SQUARE_SIZE*1.5, CFG.SQUARE_SIZE*1.5))

        elif self.cur_dir == CFG.LEFT:
            self.pacman_sprite = pygame.image.load(f"Assets/PacmanSprites/pacman_mouth_left{self.sprite_state}.png")
            self.pacman_sprite = pygame.transform.scale(self.pacman_sprite, (CFG.SQUARE_SIZE*1.5, CFG.SQUARE_SIZE*1.5))

        elif self.cur_dir == CFG.DOWN:
            self.pacman_sprite = pygame.image.load(f"Assets/PacmanSprites/pacman_mouth_down{self.sprite_state}.png")
            self.pacman_sprite = pygame.transform.scale(self.pacman_sprite, (CFG.SQUARE_SIZE*1.5, CFG.SQUARE_SIZE*1.5))

        elif self.cur_dir == CFG.RIGHT:
            self.pacman_sprite = pygame.image.load(f"Assets/PacmanSprites/pacman_mouth_right{self.sprite_state}.png")
            self.pacman_sprite = pygame.transform.scale(self.pacman_sprite, (CFG.SQUARE_SIZE*1.5, CFG.SQUARE_SIZE*1.5))



