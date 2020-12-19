
class status(object):

    @staticmethod
    def display_status(game):
        game.display()
        game.display("               Time Remaining: {0}".format(game.time_remaining))
        game.display("      Klingon Ships Remaining: {0}".format(game.klingons))
        game.display("                    Starbases: {0}".format(game.starbases))
        game.display("           Warp Engine Damage: {0}".format(game.navigation_damage))
        game.display("   Short Range Scanner Damage: {0}".format(game.short_range_scan_damage))
        game.display("    Long Range Scanner Damage: {0}".format(game.long_range_scan_damage))
        game.display("       Shield Controls Damage: {0}".format(game.shield_control_damage))
        game.display("         Main Computer Damage: {0}".format(game.computer_damage))
        game.display("Photon Torpedo Control Damage: {0}".format(game.photon_damage))
        game.display("                Phaser Damage: {0}".format(game.phaser_damage))
        game.display()


    @staticmethod
    def display_galactic_record(game):
        game.display()
        sb = ""
        game.display("-------------------------------------------------")
        for i in range(8):
            for j in range(8):
                sb += "| "
                klingon_count = 0
                starbase_count = 0
                star_count = 0
                quadrant = game.quadrants[i][j]
                if quadrant.scanned:
                    klingon_count = quadrant.klingons
                    starbase_count = 1 if quadrant.starbase else 0
                    star_count = quadrant.stars
                sb = sb + \
                    "{0}{1}{2} ".format(klingon_count, starbase_count, star_count)
            sb += "|"
            game.display(sb)
            sb = ""
            game.display("-------------------------------------------------")
        game.display()


    @staticmethod
    def print_game_status(game):
        if game.destroyed:
            game.display("MISSION FAILED: ENTERPRISE DESTROYED!!!")
            game.display('\n'*2)
        elif game.energy == 0:
            game.display("MISSION FAILED: ENTERPRISE RAN OUT OF ENERGY.")
            game.display('\n'*2)
        elif game.klingons == 0:
            game.display("MISSION ACCOMPLISHED: ALL KLINGON SHIPS DESTROYED. WELL DONE!!!")
            game.display('\n'*2)
        elif game.time_remaining == 0:
            game.display("MISSION FAILED: ENTERPRISE RAN OUT OF TIME.")
            game.display('\n'*2)




