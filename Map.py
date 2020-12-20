import random
import TrekStrings

from Aliens import KlingonShip


class Quadrant():

    def __init__(game):
        game.name = ""
        game.klingons = 0
        game.stars = 0
        game.starbase = False
        game.scanned = False


class SectorType():

    def __init__(game):
        game.empty, game.star, game.klingon, game.enterprise, game.starbase = 1, 2, 3, 4, 5


class Map(object):

    @staticmethod
    def initialize_game(game):
        game.quadrant_x = random.randint(0, 7)
        game.quadrant_y = random.randint(0, 7)
        game.sector_x = random.randint(0, 7)
        game.sector_y = random.randint(0, 7)
        game.star_date = random.randint(0, 50) + 2250
        game.enterprise.energy = 3000
        game.photon_torpedoes = 10
        game.time_remaining = 40 + random.randint(0, 9)
        game.klingons = 15 + random.randint(0, 5)
        game.starbases = 2 + random.randint(0, 2)
        game.destroyed = False

        names = []
        for name in TrekStrings.quadrantNames:
            names.append(name)

        for i in range(8):
            for j in range(8):
                index = random.randint(0, len(names) - 1)
                quadrant = Quadrant()
                quadrant.name = names[index]
                quadrant.stars = 1 + random.randint(0, 7)
                game.quadrants[i][j] = quadrant
                del names[index]

        klingon_count = game.klingons
        starbase_count = game.starbases
        while klingon_count > 0 or starbase_count > 0:
            i = random.randint(0, 7)
            j = random.randint(0, 7)
            quadrant = game.quadrants[i][j]
            if not quadrant.starbase:
                quadrant.starbase = True
                starbase_count -= 1
            if quadrant.klingons < 3:
                quadrant.klingons += 1
                klingon_count -= 1


    @staticmethod                
    def generate_sector(game):
        quadrant = game.quadrants[game.quadrant_y][game.quadrant_x]
        starbase = quadrant.starbase
        stars = quadrant.stars
        klingons = quadrant.klingons
        game.klingon_ships = []
        for i in range(8):
            for j in range(8):
                game.sector[i][j] = game.sector_type.empty
        game.sector[game.sector_y][game.sector_x] = game.sector_type.enterprise
        while starbase or stars > 0 or klingons > 0:
            i = random.randint(0, 7)
            j = random.randint(0, 7)
            if Map.is_sector_region_empty(game, i, j):
                if starbase:
                    starbase = False
                    game.sector[i][j] = game.sector_type.starbase
                    game.starbase_y = i
                    game.starbase_x = j
                elif stars > 0:
                    game.sector[i][j] = game.sector_type.star
                    stars -= 1
                elif klingons > 0:
                    game.sector[i][j] = game.sector_type.klingon
                    klingon_ship = KlingonShip()
                    klingon_ship.shield_level = 300 + random.randint(0, 199)
                    klingon_ship.sector_y = i
                    klingon_ship.sector_x = j
                    game.klingon_ships.append(klingon_ship)
                    klingons -= 1

    @staticmethod                
    def is_sector_region_empty(game, i, j):
        for y in range(i - 1, i+1):  # i + 1?
            if Map.read_sector(game, y, j - 1) != \
                game.sector_type.empty and \
                Map.read_sector(game, y, j + 1) != \
                game.sector_type.empty:
                return False
        return Map.read_sector(game, i, j) == game.sector_type.empty


    @staticmethod                
    def read_sector(game, i, j):
        if i < 0 or j < 0 or i > 7 or j > 7:
            return game.sector_type.empty
        return game.sector[i][j]


    @staticmethod                
    def is_docking_location(game, i, j):
        for y in range(i - 1, i+1):  # i + 1?
            for x in range(j - 1, j+1):  # j + 1?
                if Map.read_sector(game, y, x) == game.sector_type.starbase:
                    return True
        return False


    @staticmethod                
    def print_sector(game, quadrant):
        game.enterprise.condition = "GREEN"
        if quadrant.klingons > 0:
            game.enterprise.condition = "RED"
        elif game.enterprise.energy < 300:
            game.enterprise.condition = "YELLOW"

        sb = ""
        game.display("-=--=--=--=--=--=--=--=-          Region: {0}".format(quadrant.name))
        Map.print_sector_row(game, sb, 0, "           Quadrant: [{0},{1}]".format(
            game.quadrant_x + 1, game.quadrant_y + 1))
        Map.print_sector_row(game, sb, 1, "             Sector: [{0},{1}]".format(game.sector_x + 1, game.sector_y + 1))
        Map.print_sector_row(game, sb, 2, "           Stardate: {0}".format(game.star_date))
        Map.print_sector_row(game, sb, 3, "     Time remaining: {0}".format(game.time_remaining))
        Map.print_sector_row(game, sb, 4, "          Condition: {0}".format(game.enterprise.condition))
        Map.print_sector_row(game, sb, 5, "             Energy: {0}".format(game.enterprise.energy))
        Map.print_sector_row(game, sb, 6, "            Shields: {0}".format(game.enterprise.shield_level))
        Map.print_sector_row(game, sb, 7, "   Photon Torpedoes: {0}".format(game.photon_torpedoes))
        game.display("-=--=--=--=--=--=--=--=-             Docked: {0}".format(game.enterprise.docked))

        if quadrant.klingons > 0:
            game.display()
            game.display("Condition RED: Klingon ship{0} detected.".format("" if quadrant.klingons == 1 else "s"))
            if game.enterprise.shield_level == 0 and not game.enterprise.docked:
                game.display("Warning: Shields are down.")
        elif game.enterprise.energy < 300:
            game.display()
            game.display("Condition YELLOW: Low energy level.")
            game.enterprise.condition = "YELLOW"


    @staticmethod                
    def print_sector_row(game, sb, row, suffix):
        for column in range(8):
            if game.sector[row][column] == game.sector_type.empty:
                sb += "   "
            elif game.sector[row][column] == game.sector_type.enterprise:
                sb += "<E>"
            elif game.sector[row][column] == game.sector_type.klingon:
                sb += "+K+"
            elif game.sector[row][column] == game.sector_type.star:
                sb += " * "
            elif game.sector[row][column] == game.sector_type.starbase:
                sb += ">S<"
        if suffix is not None:
            sb = sb + suffix
        game.display(sb)


