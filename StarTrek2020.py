import random

import TrekStrings
from Console import Con
from ShipKlingon import ShipKlingon
from ShipStarbase import ShipStarbase
from ShipEnterprise import ShipEnterprise
from Calculators import Calc
from Controls import Control
from Reports import Stats
from Points import Destination
from Quips import Quips
from MapGame import *


class Game(Con):

    def __init__(self):
        self.is_testing = False
        self.game_map = GameMap()
        self.enterprise = ShipEnterprise()
        self.star_date = 0
        self.time_remaining = 0
        self.destroyed = False

    def move_to(self, dest):
        pos = self.game_map._go_to(dest)
        area = self.game_map.pw_area()
        self.enterprise.docked = False
        for p in area._pieces:
            if p.glyph == Glyphs.STARBASE:
                if p.xpos + 1 == pos.xpos or p.ypos + 1 == pos.ypos or \
                    p.xpos - 1 == pos.xpos or p.ypos - 1 == pos.ypos:
                        self.enterprise.docked = True
        return pos

    def run(self):
        self.show_strings(TrekStrings.LOGO_TREKER)
        game.star_date = random.randint(0, 50) + 2250
        game.time_remaining = 40 + random.randint(0, 9)
        game.destroyed = False
        stars     = random.randrange(400, 600) # 4096 = ALL
        aliens    = random.randrange(12, 16)
        starbases = random.randrange(6, 8)
        game.game_map.randomize(starbases, stars, aliens)
        dest = Destination(64, 5, 5)
        game.move_to(dest)
        game.game_map.get_area(64).name = 'Outer Limits'
        self.print_mission()

        self.show_strings(TrekStrings.HELM_CMDS)
        running = True
        try:
            while running:
                self.command_prompt()
                running = self.enterprise.energy > 0 and not \
                self.destroyed and self.game_map.klingons > 0 and \
                self.time_remaining > 0
                if not running:
                    Stats.show_exit_status(game)
        except ErrorEnterpriseCollision as ex:
            Stats.show_exit_status(game)
            game.display()
            if ex.glyph == Glyphs.KLINGON:
                self.display("You flew into a KLINGON!")
            if ex.glyph == Glyphs.STARBASE:
                self.display("You flew into a STARBASE?")
            if ex.glyph == Glyphs.STAR:
                self.display("You flew into a STAR?")
            self.destroyed = True
        game.display()
        self.display(Quips.jibe_fatal_mistake())
        game.display(';-)')
        return False

    def command_prompt(self):
        command = self.read("Enter command: ").strip().lower()
        self.display()
        if command == "nav": # force of habit?
            Calc.warp_navigation(game)
        if command == "wsn":
            Calc.warp_navigation(game)
        if command == "ssn":
            Calc.sublight_navigation(game)
        elif command == "srs":
            game.enterprise.short_range_scan(game)
        elif command == "lrs":
            game.enterprise.long_range_scan(game)
        elif command == "pha":
            Control.phasers(game)
        elif command == "tor":
            Control.torpedos(game)
        elif command == "she":
            Control.shields(game)
        elif command == "com":
            Control.computer(game)
        elif command.startswith('qui') or command.startswith('exi'):
            exit()
        else:
            self.show_strings(TrekStrings.HELM_CMDS)

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
