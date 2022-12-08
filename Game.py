import pygame
import math
from random import randrange
import random
import copy
import sys
from RenderSystem import RenderSystem
from Pacman import Pacman
from GameBoard import GameBoard
from Ghost import Ghost
from pygame import mixer
from MusicSystem import MusicSystem
import os
# 28 Across 31 Tall 1: Empty Space 2: Tic-Tak 3: Wall 4: Ghost safe-space 5: Special Tic-Tak
import ConstantsForGame as CFG

# game_board = copy.deepcopy(original_game_board)
GB = GameBoard()
(width, height) = (
len(GB.current_game_board[0]) * CFG.SQUARE_SIZE, len(GB.current_game_board) * CFG.SQUARE_SIZE)  # Game screen
screen = pygame.display.set_mode((width, height))
pacman = Pacman(GB)
red_ghost = Ghost(CFG.RED_GHOST)
cyan_ghost = Ghost(CFG.CYAN_GHOST)
orange_ghost = Ghost(CFG.ORANGE_GHOST)
pink_ghost = Ghost(CFG.PINK_GHOST)

ghosts = (red_ghost, cyan_ghost, orange_ghost, pink_ghost)

for ghost in ghosts:
    ghost.setStartPosition()

pygame.init()
clock = pygame.time.Clock()
rs = RenderSystem(GB, screen)


class Game:

    def __init__(self):
        self.pressed_button_buffer = None
        self.game_ticks = 0
        self.current_amount_of_active_ghosts = 0

    def startPhase(self):
        if self.game_ticks < CFG.GAME_FPS * 4:  # 4 SECONDS DURATION
            self.game_ticks += 1
            return True
        elif self.game_ticks < CFG.GAME_FPS * 4 + 1:
            rs.drawGameBoard()
            self.game_ticks += 1
            MusicSystem.playSirenMusic(1)
            self.releaseGhost()
            return False

    def releaseGhost(self):
        self.current_amount_of_active_ghosts += 1
        ghosts[2].current_mode = CFG.GHOST_RELEASING_MODE

        pass


    def runGame(self):

        rs.drawGameBoard()
        rs.renderPacman(pacman)
        rs.renderPacmanArrow(pacman)
        rs.renderGhosts(ghosts)
        rs.drawReadyText()
        MusicSystem.playBeginningSound()

        #GAME_CYCLE
        while True:

            if (self.game_ticks % 3) == 0:
                pacman.changeCurrentSpriteState()
                #print(pacman.sprite_state)

            if self.game_ticks == CFG.GAME_FPS * 10:  # 4 SECONDS DURATION
                ghosts[1].current_mode = CFG.GHOST_RELEASING_MODE
            if self.game_ticks == CFG.GAME_FPS * 15:  # 4 SECONDS DURATION
                ghosts[3].current_mode = CFG.GHOST_RELEASING_MODE

            if self.startPhase() == True:
                clock.tick(CFG.GAME_FPS)
            else:
                rs.renderNearestTiles(pacman)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        sys.exit()
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_a:
                            pacman.new_dir = CFG.LEFT
                        elif event.key == pygame.K_d:
                            pacman.new_dir = CFG.RIGHT
                        elif event.key == pygame.K_w:
                            pacman.new_dir = CFG.UP
                            #print("GOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO")
                            #print(GB.getTileValue(13, 15), GB.getTileValue(14, 15))
                        elif event.key == pygame.K_s:
                            pacman.new_dir = CFG.DOWN

                self.moveGhosts()
                rs.renderPacman(pacman)
                rs.renderPacmanArrow(pacman)
                rs.renderGhosts(ghosts)
                # rs.drawGrid()

                if (pacman.move(GB) == CFG.CROSSED_BORDER):
                    print(pacman.cur_column, pacman.cur_row)
                    rs.renderTunnelEnds()

            pacman.collectPellet(GB)
            pygame.display.update()
            clock.tick(CFG.GAME_FPS)
            # print(self.game_ticks)
            self.game_ticks += 1

    def moveGhosts(self):
        for ghost in ghosts:
            if (ghost.move(pacman, GB) == CFG.CROSSED_BORDER):
                rs.renderTunnelEnds()
            rs.renderNearestTiles(ghost)
            # ghost.calculateTargetPath(pacman, GB)


game = Game()
game.runGame()
