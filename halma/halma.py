# Python Standard Library imports
import copy
import time
import math

# Custom module imports
from .board import Board
from .tile import Tile


class Halma():

    def __init__(self, b_size=8, c_player=Tile.P_RED):

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
        self.c_player = c_player
        self.board_view = Board(board)
        self.board = board
        self.current_player = Tile.P_GREEN
        self.selected_tile = None
        self.valid_moves = []
        self.computing = False

        if self.c_player == self.current_player:
            self.execute_computer_move()

        self.board_view.add_click_handler(self.tile_clicked)
        self.board_view.draw_tiles(board=self.board)  # Refresh the board

        self.board_view.mainloop()

    def tile_clicked(self, row, col):

        if self.computing:
            return

        new_tile = self.board[row][col]

        # If we are selecting a friendly piece
        if new_tile.piece == self.current_player:

            self.outline_tiles(None)  # Reset outlines

            # Outline the new and valid move tiles
            new_tile.outline = Tile.O_SELECT
            self.valid_moves = self.get_moves_at_tile(new_tile,
                self.board, self.current_player)
            self.outline_tiles([new_tile] + self.valid_moves)

            # Update status and save the new tile
            self.board_view.set_status("Tile `" + str(new_tile) + "` selected")
            self.selected_tile = new_tile

            self.board_view.draw_tiles(board=self.board)  # Refresh the board

        # If we already had a piece selected and we are moving a piece
        elif self.selected_tile and new_tile in self.valid_moves:

            self.outline_tiles(None)  # Reset outlines
            self.move_piece(self.selected_tile, new_tile)  # Move the piece

            # Update status and reset tracking variables
            self.selected_tile = None
            self.valid_moves = []
            self.current_player = (Tile.P_RED
                if self.current_player == Tile.P_GREEN else Tile.P_GREEN)

            self.board_view.draw_tiles(board=self.board)  # Refresh the board

            winner = self.find_winner()
            if winner:
                self.board_view.set_status("The " + ("green"
                    if winner == Tile.P_GREEN else "red") + " player has won!")
                self.current_player = None

            elif self.c_player is not None:
                self.execute_computer_move()

        else:
            self.board_view.set_status("Invalid move attempted")

    def minimax(self, board, depth, player_to_max, maxing=True):

        if depth == 0:
            return self.utility_distance(board, player_to_max), None

        best_move = None

        if maxing:
            best_val = float("-inf")
            moves = self.get_next_moves(board, player_to_max)
        else:
            best_val = float("inf")
            moves = self.get_next_moves(board, (Tile.P_RED
                    if player_to_max == Tile.P_GREEN else Tile.P_GREEN))

        for move in moves:
            for to in move["to"]:

                # Move piece to the move outlined
                piece = move["from"].piece
                move["from"].piece = Tile.P_NONE
                to.piece = piece

                val, _ = self.minimax(board, depth - 1,
                    player_to_max, not maxing)

                # Move the piece pack
                to.piece = Tile.P_NONE
                move["from"].piece = piece

                if ((maxing and val > best_val) or
                    (not maxing and val < best_val)):
                    best_val = val
                    best_move = (move["from"].loc, to.loc)

        return best_val, best_move

    def execute_computer_move(self):

        self.computing = True
        self.board_view.set_status("Computing next move...")
        self.board_view.update()

        start = time.time()
        _, move = self.minimax(self.board, 3, self.c_player)
        end = time.time()

        print("Time to compute:", round(end - start, 2))

        move_from = self.board[move[0][0]][move[0][1]]
        move_to = self.board[move[1][0]][move[1][1]]

        self.outline_tiles(None)  # Reset outlines
        self.move_piece(move_from, move_to)

        self.board_view.draw_tiles(board=self.board)  # Refresh the board

        self.current_player = (Tile.P_RED
            if self.current_player == Tile.P_GREEN else Tile.P_GREEN)

        self.computing = False

    def get_next_moves(self, board, player=1):

        moves = []  # All possible moves
        for col in range(self.b_size):
            for row in range(self.b_size):

                curr_tile = board[row][col]

                # Skip board elements that are not the current player
                if curr_tile.piece != player:
                    continue

                move = {
                    "from": curr_tile,
                    "to": self.get_moves_at_tile(curr_tile, board, player)
                }
                moves += [move]

        return moves

    def get_moves_at_tile(self, tile, board, player, moves=None, adj=True):

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
                new_tile = board[new_row][new_col]
                if new_tile.tile not in valid_tiles:
                    continue

                if new_tile.piece == Tile.P_NONE:
                    if adj:  # Don't consider adjacent on subsequent calls
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
                new_tile = board[new_row][new_col]
                if new_tile in moves or (new_tile.tile not in valid_tiles):
                    continue

                if new_tile.piece == Tile.P_NONE:
                    moves += [new_tile]
                    self.get_moves_at_tile(new_tile, board, player,
                        moves, False)

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

        self.board_view.set_status("Piece moved from `" + str(from_tile) +
            "` to `" + str(to_tile) + "`")

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

    def utility_distance(self, board, player):

        def point_distance(p0, p1):
            return math.sqrt((p1[0] - p0[0])**2 + (p1[1] - p0[1])**2)

        value = 0
        g_goal = (0, 0)
        r_goal = (self.b_size - 1, self.b_size - 1)

        for col in range(self.b_size):
            for row in range(self.b_size):

                tile = board[row][col]

                if tile.piece == Tile.P_GREEN:
                    value -= point_distance(tile.loc, g_goal)

                elif tile.piece == Tile.P_RED:
                    value += point_distance(tile.loc, r_goal)

        if player == Tile.P_RED:
            value *= -1

        return value


if __name__ == "__main__":

    halma = Halma()
