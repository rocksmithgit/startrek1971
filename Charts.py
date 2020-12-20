import random
import TrekStrings

import Glyphs
from AbsShip import KlingonShip


class Quadrant():

    def __init__(self):
        self.name = ""
        self.klingons = 0
        self.stars = 0
        self.starbase = False
        self.scanned = False


class SectorType():

    def __init__(self):
        self.empty, self.star, self.klingon, \
        self.enterprise, self.starbase = \
        Glyphs.SPACE, Glyphs.STAR, Glyphs.KLINGON, \
        Glyphs.ENTERPRISE, Glyphs.STARBASE



class Sectors(object):

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
                game.sector[i][j] = Glyphs.SPACE
        game.sector[game.sector_y][game.sector_x] = Glyphs.ENTERPRISE
        while starbase or stars > 0 or klingons > 0:
            i = random.randint(0, 7)
            j = random.randint(0, 7)
            if Sectors.is_sector_region_empty(game, i, j):
                if starbase:
                    starbase = False
                    game.sector[i][j] = Glyphs.STARBASE
                    game.starbase_y = i
                    game.starbase_x = j
                elif stars > 0:
                    game.sector[i][j] = Glyphs.STAR
                    stars -= 1
                elif klingons > 0:
                    game.sector[i][j] = Glyphs.KLINGON
                    klingon_ship = KlingonShip()
                    klingon_ship.shield_level = 300 + random.randint(0, 199)
                    klingon_ship.sector_y = i
                    klingon_ship.sector_x = j
                    game.klingon_ships.append(klingon_ship)
                    klingons -= 1

    @staticmethod                
    def is_sector_region_empty(game, i, j):
        for y in range(i - 1, i+1):  # i + 1?
            if Sectors.read_sector(game, y, j - 1) != \
                Glyphs.SPACE and \
                Sectors.read_sector(game, y, j + 1) != \
                Glyphs.SPACE:
                return False
        return Sectors.read_sector(game, i, j) == Glyphs.SPACE


    @staticmethod                
    def read_sector(game, i, j):
        if i < 0 or j < 0 or i > 7 or j > 7:
            return Glyphs.SPACE
        return game.sector[i][j]


    @staticmethod                
    def is_docking_location(game, i, j):
        for y in range(i - 1, i+1):  # i + 1?
            for x in range(j - 1, j+1):  # j + 1?
                if Sectors.read_sector(game, y, x) == Glyphs.STARBASE:
                    return True
        return False


    @staticmethod                
    def print_sector(game, quadrant):
        game.enterprise.condition = "GREEN"
        if quadrant.klingons > 0:
            game.enterprise.condition = "RED"
        elif game.enterprise.energy < 300:
            game.enterprise.condition = "YELLOW"

        sb =   "     a  b  c  d  e  f  g  h \n"
        sb += f"    -=--=--=--=--=--=--=--=-             Region: {quadrant.name}\n"
        info = list()
        info.append(f"           Quadrant: [{game.quadrant_x + 1}, {game.quadrant_y + 1}\n")
        info.append(f"             Sector: [{game.sector_x + 1}, {game.sector_y + 1}\n")
        info.append(f"           Stardate: {game.star_date}\n")
        info.append(f"     Time remaining: {game.time_remaining}\n")
        info.append(f"          Condition: {game.enterprise.condition}\n")
        info.append(f"             Energy: {game.enterprise.energy}\n")
        info.append(f"            Shields: {game.enterprise.shield_level}\n")
        info.append(f"   Photon Torpedoes: {game.photon_torpedoes}\n")
        for ss in range(8):
            sb = Sectors._get_row(game, sb, ss, info[ss])
        sb += "    -=--=--=--=--=--=--=--=-             Docked: {game.enterprise.docked}\n"
        print(sb, end='')

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
    def _get_row(game, sb, row, suffix):
        sb += f" {row} |"
        for column in range(8):
            if game.sector[row][column] == Glyphs.SPACE:
                sb += Glyphs.SPACE
            elif game.sector[row][column] == Glyphs.ENTERPRISE:
                sb += Glyphs.ENTERPRISE
            elif game.sector[row][column] == Glyphs.KLINGON:
                sb += Glyphs.KLINGON
            elif game.sector[row][column] == Glyphs.STAR:
                sb += Glyphs.STAR
            elif game.sector[row][column] == Glyphs.STARBASE:
                sb += Glyphs.STARBASE
        if suffix is not None:
            sb = sb + suffix
        return sb


