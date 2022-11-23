import pygame
import math
from random import randrange
import random
import copy
import sys
import os
UP = 0
LEFT = 1
DOWN = 2
RIGHT = 3
GAME_BOARD_WIDTH = 28
GAME_BOARD_HEIGHT = 31
square_size = 25
#spriteOffset = square * (1 - spriteRatio) * (1/2)
class RenderSystem:
    def __init__(self, game_board, screen):
        #self.game_board = game_board
        self.pacman_sprite = pygame.image.load("ElementImages/pacman_start_sprite.png")
        self.pacman_sprite = pygame.transform.scale(self.pacman_sprite, (37.5, 37.5))
        self.screen = screen
    def renderGameBoard(self):
        tile_number = 1
        for i in range(3, GAME_BOARD_HEIGHT+3):
            for j in range(GAME_BOARD_WIDTH):
                tile_number_str = str(tile_number)
                tile_name = "tile (" + tile_number_str + ").png"
                tile_image = pygame.image.load(f"BoardImages/{tile_name}")
                tile_image = pygame.transform.scale(tile_image, (square_size, square_size))

                self.screen.blit(tile_image, (j * square_size,i * square_size, square_size, square_size))

                tile_number+= 1
    def renderNearestTiles(self, moving_object):
        #moving_object.calculateColumnAndRow()
        tile_number = 0
        cur_column = math.floor(moving_object.cur_column)
        cur_row = math.floor(moving_object.cur_row)

        for i in range(cur_row-3, cur_row+3):
            for j in range(cur_column-3, cur_column+3):
                if i >= 3 and i < GAME_BOARD_HEIGHT + 3 and j >= 0 and j < GAME_BOARD_WIDTH:
                    tile_number = (i-3) * GAME_BOARD_WIDTH + j + 1
                    tile_number_str = str(tile_number)
                    tile_name = "tile (" + tile_number_str + ").png"
                    tile_image = pygame.image.load(f"BoardImages/{tile_name}")
                    tile_image = pygame.transform.scale(tile_image, (square_size, square_size))

                    self.screen.blit(tile_image, (j * square_size, i*square_size, square_size, square_size))

                    tile_number += 1


    def renderPacman(self, pacman):
        self.screen.blit(pacman.pacman_sprite, (pacman.cur_column*square_size-3.125,
                                              pacman.cur_row*square_size-3.125, square_size,square_size))
        #pygame.draw.rect(self.screen, (255, 255, 255), (pacman.cur_pos_X, pacman.cur_pos_Y, 3,3), 1)

    def renderPacmanArrow(self, pacman):
        pacman_arrow_sprite = pacman.pacman_arrow_sprite
        blit_coords_X = 0
        blit_coords_Y = 0

        if pacman.new_dir == LEFT:
            pacman_arrow_sprite = pygame.transform.rotate(pacman_arrow_sprite, 90)
            blit_coords_X = pacman.cur_column * square_size - 20
            blit_coords_Y = pacman.cur_row * square_size + 2

        elif pacman.new_dir == RIGHT:
            pacman_arrow_sprite = pygame.transform.rotate(pacman_arrow_sprite, 270)
            blit_coords_X = pacman.cur_column * square_size + 35
            blit_coords_Y = pacman.cur_row * square_size + 2

        elif pacman.new_dir == UP:
            #pacman_arrow_sprite = pygame.transform.rotate(pacman_arrow_sprite, 0)
            blit_coords_X = pacman.cur_column * square_size + 3
            blit_coords_Y = pacman.cur_row * square_size - 22

        elif pacman.new_dir == DOWN:
            pacman_arrow_sprite = pygame.transform.rotate(pacman_arrow_sprite, 180)
            blit_coords_X = pacman.cur_column * square_size + 5
            blit_coords_Y = pacman.cur_row * square_size + 34

        self.screen.blit(pacman_arrow_sprite, (blit_coords_X, blit_coords_Y, square_size, square_size))

    def drawGrid(self):
        for i in range(3,34):
            for j in range(28):
                pygame.draw.rect(self.screen, (255,255,255),(j*square_size, i*square_size, square_size, square_size), 1)

