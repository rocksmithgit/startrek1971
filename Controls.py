from math import pi, sqrt, cos, sin
import random

import TrekStrings
from Assets import Enterprise
from Aliens import KlingonShip
from Calculators import calculator
from Reports import status


class control(object):

    @staticmethod
    def computer_controls(game):
        if game.enterprise.computer_damage > 0:
            game.display("The main computer is damaged. Repairs are underway.")
            game.display()
            return
        game.print_strings(TrekStrings.computerStrings)
        command = game.read("Enter computer command: ").strip().lower()
        if command == "rec":
            status.display_galactic_record(game)
        elif command == "sta":
            status.display_status(game)
        elif command == "tor":
            calculator.photon_torpedo_calculator(game)
        elif command == "bas":
            calculator.starbase_calculator(game)
        elif command == "nav":
            calculator.navigation_calculator(game)
        else:
            game.display()
            game.display("Invalid computer command.")
            game.display()
        game.enterprise.damage(game, 4)


    @staticmethod
    def phaser_controls(game):
        if game.enterprise.phaser_damage > 0:
            game.display("Phasers are damaged. Repairs are underway.")
            game.display()
            return
        if len(game.klingon_ships) == 0:
            game.display("There are no Klingon ships in this quadrant.")
            game.display()
            return
        game.display("Phasers locked on target.")
        phaser_energy = game.read_double("Enter phaser energy (1--{0}): ".format(game.enterprise.energy))
        if not phaser_energy or phaser_energy < 1 or phaser_energy > game.enterprise.energy:
            game.display("Invalid energy level.")
            game.display()
            return
        game.display()
        game.display("Firing phasers...")
        destroyed_ships = []
        for ship in game.klingon_ships:
            game.enterprise.energy -= int(phaser_energy)
            if game.enterprise.energy < 0:
                game.enterprise.energy = 0
                break
            dist = calculator.distance(game.sector_x, game.sector_y, ship.sector_x, ship.sector_y)
            delivered_energy = phaser_energy * (1.0 - dist / 11.3)
            ship.shield_level -= int(delivered_energy)
            if ship.shield_level <= 0:
                game.display("Klingon ship destroyed at sector [{0},{1}].".format(ship.sector_x + 1, ship.sector_y + 1))
                destroyed_ships.append(ship)
            else:
                game.display("Hit ship at sector [{0},{1}]. Klingon shield strength dropped to {2}.".format(
                    ship.sector_x + 1, ship.sector_y + 1, ship.shield_level
                ))
        for ship in destroyed_ships:
            game.quadrants[game.quadrant_y][game.quadrant_x].klingons -= 1
            game.klingons -= 1
            game.sector[ship.sector_y][ship.sector_x] = game.sector_type.empty
            game.klingon_ships.remove(ship)
        if len(game.klingon_ships) > 0:
            game.display()
            KlingonShip.attack(game)
        game.display()


    def shield_controls(game):
        game.display("--- Shield Controls ----------------")
        game.display("add = Add energy to shields.")
        game.display("sub = Subtract energy from shields.")
        game.display()
        command = game.read("Enter shield control command: ").strip().lower()
        game.display()
        if command == "add":
            adding = True
            max_transfer = game.enterprise.energy
        elif command == "sub":
            adding = False
            max_transfer = game.enterprise.shield_level
        else:
            game.display("Invalid command.")
            game.display()
            return
        transfer = game.read_double(
            "Enter amount of energy (1--{0}): ".format(max_transfer))
        if not transfer or transfer < 1 or transfer > max_transfer:
            game.display("Invalid amount of energy.")
            game.display()
            return
        game.display()
        if adding:
            game.enterprise.energy -= int(transfer)
            game.enterprise.shield_level += int(transfer)
        else:
            game.enterprise.energy += int(transfer)
            game.enterprise.shield_level -= int(transfer)
        game.display("Shield strength is now {0}. Energy level is now {1}.".format(game.enterprise.shield_level, game.enterprise.energy))
        game.display()


    def torpedo_control(game):
        if game.enterprise.photon_damage > 0:
            game.display("Photon torpedo control is damaged. Repairs are underway.")
            game.display()
            return
        if game.photon_torpedoes == 0:
            game.display("Photon torpedoes exhausted.")
            game.display()
            return
        if len(game.klingon_ships) == 0:
            game.display("There are no Klingon ships in this quadrant.")
            game.display()
            return
        direction = game.read_double("Enter firing direction (1.0--9.0): ")
        if not direction or direction < 1.0 or direction > 9.0:
            game.display("Invalid direction.")
            game.display()
            return
        game.display()
        game.display("Photon torpedo fired...")
        game.photon_torpedoes -= 1
        angle = -(pi * (direction - 1.0) / 4.0)
        if random.randint(0, 2) == 0:
            angle += (1.0 - 2.0 * random.uniform(0.0, 1.0) * pi * 2.0) * 0.03
        x = game.sector_x
        y = game.sector_y
        vx = cos(angle) / 20
        vy = sin(angle) / 20
        last_x = last_y = -1
        # new_x = game.sector_x
        # new_y = game.sector_y
        hit = False
        while x >= 0 and y >= 0 and round(x) < 8 and round(y) < 8:
            new_x = int(round(x))
            new_y = int(round(y))
            if last_x != new_x or last_y != new_y:
                game.display("  [{0},{1}]".format(new_x + 1, new_y + 1))
                last_x = new_x
                last_y = new_y
            for ship in game.klingon_ships:
                if ship.sector_x == new_x and ship.sector_y == new_y:
                    game.display("Klingon ship destroyed at sector [{0},{1}].".format(ship.sector_x + 1, ship.sector_y + 1))
                    game.sector[ship.sector_y][ship.sector_x] = game.sector_type.empty
                    game.klingons -= 1
                    game.klingon_ships.remove(ship)
                    game.quadrants[game.quadrant_y][game.quadrant_x].klingons -= 1
                    hit = True
                    break  # break out of the for loop
            if hit:
                break  # break out of the while loop
            if game.sector[new_y][new_x] == game.sector_type.starbase:
                game.starbases -= 1
                game.quadrants[game.quadrant_y][game.quadrant_x].starbase = False
                game.sector[new_y][new_x] = game.sector_type.empty
                game.display("The Enterprise destroyed a Federation starbase at sector [{0},{1}]!".format(new_x + 1, new_y + 1))
                hit = True
                break
            elif game.sector[new_y][new_x] == game.sector_type.star:
                game.display("The torpedo was captured by a star's gravitational field at sector [{0},{1}].".format(
                    new_x + 1, new_y + 1
                ))
                hit = True
                break
            x += vx
            y += vy
        if not hit:
            game.display("Photon torpedo failed to hit anything.")
        if len(game.klingon_ships) > 0:
            game.display()
            KlingonShip.attack(game)
        game.display()





