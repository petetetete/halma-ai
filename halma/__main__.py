# Python Standard Library imports
import sys

# Custom module imports
from .board import Board

BOARD_SIZES = ["8", "10", "16"]
RED_OPTIONS = ["r", "re", "red"]
GREEN_OPTIONS = ["g", "ge", "green"]

# Process and pass along command line parameters
if __name__ == "__main__":

    # Catch missing parameters
    if len(sys.argv) < 4:
        print("usage: halma <b-size> <t-limit> <h-player>")
        sys.exit(-1)

    # Unpack params into variables
    b_size, t_limit, h_player = sys.argv[1:5]

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
    h_player = h_player.lower()

    if h_player in RED_OPTIONS:
        h_player = "r"
    elif h_player in GREEN_OPTIONS:
        h_player = "g"
    else:
        print("error: <h-player> should be [" +
              ", ".join(RED_OPTIONS + GREEN_OPTIONS) + "]")
        sys.exit(-1)

    board = Board(b_size, h_player)
    board.mainloop()
