import random


class Enterprise(object):

    def __init__(self):
        self.energy = 0
        self.shield_level = 0
        self.docked = False
        self.condition = "GREEN"
        self.navigation_damage = 0
        self.short_range_scan_damage = 0
        self.long_range_scan_damage = 0
        self.shield_control_damage = 0
        self.computer_damage = 0
        self.photon_damage = 0
        self.phaser_damage = 0


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






