import tkinter as tk


class Board(tk.Tk):

    def __init__(self, b_size=8, *args, **kwargs):

        # Initialize parent tk class
        tk.Tk.__init__(self, *args, **kwargs)

        # Save metadata
        self.title("Halma | Deep Red")
        self.wm_iconbitmap("deep_red.ico")
        self.resizable(False, False)
        self.configure(bg="#fff")

        # Save tracking variables
        self.b_size = b_size
        self.tiles = {}

        # Create column/row labels
        label_font = "Helvetica 16"
        label_bg = "#fff"
        label_fg = "#333"
        for i in range(b_size):

            row_label1 = tk.Label(self, text=i + 1, font=label_font,
                bg=label_bg, fg=label_fg)
            row_label1.grid(row=i + 1, column=0)

            row_label2 = tk.Label(self, text=i + 1, font=label_font,
                bg=label_bg, fg=label_fg)
            row_label2.grid(row=i + 1, column=b_size + 2)

            col_label1 = tk.Label(self, text=chr(i + 97), font=label_font,
                bg=label_bg, fg=label_fg)
            col_label1.grid(row=0, column=i + 1)

            col_label2 = tk.Label(self, text=chr(i + 97), font=label_font,
                bg=label_bg, fg=label_fg)
            col_label2.grid(row=b_size + 2, column=i + 1)

        # Create grid canvas
        self.canvas = tk.Canvas(self, width=550, height=550, bg="#fff",
            highlightthickness=0)
        self.canvas.grid(row=1, column=1, columnspan=b_size, rowspan=b_size)

        # Create status label
        self.status = tk.Label(self, anchor="c", font=(None, 16),
            bg="#EF4235", fg="#fff", text="Status Messages")
        self.status.grid(row=b_size + 3, column=0, columnspan=b_size + 3,
            sticky="ewns")

        # Bind the drawing function and configure grid sizes
        self.canvas.bind("<Configure>", self.redraw)
        self.columnconfigure(0, minsize=48)
        self.rowconfigure(0, minsize=48)
        self.columnconfigure(b_size + 2, minsize=48)
        self.rowconfigure(b_size + 2, minsize=48)
        self.rowconfigure(b_size + 3, minsize=48)

    def redraw(self, event=None):

        # Delete old rectangles and save properties
        self.canvas.delete("rec")
        cell_width = int(self.canvas.winfo_width() / self.b_size)
        cell_height = int(self.canvas.winfo_height() / self.b_size)
        border_size = 5

        # Recreate each rectangle
        for column in range(self.b_size):
            for row in range(self.b_size):

                color = "#8C6C50" if (row + column) % 2 else "#DBBFA0"

                # Calculate pixel positions
                x1 = column * cell_width + border_size
                y1 = row * cell_height + border_size
                x2 = x1 + cell_width - border_size
                y2 = y1 + cell_height - border_size

                # Create and save tile
                tile = self.canvas.create_rectangle(x1, y1, x2, y2, tags="rec",
                    width=border_size, fill=color, outline=color)
                self.tiles[row, column] = tile
                self.canvas.tag_bind(tile, "<1>", lambda event, row=row,
                    column=column: self.clicked(row, column))

    def clicked(self, row, column):
        tile = self.tiles[row, column]
        tile_color = self.canvas.itemcget(tile, "outline")
        new_color = "blue" if tile_color == "red" else "red"
        self.canvas.itemconfig(tile, outline=new_color)
        self.status.configure(text="You clicked on %s/%s" % (row, column))


if __name__ == "__main__":

    board = Board()
    board.mainloop()
