from math import pi, sqrt, cos, sin
import random

import TrekStrings

from AbsDisplay import Con
from Calculators import Calc
from Controls import control
from Reports import Stats
from AbsShip import *
from Charts import *


class Game(Con):

    def __init__(self):
        self.enterprise = Enterprise()
        self.star_date = 0
        self.time_remaining = 0
        self.klingons = 0
        self.starbases = 0
        self.quadrant_x, self.quadrant_y = 0, 0
        self.sector_x, self.sector_y = 0, 0
        self.photon_torpedoes = 0
        self.destroyed = False
        self.starbase_x, self.starbase_y = 0, 0
        self.quadrants = [[Quadrant() for _ in range(8)] for _ in range(8)]
        self.sector = [[SectorType() for _ in range(8)] for _ in range(8)]
        self.klingon_ships = []


    def run(self):
        self.print_strings(TrekStrings.titleStrings)
        Sectors.initialize_game(game)
        self.print_mission()
        Sectors.generate_sector(game)
        self.print_strings(TrekStrings.commandStrings)
        while self.enterprise.energy > 0 and not \
            self.destroyed and self.klingons > 0 and \
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
            control.phaser_controls(game)
        elif command == "tor":
            control.torpedo_control(game)
        elif command == "she":
            control.shield_controls(game)
        elif command == "com":
            control.computer_controls(game)
        elif command.startswith('qui') or command.startswith('exi'):
            exit()
        else:
            self.print_strings(TrekStrings.commandStrings)


    def print_mission(self):
        self.display("Mission: Destroy {0} Klingon ships in {1} stardates with {2} starbases.".format(
            self.klingons, self.time_remaining, self.starbases))
        self.display()


if __name__ == '__main__':
    game = Game()
    game.run()
