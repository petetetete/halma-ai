# Python Standard Library imports
import sys

# Custom module imports
from .halma import Halma
from .tile import Tile

BOARD_SIZES = ["8", "10", "16"]
RED_OPTIONS = ["r", "re", "red"]
GREEN_OPTIONS = ["g", "ge", "green"]

# Process and pass along command line parameters
if __name__ == "__main__":

    # Catch missing parameters
    if len(sys.argv) < 3:
        print("usage: halma <b-size> <t-limit> [<h-player>]")
        sys.exit(-1)

    # Unpack params into variables
    b_size, t_limit = sys.argv[1:3]
    h_player = sys.argv[3] if len(sys.argv) == 4 else None

    # Validate b_size and t_limit
    if b_size not in BOARD_SIZES:
        print("error: <b-size> and should be [" + ", ".join(BOARD_SIZES) + "]")
        sys.exit(-1)

    if not b_size.isdigit() or not t_limit.isdigit():
        print("error: <b-size> and <t-limit> should be integers")
        sys.exit(-1)

    b_size = int(b_size)
    t_limit = int(t_limit)

    # Validate h_player
    if h_player is None:
        c_player = None

    else:
        h_player = h_player.lower()

        if h_player in RED_OPTIONS:
            c_player = Tile.P_GREEN
        elif h_player in GREEN_OPTIONS:
            c_player = Tile.P_RED
        else:
            print("error: <h-player> should be [" +
                  ", ".join(RED_OPTIONS + GREEN_OPTIONS) + "]")
            sys.exit(-1)

    halma = Halma(b_size, c_player)
