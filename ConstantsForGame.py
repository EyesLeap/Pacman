import pygame.image

UP = 1
DOWN = -1
LEFT = 2
RIGHT = -2

GAME_BOARD_WIDTH = 28
GAME_BOARD_HEIGHT = 31

SQUARE_SIZE = 25
PACMAN_SPEED = 1/4
GHOST_SPEED = 1/8
GHOST_SPEED_NORMAL = 1/8
GHOST_SPEED_EATEN = 1/4

OPPOSITE_DIRECTION = -1

BORDER_LEFT = 0
BORDER_RIGHT = 27

EMPTY_TILE = 1
PELLET = 2
WALL = 3
CAGE_GATE = 5
POWER_PILL = 6

GAME_FPS = 50
GAME_SECOND = GAME_FPS

CROSSED_TUNNEL = 1

PELLET_COLOR = (222, 161, 133)
BLACK_COLOR = (0,0,0)

RED_GHOST = 1
CYAN_GHOST = 2
ORANGE_GHOST = 3
PINK_GHOST = 4

GHOST_SPRITE_RIGHT = 1
GHOST_SPRITE_DOWN = 3
GHOST_SPRITE_LEFT = 5
GHOST_SPRITE_UP = 7

GHOST_CAGE_STRATEGY = 0
GHOST_SCATTER_STRATEGY = 1
GHOST_CHASE_STRATEGY = 2
GHOST_FRIGHTENED_STRATEGY = 3
GHOST_EATEN_STRATEGY = 4
GHOST_RELEASING_STRATEGY = 5
GHOST_ENTERING_CAGE_STRATEGY = 6
GHOST_BLINKY_CHASE_STRATEGY = 7
GHOST_PINKY_CHASE_STRATEGY = 8
GHOST_INKY_CHASE_STRATEGY = 9
GHOST_CLYDE_CHASE_STRATEGY = 10

RIGHT_UPPER_CORNER = (27,4)
LEFT_UPPER_CORNER = (1,4)
RIGHT_BOTTOM_CORNER = (27,31)
LEFT_BOTTOM_CORNER = (1,31)

IN_CAGE_MODE = 0
FULLY_RELEASED = 0


ALL_GHOSTS_SCATTER_MODE = 1
ALL_GHOSTS_CHASE_MODE = 2


PACMAN_MOUTH_CLOSED = 0
PACMAN_MOUTH_OPENED1 = 1
PACMAN_MOUTH_OPENED2 = 2

SIREN_MUSIC1 = 1

SCATTER_MODE_DURATION = 5
CHASE_MODE_DURATION = 20


original_game_board = [
        [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
        [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
        [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
        [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
        [3, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3, 3, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3],
        [3, 2, 3, 3, 3, 3, 2, 3, 3, 3, 3, 3, 2, 3, 3, 2, 3, 3, 3, 3, 3, 2, 3, 3, 3, 3, 2, 3],
        [3, 6, 3, 3, 3, 3, 2, 3, 3, 3, 3, 3, 2, 3, 3, 2, 3, 3, 3, 3, 3, 2, 3, 3, 3, 3, 6, 3],
        [3, 2, 3, 3, 3, 3, 2, 3, 3, 3, 3, 3, 2, 3, 3, 2, 3, 3, 3, 3, 3, 2, 3, 3, 3, 3, 2, 3],
        [3, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3],
        [3, 2, 3, 3, 3, 3, 2, 3, 3, 2, 3, 3, 3, 3, 3, 3, 3, 3, 2, 3, 3, 2, 3, 3, 3, 3, 2, 3],
        [3, 2, 3, 3, 3, 3, 2, 3, 3, 2, 3, 3, 3, 3, 3, 3, 3, 3, 2, 3, 3, 2, 3, 3, 3, 3, 2, 3],
        [3, 2, 2, 2, 2, 2, 2, 3, 3, 2, 2, 2, 2, 3, 3, 2, 2, 2, 2, 3, 3, 2, 2, 2, 2, 2, 2, 3],
        [3, 3, 3, 3, 3, 3, 2, 3, 3, 3, 3, 3, 1, 3, 3, 1, 3, 3, 3, 3, 3, 2, 3, 3, 3, 3, 3, 3],
        [3, 3, 3, 3, 3, 3, 2, 3, 3, 3, 3, 3, 1, 3, 3, 1, 3, 3, 3, 3, 3, 2, 3, 3, 3, 3, 3, 3],
        [3, 3, 3, 3, 3, 3, 2, 3, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 3, 2, 3, 3, 3, 3, 3, 3],
        [3, 3, 3, 3, 3, 3, 2, 3, 3, 1, 3, 3, 3, 3, 3, 3, 3, 3, 1, 3, 3, 2, 3, 3, 3, 3, 3, 3],
        [3, 3, 3, 3, 3, 3, 2, 3, 3, 1, 3, 4, 4, 4, 4, 4, 4, 3, 1, 3, 3, 2, 3, 3, 3, 3, 3, 3],
        [1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 3, 4, 4, 4, 4, 4, 4, 3, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1], # Middle Lane Row: 17
        [3, 3, 3, 3, 3, 3, 2, 3, 3, 1, 3, 4, 4, 4, 4, 4, 4, 3, 1, 3, 3, 2, 3, 3, 3, 3, 3, 3],
        [3, 3, 3, 3, 3, 3, 2, 3, 3, 1, 3, 3, 3, 3, 3, 3, 3, 3, 1, 3, 3, 2, 3, 3, 3, 3, 3, 3],
        [3, 3, 3, 3, 3, 3, 2, 3, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 3, 2, 3, 3, 3, 3, 3, 3],
        [3, 3, 3, 3, 3, 3, 2, 3, 3, 1, 3, 3, 3, 3, 3, 3, 3, 3, 1, 3, 3, 2, 3, 3, 3, 3, 3, 3],
        [3, 3, 3, 3, 3, 3, 2, 3, 3, 1, 3, 3, 3, 3, 3, 3, 3, 3, 1, 3, 3, 2, 3, 3, 3, 3, 3, 3],
        [3, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3, 3, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3],
        [3, 2, 3, 3, 3, 3, 2, 3, 3, 3, 3, 3, 2, 3, 3, 2, 3, 3, 3, 3, 3, 2, 3, 3, 3, 3, 2, 3],
        [3, 2, 3, 3, 3, 3, 2, 3, 3, 3, 3, 3, 2, 3, 3, 2, 3, 3, 3, 3, 3, 2, 3, 3, 3, 3, 2, 3],
        [3, 6, 2, 2, 3, 3, 2, 2, 2, 2, 2, 2, 2, 1, 1, 2, 2, 2, 2, 2, 2, 2, 3, 3, 2, 2, 6, 3],  # (13, 25)
        [3, 3, 3, 2, 3, 3, 2, 3, 3, 2, 3, 3, 3, 3, 3, 3, 3, 3, 2, 3, 3, 2, 3, 3, 2, 3, 3, 3],
        [3, 3, 3, 2, 3, 3, 2, 3, 3, 2, 3, 3, 3, 3, 3, 3, 3, 3, 2, 3, 3, 2, 3, 3, 2, 3, 3, 3],
        [3, 2, 2, 2, 2, 2, 2, 3, 3, 2, 2, 2, 2, 3, 3, 2, 2, 2, 2, 3, 3, 2, 2, 2, 2, 2, 2, 3],
        [3, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 2, 3, 3, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 2, 3],
        [3, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 2, 3, 3, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 2, 3],
        [3, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3],
        [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
        [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
        [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
    ]

#When leaving their cage, the ghosts move along a certain route:

RED_GHOST_ROUTE = [()] * 25
ORANGE_GHOST_ROUTE = [()] * 25
PINK_GHOST_ROUTE = [()] * 42
CYAN_GHOST_ROUTE = [()] * 42


CAGE_RELEASING_ROUTE1_LENGTH = 17
CAGE_RELEASING_ROUTE2_LENGTH = 25

for i in range (CAGE_RELEASING_ROUTE1_LENGTH):
        CYAN_GHOST_ROUTE[i] = (11.5 + (i * 0.125), 17)
        PINK_GHOST_ROUTE[i] = (15.5 - (i * 0.125), 17)


for i in range(CAGE_RELEASING_ROUTE2_LENGTH):
        RED_GHOST_ROUTE[i] = (13.5, 17 - (i * 0.125))
        ORANGE_GHOST_ROUTE[i] = (13.5, 17 - (i * 0.125))
        PINK_GHOST_ROUTE[i + CAGE_RELEASING_ROUTE1_LENGTH] = (13.5, 17 - (i * 0.125))
        CYAN_GHOST_ROUTE[i + CAGE_RELEASING_ROUTE1_LENGTH] = (13.5, 17 - (i * 0.125))


# --------------------------------------------------------------


BACK_TO_CAGE_ROUTE = [()] * 25
BACK_TO_CAGE_ROUTE_LENGTH = 25

for i in range(CAGE_RELEASING_ROUTE2_LENGTH):
        BACK_TO_CAGE_ROUTE[i] = (13.5, 14 + (i * 0.125))