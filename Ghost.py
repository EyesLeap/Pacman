import pygame
from MovingObject import MovingObject
import ConstantsForGame as CFG
from operator import itemgetter
from GhostSprite import GhostSprite
import GhostStrategies.GhostStrategy


class Ghost(MovingObject):
    def __init__(self, ghost_type):
        self.sprite = None

        self.current_sprite_state = 1  # 1-2 Right, 3-4 Down, 5-6 Left, 7-8 Up
        self.current_sprite = None
        self.spriteAnimationFlag = 1

        self.ghost_type = ghost_type
        self.speed = CFG.GHOST_SPEED_NORMAL

        self.strategy = None
        self.prev_strategy_index = CFG.GHOST_SCATTER_STRATEGY
        self.strategy_index = CFG.GHOST_CAGE_STRATEGY

        self.IsFrightened = False
        self.IsFrightenedModeEnding = False

        self.new_direction = None

        self.target = None

        self.release_state = CFG.IN_CAGE_MODE
        self.entering_cage_state = 0

        self.frightenedModeActive = False
        self.frightenedModeInvertedDir = False
        self.frightened_sprite_state = 1

    def setStartPosition(self):

        if self.ghost_type == CFG.RED_GHOST:

            self.current_column = 13.5
            self.current_row = 14
            self.sprite = GhostSprite(f"GhostsSprites/red_ghost (5).png", self.ghost_type, 5)
            self.current_sprite_state = 5
            self.current_sprite = pygame.image.load(f"GhostsSprites/red_ghost (5).png")
            self.current_sprite = pygame.transform.scale(self.current_sprite,
                                                         (int(CFG.SQUARE_SIZE * 3 / 2), int(CFG.SQUARE_SIZE * 3 / 2)))
            self.current_direction = CFG.LEFT

            self.strategy_index = CFG.GHOST_SCATTER_STRATEGY
            # self.setStrategy(ScatterInCornersStrategy())

        elif self.ghost_type == CFG.CYAN_GHOST:

            self.current_column = 11.5
            self.current_row = 17
            self.sprite = GhostSprite(f"GhostsSprites/cyan_ghost (7).png", self.ghost_type, 7)
            self.current_sprite_state = 7
            self.current_sprite = pygame.image.load(f"GhostsSprites/cyan_ghost (7).png")
            self.current_sprite = pygame.transform.scale(self.current_sprite,
                                                         (int(CFG.SQUARE_SIZE * 3 / 2), int(CFG.SQUARE_SIZE * 3 / 2)))
            self.current_direction = CFG.UP
            self.strategy_index = CFG.GHOST_CAGE_STRATEGY

            #self.strategy_index = CFG.GHOST_INKY_CHASE_STRATEGY

        elif self.ghost_type == CFG.ORANGE_GHOST:

            self.current_column = 13.5
            self.current_row = 17
            self.sprite = GhostSprite(f"GhostsSprites/orange_ghost (3).png", self.ghost_type, 3)
            self.current_sprite_state = 3
            self.current_sprite = pygame.image.load(f"GhostsSprites/orange_ghost (3).png")
            self.current_sprite = pygame.transform.scale(self.current_sprite,
                                                         (int(CFG.SQUARE_SIZE * 3 / 2), int(CFG.SQUARE_SIZE * 3 / 2)))
            self.current_direction = CFG.DOWN
            self.strategy_index = CFG.GHOST_CAGE_STRATEGY



        elif self.ghost_type == CFG.PINK_GHOST:

            self.current_column = 15.5
            self.current_row = 17
            self.sprite = GhostSprite(f"GhostsSprites/pink_ghost (7).png", self.ghost_type, 7)
            self.current_sprite_state = 7
            self.current_sprite = pygame.image.load(f"GhostsSprites/pink_ghost (7).png")
            self.current_sprite = pygame.transform.scale(self.current_sprite,
                                                         (int(CFG.SQUARE_SIZE * 3 / 2), int(CFG.SQUARE_SIZE * 3 / 2)))
            self.current_direction = CFG.UP
            self.strategy_index = CFG.GHOST_CAGE_STRATEGY
    def changeSpriteState(self):

        if self.new_direction == CFG.UP:
            self.current_sprite_state = CFG.GHOST_SPRITE_UP
            self.spriteAnimationFlag = 1
        elif self.new_direction == CFG.LEFT:
            self.current_sprite_state = CFG.GHOST_SPRITE_LEFT
            self.spriteAnimationFlag = 1
        elif self.new_direction == CFG.DOWN:
            self.current_sprite_state = CFG.GHOST_SPRITE_DOWN
            self.spriteAnimationFlag = 1
        elif self.new_direction == CFG.RIGHT:
            self.current_sprite_state = CFG.GHOST_SPRITE_RIGHT
            self.spriteAnimationFlag = 1


    def animateGhost(self, IsPowerPillEnding):
        if self.strategy_index == CFG.GHOST_EATEN_STRATEGY or self.strategy_index == CFG.GHOST_ENTERING_CAGE_STRATEGY:
            self.sprite.changeOnEaten()
        elif self.IsFrightened:
            self.sprite.changeOnFrightened(IsPowerPillEnding)
        else:
            self.sprite.changeOnNormal()

    def changeSpriteAnimationFlag(self):

        if self.spriteAnimationFlag == 1:
            self.current_sprite_state += 1
            self.spriteAnimationFlag = 2

        elif self.spriteAnimationFlag == 2:

            self.current_sprite_state -= 1
            self.spriteAnimationFlag = 1

        self.changeCurrentSprite()

    def changeCurrentSprite(self):
        sprite_name = "red_ghost"
        if self.ghost_type == CFG.RED_GHOST:
            sprite_name = "red_ghost"
        elif self.ghost_type == CFG.CYAN_GHOST:
            sprite_name = "cyan_ghost"
        elif self.ghost_type == CFG.ORANGE_GHOST:
            sprite_name = "orange_ghost"
        elif self.ghost_type == CFG.PINK_GHOST:
            sprite_name = "pink_ghost"

        self.changeSprite(sprite_name, self.current_sprite_state)





    def changeSprite(self, sprite_name, sprite_state):
        self.current_sprite = pygame.image.load(f"GhostsSprites/{sprite_name} ({sprite_state}).png")
        self.current_sprite = pygame.transform.scale(self.current_sprite,
                                                     (CFG.SQUARE_SIZE * 1.5, CFG.SQUARE_SIZE * 1.5))

    def changeSpriteWhenEaten(self):
        sprite_name = "eaten_ghost"
        self.changeSprite(sprite_name, 1)

    def changeFrightenedSpriteState(self):

        if self.frightened_sprite_state == 1:
            self.frightened_sprite_state = 2
        elif self.frightened_sprite_state == 2:
            self.frightened_sprite_state = 1

        sprite_name = "frightened_ghost"
        self.changeSprite(sprite_name, self.frightened_sprite_state)

    def chooseCornerToMove(self):

        corner = None
        if self.ghost_type == CFG.RED_GHOST:
            corner = CFG.RIGHT_UPPER_CORNER
        elif self.ghost_type == CFG.CYAN_GHOST:
            corner = CFG.RIGHT_BOTTOM_CORNER
        elif self.ghost_type == CFG.ORANGE_GHOST:
            corner = CFG.LEFT_BOTTOM_CORNER
        elif self.ghost_type == CFG.PINK_GHOST:
            corner = CFG.LEFT_UPPER_CORNER

        return corner

    def frightenedModeInvertCheck(self, game_board):
        if self.strategy_index != CFG.GHOST_FRIGHTENED_STRATEGY:
            return
        if not self.frightenedModeInvertedDir:

            self.current_direction = self.invertedDirection()
            if self.checkIfWallInFront(self.rounded_column, self.rounded_row, game_board):
                self.current_direction = self.invertedDirection()

            self.frightenedModeInvertedDir = True

    def chooseNewDirectionToMove(self, target, game_board):

        if CFG.BORDER_LEFT <= self.current_column < CFG.BORDER_RIGHT:

            self.new_direction = self.calculateDirectionToTarget(target, game_board)

            if self.canChangeDirBeetweenWalls(self.rounded_column, self.rounded_row, game_board):

                if self.new_direction != self.current_direction:
                    self.sprite.newDirectionSpriteChange(self.new_direction)

                self.current_direction = self.new_direction

            if self.checkIfWallInFront(self.rounded_column, self.rounded_row, game_board) is False:
                self.changePositionBySpeed(self.speed)

    # Executing current Strategy



    def setStrategy(self, _strategy):

        self.strategy = _strategy

    def setGhostStrategyIndexToChase(self):
        if self.ghost_type == CFG.RED_GHOST:
            self.strategy_index = CFG.GHOST_BLINKY_CHASE_STRATEGY

        elif self.ghost_type == CFG.PINK_GHOST:
            self.strategy_index = CFG.GHOST_PINKY_CHASE_STRATEGY

        elif self.ghost_type == CFG.CYAN_GHOST:
            self.strategy_index = CFG.GHOST_INKY_CHASE_STRATEGY

        elif self.ghost_type == CFG.ORANGE_GHOST:
            self.strategy_index = CFG.GHOST_CLYDE_CHASE_STRATEGY

    def setGhostStrategyIndexToScatter(self):
        self.strategy_index = CFG.GHOST_SCATTER_STRATEGY



    def convertDirectionToConstant(self, direction):

        if direction == 1:
            return CFG.UP
        elif direction == 2:
            return CFG.LEFT
        elif direction == 3:
            return CFG.DOWN
        elif direction == 4:
            return CFG.RIGHT
        else:
            return None

    def calculateDistancesToTarget(self, target, distances_to_target, game_board):
        target_col, target_row = target[0], target[1]

        IsWallAbove = (game_board.getTileValue(self.rounded_column, self.rounded_row - 1) == CFG.WALL)
        IsWallOnTheLeft = (game_board.getTileValue(self.rounded_column - 1, self.rounded_row) == CFG.WALL)
        IsWallBelow = (game_board.getTileValue(self.rounded_column, self.rounded_row + 1) == CFG.WALL)
        IsWallOnTheRight = (game_board.getTileValue(self.rounded_column + 1, self.rounded_row) == CFG.WALL)


        if IsWallAbove is False:
            distances_to_target[0]['distance'] = self.calculateDistanceBetweenObjects(self.rounded_column,
                                                                                      self.rounded_row - 1,
                                                                                      target_col,
                                                                                      target_row)
        if IsWallOnTheLeft is False:
            distances_to_target[1]['distance'] = self.calculateDistanceBetweenObjects(self.rounded_column - 1,
                                                                                      self.rounded_row,
                                                                                      target_col,
                                                                                      target_row)

        if IsWallBelow is False:
            distances_to_target[2]['distance'] = self.calculateDistanceBetweenObjects(self.rounded_column,
                                                                                      self.rounded_row + 1,
                                                                                      target_col,
                                                                                      target_row)

        if IsWallOnTheRight is False:
            distances_to_target[3]['distance'] = self.calculateDistanceBetweenObjects(self.rounded_column + 1,
                                                                                      self.rounded_row,
                                                                                      target_col,
                                                                                      target_row)

        return distances_to_target

    def calculateDirectionToTarget(self, target, game_board):
        calculated_direction = CFG.UP

        # ghost_col, ghost_row = self.calculateRoundedColumnRow()
        distances_to_target = [{'distance': 1000, 'direction': CFG.UP}, {'distance': 1000, 'direction': CFG.LEFT},
                               {'distance': 1000, 'direction': CFG.DOWN}, {'distance': 1000, 'direction': CFG.RIGHT}]

        distances_to_target = self.calculateDistancesToTarget(target, distances_to_target, game_board)

        distances_to_target = sorted(distances_to_target, key=itemgetter('distance'))

        calculated_direction = distances_to_target[0]['direction']

        for i in range(4):
            if calculated_direction == self.invertedDirection():
                calculated_direction = distances_to_target[i]['direction']
            else:
                break

            # print(self.cur_dir)
        return calculated_direction
