import Glyphs

class Quadrant():
    def __init__(self, num=-1, name='', lines=[], 
                 aliens=-1, stars=-1, starbases=-1):
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
        return Quadrant(num, name, map, 
                        area.get_data(Glyphs.KLINGON),
                        area.count_glyphs(Glyphs.STAR),
                        area.count_glyphs(Glyphs.STARBASE))

