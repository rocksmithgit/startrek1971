import Glyphs

class Stats():

    @staticmethod
    def show_ship_status(game):
        game.display()
        game.display(f"               Time Remaining: {game.time_remaining}")
        game.display(f"      Klingon Ships Remaining: {game.game_map.klingons}")
        game.display(f"                    Starbases: {game.game_map.starbases}")
        game.display(f"           Warp Engine Damage: {game.enterprise.navigation_damage}")
        game.display(f"   Short Range Scanner Damage: {game.enterprise.short_range_scan_damage}")
        game.display(f"    Long Range Scanner Damage: {game.enterprise.long_range_scan_damage}")
        game.display(f"       Shield Controls Damage: {game.enterprise.shield_control_damage}")
        game.display(f"         Main Computer Damage: {game.enterprise.computer_damage}")
        game.display(f"Photon Torpedo Control Damage: {game.enterprise.photon_damage}")
        game.display(f"                Phaser Damage: {game.enterprise.phaser_damage}")
        game.display()


    @staticmethod
    def show_galactic_status(game):
        game.display()
        game.display("-------------------------------------------------")
        game.display(
            f"{Glyphs.KLINGON}{game.game_map.klingons}|" +
            f"{Glyphs.STARBASE}|{game.game_map.starbases}|" +
            f"{Glyphs.STAR}{game.game_map.stars}")
        game.display("-------------------------------------------------")
        game.display()


    @staticmethod
    def show_exit_status(game):
        if game.destroyed:
            msg = "MISSION FAILED: ENTERPRISE DESTROYED!!!"
            game.display('!' * len(msg))
            game.display(msg)
            game.display('!' * len(msg))
        elif game.enterprise.energy == 0:
            msg = "MISSION FAILED: ENTERPRISE RAN OUT OF ENERGY."
            game.display('!' * len(msg))
            game.display(msg)
            game.display('!' * len(msg))
        elif game.game_map.klingons == 0:
            msg = "MISSION ACCOMPLISHED: ALL ENEMY SHIPS DESTROYED. WELL DONE!!!"
            game.display('!' * len(msg))
            game.display(msg)
            game.display('!' * len(msg))
        elif game.time_remaining == 0:
            msg = "MISSION FAILED: ENTERPRISE RAN OUT OF TIME."
            game.display('!' * len(msg))
            game.display(msg)
            game.display('!' * len(msg))

