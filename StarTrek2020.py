from math import pi, sqrt, cos, sin
import random

import TrekStrings

from Console import Con
from Calculators import Calc
from Controls import Control
from Reports import Stats
from AbsShip import *
from MapGame import *
from Points import Destination


class Game(Con):

    def __init__(self):
        self.is_testing = False
        self.game_map = GameMap()
        self.enterprise = Enterprise()
        self.star_date = 0
        self.time_remaining = 0
        self.destroyed = False

    def run(self):
        self.print_strings(TrekStrings.titleStrings)
        game.star_date = random.randint(0, 50) + 2250
        game.time_remaining = 40 + random.randint(0, 9)
        game.destroyed = False
        stars     = random.randrange(32, 64)
        aliens    = random.randrange(12, 16)
        starbases = random.randrange(6, 8)
        game.game_map.randomize(starbases, stars, aliens)
        self.print_mission()

        self.print_strings(TrekStrings.commandStrings)
        while self.enterprise.energy > 0 and not \
            self.destroyed and self.game_map.klingons > 0 and \
            self.time_remaining > 0:
            self.command_prompt()
            Stats.print_game_status(game)

    def command_prompt(self):
        command = self.read("Enter command: ").strip().lower()
        self.display()
        if command == "nav":
            Calc.navigation(game)
        elif command == "srs":
            game.enterprise.short_range_scan(game)
        elif command == "lrs":
            game.enterprise.long_range_scan(game)
        elif command == "pha":
            Control.phaser_controls(game)
        elif command == "tor":
            Control.torpedo_control(game)
        elif command == "she":
            Control.shield_controls(game)
        elif command == "com":
            Control.computer_controls(game)
        elif command.startswith('qui') or command.startswith('exi'):
            exit()
        else:
            self.print_strings(TrekStrings.commandStrings)

    def print_mission(self):
        self.display("Mission: Destroy {0} Klingon ships in {1} stardates with {2} starbases.".format(
            self.game_map.klingons, self.time_remaining, self.game_map.starbases))
        self.display()


if __name__ == '__main__':
    import traceback
    game = Game()
    try:
        game.run()
    except Exception as ex:
        print(ex)
        # Stack trace:
        traceback.print_exc() 
