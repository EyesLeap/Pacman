from abc import ABC, abstractmethod
import ConstantsForGame as CFG
from random import randint

## Strategy interface
class GhostStrategy(ABC):

    def __init__(self):
        self.next_strategy = None

    @abstractmethod
    def execute(self, ghost, game_board):
        pass




