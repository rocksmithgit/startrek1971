class scanner(object):

    @staticmethod
    def short_range_scan(game):
        if game.short_range_scan_damage > 0:
            game.display("Short range scanner is damaged. Repairs are underway.")
            game.display()
        else:
            quadrant = game.quadrants[game.quadrant_y][game.quadrant_x]
            quadrant.scanned = True
            game.print_sector(quadrant)
        game.display()

    @staticmethod
    def long_range_scan(game):
        if game.long_range_scan_damage > 0:
            game.display("Long range scanner is damaged. Repairs are underway.")
            game.display()
            return
        sb = ""
        game.display("-------------------")
        for i in range(game.quadrant_y - 1, game.quadrant_y+2):  # quadrantY + 1 ?
            for j in range(game.quadrant_x - 1, game.quadrant_x+2):  # quadrantX + 1?
                sb += "| "
                klingon_count = 0
                starbase_count = 0
                star_count = 0
                if 0 <= i < 8 and 0 <= j < 8:
                    quadrant = game.quadrants[i][j]
                    quadrant.scanned = True
                    klingon_count = quadrant.klingons
                    starbase_count = 1 if quadrant.starbase else 0
                    star_count = quadrant.stars
                sb = sb + \
                    "{0}{1}{2} ".format(klingon_count, starbase_count, star_count)
            sb += "|"
            game.display(sb)
            sb = ""
            game.display("-------------------")
        game.display()




