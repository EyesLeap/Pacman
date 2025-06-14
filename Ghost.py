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
        params = CFG.GHOST_START_PARAMS.get(self.ghost_type)
        if not params:
            return

        self.current_column, self.current_row = params["position"]
        sprite_path = f"GhostsSprites/{params['sprite_name']} ({params['sprite_file_index']}).png"
        self.sprite = GhostSprite(sprite_path, self.ghost_type, params["sprite_file_index"])
        self.current_sprite_state = params["sprite_state"]

        self.current_sprite = pygame.image.load(sprite_path)
        self.current_sprite = pygame.transform.scale(
            self.current_sprite,
            (int(CFG.SQUARE_SIZE * 3 / 2), int(CFG.SQUARE_SIZE * 3 / 2))
        )

        self.current_direction = params["direction"]
        self.strategy_index = params["strategy"]

    def changeSpriteState(self):
        direction_to_sprite = {
            CFG.UP: CFG.GHOST_SPRITE_UP,
            CFG.LEFT: CFG.GHOST_SPRITE_LEFT,
            CFG.DOWN: CFG.GHOST_SPRITE_DOWN,
            CFG.RIGHT: CFG.GHOST_SPRITE_RIGHT,
        }
        if self.new_direction in direction_to_sprite:
            self.current_sprite_state = direction_to_sprite[self.new_direction]
            self.spriteAnimationFlag = 1

    def animateGhost(self, IsPowerPillEnding):
        if self.strategy_index in (CFG.GHOST_EATEN_STRATEGY, CFG.GHOST_ENTERING_CAGE_STRATEGY):
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
        sprite_names = {
            CFG.RED_GHOST: "red_ghost",
            CFG.CYAN_GHOST: "cyan_ghost",
            CFG.ORANGE_GHOST: "orange_ghost",
            CFG.PINK_GHOST: "pink_ghost"
        }
        sprite_name = sprite_names.get(self.ghost_type, "red_ghost")
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
        corners = {
            CFG.RED_GHOST: CFG.RIGHT_UPPER_CORNER,
            CFG.CYAN_GHOST: CFG.RIGHT_BOTTOM_CORNER,
            CFG.ORANGE_GHOST: CFG.LEFT_BOTTOM_CORNER,
            CFG.PINK_GHOST: CFG.LEFT_UPPER_CORNER,
        }
        return corners.get(self.ghost_type)

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

    def setStrategy(self, _strategy):
        self.strategy = _strategy

    def setGhostStrategyIndexToChase(self):
        chase_strategies = {
            CFG.RED_GHOST: CFG.GHOST_BLINKY_CHASE_STRATEGY,
            CFG.PINK_GHOST: CFG.GHOST_PINKY_CHASE_STRATEGY,
            CFG.CYAN_GHOST: CFG.GHOST_INKY_CHASE_STRATEGY,
            CFG.ORANGE_GHOST: CFG.GHOST_CLYDE_CHASE_STRATEGY,
        }

        self.strategy_index = chase_strategies.get(self.ghost_type)

    def setGhostStrategyIndexToScatter(self):
        self.strategy_index = CFG.GHOST_SCATTER_STRATEGY

    def convertDirectionToConstant(self, direction):
        return {
            1: CFG.UP,
            2: CFG.LEFT,
            3: CFG.DOWN,
            4: CFG.RIGHT
        }.get(direction)

    def calculateDistancesToTarget(self, target, distances_to_target, game_board):
        target_col, target_row = target

        directions = {
            0: (0, -1),  # Up
            1: (-1, 0),  # Left
            2: (0, 1),  # Down
            3: (1, 0)  # Right
        }

        for index, (dx, dy) in directions.items():
            new_col = self.rounded_column + dx
            new_row = self.rounded_row + dy

            if game_board.getTileValue(new_col, new_row) != CFG.WALL:
                distances_to_target[index]['distance'] = self.calculateDistanceBetweenObjects(
                    new_col, new_row, target_col, target_row
                )

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

        return calculated_direction
