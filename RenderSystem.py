import pygame
import math
from random import randrange
import random
import copy
import sys
import os
import ConstantsForGame as CFG


square_size = 25
#spriteOffset = square * (1 - spriteRatio) * (1/2)
class RenderSystem:
    def __init__(self, gb, screen):
        self.pacman_sprite = pygame.image.load("ElementImages/pacman_start_sprite.png")
        self.pacman_sprite = pygame.transform.scale(self.pacman_sprite, (37.5, 37.5))
        self.screen = screen
        self.gameBoard = gb
    def drawGameBoard(self):
        tile_number = 1
        for i in range(3, CFG.GAME_BOARD_HEIGHT+3):
            for j in range(CFG.GAME_BOARD_WIDTH):
                tile_number_str = str(tile_number)
                tile_name = "tile (" + tile_number_str + ").png"
                tile_image = pygame.image.load(f"BoardImages/{tile_name}")
                tile_image = pygame.transform.scale(tile_image, (CFG.SQUARE_SIZE, CFG.SQUARE_SIZE))

                self.screen.blit(tile_image, (j * CFG.SQUARE_SIZE,i * CFG.SQUARE_SIZE, CFG.SQUARE_SIZE, CFG.SQUARE_SIZE))

                tile_number+= 1

                if self.gameBoard.current_game_board[i][j] == CFG.PELLET:
                    #pygame.draw.rect(self.screen, (255, 255, 255), (pacman.cur_pos_X, pacman.cur_pos_Y, 3, 3), 1)
                    pygame.draw.rect(self.screen, CFG.PELLET_COLOR,
                                     (j * CFG.SQUARE_SIZE + CFG.SQUARE_SIZE//2 - 1,
                                      i * CFG.SQUARE_SIZE + CFG.SQUARE_SIZE//2, CFG.SQUARE_SIZE//4, CFG.SQUARE_SIZE//4))

    def renderNearestTiles(self, moving_object):
        #moving_object.calculateColumnAndRow()
        cur_column = math.floor(moving_object.cur_column)
        cur_row = math.floor(moving_object.cur_row)

        for i in range(cur_row-3, cur_row+3):
            for j in range(cur_column-3, cur_column+3):
                if i >= 3 and i < CFG.GAME_BOARD_HEIGHT + 3 and j >= 0 and j < CFG.GAME_BOARD_WIDTH:
                    tile_number = (i-3) * CFG.GAME_BOARD_WIDTH + j + 1
                    tile_number_str = str(tile_number)
                    tile_name = "tile (" + tile_number_str + ").png"
                    tile_image = pygame.image.load(f"BoardImages/{tile_name}")
                    tile_image = pygame.transform.scale(tile_image, (CFG.SQUARE_SIZE, CFG.SQUARE_SIZE))

                    self.screen.blit(tile_image, (j * CFG.SQUARE_SIZE, i*CFG.SQUARE_SIZE, CFG.SQUARE_SIZE, CFG.SQUARE_SIZE))

                    tile_number += 1

                    if self.gameBoard.current_game_board[i][j] == CFG.PELLET:
                        # pygame.draw.rect(self.screen, (255, 255, 255), (pacman.cur_pos_X, pacman.cur_pos_Y, 3, 3), 1)
                        pygame.draw.rect(self.screen, CFG.PELLET_COLOR,
                                         (j * CFG.SQUARE_SIZE + CFG.SQUARE_SIZE // 2 - 1,
                                          i * CFG.SQUARE_SIZE + CFG.SQUARE_SIZE // 2, CFG.SQUARE_SIZE // 4, CFG.SQUARE_SIZE // 4))

    def renderPacman(self, pacman):
        self.screen.blit(pacman.pacman_sprite, (pacman.cur_column*CFG.SQUARE_SIZE-4,
                                              pacman.cur_row*CFG.SQUARE_SIZE-3.125, CFG.SQUARE_SIZE,CFG.SQUARE_SIZE))
        #pygame.draw.rect(self.screen, (255, 255, 255), (pacman.cur_pos_X, pacman.cur_pos_Y, 3,3), 1)
    def renderGhosts(self, ghosts):
        for ghost in ghosts:
            self.screen.blit(ghost.current_sprite, (ghost.cur_column * CFG.SQUARE_SIZE - 4,
                                                    ghost.cur_row * CFG.SQUARE_SIZE - 3.125, CFG.SQUARE_SIZE,
                                                    CFG.SQUARE_SIZE))

    def drawReadyText(self):
        ready_text = ["R_letter.png", "E_letter.png", "A_letter.png", "D_letter.png", "Y_letter.png", "ex_mark.png"]
        for i in range(len(ready_text)):

            letter = pygame.image.load(f"TextSprites/" + ready_text[i])
            letter = pygame.transform.scale(letter, (int(CFG.SQUARE_SIZE), int(CFG.SQUARE_SIZE)))
            self.screen.blit(letter, ((11 + i) * CFG.SQUARE_SIZE, 20 * CFG.SQUARE_SIZE, CFG.SQUARE_SIZE, CFG.SQUARE_SIZE))

    def renderPacmanArrow(self, pacman):
        pacman_arrow_sprite = pacman.pacman_arrow_sprite
        blit_coords_X = 0
        blit_coords_Y = 0

        if pacman.new_dir == CFG.LEFT:
            pacman_arrow_sprite = pygame.transform.rotate(pacman_arrow_sprite, 90)
            blit_coords_X = pacman.cur_column * CFG.SQUARE_SIZE - 20
            blit_coords_Y = pacman.cur_row * CFG.SQUARE_SIZE + 2

        elif pacman.new_dir == CFG.RIGHT:
            pacman_arrow_sprite = pygame.transform.rotate(pacman_arrow_sprite, 270)
            blit_coords_X = pacman.cur_column * CFG.SQUARE_SIZE + 35
            blit_coords_Y = pacman.cur_row * CFG.SQUARE_SIZE + 2

        elif pacman.new_dir == CFG.UP:
            #pacman_arrow_sprite = pygame.transform.rotate(pacman_arrow_sprite, 0)
            blit_coords_X = pacman.cur_column * CFG.SQUARE_SIZE + 3
            blit_coords_Y = pacman.cur_row * CFG.SQUARE_SIZE - 22

        elif pacman.new_dir == CFG.DOWN:
            pacman_arrow_sprite = pygame.transform.rotate(pacman_arrow_sprite, 180)
            blit_coords_X = pacman.cur_column * CFG.SQUARE_SIZE + 5
            blit_coords_Y = pacman.cur_row * CFG.SQUARE_SIZE + 34

        self.screen.blit(pacman_arrow_sprite, (blit_coords_X, blit_coords_Y, CFG.SQUARE_SIZE, CFG.SQUARE_SIZE))

    def drawGrid(self):
        for i in range(3,34):
            for j in range(28):
                pygame.draw.rect(self.screen, (255,255,255),(j*CFG.SQUARE_SIZE, i*CFG.SQUARE_SIZE, CFG.SQUARE_SIZE, CFG.SQUARE_SIZE), 1)


