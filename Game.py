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
from GameManager import GameManager

# game_board = copy.deepcopy(original_game_board)
game_board = GameBoard()


width = len(game_board.current_game_board[0]) * CFG.SQUARE_SIZE
height = len(game_board.current_game_board) * CFG.SQUARE_SIZE
#(width, height) = (len(game_board.current_game_board[0]) * CFG.SQUARE_SIZE, len(game_board.current_game_board) * CFG.SQUARE_SIZE)  # Game screen
screen = pygame.display.set_mode((width, height))
pacman = Pacman()
red_ghost = Ghost(CFG.RED_GHOST)
cyan_ghost = Ghost(CFG.CYAN_GHOST)
orange_ghost = Ghost(CFG.ORANGE_GHOST)
pink_ghost = Ghost(CFG.PINK_GHOST)

ghosts = (red_ghost, cyan_ghost, orange_ghost, pink_ghost)

for ghost in ghosts:
    ghost.setStartPosition()

pygame.init()
clock = pygame.time.Clock()

class Game:

    def __init__(self):
       # self.pressed_button_buffer = None
        self.game_ticks = 0
        #self.current_amount_of_active_ghosts = 0
        self.render_system = RenderSystem(game_board, screen)
        self.game_manager = GameManager(ghosts, ghosts[0], pacman, self.render_system, game_board, self.game_ticks)

    def runGame(self):

        self.render_system.drawGameBoard(pacman.lives_count)
        self.render_system.renderPacman(pacman)
        self.render_system.renderPacmanArrow(pacman)
        self.render_system.renderGhosts(ghosts)
        self.render_system.drawReadyText()

        MusicSystem.playBeginningSound()
        #GAME_CYCLE
        while True:

            self.game_manager.animateGhostsAndPacman()
            self.render_system.displayCurrentScore(pacman.current_score)
            self.render_system.displayHighScore(self.game_manager.score_system.loadHighScore())

            if self.game_manager.startPhase(pacman.lives_count) == True:
                clock.tick(CFG.GAME_FPS)
            else:
                self.game_manager.ghostReleasingQueue()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.game_manager.sendScoreToScoreSystem()
                        sys.exit()
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_a:
                            pacman.new_direction = CFG.LEFT
                        elif event.key == pygame.K_d:
                            pacman.new_direction = CFG.RIGHT
                        elif event.key == pygame.K_w:
                            pacman.new_direction = CFG.UP
                            #print("GOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO")
                            #print(GB.getTileValue(13, 15), GB.getTileValue(14, 15))
                        elif event.key == pygame.K_s:
                            pacman.new_direction = CFG.DOWN

                self.render_system.renderNearestTiles(pacman)

                self.game_manager.switchAllGhostsModes()
                self.game_manager.moveAllGhosts()
                self.game_manager.checkGhostPacmanCollision()

                self.render_system.renderPacman(pacman)
                self.render_system.renderPacmanArrow(pacman)
                self.render_system.renderPacmanLives(pacman.lives_count)
                self.render_system.renderGhosts(ghosts)


                if (pacman.move(game_board) == CFG.CROSSED_TUNNEL):
                    self.render_system.renderTunnelEnds()

                if (pacman.IsAlive == False):
                    self.game_manager.restartGameWhenDead()

                print("PELLETS: ", game_board.pellets_count)
                if (game_board.pellets_count == 0):

                    self.game_manager.startNextLevel()

            pacman.collectPellet(game_board)
            pacman.eatPowerPill(game_board)
            self.game_manager.powerPillUsing()

            pygame.display.update()
            clock.tick(CFG.GAME_FPS)

            self.game_manager.game_ticks += 1


game = Game()
game.runGame()
