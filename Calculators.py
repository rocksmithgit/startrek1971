from math import atan2, pi, sqrt, cos, sin
import random

from MapGame import *
from AbsShip import *
from Points import Destination

class Calc():

    @staticmethod
    def distance(x1, y1, x2, y2):
        x = x2 - x1
        y = y2 - y1
        return sqrt(x * x + y * y)


    @staticmethod
    def navigation(game):
        if game.enterprise.navigation_damage > 0:
            max_warp_factor = 0.2 + random.randint(0, 8) / 10.0
            game.display("Warp engines damaged. Maximum warp factor: {0}".format(max_warp_factor))
            game.display()

        dest_sys = game.read_sector()
        if not dest_sys:
            game.display("Invalid course.")
            game.display()
            return

        game.display()

        dist = dest_sys.warp * 8
        energy_required = int(dist)
        if energy_required >= game.enterprise.energy:
            game.display("Insufficient energy to travel at that speed.")
            game.display()
            return
        else:
            game.display("Warp engines engaged.")
            game.display()
            game.enterprise.energy -= energy_required

        game.game_map.go_to(dest_sys)

        game.time_remaining -= 1
        game.star_date += 1

        game.enterprise.short_range_scan(game)

        if game.enterprise.docked:
            game.display("Lowering shields as part of docking sequence...")
            game.display("Enterprise successfully docked with starbase.")
            game.display()
        else:
            if game.game_map.klingons > 0:
                KlingonShip.attack(game)
                game.display()
            elif not game.enterprise.repair(game):
                game.enterprise.damage(game, -1)


    @staticmethod
    def show_starbase(game):
        game.display()
        bases = game.game_map.get_all(Glyphs.STARBASE)
        game.display()
        if bases:
            game.display("Starbases:")
            for info in bases:
                area = info[0]; base = info[1]
                game.display(f"\tSector #{area.number} at [{base.xpos},{base.ypos}].")
        else:
            game.display("There are no Starbases.")
        game.display()


    @staticmethod
    def show_torp_targets(game):
        game.display()
        kships = game.game_map.get_area_klingons()
        if len(kships) == 0:
            game.display("There are no enemies in this quadrant.")
            return

        game.display("Enemies:")
        for ship in kships:
            game.display(f"\tKlingon [{ship.xpos},{ship.ypos}].")
        game.display()





