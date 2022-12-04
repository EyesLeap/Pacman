import MovingObject
import pygame
from MovingObject import MovingObject
import ConstantsForGame as CFG
import random
from operator import itemgetter

class Ghost(MovingObject):
    def __init__(self, ghost_type):
        self.current_sprite_state = 1  # 1-8 Up, Down, Left, Right
        self.current_sprite = None
        self.ghost_type = ghost_type
        self.current_mode = CFG.GHOST_CAGE_MODE
        self.target_to_move = None
        self.new_dir = None
        self.counter = 0
        self.target = None

    def setStartPosition(self):
        if self.ghost_type == CFG.RED_GHOST:
            self.cur_column = 13.5
            self.cur_row = 14
            self.current_sprite = pygame.image.load(f"GhostsSprites/red_ghost (5).png")
            self.current_sprite = pygame.transform.scale(self.current_sprite,
                                                         (int(CFG.SQUARE_SIZE * 3 / 2), int(CFG.SQUARE_SIZE * 3 / 2)))
            self.cur_dir = CFG.LEFT
            self.current_mode = CFG.GHOST_SCATTER_MODE

        if self.ghost_type == CFG.CYAN_GHOST:
            self.cur_column = 11.5
            self.cur_row = 17
            self.current_sprite = pygame.image.load(f"GhostsSprites/cyan_ghost (7).png")
            self.current_sprite = pygame.transform.scale(self.current_sprite,
                                                         (int(CFG.SQUARE_SIZE * 3 / 2), int(CFG.SQUARE_SIZE * 3 / 2)))
            self.cur_dir = CFG.UP


        elif self.ghost_type == CFG.ORANGE_GHOST:
            self.cur_column = 13.5
            self.cur_row = 17
            self.current_sprite = pygame.image.load(f"GhostsSprites/orange_ghost (3).png")
            self.current_sprite = pygame.transform.scale(self.current_sprite,
                                                         (int(CFG.SQUARE_SIZE * 3 / 2), int(CFG.SQUARE_SIZE * 3 / 2)))
            self.cur_dir = CFG.DOWN


        elif self.ghost_type == CFG.PINK_GHOST:
            self.cur_column = 15.5
            self.cur_row = 17
            self.current_sprite = pygame.image.load(f"GhostsSprites/pink_ghost (7).png")
            self.current_sprite = pygame.transform.scale(self.current_sprite,
                                                         (int(CFG.SQUARE_SIZE * 3 / 2), int(CFG.SQUARE_SIZE * 3 / 2)))
            self.cur_dir = CFG.UP

    def changeSpriteState(self, change):
        if change == 1:
            self.current_sprite_state += 1
        elif change == 0:
            self.current_sprite_state -= 1

    def changeGhostPositon(self):
        if self.cur_dir == CFG.LEFT:
            self.cur_column -= CFG.GHOST_SPEED
        elif self.cur_dir == CFG.RIGHT:
            self.cur_column += CFG.GHOST_SPEED
        elif self.cur_dir == CFG.DOWN:
            self.cur_row += CFG.GHOST_SPEED
        elif self.cur_dir == CFG.UP:
            self.cur_row -= CFG.GHOST_SPEED

    def move(self, pacman, game_board):
        col, row = self.calculateColumnAndRow()

        if (self.current_mode == CFG.GHOST_CAGE_MODE):
            self.ghostCageMode(col, row)

        elif (self.current_mode == CFG.GHOST_SCATTER_MODE):
            self.scatterMode(col, row, pacman, game_board)

        if self.checkIfWallIsNext(col, row) == True:
            return


        elif self.cur_column < CFG.BORDER_LEFT:
            self.cur_column = 26.75
            return CFG.CROSSED_BORDER

        elif self.cur_column >= CFG.BORDER_RIGHT:
            self.cur_column = 0
            return CFG.CROSSED_BORDER

    def ghostCageMode(self, col, row):
        if self.cur_dir == CFG.UP:
            self.cur_row -= 0.25
            col, row = self.calculateColumnAndRow()
            if self.checkIfWallIsNext(col, row):
                self.cur_dir *= -1  # OPPOSITE DIRECTION
            self.cur_row += 0.25
        elif self.cur_dir == CFG.DOWN:
            self.cur_row += 0.25
            col, row = self.calculateColumnAndRow()
            if self.checkIfWallIsNext(col, row):
                self.cur_dir *= -1  # OPPOSITE DIRECTION
            self.cur_row -= 0.25
            '''if self.ghost_type == CFG.CYAN_GHOST:
                print("CHANGED")
                print(self.cur_row)'''

        self.changeGhostPositon()
        # print()

        pass

    def chaseMode(self, col, row):
        pass

    def scatterMode(self, col, row, pacman, game_board):
        if self.cur_column >= CFG.BORDER_LEFT and self.cur_column < CFG.BORDER_RIGHT:
            #if self.canChangeDirBeetweenWalls(col, row) is True:
            #print(col, row)


            self.new_dir = self.calculateTargetPath(pacman, game_board)
            #print(self.cur_dir)
            if self.canChangeDirBeetweenWalls(col, row):

                self.cur_dir = self.new_dir
            else:
                print("НЕЛЬЗЯЯЯ")




            ''''''
            if self.checkIfWallIsNext(col, row) != True:
                self.changeGhostPositon()

        pass

    def frightenedMode(self):
        pass

    def calculateTargetPath(self, target, game_board):
        calculated_direction = None
        if self.ghost_type == CFG.RED_GHOST:
            target_col, target_row = 27, 4

        #target_col, target_row = target.cur_column, target.cur_row
        ghost_col, ghost_row = self.calculateColumnAndRow()
        distances_to_target = [{'distance' : 1000, 'direction': 1}, {'distance' : 1000, 'direction': 2},
                               {'distance' : 1000, 'direction': -1}, {'distance' : 1000, 'direction': -2}]

        if game_board.getTileValue(ghost_col, ghost_row - 1) != CFG.WALL:
            distances_to_target[0]['distance'] = ((abs(ghost_col - target_col) ** 2) + ((abs((ghost_row - 1) - target_row)) ** 2))
        if game_board.getTileValue(ghost_col - 1, ghost_row) != CFG.WALL:
            distances_to_target[1]['distance'] = ((abs((ghost_col - 1) - target_col) ** 2) + ((abs(ghost_row - target_row)) ** 2))
        if game_board.getTileValue(ghost_col, ghost_row + 1) != CFG.WALL:
            distances_to_target[2]['distance'] = ((abs(ghost_col - target_col) ** 2) + ((abs((ghost_row + 1) - target_row)) ** 2))
        if game_board.getTileValue(ghost_col + 1, ghost_row) != CFG.WALL:
            distances_to_target[3]['distance'] = ((abs((ghost_col+1) - target_col) ** 2) + ((abs(ghost_row - target_row)) ** 2))

        #distances_to_target.sort()
        distances_to_target = sorted(distances_to_target, key=itemgetter('distance'))

        calculated_direction = distances_to_target[0]['direction']





        for i in range(4):
            if calculated_direction == (self.cur_dir * -1):
                calculated_direction = distances_to_target[i]['direction']
            else:
                break
        #print("Направление 1: " + str(distances_to_target[0]['direction']))
        #print("Дистанция 1: " + str(distances_to_target[0]['distance']))
        #print("Направление 2: " + str(distances_to_target[1]['direction']))
        #print("Дистанция 2: " + str(distances_to_target[1]['distance']))
        #print("Направление 3: " + str(distances_to_target[2]['direction']))
        #print("Дистанция 3: " + str(distances_to_target[2]['distance']))
        #print("Направление 4: " + str(distances_to_target[3]['direction']))
        #print("Дистанция 4: " + str(distances_to_target[3]['distance']))
        #print("Направление текущее: " + str(self.cur_dir))
        #print("Направление новое: " + str(self.new_dir))
        #distances_to_target.sort(reverse=True)

        if self.ghost_type == CFG.RED_GHOST:
            #print(self.cur_dir)
            return calculated_direction
