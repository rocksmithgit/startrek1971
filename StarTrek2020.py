from math import pi, sqrt, cos, sin
import random

import TrekStrings

from AbsDisplay import console
from Calculators import calculator
from Controls import control
from Scanners import scanner
from Reports import status
from Assets import Enterprise
from Aliens import KlingonShip
from Map import *


class Game(console):

    def __init__(self):
        self.enterprise = Enterprise()
        self.star_date = 0
        self.time_remaining = 0
        self.klingons = 0
        self.starbases = 0
        self.sector_type = SectorType()
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
        Map.initialize_game(game)
        self.print_mission()
        Map.generate_sector(game)
        self.print_strings(TrekStrings.commandStrings)
        while self.enterprise.energy > 0 and not \
            self.destroyed and self.klingons > 0 and \
            self.time_remaining > 0:
            self.command_prompt()
            status.print_game_status(game)


    def command_prompt(self):
        command = self.read("Enter command: ").strip().lower()
        self.display()
        if command == "nav":
            calculator.navigation(game)
        elif command == "srs":
            scanner.short_range_scan(game)
        elif command == "lrs":
            scanner.long_range_scan(game)
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
