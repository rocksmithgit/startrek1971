from math import atan2, pi, sqrt, cos, sin
import random

from Map import *
from Scanners import scanner
from Assets import Enterprise
from Aliens import KlingonShip

class calculator(object):

    @staticmethod
    def distance(x1, y1, x2, y2):
        x = x2 - x1
        y = y2 - y1
        return sqrt(x * x + y * y)

    @staticmethod
    def navigation(game):
        max_warp_factor = 8.0
        if game.enterprise.navigation_damage > 0:
            max_warp_factor = 0.2 + random.randint(0, 8) / 10.0
            game.display("Warp engines damaged. Maximum warp factor: {0}".format(max_warp_factor))
            game.display()

        direction = game.read_double("Enter course (1.0--8.9): ")
        if not direction or direction < 1.0 or direction > 9.0:
            game.display("Invalid course.")
            game.display()
            return

        dist = game.read_double(
            "Enter warp factor (0.1--{0}): ".format(max_warp_factor))
        if not dist or dist < 0.1 or dist > max_warp_factor:
            game.display("Invalid warp factor.")
            game.display()
            return

        game.display()

        dist *= 8
        energy_required = int(dist)
        if energy_required >= game.enterprise.energy:
            game.display("Unable to comply. Insufficient energy to travel that speed.")
            game.display()
            return
        else:
            game.display("Warp engines engaged.")
            game.display()
            game.enterprise.energy -= energy_required

        last_quad_x = game.quadrant_x
        last_quad_y = game.quadrant_y
        angle = -(pi * (direction - 1.0) / 4.0)
        x = game.quadrant_x * 8 + game.sector_x
        y = game.quadrant_y * 8 + game.sector_y
        dx = dist * cos(angle)
        dy = dist * sin(angle)
        vx = dx / 1000
        vy = dy / 1000
        # quad_x = quad_y = sect_x = sect_y = 0
        last_sect_x = game.sector_x
        last_sect_y = game.sector_y
        game.sector[game.sector_y][game.sector_x] = game.sector_type.empty
        obstacle = False
        for i in range(999):
            x += vx
            y += vy
            quad_x = int(round(x)) / 8
            quad_y = int(round(y)) / 8
            if quad_x == game.quadrant_x and quad_y == game.quadrant_y:
                sect_x = int(round(x)) % 8
                sect_y = int(round(y)) % 8
                if game.sector[sect_y][sect_x] != game.sector_type.empty:
                    game.sector_x = last_sect_x
                    game.sector_y = last_sect_y
                    game.sector[game.sector_y][game.sector_x] = game.sector_type.enterprise
                    game.display("Encountered obstacle within quadrant.")
                    game.display()
                    obstacle = True
                    break
                last_sect_x = sect_x
                last_sect_y = sect_y

        if not obstacle:
            if x < 0:
                x = 0
            elif x > 63:
                x = 63
            if y < 0:
                y = 0
            elif y > 63:
                y = 63
            quad_x = int(round(x)) / 8
            quad_y = int(round(y)) / 8
            game.sector_x = int(round(x)) % 8
            game.sector_y = int(round(y)) % 8
            if quad_x != game.quadrant_x or quad_y != game.quadrant_y:
                game.quadrant_x = int(quad_x)
                game.quadrant_y = int(quad_y)
                Map.generate_sector(game)
            else:
                game.quadrant_x = int(quad_x)
                game.quadrant_y = int(quad_y)
                game.sector[game.sector_y][game.sector_x] = game.sector_type.enterprise
        if Map.is_docking_location(game, game.sector_y, game.sector_x):
            game.enterprise.energy = 3000
            game.photon_torpedoes = 10
            game.enterprise.navigation_damage = 0
            game.enterprise.short_range_scan_damage = 0
            game.enterprise.long_range_scan_damage = 0
            game.enterprise.shield_control_damage = 0
            game.enterprise.computer_damage = 0
            game.enterprise.photon_damage = 0
            game.enterprise.phaser_damage = 0
            game.enterprise.shield_level = 0
            game.enterprise.docked = True
        else:
            game.enterprise.docked = False

        if last_quad_x != game.quadrant_x or last_quad_y != game.quadrant_y:
            game.time_remaining -= 1
            game.star_date += 1

        scanner.short_range_scan(game)

        if game.enterprise.docked:
            game.display("Lowering shields as part of docking sequence...")
            game.display("Enterprise successfully docked with starbase.")
            game.display()
        else:
            if game.quadrants[game.quadrant_y][game.quadrant_x].klingons > 0 \
                    and last_quad_x == game.quadrant_x and last_quad_y == game.quadrant_y:
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
            (game.quadrant_x + 1, game.quadrant_y + 1))
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
        if qx == game.quadrant_x and qy == game.quadrant_y:
            game.display("That is the current location of the Enterprise.")
            game.display()
            return
        direction = calculator.compute_direction(game.quadrant_x, game.quadrant_y, qx, qy)
        game.display("Direction: {0:1.2f}".format(direction))
        game.display("Distance:  {0:2.2f}".format(
            calculator.distance(game.quadrant_x, game.quadrant_y, qx, qy)))
        game.display()

    @staticmethod
    def starbase_calculator(game):
        game.display()
        if game.quadrants[game.quadrant_y][game.quadrant_x].starbase:
            game.display("Starbase in sector [%s,%s]." % (game.starbase_x + 1, game.starbase_y + 1))
            direction = calculator.compute_direction(game.sector_x, game.sector_y, game.starbase_x, game.starbase_y)
            game.display("Direction: {0:1.2f}".format(direction))
            game.display("Distance:  {0:2.2f}".format(
                calculator.distance(game.sector_x, game.sector_y, game.starbase_x, game.starbase_y) / 8))
        else:
            game.display("There are no starbases in this quadrant.")
        game.display()

    @staticmethod
    def photon_torpedo_calculator(game):
        game.display()
        if len(game.klingon_ships) == 0:
            game.display("There are no Klingon ships in this quadrant.")
            game.display()
            return

        for ship in game.klingon_ships:
            text = "Direction {2:1.2f}: Klingon ship in sector [{0},{1}]."
            direction = compute_direction(game.sector_x, game.sector_y, ship.sector_x, ship.sector_y)
            game.display(text.format(
                ship.sector_x + 1, ship.sector_y + 1, direction))
        game.display()





