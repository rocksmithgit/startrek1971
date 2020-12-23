import Glyphs

class Quadrant():
    def __init__(self, num=-1, name='', 
                 aliens=-1, stars=-1, 
                 starbases=-1, lines=[]):
        self.name = name
        self.number = num
        self.lines = lines
        self.klingons = aliens
        self.stars = stars
        self.starbases = starbases
        self.scanned = True # meh

    def is_null(self):
        return self.num == -1

    @staticmethod
    def from_area(area):
        if not area:
            return Quadrant()
        name = area.name
        num = area.number
        map = area.get_map()
        return Quadrant(num, name, 
                        area.count_glyphs(Glyphs.KLINGON),
                        area.count_glyphs(Glyphs.STAR),
                        area.count_glyphs(Glyphs.STARBASE),
                        map)


    @staticmethod                
    def display_area(game, quad):
        game.enterprise.condition = "GREEN"
        if game.game_map.num_area_klingons() > 0:
            game.enterprise.condition = "RED"
        elif game.enterprise.energy < 300:
            game.enterprise.condition = "YELLOW"

        sb =   "     a  b  c  d  e  f  g  h \n"
        sb += f"    -=--=--=--=--=--=--=--=-           Quadrant: {quad.name}\n"
        info = list()
        info.append(f"               Area: [{quad.number}]\n")
        info.append(f"           Hazzards: [{quad.stars + quad.klingons}]\n")
        info.append(f"           Stardate: {game.star_date}\n")
        info.append(f"          Condition: {game.enterprise.condition}\n")
        info.append(f"             Energy: {game.enterprise.energy}\n")
        info.append(f"            Shields: {game.enterprise.shield_level}\n")
        info.append(f"   Photon Torpedoes: {game.enterprise.photon_torpedoes}\n")
        info.append(f"     Time remaining: {game.time_remaining}\n")
        for row, line in enumerate(quad.lines):
            sb += f" {row+1} |"
            for col in line:
                sb += col
            sb += info[row]
        sb += f"    -=--=--=--=--=--=--=--=-             Docked: {game.enterprise.docked}\n"
        print(sb, end='')

        if quad.klingons > 0:
            game.display()
            game.display("Condition RED: Klingon ship{0} detected.".format("" if quad.klingons == 1 else "s"))
            if game.enterprise.shield_level == 0 and not game.enterprise.docked:
                game.display("Warning: Shields are down.")
        elif game.enterprise.energy < 300:
            game.display()
            game.display("Condition YELLOW: Low energy level.")
            game.enterprise.condition = "YELLOW"


