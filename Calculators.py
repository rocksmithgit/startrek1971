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
            game.display("Unable to comply. Insufficient energy to travel that speed.")
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
    def compute_direction(x1, y1, x2, y2):
        if x1 == x2:
            if y1 < y2:
                direction = 7
            else:
                direction = 3
        elif y1 == y2:
            if x1 < x2:
                direction = 1
            else:
                direction = 5
        else:
            dy = abs(y2 - y1)
            dx = abs(x2 - x1)
            angle = atan2(dy, dx)
            if x1 < x2:
                if y1 < y2:
                    direction = 9.0 - 4.0 * angle / pi
                else:
                    direction = 1.0 + 4.0 * angle / pi
            else:
                if y1 < y2:
                    direction = 5.0 + 4.0 * angle / pi
                else:
                    direction = 5.0 - 4.0 * angle / pi
        return direction


    @staticmethod
    def navigation_calculator(game):
        game.display()
        game.display("Enterprise located in quadrant [%s,%s]." % \
            (game.game_map.major_x + 1, game.game_map.major_y + 1))
        game.display()
        quad_x = game.read_double("Enter destination quadrant X (1--8): ")
        if quad_x is False or quad_x < 1 or quad_x > 8:
            game.display("Invalid X coordinate.")
            game.display()
            return
        quad_y = game.read_double("Enter destination quadrant Y (1--8): ")
        if quad_y is False or quad_y < 1 or quad_y > 8:
            game.display("Invalid Y coordinate.")
            game.display()
            return
        game.display()
        qx = int(quad_x) - 1
        qy = int(quad_y) - 1
        if qx == game.game_map.major_x and qy == game.game_map.major_y:
            game.display("That is the current location of the Enterprise.")
            game.display()
            return
        direction = Calc.compute_direction(
            game.game_map.major_x, 
            game.game_map.major_y, 
            qx, qy)
        game.display("Direction: {0:1.2f}".format(direction))
        game.display("Distance:  {0:2.2f}".format(
            Calc.distance(game.game_map.major_x, game.game_map.major_y, qx, qy)))
        game.display()


    @staticmethod
    def starbase_inventory(game):
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
    def photon_torpedo_calculator(game):
        game.display()
        kships = game.game_map.get_area_klingons()
        if len(kships) == 0:
            game.display("There are no enemy ships in this quadrant.")
            return

        game.display("Enemies:")
        for ship in kships:
            game.display(f"\tKlingon [{ship.xpos},{ship.ypos}].")
        game.display()





