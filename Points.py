

class Destination():
    ''' Zero based, Map navigation '''
    def __init__(self, sector=-1, xpos=-1, ypos=-1, warp=0):
        if sector > 64: sector = 64 # zOuter Limits =)
        if xpos > 7:  xpos = 7
        if ypos > 7:  ypos = 7
        if xpos < 0:  xpos = 0
        if ypos < 0:  ypos = 0
        if warp > 10: warp = 10
        if warp < 0:  warp = 0
        self.warp = warp
        self.sector = sector
        self.xpos = xpos
        self.ypos = ypos

    @staticmethod
    def parse_sector(dest, sep=','):
        '''
        Parse: sector#, alpha-col, row-num
        Example: 5,b,1 
        '''
        dest = str(dest)
        cols = dest.split(sep)
        if len(cols) == 3:
            try:
                sector = int(cols[0]) % 8
                if str(cols[1]).isalpha():
                    xpos = ((ord(cols[1]) - ord('a')) % 8)
                    ypos = int(cols[2]) % 8
                    return Destination(sector, xpos, ypos)
            except:
                pass
        return None

    @staticmethod
    def parse_xypos(dest, sep=','):
        '''
        WARNING: USER 1's -> 0-BASED TRANSLATION HERE

        Parse: [a-h], ypos 
                or 
                #,#  
           Return None on error
        Example: b,5 
        '''
        dest = str(dest)
        cols = dest.split(sep)
        if len(cols) == 2:
            try:
                alph = cols[0].strip().lower()[0]
                num = 0
                if alph.isalpha():
                    num = ord(alph) - 96 # 'a' == 1
                else:
                    num = int(alph)
                xpos = num
                ypos = int(cols[1].strip()[0])
                return Destination(-1, xpos-1, ypos-1, -1)
            except:
                pass
        return None

    @staticmethod
    def parse_warp(dest, sep=','):
        '''
        Parse: sector-num, speed-float - None on error
        Example: 5,1.1 
        '''
        dest = str(dest)
        cols = dest.split(sep)
        if len(cols) == 2:
            try:
                sector = int(cols[0].strip())
                if sector < 1:
                    sector = 1
                speed = float(cols[1].strip())
                if speed < 0: speed = 0.1
                if speed > 9: speed = 9.0
                return Destination(sector, -1, -1, speed)
            except:
                pass
        return None






