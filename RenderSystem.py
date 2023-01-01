import pygame
import math
from random import randrange
import random
import copy
import sys
import os
import ConstantsForGame as CFG
from MovingObject import MovingObject


#spriteOffset = square * (1 - spriteRatio) * (1/2)
class RenderSystem:
    def __init__(self, gb, screen):
        self.pacman_sprite = pygame.image.load("ElementImages/pacman_start_sprite.png")
        self.pacman_sprite = pygame.transform.scale(self.pacman_sprite, (CFG.SQUARE_SIZE * 1.5, CFG.SQUARE_SIZE * 1.5))
        self.screen = screen
        self.gameBoard = gb

        self.pacman_life_icon = pygame.image.load(f"Assets/PacmanSprites/pacman_life_icon.png")
        self.pacman_life_icon = pygame.transform.scale(self.pacman_life_icon, (CFG.SQUARE_SIZE * 1.5, CFG.SQUARE_SIZE * 1.5))
    def drawGameBoard(self, pacman_lives_count):

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
                elif self.gameBoard.current_game_board[i][j] == CFG.POWER_PILL:
                    pygame.draw.circle(self.screen, CFG.PELLET_COLOR, (j * CFG.SQUARE_SIZE + CFG.SQUARE_SIZE//2 + 2,
                                      i * CFG.SQUARE_SIZE + CFG.SQUARE_SIZE//2), 10)

        self.renderPacmanLives(pacman_lives_count)

    def renderTunnelEnds(self):
        tunnel_end1 = MovingObject(0,17)
        tunnel_end2 = MovingObject(26.75,17)

        self.renderNearestTiles(tunnel_end1)
        self.renderNearestTiles(tunnel_end2)


    def renderNearestTiles(self, moving_object):
        #moving_object.calculateColumnAndRow()
        cur_column = math.floor(moving_object.current_column)
        cur_row = math.floor(moving_object.current_row)

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
                        
                    elif self.gameBoard.current_game_board[i][j] == CFG.POWER_PILL:
                        pygame.draw.circle(self.screen, CFG.PELLET_COLOR,
                                           (j * CFG.SQUARE_SIZE + CFG.SQUARE_SIZE // 2 + 2,
                                            i * CFG.SQUARE_SIZE + CFG.SQUARE_SIZE // 2), 10)

    def renderPacman(self, pacman):


        self.screen.blit(pacman.pacman_sprite, (pacman.current_column * CFG.SQUARE_SIZE - 4,
                                                pacman.current_row * CFG.SQUARE_SIZE - 3.125, CFG.SQUARE_SIZE, CFG.SQUARE_SIZE))
        #pygame.draw.rect(self.screen, (255, 255, 255), (pacman.cur_pos_X, pacman.cur_pos_Y, 3,3), 1)

    def renderPacmanLives(self, pacman_lives_count):
        pygame.draw.rect(self.screen, CFG.BLACK_COLOR, pygame.Rect(10, 860, 1000, 50))

        for i in range(0, pacman_lives_count-1):
            self.screen.blit(self.pacman_life_icon, ((i * 50) + 12,
                                                    860, CFG.SQUARE_SIZE,
                                                    CFG.SQUARE_SIZE))
    def renderGhosts(self, ghosts):
        for ghost in ghosts:
            self.screen.blit(ghost.sprite.image, (ghost.current_column * CFG.SQUARE_SIZE - 4,
                                                    ghost.current_row * CFG.SQUARE_SIZE - 3.125,
                                                    CFG.SQUARE_SIZE,
                                                    CFG.SQUARE_SIZE))

    def drawReadyText(self):
        ready_text = ["R_letter.png", "E_letter.png", "A_letter.png", "D_letter.png", "Y_letter.png", "ex_mark.png"]
        for i in range(len(ready_text)):

            letter = pygame.image.load(f"TextSprites/" + ready_text[i])
            letter = pygame.transform.scale(letter, (int(CFG.SQUARE_SIZE), int(CFG.SQUARE_SIZE)))
            self.screen.blit(letter, ((11 + i) * CFG.SQUARE_SIZE, 20 * CFG.SQUARE_SIZE, CFG.SQUARE_SIZE, CFG.SQUARE_SIZE))

    def drawGameOverText(self):
        game_over_text = ["G_letter.png", "A_letter.png", "M_letter.png", "E_letter.png",
                          "O_letter.png", "V_letter.png", "E_letter.png", "R_letter.png"]

        for i in range(4):
            letter = pygame.image.load(f"TextSprites/GameOverText/" + game_over_text[i])
            letter = pygame.transform.scale(letter, (int(CFG.SQUARE_SIZE), int(CFG.SQUARE_SIZE)))
            self.screen.blit(letter,
                             ((9 + i) * CFG.SQUARE_SIZE + 11, 20 * CFG.SQUARE_SIZE, CFG.SQUARE_SIZE, CFG.SQUARE_SIZE))

        for i in range(4,8):
            letter = pygame.image.load(f"TextSprites/GameOverText/" + game_over_text[i])
            letter = pygame.transform.scale(letter, (int(CFG.SQUARE_SIZE), int(CFG.SQUARE_SIZE)))
            self.screen.blit(letter,
                             ((10 + i) * CFG.SQUARE_SIZE + 11, 20 * CFG.SQUARE_SIZE, CFG.SQUARE_SIZE, CFG.SQUARE_SIZE))

    def renderPacmanArrow(self, pacman):
        pacman_arrow_sprite = pacman.pacman_arrow_sprite
        blit_coords_X = 0
        blit_coords_Y = 0

        if pacman.new_direction == CFG.LEFT:
            pacman_arrow_sprite = pygame.transform.rotate(pacman_arrow_sprite, 90)
            blit_coords_X = pacman.current_column * CFG.SQUARE_SIZE - 20
            blit_coords_Y = pacman.current_row * CFG.SQUARE_SIZE + 2

        elif pacman.new_direction == CFG.RIGHT:
            pacman_arrow_sprite = pygame.transform.rotate(pacman_arrow_sprite, 270)
            blit_coords_X = pacman.current_column * CFG.SQUARE_SIZE + 35
            blit_coords_Y = pacman.current_row * CFG.SQUARE_SIZE + 2

        elif pacman.new_direction == CFG.UP:
            #pacman_arrow_sprite = pygame.transform.rotate(pacman_arrow_sprite, 0)
            blit_coords_X = pacman.current_column * CFG.SQUARE_SIZE + 3
            blit_coords_Y = pacman.current_row * CFG.SQUARE_SIZE - 22

        elif pacman.new_direction == CFG.DOWN:
            pacman_arrow_sprite = pygame.transform.rotate(pacman_arrow_sprite, 180)
            blit_coords_X = pacman.current_column * CFG.SQUARE_SIZE + 5
            blit_coords_Y = pacman.current_row * CFG.SQUARE_SIZE + 34

        self.screen.blit(pacman_arrow_sprite, (blit_coords_X, blit_coords_Y, CFG.SQUARE_SIZE, CFG.SQUARE_SIZE))

    def displayCurrentScore(self, score):
        oneUpText = ["1_number.png", "U_letter.png", "P_letter.png"]


        for i in range(len(oneUpText)):
            letter = pygame.image.load(f"TextSprites/ScoreText/" + oneUpText[i])
            letter = pygame.transform.scale(letter, (int(CFG.SQUARE_SIZE), int(CFG.SQUARE_SIZE)))
            self.screen.blit(letter,
                             ((3 + i) * CFG.SQUARE_SIZE, 5, CFG.SQUARE_SIZE, CFG.SQUARE_SIZE))



        score_copy = copy.deepcopy(score)
        index = 0

        while score_copy != 0:
            number = score_copy % 10
            number = int(number)
            score_copy /= 10
            score_copy = int(score_copy)

            number_to_display = pygame.image.load(f"TextSprites/ScoreText/{number}_number.png")
            number_to_display = pygame.transform.scale(number_to_display, (int(CFG.SQUARE_SIZE), int(CFG.SQUARE_SIZE)))
            self.screen.blit(number_to_display,
                             ((7 - index) * CFG.SQUARE_SIZE - 10, 30, CFG.SQUARE_SIZE, CFG.SQUARE_SIZE))

            index += 1

    def displayHighScore(self, high_score):
        highScoreText = ["H_letter.png", "I_letter.png", "G_letter.png", "H_letter.png", "blank_letter.png",
                         "S_letter.png",
                         "C_letter.png", "O_letter.png", "R_letter.png", "E_letter.png"]



        for i in range(len(highScoreText)):
            letter = pygame.image.load(f"TextSprites/ScoreText/" + highScoreText[i])
            letter = pygame.transform.scale(letter, (int(CFG.SQUARE_SIZE), int(CFG.SQUARE_SIZE)))
            self.screen.blit(letter,
                             ((10 + i) * CFG.SQUARE_SIZE, 5, CFG.SQUARE_SIZE, CFG.SQUARE_SIZE))

        high_score_copy = copy.deepcopy(high_score)
        index = 0

        while high_score_copy != 0:
            number = high_score_copy % 10
            number = int(number)
            high_score_copy /= 10
            high_score_copy = int(high_score_copy)

            number_to_display = pygame.image.load(f"TextSprites/ScoreText/{number}_number.png")
            number_to_display = pygame.transform.scale(number_to_display, (int(CFG.SQUARE_SIZE), int(CFG.SQUARE_SIZE)))
            self.screen.blit(number_to_display,
                             ((16 - index) * CFG.SQUARE_SIZE - 10, 30, CFG.SQUARE_SIZE, CFG.SQUARE_SIZE))

            index += 1


        '''
        index = 0
        scoreStart = 5
        highScoreStart = 11
        for i in range(scoreStart, scoreStart + len(textOneUp)):
            tileImage = pygame.image.load(TextPath + textOneUp[index])
            tileImage = pygame.transform.scale(tileImage, (square, square))
            screen.blit(tileImage, (i * square, 4, square, square))
            index += 1
        score = str(self.score)
        if score == "0":
            score = "00"
        index = 0
        for i in range(0, len(score)):
            digit = int(score[i])
            tileImage = pygame.image.load(TextPath + "tile0" + str(32 + digit) + ".png")
            tileImage = pygame.transform.scale(tileImage, (square, square))
            screen.blit(tileImage, ((scoreStart + 2 + index) * square, square + 4, square, square))
            index += 1

        index = 0
        for i in range(highScoreStart, highScoreStart + len(textHighScore)):
            tileImage = pygame.image.load(TextPath + textHighScore[index])
            tileImage = pygame.transform.scale(tileImage, (square, square))
            screen.blit(tileImage, (i * square, 4, square, square))
            index += 1

        highScore = str(self.highScore)
        if highScore == "0":
            highScore = "00"
        index = 0
        for i in range(0, len(highScore)):
            digit = int(highScore[i])
            tileImage = pygame.image.load(TextPath + "tile0" + str(32 + digit) + ".png")
            tileImage = pygame.transform.scale(tileImage, (square, square))
            screen.blit(tileImage, ((highScoreStart + 6 + index) * square, square + 4, square, square))
            index += 1

    def drawGrid(self):
        for i in range(3,34):
            for j in range(28):
                pygame.draw.rect(self.screen, (255,255,255),(j*CFG.SQUARE_SIZE, i*CFG.SQUARE_SIZE, CFG.SQUARE_SIZE, CFG.SQUARE_SIZE), 1)

        '''
