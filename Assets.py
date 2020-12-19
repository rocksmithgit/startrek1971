import random


class ship(object):

    @staticmethod
    def induce_damage(game, item):
        if random.randint(0, 6) > 0:
            return
        damage = 1 + random.randint(0, 4)
        if item < 0:
            item = random.randint(0, 6)
        if item == 0:
            game.navigation_damage = damage
            game.display("Warp engines are malfunctioning.")
        elif item == 1:
            game.short_range_scan_damage = damage
            game.display("Short range scanner is malfunctioning.")
        elif item == 2:
            game.long_range_scan_damage = damage
            game.display("Long range scanner is malfunctioning.")
        elif item == 3:
            game.shield_control_damage = damage
            game.display("Shield controls are malfunctioning.")
        elif item == 4:
            game.computer_damage = damage
            game.display("The main computer is malfunctioning.")
        elif item == 5:
            game.photon_damage = damage
            game.display("Photon torpedo controls are malfunctioning.")
        elif item == 6:
            game.phaser_damage = damage
            game.display("Phasers are malfunctioning.")
        game.display()


    @staticmethod
    def repair_damage(game):
        if game.navigation_damage > 0:
            game.navigation_damage -= 1
            if game.navigation_damage == 0:
                game.display("Warp engines have been repaired.")
            game.display()
            return True
        if game.short_range_scan_damage > 0:
            game.short_range_scan_damage -= 1
            if game.short_range_scan_damage == 0:
                game.display("Short range scanner has been repaired.")
            game.display()
            return True
        if game.long_range_scan_damage > 0:
            game.long_range_scan_damage -= 1
            if game.long_range_scan_damage == 0:
                game.display("Long range scanner has been repaired.")
            game.display()
            return True
        if game.shield_control_damage > 0:
            game.shield_control_damage -= 1
            if game.shield_control_damage == 0:
                game.display("Shield controls have been repaired.")
            game.display()
            return True
        if game.computer_damage > 0:
            game.computer_damage -= 1
            if game.computer_damage == 0:
                game.display("The main computer has been repaired.")
            game.display()
            return True
        if game.photon_damage > 0:
            game.photon_damage -= 1
            if game.photon_damage == 0:
                game.display("Photon torpedo controls have been repaired.")
            game.display()
            return True
        if game.phaser_damage > 0:
            game.phaser_damage -= 1
            if game.phaser_damage == 0:
                game.display("Phasers have been repaired.")
            game.display()
            return True
        return False






