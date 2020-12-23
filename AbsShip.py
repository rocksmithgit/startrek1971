import abc
import random

import Glyphs
from Quips import Quips
from Quadrant import Quadrant

class AbsShip(abc.ABC):
    ''' The first step, into a much larger universe ... '''

    def __init__(self):
        self.shield_level = 0

    @abc.abstractmethod
    def get_glyph(self):
        pass

class ShipStarbase(AbsShip):

    def __init__(self):
        super().__init__()

    def get_glyph(self):
        return Glyphs.STARBASE

    @staticmethod
    def dock_enterprise(ship):
        ship.energy = 3000
        ship.photon_torpedoes = 10
        ship.navigation_damage = 0
        ship.short_range_scan_damage = 0
        ship.long_range_scan_damage = 0
        ship.shield_control_damage = 0
        ship.computer_damage = 0
        ship.photon_damage = 0
        ship.phaser_damage = 0
        ship.shield_level = 0
        ship.docked = True

    @staticmethod
    def launch_enterprise(ship):
        ship.docked = False


class ShipEnterprise(AbsShip):

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
        self.photon_torpedoes = 0
        ShipStarbase.dock_enterprise(self)
        ShipStarbase.launch_enterprise(self)

    def get_glyph(self):
        return Glyphs.ENTERPRISE

    def damage(self, game, item):
        '''
        Damage the Enterprise.
        '''
        if game.is_testing:
            return
        if random.randint(0, 6) > 0:
            return
        damage = 1 + random.randint(0, 4)
        if item < 0:
            item = random.randint(0, 6)
        if item == 0:
            self.navigation_damage = damage
            game.display(Quips.jibe_damage('Warp Engines'))
        elif item == 1:
            self.short_range_scan_damage = damage
            game.display(Quips.jibe_damage('Short Range Scanners'))
        elif item == 2:
            self.long_range_scan_damage = damage
            game.display(Quips.jibe_damage('Long Range Scanners'))
        elif item == 3:
            self.shield_control_damage = damage
            game.display(Quips.jibe_damage('Shield Controls'))
        elif item == 4:
            self.computer_damage = damage
            game.display(Quips.jibe_damage('Main Computer'))
        elif item == 5:
            self.photon_damage = damage
            game.display(Quips.jibe_damage('Photon Torpedo Controls'))
        elif item == 6:
            self.phaser_damage = damage
            game.display(Quips.jibe_damage('Phasers'))
        game.display()

    def repair(self, game):
        '''
        Repair damage to the Enterprise.
        '''
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
        if self.short_range_scan_damage > 0:
            game.display(Quips.jibe_damage('Short Ranged Scanners'))
            game.display()
        else:
            quad = game.game_map.quad()
            Quadrant.display_area(game, quad)
        game.display()

    def long_range_scan(self, game):
        if self.long_range_scan_damage > 0:
            game.display(Quips.jibe_damage('Long Ranged Scanners'))
            game.display()
            return
        sb = ""
        pw_sector = game.game_map.sector
        if pw_sector < 5:
            pw_sector = 6
        elif pw_sector > 59:
            pw_sector = 59
        dots = None
        for peek in range(pw_sector-5, pw_sector + 6):
            quad = game.game_map.scan_quad(peek)
            lines = \
                (f"| Sector: {quad.number:>02}",
                f"Enemies: {quad.klingons:>02}",
                f"Bases: {quad.starbases:>02}",
                f"Stars: {quad.stars:>03} |")
            str_ = ' | '.join(lines)
            dots = '-' * len(str_) + "\n"
            sb += dots
            sb += str_
            game.display(sb)
            sb = ""
        game.display(dots)
        game.display()


class ShipKlingon(AbsShip):

    def __init__(self):
        super().__init__()
        self.xpos = 0
        self.ypos = 0
        self.shield_level = 0

    def get_glyph(self):
        return Glyphs.KLINGON

    def from_map(self, xpos, ypos):
        self.xpos = xpos
        self.ypos = ypos
        self.shield_level = 300 + random.randint(0, 199)

    @staticmethod
    def attack(game):
        from Calculators import Calc
        kships = game.game_map.get_area_klingons()
        if len(kships) > 0:
            for ship in kships:
                if game.enterprise.docked:
                    game.display("Enterprise hit by ship at sector [{0},{1}]. No damage due to starbase shields.".format(
                        ship.xpos + 1, ship.ypos + 1
                    ))
                else:
                    dist = Calc.distance(
                        game.game_map.xpos, game.game_map.ypos, ship.xpos, ship.ypos)
                    delivered_energy = 300 * \
                        random.uniform(0.0, 1.0) * (1.0 - dist / 11.3)
                    game.enterprise.shield_level -= int(delivered_energy)
                    if game.enterprise.shield_level < 0:
                        game.enterprise.shield_level = 0
                        game.destroyed = True
                    game.display("Enterprise hit by ship at sector [{0},{1}]. Shields dropped to {2}.".format(
                        ship.xpos + 1, ship.ypos + 1, game.enterprise.shield_level
                    ))
                    if game.enterprise.shield_level == 0:
                        return True
            return True
        return False
