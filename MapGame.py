import random
import TrekStrings

import Glyphs
from ShipKlingon import ShipKlingon
from Points import Destination
from Quadrant import Quadrant
from ErrorCollision import ErrorEnterpriseCollision

import MapSparse

class GameMap(MapSparse.SparseMap):

    def __init__(self):
        super().__init__()
        self.sector = -1
        self.xpos = self.ypos = -1
        self.stars      = -1
        self.klingons   = -1
        self.starbases  = -1
        self.last_nav = None
        
    def place(self, takers):
        ''' 
        Randomly place game-objects, into the map.
        '''
        if not sum(takers):
            return None
        takers =list(takers)
        for which, nelem in enumerate(takers):
            if not nelem:
                continue
            to_take = random.randrange(0, nelem)
            if nelem is 1:
                to_take = 1
            if not to_take:
                continue
            taken = 0
            while taken != to_take:
                ss = random.randrange(1, 64)
                area = self.get_area(ss)
                should_take = random.randrange(1, 8)
                if which is 0:
                    if area.count_glyphs(Glyphs.STARBASE) != 0:
                        continue
                    area.place_glyph(Glyphs.STARBASE)
                elif which is 1:
                    area.place_glyph(Glyphs.STAR)
                elif which is 2:
                    if area.count_glyphs(Glyphs.KLINGON) > 3:
                        continue
                    area.place_glyph(Glyphs.KLINGON)
                taken += 1
                if taken == to_take:
                    break;
            takers[which] -= taken
        return tuple(takers)

    def enterprise_in(self, dest=None):
        ''' Place the ENTERPRISE at the destination, else a 
        random one. 
        
        Will raise an ErrorEnterpriseCollision, upon same.

        Returns the final x, y location upon success '''
        area = self.pw_area()
        berror = False
        if area:
            for p in area._pieces:
                if p.xpos == dest.xpos and p.ypos == dest.ypos:
                    pos = area.place_glyph(Glyphs.ENTERPRISE)
                    berror = p.glyph
            pos = area.place_glyph(Glyphs.ENTERPRISE, dest)
            if berror:
                raise ErrorEnterpriseCollision(berror)
            if pos:
                return pos
        return False

    def enterprise_location(self):
        ''' Get Enterprise location. False if not found. '''
        area = self.pw_area()
        if area:
            for obj in area._pieces:
                if obj.glyph == Glyphs.ENTERPRISE:
                    return obj.xpos, obj.ypos
        return False

    def enterprise_out(self):
        ''' Remove the ENTERPRISE from the present AREA '''
        pos = self.enterprise_location()
        if pos:
            self.remove(*pos)

    def place_glyph(self, glyph, dest=None):
        ''' Place the glyph as the destination, else a random one '''
        area = self.pw_area()
        if area:
            pos = area.place_glyph(self, glyph, dest)
            if pos:
                return True
        return False

    def remove(self, xpos, ypos):
        ''' Remove ANYTHING from the present AREA '''
        area = self.pw_area()
        if area:
            area.remove(xpos, ypos)

    def pw_area(self):
        ''' 
        Return the internal / sparsely populated AREA object.
        Return an empty / default AREA upon coordinate error.
        '''
        if self.sector > 0:
            for area in self.areas():
                if area.number == self.sector:
                    return area
        return MapSparse.SparseMap.Area()

    def scan_quad(self, sector):
        '''
        Return a scan (LRS?) for a specific quadrant.
        Return empty quadrant, on error.
        '''
        area = self.get_area(sector)
        if area:
            return Quadrant.from_area(area)
        return Quadrant()

    def _count_area(self, glyph):
        ''' Tally the number of glyphs in the AREA '''
        count = 0
        area = self.pw_area()
        if area:
            for obj in area._pieces:
                if obj.glyph == glyph:
                    count += 1
        return count

    def update_counts(self):
        self.klingons = self.starbases = self.stars = 0
        for area in self.areas():
            self.klingons  += area.count_glyphs(Glyphs.KLINGON)
            self.starbases += area.count_glyphs(Glyphs.STARBASE)
            self.stars     += area.count_glyphs(Glyphs.STAR)

    def remove_items(self, removed):
        area = self.pw_area()
        for obj in removed:
            area.remove(obj.xpos, obj.ypos)
        self.update_counts()

    def get_area_klingons(self):
        '''
        Return this Area's data for Kingons, in an array.
        '''
        results = []
        area = self.pw_area()
        for data in area.get_data(Glyphs.KLINGON):
            ship = ShipKlingon()
            ship.from_map(data.xpos, data.ypos)
            results.append(ship)
        return results

    def num_area_klingons(self):
        return self._count_area(Glyphs.KLINGON)

    def num_area_starbases(self):
        return self._count_area(Glyphs.STARBASE)

    def num_area_stars(self):
        return self._count_area(Glyphs.STAR)

    def get_area_objects(self):
        '''
        Return the actual objects, as located in the Area. 
        NOTE: Changes to this collection will update Area
        content.
        '''
        area = self.pw_area()
        return area._pieces

    def game_id(self, piece):
        '''
        Uniquely identify a game piece / object.
        '''
        area = self.pw_area()
        num = (area.number * 100) + (piece.ypos * 8) + piece.xpos
        return f"{piece.glyph[1]}x{num}"

    def get_all(self, glyph):
        '''
        Return [ [AREA, PIECE], ... ] for every glyph found.
        '''
        results = []
        for area in self.areas():
            for piece in area.get_data(glyph):
                results.append([area, piece])
        return results

    def quad(self):
        area = self.pw_area()
        return Quadrant.from_area(area)

    def get_map(self):
        ''' 
        Generate AREA map of the present sector.
        '''
        area = self.pw_area()
        return area.get_map()

    def random_jump(self):
        dest = Destination(
            random.randint(1, 64),
            random.randint(0, 7),
            random.randint(0, 7)
            )
        self._go_to(dest)

    def _go_to(self, dest):
        '''
        Place the main player (Enterprise, for now) into the Area.
        Returns the final, effective, player location.
        '''
        if self.last_nav:
            self.enterprise_out()
        if dest.sector > 0:
            self.sector = dest.sector
        if dest.xpos != -1:
            self.xpos = dest.xpos
            self.ypos = dest.ypos
        dest.sector = self.sector
        dest.xpos = self.xpos
        dest.ypos = self.ypos
        pos = self.enterprise_in(dest)
        dest.xpos = pos[0]
        dest.ypos = pos[1]
        self.last_nav = dest
        return dest

    def randomize(self, bases=None, stars=None, aliens=None):
        if not aliens:
            aliens = 15 + random.randint(0, 5)
        if not bases:
            bases = 2 + random.randint(0, 2)
        self.starbases = bases
        self.klingons = aliens
        self.stars = stars
        self.init()
        takers = bases, stars, aliens
        while takers:
            for lrs in self._map:
                takers = self.place(takers)
                if not takers:
                    break



