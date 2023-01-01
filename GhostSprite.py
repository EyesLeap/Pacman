import pygame
#import GhostStrategies.GhostStrategy
import ConstantsForGame as CFG

class GhostSprite (pygame.sprite.Sprite):


    def __init__(self, sprite_location, ghost_type, normal_sprite_state):
        self.normal_sprite_state = normal_sprite_state  # Normal sprite when SCATTER_MODE/CHASE_MODE on
        self.normalSpriteFLag = 0
        self.ghost_type = ghost_type

        self.frightened_sprite_state = 1
        self.image = pygame.image.load(sprite_location)
        self.image = pygame.transform.scale(self.image, (CFG.SQUARE_SIZE * 1.5, CFG.SQUARE_SIZE * 1.5))
        self.current_sprite = None



    def newDirectionSpriteChange(self, new_direction):

        self.normalSpriteFLag = 0

        if new_direction == CFG.UP:
            self.normal_sprite_state = CFG.GHOST_SPRITE_UP

        elif new_direction == CFG.LEFT:
            self.normal_sprite_state = CFG.GHOST_SPRITE_LEFT

        elif new_direction == CFG.DOWN:
            self.normal_sprite_state = CFG.GHOST_SPRITE_DOWN

        elif new_direction == CFG.RIGHT:
            self.normal_sprite_state = CFG.GHOST_SPRITE_RIGHT


    def switchNormalSpriteFlag(self):

        if self.normalSpriteFLag == 0:
            self.normal_sprite_state += 1
            self.normalSpriteFLag = 1

        elif self.normalSpriteFLag == 1:
            self.normal_sprite_state -= 1
            self.normalSpriteFLag = 0


    def switchFrightenedSpriteState(self, IsPowerPillEnding):

        if IsPowerPillEnding:
            if self.frightened_sprite_state == 2:
                self.frightened_sprite_state = 3

            elif self.frightened_sprite_state == 3:
                self.frightened_sprite_state = 4

            elif self.frightened_sprite_state == 4:
                self.frightened_sprite_state = 1


        if self.frightened_sprite_state == 1:
            self.frightened_sprite_state = 2

        elif self.frightened_sprite_state == 2:
            self.frightened_sprite_state = 1




    def changeOnNormal(self):
        self.switchNormalSpriteFlag()

        sprite_name = "red_ghost"
        if self.ghost_type == CFG.RED_GHOST:
            sprite_name = "red_ghost"
        elif self.ghost_type == CFG.CYAN_GHOST:
            sprite_name = "cyan_ghost"
        elif self.ghost_type == CFG.ORANGE_GHOST:
            sprite_name = "orange_ghost"
        elif self.ghost_type == CFG.PINK_GHOST:
            sprite_name = "pink_ghost"

        self.setCurrentImage(sprite_name, self.normal_sprite_state)

    def changeOnFrightened(self, IsPowerPillEnding):

        self.switchFrightenedSpriteState(IsPowerPillEnding)

        sprite_name = "frightened_ghost"
        self.setCurrentImage(sprite_name, self.frightened_sprite_state)



    def changeOnEaten(self):
        sprite_name = "eaten_ghost"
        self.setCurrentImage(sprite_name, 1)


    def setCurrentImage(self, sprite_name, sprite_state):
        self.image = pygame.image.load(f"GhostsSprites/{sprite_name} ({sprite_state}).png")
        self.image = pygame.transform.scale(self.image,(CFG.SQUARE_SIZE * 1.5, CFG.SQUARE_SIZE * 1.5))

