# Custom module imports
from .board import Board


class Halma():

    def __init__(self, b_size=8, h_player="g"):

        # Create initial board
        board = [[0] * b_size for _ in range(b_size)]
        for row in range(b_size):
            for col in range(b_size):

                if row + col < 4:
                    element = [2, 2, 0]
                elif row + col > 2 * (b_size - 3):
                    element = [1, 1, 0]
                else:
                    element = [0, 0, 0]

                board[row][col] = element

        # Save member variables
        self.board_view = Board(board)
        self.board = board

        self.board_view.add_click_handler(self.tile_clicked)
        self.board_view.mainloop()

    def tile_clicked(self, row, column):
        self.board_view.set_status("You clicked on %s/%s" % (row, column))
        self.board[row][column][2] = 1

        self.board_view.draw_tiles(board=self.board)


if __name__ == "__main__":

    halma = Halma()
