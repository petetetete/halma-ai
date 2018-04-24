# index 0 is space type
#   0 = blank normal space
#   1 = blank green goal space
#   2 = blank red goal space
#
# index 1 is piece type
#   0 = no piece
#   1 = green piece
#   2 = red piece
#
# index 2 is the outline type
#   0 = no outline
#   1 = selected outline
#   2 = just moved


class Tile():

    S_NORMAL = 0
    S_G_GOAL = 1
    S_R_GOAL = 2

    P_NORMAL = 0
    P_GREEN = 1
    P_RED = 2

    O_NORMAL = 0
    O_SELECT = 1

    def __init__(self, tile=0, piece=0, outline=0):
        self.tile = tile
        self.piece = piece
        self.outline = outline
