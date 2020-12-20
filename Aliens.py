import random

from Assets import Enterprise

class KlingonShip(object):

    def __init__(self):
        self.sector_x = 0
        self.sector_y = 0
        self.shield_level = 0

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





