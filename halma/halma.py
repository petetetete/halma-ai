# Custom module imports
from .board import Board

# Move -> [(from_r, from_c), (to_r, to_c)]


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
        self.b_size = b_size
        self.h_player = h_player
        self.board_view = Board(board)
        self.board = board

        self.board_view.add_click_handler(self.tile_clicked)
        print(self.get_next_moves())  # TODO: Remove
        self.board_view.mainloop()

    def tile_clicked(self, row, column):

        # TODO: CHange
        self.board_view.set_status("You clicked on %s/%s" % (row, column))
        # self.board[row][column][2] = (self.board[row][column][2] + 1) % 2
        # self.move_piece((6, 3), (5, 2))
        self.move_piece((7, 4), (6, 3))

        self.board_view.draw_tiles(board=self.board)

    def get_next_moves(self, player=1):

        moves = []  # All possible moves
        for col in range(self.b_size):
            for row in range(self.b_size):

                # Skip board elements that are not the current player
                if self.board[row][col][1] != player:
                    continue

                move = {
                    "from": (row, col),
                    "to": self.get_moves_at_tile(row, col, [])
                }
                moves += [move]

        return moves

    def get_moves_at_tile(self, row, col, moves, adjacent=True):

        # Find and save immediately adjacent moves
        for col_delta in range(-1, 2):
            for row_delta in range(-1, 2):

                # Check adjacent tiles

                new_row = row + row_delta
                new_col = col + col_delta

                # Skip checking degenerate values
                if ((new_row, new_col) in moves or
                    (new_row == row and new_col == col) or
                    new_row < 0 or new_col < 0 or
                    new_row >= self.b_size or new_col >= self.b_size):
                    continue

                if self.board[new_row][new_col][1] == 0:
                    if adjacent:  # Don't consider adjacent on subsequent calls
                        moves += [(new_row, new_col)]
                    continue

                # Check jump tiles

                new_row = new_row + row_delta
                new_col = new_col + col_delta

                # Skip checking degenerate values
                if ((new_row, new_col) in moves or
                    (new_row == row and new_col == col) or
                    new_row < 0 or new_col < 0 or
                    new_row >= self.b_size or new_col >= self.b_size):
                    continue

                if self.board[new_row][new_col][1] == 0:
                    moves += [(new_row, new_col)]
                    self.get_moves_at_tile(new_row, new_col, moves, False)

        return moves

    def move_piece(self, from_tile, to_tile):

        board_from = self.board[from_tile[0]][from_tile[1]]
        board_to = self.board[to_tile[0]][to_tile[1]]

        if board_from[1] == 0:
            self.board_view.set_status("Invalid move")
            return

        # Move piece
        board_to[1] = board_from[1]
        board_from[1] = 0

        # Update outline
        board_to[2] = 2
        board_from[2] = 2


if __name__ == "__main__":

    halma = Halma()