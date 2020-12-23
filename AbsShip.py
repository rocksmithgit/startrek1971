import abc
import random

import Glyphs
from Quips import Quips
from Quadrant import Quadrant

class AbsShip(abc.ABC):
    ''' The first step, into a much larger universe ... '''

    def __init__(self):
        self.shield_level = 0

    @abc.abstractmethod
    def get_glyph(self):
        pass

