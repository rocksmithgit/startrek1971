from math import pi, sqrt, cos, sin
import random

import TrekStrings

from AbsDisplay import console
from Calculators import calculator
from Controls import control
from Scanners import scanner
from Reports import status


class Quadrant():

    def __init__(self):
        self.name = ""
        self.klingons = 0
        self.stars = 0
        self.starbase = False
        self.scanned = False


class SectorType():

    def __init__(self):
        self.empty, self.star, self.klingon, self.enterprise, self.starbase = 1, 2, 3, 4, 5


class KlingonShip():

    def __init__(self):
        self.sector_x = 0
        self.sector_y = 0
        self.shield_level = 0


class Game(console):

    def __init__(self):
        self.star_date = 0
        self.time_remaining = 0
        self.energy = 0
        self.klingons = 0
        self.starbases = 0
        self.sector_type = SectorType()
        self.quadrant_x, self.quadrant_y = 0, 0
        self.sector_x, self.sector_y = 0, 0
        self.shield_level = 0
        self.navigation_damage = 0
        self.short_range_scan_damage = 0
        self.long_range_scan_damage = 0
        self.shield_control_damage = 0
        self.computer_damage = 0
        self.photon_damage = 0
        self.phaser_damage = 0
        self.photon_torpedoes = 0
        self.docked = False
        self.destroyed = False
        self.starbase_x, self.starbase_y = 0, 0
        self.quadrants = [[Quadrant() for _ in range(8)] for _ in range(8)]
        self.sector = [[SectorType() for _ in range(8)] for _ in range(8)]
        self.klingon_ships = []


    def run(self):
        self.print_strings(TrekStrings.titleStrings)
        while True:
            self.initialize_game()
            self.print_mission()
            self.generate_sector()
            self.print_strings(TrekStrings.commandStrings)
            while self.energy > 0 and not self.destroyed and self.klingons > 0 and self.time_remaining > 0:
                self.command_prompt()
                status.print_game_status(game)

    def initialize_game(self):
        self.quadrant_x = random.randint(0, 7)
        self.quadrant_y = random.randint(0, 7)
        self.sector_x = random.randint(0, 7)
        self.sector_y = random.randint(0, 7)
        self.star_date = random.randint(0, 50) + 2250
        self.energy = 3000
        self.photon_torpedoes = 10
        self.time_remaining = 40 + random.randint(0, 9)
        self.klingons = 15 + random.randint(0, 5)
        self.starbases = 2 + random.randint(0, 2)
        self.destroyed = False
        self.navigation_damage = 0
        self.short_range_scan_damage = 0
        self.long_range_scan_damage = 0
        self.shield_control_damage = 0
        self.computer_damage = 0
        self.photon_damage = 0
        self.phaser_damage = 0
        self.shield_level = 0
        self.docked = False

        names = []
        for name in TrekStrings.quadrantNames:
            names.append(name)

        for i in range(8):
            for j in range(8):
                index = random.randint(0, len(names) - 1)
                quadrant = Quadrant()
                quadrant.name = names[index]
                quadrant.stars = 1 + random.randint(0, 7)
                self.quadrants[i][j] = quadrant
                del names[index]

        klingon_count = self.klingons
        starbase_count = self.starbases
        while klingon_count > 0 or starbase_count > 0:
            i = random.randint(0, 7)
            j = random.randint(0, 7)
            quadrant = self.quadrants[i][j]
            if not quadrant.starbase:
                quadrant.starbase = True
                starbase_count -= 1
            if quadrant.klingons < 3:
                quadrant.klingons += 1
                klingon_count -= 1


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


    def is_sector_region_empty(self, i, j):
        for y in range(i - 1, i+1):  # i + 1?
            if self.read_sector(y, j - 1) != \
                self.sector_type.empty and \
                self.read_sector(y, j + 1) != \
                self.sector_type.empty:
                return False
        return self.read_sector(i, j) == self.sector_type.empty


    def read_sector(self, i, j):
        if i < 0 or j < 0 or i > 7 or j > 7:
            return self.sector_type.empty
        return self.sector[i][j]


    def is_docking_location(self, i, j):
        for y in range(i - 1, i+1):  # i + 1?
            for x in range(j - 1, j+1):  # j + 1?
                if self.read_sector(y, x) == self.sector_type.starbase:
                    return True
        return False


    def generate_sector(self):
        quadrant = self.quadrants[self.quadrant_y][self.quadrant_x]
        starbase = quadrant.starbase
        stars = quadrant.stars
        klingons = quadrant.klingons
        self.klingon_ships = []
        for i in range(8):
            for j in range(8):
                self.sector[i][j] = self.sector_type.empty
        self.sector[self.sector_y][self.sector_x] = self.sector_type.enterprise
        while starbase or stars > 0 or klingons > 0:
            i = random.randint(0, 7)
            j = random.randint(0, 7)
            if self.is_sector_region_empty(i, j):
                if starbase:
                    starbase = False
                    self.sector[i][j] = self.sector_type.starbase
                    self.starbase_y = i
                    self.starbase_x = j
                elif stars > 0:
                    self.sector[i][j] = self.sector_type.star
                    stars -= 1
                elif klingons > 0:
                    self.sector[i][j] = self.sector_type.klingon
                    klingon_ship = KlingonShip()
                    klingon_ship.shield_level = 300 + random.randint(0, 199)
                    klingon_ship.sector_y = i
                    klingon_ship.sector_x = j
                    self.klingon_ships.append(klingon_ship)
                    klingons -= 1


    def print_sector(self, quadrant):
        self.condition = "GREEN"
        if quadrant.klingons > 0:
            self.condition = "RED"
        elif self.energy < 300:
            self.condition = "YELLOW"

        sb = ""
        self.display("-=--=--=--=--=--=--=--=-          Region: {0}".format(quadrant.name))
        self.print_sector_row(sb, 0, "           Quadrant: [{0},{1}]".format(
            self.quadrant_x + 1, self.quadrant_y + 1))
        self.print_sector_row(sb, 1, "             Sector: [{0},{1}]".format(self.sector_x + 1, self.sector_y + 1))
        self.print_sector_row(sb, 2, "           Stardate: {0}".format(self.star_date))
        self.print_sector_row(sb, 3, "     Time remaining: {0}".format(self.time_remaining))
        self.print_sector_row(sb, 4, "          Condition: {0}".format(self.condition))
        self.print_sector_row(sb, 5, "             Energy: {0}".format(self.energy))
        self.print_sector_row(sb, 6, "            Shields: {0}".format(self.shield_level))
        self.print_sector_row(sb, 7, "   Photon Torpedoes: {0}".format(self.photon_torpedoes))
        self.display("-=--=--=--=--=--=--=--=-             Docked: {0}".format(self.docked))

        if quadrant.klingons > 0:
            self.display()
            self.display("Condition RED: Klingon ship{0} detected.".format("" if quadrant.klingons == 1 else "s"))
            if self.shield_level == 0 and not self.docked:
                self.display("Warning: Shields are down.")
        elif self.energy < 300:
            self.display()
            self.display("Condition YELLOW: Low energy level.")
            self.condition = "YELLOW"


    def print_sector_row(self, sb, row, suffix):
        for column in range(8):
            if self.sector[row][column] == self.sector_type.empty:
                sb += "   "
            elif self.sector[row][column] == self.sector_type.enterprise:
                sb += "<E>"
            elif self.sector[row][column] == self.sector_type.klingon:
                sb += "+K+"
            elif self.sector[row][column] == self.sector_type.star:
                sb += " * "
            elif self.sector[row][column] == self.sector_type.starbase:
                sb += ">S<"
        if suffix is not None:
            sb = sb + suffix
        self.display(sb)


    def print_mission(self):
        self.display("Mission: Destroy {0} Klingon ships in {1} stardates with {2} starbases.".format(
            self.klingons, self.time_remaining, self.starbases))
        self.display()


if __name__ == '__main__':
    game = Game()
    game.run()
