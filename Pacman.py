# WASD
import math
import pygame
import ConstantsForGame as CFG
from MovingObject import MovingObject
from MusicSystem import MusicSystem

class Pacman(MovingObject):

    def __init__(self):
        self.current_direction = CFG.LEFT
        self.new_direction = CFG.LEFT
        # self.cur_pos_X = 350 #STARTPOS X
        # self.cur_pos_Y = 650 #STARTPOS Y
        self.current_column = 13.5
        self.current_row = 26

        self.pacman_sprite = pygame.image.load("ElementImages/pacman_start_sprite.png")
        self.pacman_sprite = pygame.transform.scale(self.pacman_sprite, (37, 37))
        self.pacman_arrow_sprite = pygame.image.load("ElementImages/pacman_arrow.png")

        self.sprite_state = CFG.PACMAN_MOUTH_CLOSED
        self.death_sprite_state = 1

        self.current_score = 0
        self.lives_count = 3
        self.IsAlive = True

        self.powerPillActivated = False
        self.IsPowerPillEnding = False
        self.power_pill_timer = 0

    def placeOnStartPosition(self):
        self.current_column = 13.5
        self.current_row = 26
        self.current_direction = CFG.LEFT
        self.new_direction = CFG.LEFT
        self.pacman_sprite = pygame.image.load("ElementImages/pacman_start_sprite.png")
        self.pacman_sprite = pygame.transform.scale(self.pacman_sprite, (37, 37))

        self.sprite_state = CFG.PACMAN_MOUTH_CLOSED
        self.death_sprite_state = 1

        self.powerPillActivated = False
        self.IsPowerPillEnding = False
        self.power_pill_timer = 0

    def move(self, game_board):
        self.calculateRoundedColumnRow()
        if CFG.BORDER_LEFT <= self.current_column < CFG.BORDER_RIGHT:

            if self.canChangeDirBeetweenWalls(self.rounded_column, self.rounded_row, game_board):
                self.current_direction = self.new_direction

            if self.checkIfWallInFront(self.rounded_column, self.rounded_row, game_board):
                return

            self.changePositionBySpeed(CFG.PACMAN_SPEED)

        if self.goesThroughTunnel():
            return CFG.CROSSED_TUNNEL

    def collectPellet(self, game_board):
        self.calculateRoundedColumnRow()
        if game_board.getTileValue(self.rounded_column, self.rounded_row) == CFG.PELLET:

            game_board.setTileValue(self.rounded_column, self.rounded_row, CFG.EMPTY_TILE)
            game_board.pellets_count -= 1

            self.current_score += 10
            MusicSystem.playMunchSound()

    def eatPowerPill(self, game_board):
        self.calculateRoundedColumnRow()

        if game_board.getTileValue(self.rounded_column, self.rounded_row) == CFG.POWER_PILL:

            game_board.setTileValue(self.rounded_column, self.rounded_row, CFG.EMPTY_TILE)
            self.current_score += 50
            self.powerPillActivated = True
            self.power_pill_timer = 0

            MusicSystem.playMunchSound()

    def eatGhost(self, ghost):
        if ghost.IsFrightened and ghost.strategy_index != CFG.GHOST_EATEN_STRATEGY\
                and ghost.strategy_index != CFG.GHOST_ENTERING_CAGE_STRATEGY:
            self.current_score += 200
            ghost.release_state = CFG.FULLY_RELEASED
            ghost.entering_cage_state = CFG.FULLY_RELEASED
            ghost.strategy_index = CFG.GHOST_EATEN_STRATEGY

            ghost.current_column, ghost.current_row = ghost.calculateRoundedColumnRow()

    def animatePacman(self):
        if self.IsAlive:
            self.changeSpriteStateWhenAlive()
        else:
            self.animatePacmanDeath()

    def changeSpriteStateWhenAlive(self):

        if self.sprite_state == CFG.PACMAN_MOUTH_CLOSED:
            self.sprite_state = CFG.PACMAN_MOUTH_OPENED1

        elif self.sprite_state == CFG.PACMAN_MOUTH_OPENED1:
            self.sprite_state = CFG.PACMAN_MOUTH_OPENED2

        elif self.sprite_state == CFG.PACMAN_MOUTH_OPENED2:
            self.sprite_state = CFG.PACMAN_MOUTH_CLOSED

        self.changeSpriteWhenAlive()

    def changeSpriteWhenAlive(self):

        sprite_name = ""

        if self.sprite_state == CFG.PACMAN_MOUTH_CLOSED:
            sprite_name = "pacman_mouth_closed"
        elif self.current_direction == CFG.UP:
            sprite_name = "pacman_mouth_up"
        elif self.current_direction == CFG.LEFT:
            sprite_name = "pacman_mouth_left"
        elif self.current_direction == CFG.DOWN:
            sprite_name = "pacman_mouth_down"
        elif self.current_direction == CFG.RIGHT:
            sprite_name = "pacman_mouth_right"


        self.setCurrentSprite(sprite_name, self.sprite_state)

    def setCurrentSprite(self, sprite_name, sprite_state):
        self.pacman_sprite = pygame.image.load(f"Assets/PacmanSprites/{sprite_name} ({sprite_state}).png")
        self.pacman_sprite = pygame.transform.scale(self.pacman_sprite, (CFG.SQUARE_SIZE * 1.5, CFG.SQUARE_SIZE * 1.5))

    def animatePacmanDeath(self):
        sprite_name = "pacman_dying"

        self.setCurrentSprite(sprite_name, self.death_sprite_state)

        self.death_sprite_state += 1
        if self.death_sprite_state == 12:

            self.IsAlive = True
            self.death_sprite_state = 1

    def takeLife(self):
        self.lives_count -= 1
        self.IsAlive = False
