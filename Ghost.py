import MovingObject
import pygame
from MovingObject import MovingObject
import ConstantsForGame as CFG
import random
from operator import itemgetter
from MusicSystem import MusicSystem

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
        self.release_state = CFG.IN_CAGE_MODE

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

    def releaseGhost(self):

        point_to_move = (13.5, 14)


        ghost_coords = (self.cur_column, self.cur_row)

        if self.ghost_type == CFG.ORANGE_GHOST:
            if (ghost_coords != point_to_move):

                self.cur_column = CFG.ORANGE_GHOST_ROUTE[self.release_state][0]
                self.cur_row = CFG.ORANGE_GHOST_ROUTE[self.release_state][1]
                self.release_state += 1
            else:
                self.current_mode = CFG.GHOST_SCATTER_MODE

        elif self.ghost_type == CFG.CYAN_GHOST:
            if (ghost_coords != point_to_move):

                self.cur_column = CFG.CYAN_GHOST_ROUTE[self.release_state][0]
                self.cur_row = CFG.CYAN_GHOST_ROUTE[self.release_state][1]
                self.release_state += 1
            else:
                self.current_mode = CFG.GHOST_CHASE_MODE

        elif self.ghost_type == CFG.PINK_GHOST:
            if (ghost_coords != point_to_move):

                self.cur_column = CFG.PINK_GHOST_ROUTE[self.release_state][0]
                self.cur_row = CFG.PINK_GHOST_ROUTE[self.release_state][1]
                self.release_state += 1
            else:
                self.current_mode = CFG.GHOST_SCATTER_MODE
        '''
        #orange_ghost_route = [(13.5, 17)]
        if self.ghost_type == CFG.CYAN_GHOST:
            print(self.cur_column, self.cur_row)


        if self.release_state == CFG.IN_CAGE_MODE:
            self.cur_dir = self.calculateTargetPath(point1_to_move, game_board)
            ghost_coords = (self.cur_column, self.cur_row)
            if ghost_coords == point1_to_move:
                self.release_state = CFG.IN_POINT1

        elif self.release_state == CFG.IN_POINT1:
            self.cur_dir = self.calculateTargetPath(point2_to_move, game_board)
            ghost_coords = (self.cur_column, self.cur_row)

            print ((abs(self.cur_column - 13.5) ** 2) + ((abs((self.cur_row) - 14)) ** 2))

            if ((abs(self.cur_column - 13.5) ** 2) + ((abs((self.cur_row) - 14)) ** 2)) < 1:
                self.cur_column = 13.5
                self.cur_row = 14
                self.release_state = CFG.FULLY_RELEASED
                self.current_mode = CFG.GHOST_SCATTER_MODE
                print("GOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO")
                print(game_board.getTileValue(13, 15), game_board.getTileValue(14, 15))
                game_board.setTileValue(13, 15, 3)
                game_board.setTileValue(14, 15, 3)
                print(game_board.getTileValue(13, 15), game_board.getTileValue(14, 15))

        self.changeGhostPositon()

        #[(13.5, 17), (13.5, 14)]
        pass
        '''

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
            self.ghostCageMode(col, row, game_board)
        elif(self.current_mode == CFG.GHOST_RELEASING_MODE):
            self.releaseGhost()

        elif (self.current_mode == CFG.GHOST_SCATTER_MODE):
            self.scatterMode(col, row, game_board)

        elif (self.current_mode == CFG.GHOST_CHASE_MODE):
            self.chaseMode(pacman, col, row, game_board)

        if self.checkIfWallIsNext(col, row, game_board) == True:
            return


        elif self.cur_column < CFG.BORDER_LEFT:
            self.cur_column = 26.75
            return CFG.CROSSED_BORDER

        elif self.cur_column >= CFG.BORDER_RIGHT:
            self.cur_column = 0
            return CFG.CROSSED_BORDER

    def ghostCageMode(self, col, row, game_board):
        if self.cur_dir == CFG.UP:
            self.cur_row -= 0.25
            col, row = self.calculateColumnAndRow()
            if self.checkIfWallIsNext(col, row, game_board):
                self.cur_dir *= -1  # OPPOSITE DIRECTION
            self.cur_row += 0.25
        elif self.cur_dir == CFG.DOWN:
            self.cur_row += 0.25
            col, row = self.calculateColumnAndRow()
            if self.checkIfWallIsNext(col, row, game_board):
                self.cur_dir *= -1  # OPPOSITE DIRECTION
            self.cur_row -= 0.25

        self.changeGhostPositon()
        # print()

        pass

    def chaseMode(self, pacman, col, row, game_board):

        target = (pacman.cur_column, pacman.cur_row)

        if self.cur_column >= CFG.BORDER_LEFT and self.cur_column < CFG.BORDER_RIGHT:
            self.new_dir = self.calculateTargetPath(target, game_board)

            if self.canChangeDirBeetweenWalls(col, row, game_board) == True:
                self.cur_dir = self.new_dir

            if self.checkIfWallIsNext(col, row, game_board) != True:
                self.changeGhostPositon()



    def scatterMode(self, col, row, game_board):

        target = None
        if self.ghost_type == CFG.RED_GHOST:
            target = CFG.RIGHT_UPPER_CORNER
        elif self.ghost_type == CFG.PINK_GHOST:
            target = CFG.LEFT_UPPER_CORNER
        elif self.ghost_type == CFG.CYAN_GHOST:
            target = CFG.RIGHT_BOTTOM_CORNER
        elif self.ghost_type == CFG.ORANGE_GHOST:
            target = CFG.LEFT_BOTTOM_CORNER


        if self.cur_column >= CFG.BORDER_LEFT and self.cur_column < CFG.BORDER_RIGHT:
            self.new_dir = self.calculateTargetPath(target, game_board)

            if self.canChangeDirBeetweenWalls(col, row, game_board) == True:
                self.cur_dir = self.new_dir


            if self.checkIfWallIsNext(col, row, game_board) != True:
                self.changeGhostPositon()



    def frightenedMode(self):
        pass

    def calculateTargetPath(self, target, game_board):
        calculated_direction = CFG.UP
        target_col, target_row = target[0], target[1]

        ghost_col, ghost_row = self.calculateColumnAndRow()
        distances_to_target = [{'distance' : 1000, 'direction': 1}, {'distance' : 1000, 'direction': 2},
                               {'distance' : 1000, 'direction': -1}, {'distance' : 1000, 'direction': -2}]

        '''
        isReleased = self.current_mode is CFG.FULLY_RELEASED

        isReleased and game_board.getTileValue(ghost_col, ghost_row - 1) != CFG.CAGE_GATE

        IsCageGateAbove = game_board.getTileValue(ghost_col, ghost_row - 1) == CFG.CAGE_GATE
        IsCageGateOnTheLeft = game_board.getTileValue(ghost_col - 1, ghost_row) == CFG.CAGE_GATE
        IsCageGateBelow = game_board.getTileValue(ghost_col, ghost_row + 1) == CFG.CAGE_GATE
        IsCageGateOnTheRight = game_board.getTileValue(ghost_col + 1, ghost_row) == CFG.CAGE_GATE
        '''

        IsWallAbove = game_board.getTileValue(ghost_col, ghost_row - 1) == CFG.WALL
        IsWallOnTheLeft = game_board.getTileValue(ghost_col - 1, ghost_row) == CFG.WALL
        IsWallBelow = game_board.getTileValue(ghost_col, ghost_row + 1) == CFG.WALL
        IsWallOnTheRight = game_board.getTileValue(ghost_col + 1, ghost_row) == CFG.WALL


        if IsWallAbove is False:
            distances_to_target[0]['distance'] = ((abs(ghost_col - target_col) ** 2) + ((abs((ghost_row - 1) - target_row)) ** 2))

        if IsWallOnTheLeft is False:
            distances_to_target[1]['distance'] = ((abs((ghost_col - 1) - target_col) ** 2) + ((abs(ghost_row - target_row)) ** 2))

        if IsWallBelow is False:
            distances_to_target[2]['distance'] = ((abs(ghost_col - target_col) ** 2) + ((abs((ghost_row + 1) - target_row)) ** 2))

        if IsWallOnTheRight is False:
            distances_to_target[3]['distance'] = ((abs((ghost_col+1) - target_col) ** 2) + ((abs(ghost_row - target_row)) ** 2))


        distances_to_target = sorted(distances_to_target, key=itemgetter('distance'))

        calculated_direction = distances_to_target[0]['direction']


        for i in range(4):
            if calculated_direction == (self.cur_dir * -1):
                calculated_direction = distances_to_target[i]['direction']
            else:
                break

            #print(self.cur_dir)
        return calculated_direction
