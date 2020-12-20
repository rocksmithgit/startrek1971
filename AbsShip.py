import abc
import random

import Glyphs

class AbsShip(abc.ABC):
    ''' The first step, into a much larger universe ... '''

    def __init__(self):
        self.shield_level = 0

    @abc.abstractmethod
    def get_glyph(self):
        pass


class Enterprise(AbsShip):

    def __init__(self):
        super().__init__()
        self.energy = 0
        self.docked = False
        self.condition = "GREEN"
        self.navigation_damage = 0
        self.short_range_scan_damage = 0
        self.long_range_scan_damage = 0
        self.shield_control_damage = 0
        self.computer_damage = 0
        self.photon_damage = 0
        self.phaser_damage = 0


    def get_glyph(self):
        return Glyphs.ENTERPRISE


    def damage(self, game, item):
        if random.randint(0, 6) > 0:
            return
        damage = 1 + random.randint(0, 4)
        if item < 0:
            item = random.randint(0, 6)
        if item == 0:
            self.navigation_damage = damage
            game.display("Warp engines are malfunctioning.")
        elif item == 1:
            self.short_range_scan_damage = damage
            game.display("Short range scanner is malfunctioning.")
        elif item == 2:
            self.long_range_scan_damage = damage
            game.display("Long range scanner is malfunctioning.")
        elif item == 3:
            self.shield_control_damage = damage
            game.display("Shield controls are malfunctioning.")
        elif item == 4:
            self.computer_damage = damage
            game.display("The main computer is malfunctioning.")
        elif item == 5:
            self.photon_damage = damage
            game.display("Photon torpedo controls are malfunctioning.")
        elif item == 6:
            self.phaser_damage = damage
            game.display("Phasers are malfunctioning.")
        game.display()


    def repair(self, game):
        if self.navigation_damage > 0:
            self.navigation_damage -= 1
            if self.navigation_damage == 0:
                game.display("Warp engines have been repaired.")
            game.display()
            return True
        if self.short_range_scan_damage > 0:
            self.short_range_scan_damage -= 1
            if self.short_range_scan_damage == 0:
                game.display("Short range scanner has been repaired.")
            self.display()
            return True
        if self.long_range_scan_damage > 0:
            self.long_range_scan_damage -= 1
            if self.long_range_scan_damage == 0:
                game.display("Long range scanner has been repaired.")
            game.display()
            return True
        if self.shield_control_damage > 0:
            self.shield_control_damage -= 1
            if self.shield_control_damage == 0:
                game.display("Shield controls have been repaired.")
            game.display()
            return True
        if self.computer_damage > 0:
            self.computer_damage -= 1
            if self.computer_damage == 0:
                game.display("The main computer has been repaired.")
            game.display()
            return True
        if self.photon_damage > 0:
            self.photon_damage -= 1
            if self.photon_damage == 0:
                game.display("Photon torpedo controls have been repaired.")
            game.display()
            return True
        if self.phaser_damage > 0:
            self.phaser_damage -= 1
            if self.phaser_damage == 0:
                game.display("Phasers have been repaired.")
            game.display()
            return True
        return False


    def short_range_scan(self, game):
        from Charts import Sectors

        if self.short_range_scan_damage > 0:
            game.display("Short range scanner is damaged. Repairs are underway.")
            game.display()
        else:
            quadrant = game.quadrants[game.quadrant_y][game.quadrant_x]
            quadrant.scanned = True
            Sectors.print_sector(game, quadrant)
        game.display()


    def long_range_scan(self, game):
        if self.long_range_scan_damage > 0:
            game.display("Long range scanner is damaged. Repairs are underway.")
            game.display()
            return
        sb = ""
        game.display("-------------------")
        for i in range(game.quadrant_y - 1, game.quadrant_y+2):  # quadrantY + 1 ?
            for j in range(game.quadrant_x - 1, game.quadrant_x+2):  # quadrantX + 1?
                sb += "| "
                klingon_count = 0
                starbase_count = 0
                star_count = 0
                if 0 <= i < 8 and 0 <= j < 8:
                    quadrant = game.quadrants[i][j]
                    quadrant.scanned = True
                    klingon_count = quadrant.klingons
                    starbase_count = 1 if quadrant.starbase else 0
                    star_count = quadrant.stars
                sb = sb + \
                    "{0}{1}{2} ".format(klingon_count, starbase_count, star_count)
            sb += "|"
            game.display(sb)
            sb = ""
            game.display("-------------------")
        game.display()


class KlingonShip(AbsShip):

    def __init__(self):
        super().__init__()
        self.sector_x = 0
        self.sector_y = 0


    def get_glyph(self):
        return Glyphs.KLINGON


    @staticmethod
    def attack(game):
        from Calculators import calculator
        if len(game.klingon_ships) > 0:
            for ship in game.klingon_ships:
                if game.enterprise.docked:
                    game.display("Enterprise hit by ship at sector [{0},{1}]. No damage due to starbase shields.".format(
                        ship.sector_x + 1, ship.sector_y + 1
                    ))
                else:
                    dist = calculator.distance(
                        game.sector_x, game.sector_y, ship.sector_x, ship.sector_y)
                    delivered_energy = 300 * \
                        random.uniform(0.0, 1.0) * (1.0 - dist / 11.3)
                    game.enterprise.shield_level -= int(delivered_energy)
                    if game.enterprise.shield_level < 0:
                        game.enterprise.shield_level = 0
                        game.destroyed = True
                    game.display("Enterprise hit by ship at sector [{0},{1}]. Shields dropped to {2}.".format(
                        ship.sector_x + 1, ship.sector_y + 1, game.enterprise.shield_level
                    ))
                    if game.enterprise.shield_level == 0:
                        return True
            return True
        return False
