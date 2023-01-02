import pygame
from  ScoreSystem import ScoreSystem
from MusicSystem import MusicSystem
#import GhostStrategies.GhostStrategy

#import GhostStrategies.GhostStrategy
from GhostStrategies.ChaseStrategy import ChaseStrategy
from GhostStrategies.ScatterInCornersStrategy import ScatterInCornersStrategy

from GhostStrategies.BlinkyChaseStrategy import BlinkyChaseStrategy
from GhostStrategies.PinkyChaseStrategy import PinkyChaseStrategy
from GhostStrategies.InkyChaseStrategy import InkyChaseStrategy
from GhostStrategies.ClydeChaseStrategy import ClydeChaseStrategy

from GhostStrategies.StartInCageStrategy import StartInCageStrategy
from GhostStrategies.FrightenedGhostStrategy import FrightenedGhostStrategy
from GhostStrategies.EatenGhostStrategy import EatenGhostStrategy
from GhostStrategies.ReleasingGhostStrategy import ReleasingGhostStrategy
from GhostStrategies.EnteringCageStrategy import EnteringCageStrategy

import ConstantsForGame as CFG


class GameManager:

    def __init__(self, ghosts, red_ghost, pacman, render_system, game_board, game_ticks):
        self.ghosts = ghosts
        self.red_ghost = red_ghost
        self.pacman = pacman
        self.render_system = render_system
        self.game_board = game_board
        self.game_ticks = game_ticks
        self.score_system = ScoreSystem()
        self.score_system.loadHighScore()

        self.current_all_ghosts_mode = CFG.ALL_GHOSTS_SCATTER_MODE
        self.all_ghosts_mode_timer = 0

    def switchAllGhostsModes(self):
        #Chase Mode duration = 20 seconds
        #Scatter Mode duration = 5 seconds
        if self.game_ticks % CFG.GAME_SECOND == 0:
            self.all_ghosts_mode_timer += 1

        if self.current_all_ghosts_mode == CFG.ALL_GHOSTS_SCATTER_MODE:
            if self.all_ghosts_mode_timer >= CFG.SCATTER_MODE_DURATION:
                self.setAllGhostsChaseMode()
                self.all_ghosts_mode_timer = 0
                self.current_all_ghosts_mode = CFG.ALL_GHOSTS_CHASE_MODE

        elif self.current_all_ghosts_mode == CFG.ALL_GHOSTS_CHASE_MODE:
            if self.all_ghosts_mode_timer >= CFG.CHASE_MODE_DURATION:
                self.setAllGhostsScatterMode()
                self.all_ghosts_mode_timer = 0
                self.current_all_ghosts_mode = CFG.ALL_GHOSTS_SCATTER_MODE

    def ghostHasNonSwitchableStrategy(self, ghost):
        if ghost.strategy_index == CFG.GHOST_EATEN_STRATEGY:
            return True
        elif ghost.strategy_index == CFG.GHOST_RELEASING_STRATEGY:
            return True
        elif ghost.strategy_index == CFG.GHOST_ENTERING_CAGE_STRATEGY:
            return True
        elif ghost.strategy_index == CFG.GHOST_CAGE_STRATEGY:
            return True
        else:
            return False

    def setAllGhostsScatterMode(self):
        for ghost in self.ghosts:

            if self.ghostHasNonSwitchableStrategy(ghost):
                continue
            elif ghost.strategy_index == CFG.GHOST_FRIGHTENED_STRATEGY:
                continue
            else:
                ghost.prev_strategy_index = ghost.strategy_index
                ghost.setGhostStrategyIndexToScatter()

    def setAllGhostsChaseMode(self):
        for ghost in self.ghosts:
            if self.ghostHasNonSwitchableStrategy(ghost):
                continue
            elif ghost.strategy_index == CFG.GHOST_FRIGHTENED_STRATEGY:
                continue
            else:
                ghost.prev_strategy_index = ghost.strategy_index
                ghost.setGhostStrategyIndexToChase()

    def setAllGhostsFrightenedMode(self):
        for ghost in self.ghosts:
            ghost.IsFrightened = True
            ghost.IsFrightenedModeEnding = False
            ghost.sprite.frightened_sprite_state = 1
            if self.ghostHasNonSwitchableStrategy(ghost):
                continue
            else:
                ghost.IsFrightened = True
                ghost.prev_strategy_index = ghost.strategy_index
                ghost.strategy_index = CFG.GHOST_FRIGHTENED_STRATEGY

    def sendScoreToScoreSystem(self):
        self.score_system.recordHighScore(self.pacman.current_score)

    #When power pill ends
    def returnPreviousStrategyToGhosts(self):
        self.current_all_ghosts_mode = CFG.ALL_GHOSTS_SCATTER_MODE
        self.all_ghosts_mode_timer = 0
        for ghost in self.ghosts:

            ghost.IsFrightened = False
            ghost.sprite.frightened_sprite_state = 1
            if ghost.strategy_index == CFG.GHOST_EATEN_STRATEGY:
                continue
            elif ghost.strategy_index == CFG.GHOST_RELEASING_STRATEGY:
                continue
            elif ghost.strategy_index == CFG.GHOST_ENTERING_CAGE_STRATEGY:
                continue
            elif ghost.strategy_index == CFG.GHOST_CAGE_STRATEGY:
                continue

            ghost.strategy_index = ghost.prev_strategy_index

    def startPhase(self, pacman_lives_count):
        if self.game_ticks < CFG.GAME_SECOND * 4:  # 4 SECONDS DURATION
            self.game_ticks += 1
            return True

        elif self.game_ticks == CFG.GAME_SECOND * 4 + 1:

            self.render_system.drawGameBoard(pacman_lives_count)
            self.game_ticks += 1
            MusicSystem.playSirenMusic(CFG.SIREN_MUSIC1)
            return False

    def pauseGame(self, milliseconds):
        pygame.time.delay(milliseconds)

    def showPacmanDeath(self):
        self.pauseGame(500)
        MusicSystem.stopPlayingMusic()
        MusicSystem.playPacmanDeathSound()
        for i in range(11):
            self.pacman.animatePacman()
            self.render_system.drawGameBoard(self.pacman.lives_count)
            self.render_system.renderPacman(self.pacman)
            pygame.display.update()
            self.pauseGame(100)

    def animateGhostsAndPacman(self):
        if (self.game_ticks % 5) == 0:
            self.pacman.animatePacman()

            for ghost in self.ghosts:
                ghost.animateGhost(self.pacman.IsPowerPillEnding)
        if (self.game_ticks % 5) == 0:
            self.printGhostsInfo()

    def moveAllGhosts(self):
        for ghost in self.ghosts:
            if (self.moveGhost(self.pacman, self.game_board, ghost) == CFG.CROSSED_TUNNEL):
                self.render_system.renderTunnelEnds()
            self.render_system.renderNearestTiles(ghost)

    def convertStrategyToText(self, strategy_index):
        if strategy_index == CFG.GHOST_CAGE_STRATEGY:
            return "CAGE_STRATEGY"
        elif strategy_index == CFG.GHOST_SCATTER_STRATEGY:
            return "SCATTER_STRATEGY"
        elif strategy_index == CFG.GHOST_CHASE_STRATEGY:
            return "CHASE_STRATEGY"
        elif strategy_index == CFG.GHOST_RELEASING_STRATEGY:
            return "RELEASING_STRATEGY"
        elif strategy_index == CFG.GHOST_EATEN_STRATEGY:
            return "EATEN_STRATEGY"
        elif strategy_index == CFG.GHOST_FRIGHTENED_STRATEGY:
            return "FRIGHTENED_STRATEGY"
        elif strategy_index == CFG.GHOST_ENTERING_CAGE_STRATEGY:
            return "ENTERING_CAGE_STRATEGY"
        elif strategy_index == CFG.GHOST_BLINKY_CHASE_STRATEGY:
            return "BLINKY_CHASE_STRATEGY"
        elif strategy_index == CFG.GHOST_PINKY_CHASE_STRATEGY:
            return "PINKY_CHASE_STRATEGY"
        elif strategy_index == CFG.GHOST_INKY_CHASE_STRATEGY:
            return "INKY_CHASE_STRATEGY"
        elif strategy_index == CFG.GHOST_CLYDE_CHASE_STRATEGY:
            return "CLYDE_CHASE_STRATEGY"

    def printGhostsInfo(self):
        print("PACMAN POWER PILL = ", self.pacman.powerPillActivated)
        print("POWER PILL TIMER =  ", self.pacman.power_pill_timer)
        for ghost in self.ghosts:
            if ghost.ghost_type == CFG.RED_GHOST:
                print("1. RED_GHOST", self.convertStrategyToText(ghost.strategy_index), "FRIGHTENED? - ",
                      ghost.IsFrightened, "  ", ghost.current_column, ":", ghost.current_row)
            elif ghost.ghost_type == CFG.ORANGE_GHOST:
                print("2. ORANGE_GHOST", self.convertStrategyToText(ghost.strategy_index), "FRIGHTENED? - ",
                      ghost.IsFrightened, "  ", ghost.current_column, ":", ghost.current_row)
            elif ghost.ghost_type == CFG.CYAN_GHOST:
                print("3. CYAN_GHOST", self.convertStrategyToText(ghost.strategy_index), "FRIGHTENED? - ",
                      ghost.IsFrightened, "  ", ghost.current_column, ":", ghost.current_row)
            elif ghost.ghost_type == CFG.PINK_GHOST:
                print("4. PINK_GHOST", self.convertStrategyToText(ghost.strategy_index), "FRIGHTENED? - ",
                      ghost.IsFrightened, "  ", ghost.current_column, ":", ghost.current_row)

            print("")
        print("\n")

    def releaseGhost(self, ghost):
        ghost.strategy_index = CFG.GHOST_RELEASING_STRATEGY

    def ghostReleasingQueue(self):
        if self.game_ticks == CFG.GAME_SECOND * 10:
            self.releaseGhost(self.ghosts[2])
        elif self.game_ticks == CFG.GAME_FPS * 14:
            self.releaseGhost(self.ghosts[1])
        elif self.game_ticks == CFG.GAME_FPS * 19:
            self.releaseGhost(self.ghosts[3])

    def checkGhostPacmanCollision(self):
        for ghost in self.ghosts:

            DistanceBetweenPacmanGhost = self.pacman.calculateDistanceBetweenObjects(self.pacman.current_column,
                                                                                     self.pacman.current_row,
                                                                                     ghost.current_column,
                                                                                     ghost.current_row)
            if DistanceBetweenPacmanGhost <= 1 and not ghost.IsFrightened \
                    and ghost.strategy_index != CFG.GHOST_EATEN_STRATEGY:
                self.pacman.takeLife()
                print("ЖИЗНИ: ", self.pacman.lives_count)
            elif DistanceBetweenPacmanGhost <= 1 and ghost.IsFrightened:
                self.pacman.eatGhost(ghost)

    def takeUpStartPositions(self):
        self.placeAllGhostsOnStartPosition()
        self.pacman.placeOnStartPosition()

    def restartGameWhenDead(self):
        self.game_ticks = CFG.GAME_SECOND * 4 + 1
        self.current_all_ghosts_mode = CFG.ALL_GHOSTS_SCATTER_MODE
        self.all_ghosts_mode_timer = 0
        self.showPacmanDeath()
        self.render_system.drawGameBoard(self.pacman.lives_count)

        if (self.pacman.lives_count == 0):
            self.render_system.drawGameOverText()
            self.sendScoreToScoreSystem()
            pygame.display.update()
            self.pauseGame(3000)
            exit()

        else:
            self.takeUpStartPositions()
            self.render_system.drawReadyText()
            self.render_system.renderPacman(self.pacman)
            self.render_system.renderPacmanArrow(self.pacman)
            self.render_system.renderGhosts(self.ghosts)
            pygame.display.update()

            self.pauseGame(3000)
            MusicSystem.playSirenMusic(CFG.SIREN_MUSIC1)
            self.render_system.drawGameBoard(self.pacman.lives_count)

    def placeAllGhostsOnStartPosition(self):
        for ghost in self.ghosts:
            ghost.setStartPosition()
            ghost.IsFrightened = False

    def powerPillUsing(self):
        if self.pacman.powerPillActivated == False:
            return

        MusicSystem.playPowerPillMusic()

        if self.pacman.power_pill_timer == 0:
            self.pacman.IsPowerPillEnding = False
            self.setAllGhostsFrightenedMode()

        if self.pacman.powerPillActivated and self.pacman.power_pill_timer == CFG.GAME_SECOND * 5:
            self.pacman.IsPowerPillEnding = True

        if self.pacman.powerPillActivated and self.pacman.power_pill_timer < CFG.GAME_SECOND * 7:
            self.pacman.power_pill_timer += 1

        else:
            self.returnPreviousStrategyToGhosts()
            MusicSystem.playSirenMusic(CFG.SIREN_MUSIC1)
            self.pacman.powerPillActivated = False
            self.pacman.IsPowerPillEnding = False
            self.pacman.power_pill_timer = 0

    def startNextLevel(self):
        MusicSystem.stopPlayingMusic()
        CFG.SCATTER_MODE_DURATION -= 1

        self.game_ticks = (CFG.GAME_SECOND * 4)
        self.render_system.drawGameBoard(self.pacman.lives_count)
        self.render_system.renderPacman(self.pacman)
        self.render_system.renderPacmanArrow(self.pacman)
        pygame.display.update()
        self.pauseGame(2000)

        self.game_board.restartGameBoard()
        self.render_system.drawGameBoard(self.pacman.lives_count)

        self.takeUpStartPositions()
        self.render_system.drawReadyText()
        self.render_system.renderPacman(self.pacman)
        self.render_system.renderPacmanArrow(self.pacman)
        self.render_system.renderGhosts(self.ghosts)
        pygame.display.update()

        self.pauseGame(2000)
        MusicSystem.playSirenMusic(CFG.SIREN_MUSIC1)
        self.render_system.drawGameBoard(self.pacman.lives_count)

    def moveGhost(self, pacman, game_board, ghost):
        ghost.calculateRoundedColumnRow()

        if (ghost.strategy_index == CFG.GHOST_CAGE_STRATEGY):
            ghost.setStrategy(StartInCageStrategy())

        elif (ghost.strategy_index == CFG.GHOST_RELEASING_STRATEGY):
            ghost.setStrategy(ReleasingGhostStrategy())

        elif (ghost.strategy_index == CFG.GHOST_SCATTER_STRATEGY):
            ghost.setStrategy(ScatterInCornersStrategy())

        elif (ghost.strategy_index == CFG.GHOST_FRIGHTENED_STRATEGY):
            ghost.setStrategy(FrightenedGhostStrategy())

        elif (ghost.strategy_index == CFG.GHOST_EATEN_STRATEGY):
            ghost.setStrategy(EatenGhostStrategy())

        elif (ghost.strategy_index == CFG.GHOST_ENTERING_CAGE_STRATEGY):
            ghost.setStrategy(EnteringCageStrategy())

        elif (ghost.strategy_index == CFG.GHOST_BLINKY_CHASE_STRATEGY):
            ghost.setStrategy(BlinkyChaseStrategy(pacman))

        elif (ghost.strategy_index == CFG.GHOST_PINKY_CHASE_STRATEGY):
            ghost.setStrategy(PinkyChaseStrategy(pacman))

        elif (ghost.strategy_index == CFG.GHOST_INKY_CHASE_STRATEGY):
           ghost.setStrategy(InkyChaseStrategy(pacman, self.red_ghost))

        elif (ghost.strategy_index == CFG.GHOST_CLYDE_CHASE_STRATEGY):
            ghost.setStrategy(ClydeChaseStrategy(pacman))

        ghost.strategy.execute(ghost, game_board)

        if ghost.checkIfWallInFront(ghost.rounded_column, ghost.rounded_row, game_board):
            return

        if ghost.goesThroughTunnel():
            return CFG.CROSSED_TUNNEL
