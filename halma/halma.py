# Custom module imports
from .board import Board
from .tile import Tile


class Halma():

    def __init__(self, b_size=8, h_player="g"):

        # Create initial board
        board = [[None] * b_size for _ in range(b_size)]
        for row in range(b_size):
            for col in range(b_size):

                if row + col < 4:
                    element = Tile(2, 2, 0, row, col)
                elif row + col > 2 * (b_size - 3):
                    element = Tile(1, 1, 0, row, col)
                else:
                    element = Tile(0, 0, 0, row, col)

                board[row][col] = element

        # Save member variables
        self.b_size = b_size
        self.h_player = h_player  # TODO
        self.board_view = Board(board)
        self.board = board
        self.current_player = Tile.P_GREEN
        self.selected_tile = None
        self.valid_moves = []

        self.board_view.add_click_handler(self.tile_clicked)
        self.board_view.mainloop()

    def tile_clicked(self, row, col):

        new_tile = self.board[row][col]

        # If we are selecting a friendly piece
        if new_tile.piece == self.current_player:

            self.outline_tiles(None)  # Reset outlines

            # Outline the new and valid move tiles
            new_tile.outline = Tile.O_SELECT
            self.valid_moves = self.get_moves_at_tile(new_tile,
                self.current_player)
            self.outline_tiles([new_tile] + self.valid_moves)

            # Update status and save the new tile
            self.board_view.set_status("Tile `" + str(new_tile) + "` selected")
            self.selected_tile = new_tile

        # If we already had a piece selected and
        elif self.selected_tile and new_tile in self.valid_moves:

            self.outline_tiles(None)  # Reset outlines
            self.move_piece(self.selected_tile, new_tile)  # Move the piece

            # Update status and reset tracking variables
            self.board_view.set_status("Piece moved to `" +
                str(new_tile) + "`")
            self.selected_tile = None
            self.valid_moves = []
            self.current_player = (Tile.P_RED
                if self.current_player == Tile.P_GREEN else Tile.P_GREEN)

            winner = self.find_winner()
            if winner:
                self.board_view.set_status("The " + ("green"
                    if winner == Tile.P_GREEN else "red") + " player has won!")
                self.current_player = None

        else:
            self.board_view.set_status("Invalid move attempted")

        self.board_view.draw_tiles(board=self.board)  # Refresh the board UI

    def get_next_moves(self, player=1):

        moves = []  # All possible moves
        for col in range(self.b_size):
            for row in range(self.b_size):

                curr_tile = self.board[row][col]

                # Skip board elements that are not the current player
                if curr_tile.piece != player:
                    continue

                move = {
                    "from": (row, col),
                    "to": self.get_moves_at_tile(curr_tile, player)
                }
                moves += [move]

        return moves

    def get_moves_at_tile(self, tile, player, moves=None, adjacent=True):

        if moves is None:
            moves = []

        row = tile.loc[0]
        col = tile.loc[1]

        # List of valid tile types to move to
        valid_tiles = [Tile.T_NONE, Tile.T_GREEN, Tile.T_RED]
        if tile.tile != player:  # Moving back into your own goal
            valid_tiles.remove(player)
        if tile.tile != Tile.T_NONE and tile.tile != player:
            valid_tiles.remove(Tile.T_NONE)  # Moving out of the enemy's goal

        # Find and save immediately adjacent moves
        for col_delta in range(-1, 2):
            for row_delta in range(-1, 2):

                # Check adjacent tiles

                new_row = row + row_delta
                new_col = col + col_delta

                # Skip checking degenerate values
                if ((new_row == row and new_col == col) or
                    new_row < 0 or new_col < 0 or
                    new_row >= self.b_size or new_col >= self.b_size):
                    continue

                # Handle moves out of/in to goals
                new_tile = self.board[new_row][new_col]
                if new_tile.tile not in valid_tiles:
                    continue

                if new_tile.piece == Tile.P_NONE:
                    if adjacent:  # Don't consider adjacent on subsequent calls
                        moves += [new_tile]
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

                # Handle returning moves and moves out of/in to goals
                new_tile = self.board[new_row][new_col]
                if new_tile in moves or (new_tile.tile not in valid_tiles):
                    continue

                if new_tile.piece == Tile.P_NONE:
                    moves += [new_tile]
                    self.get_moves_at_tile(new_tile, player, moves, False)

        return moves

    def move_piece(self, from_tile, to_tile):

        # Handle trying to move a non-existant piece and moving into a piece
        if from_tile.piece == Tile.P_NONE or to_tile.piece != Tile.P_NONE:
            self.board_view.set_status("Invalid move")
            return

        # Move piece
        to_tile.piece = from_tile.piece
        from_tile.piece = Tile.P_NONE

        # Update outline
        to_tile.outline = Tile.O_MOVED
        from_tile.outline = Tile.O_MOVED

    def find_winner(self):

        g_win = True
        r_win = True

        for col in range(self.b_size):
            for row in range(self.b_size):

                if (self.board[row][col].tile == Tile.T_RED and
                    self.board[row][col].piece != Tile.P_GREEN):
                    g_win = False

                if (self.board[row][col].tile == Tile.T_GREEN and
                    self.board[row][col].piece != Tile.P_RED):
                    r_win = False

                if g_win is False and r_win is False:
                    break

        return Tile.P_GREEN if g_win else Tile.P_RED if r_win else None

    def outline_tiles(self, tiles=[], outline_type=Tile.O_SELECT):

        if tiles is None:
            tiles = [j for i in self.board for j in i]
            outline_type = Tile.O_NONE

        for tile in tiles:
            tile.outline = outline_type


if __name__ == "__main__":

    halma = Halma()
