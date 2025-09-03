import tkinter as tk
from tkinter import messagebox

class ConnectFour(tk.Tk):
    """
    A simple Connect 4 game built with Tkinter.

    Improvements over the original:
    - Cleaner layout: top bar (status + reset), game board, status bar.
    - Clear sizing constants (no magic numbers) and a slightly larger window.
    - Hover highlight to show the active column before you click.
    - Winner highlighting (the 4-in-a-row discs are outlined).
    - Safer click handling (ignores clicks outside the board).
    - Thorough beginner-friendly comments.
    """

    # ---------- Visual + Layout Constants (easy to tweak) ----------
    ROWS = 6
    COLS = 7
    CELL = 90             # pixel size of each cell (slot)
    SLOT_MARGIN = 8       # inner margin for the white slot circles
    DISC_MARGIN = 14      # inner margin for the colored discs
    BOARD_BG = "#0A3A8B"  # deep blue board (looks good)
    PADDING = 12          # outer padding around the board
    TOP_BAR_H = 64        # height for the top info area
    STATUS_H = 28         # height for the bottom status bar

    RED = "red"
    YELLOW = "gold"       # "yellow" can look dull; "gold" reads nicer

    def __init__(self):
        super().__init__()

        # ----- Window setup -----
        self.title("Connect 4")
        self.resizable(False, False)

        # Compute canvas size from constants so the geometry matches the board
        self.canvas_w = self.COLS * self.CELL
        self.canvas_h = self.ROWS * self.CELL
        total_w = self.canvas_w + self.PADDING * 2
        total_h = self.TOP_BAR_H + self.canvas_h + self.STATUS_H + self.PADDING * 2

        # Set a precise geometry string like "widthxheight"
        self.geometry(f"{total_w}x{total_h}")

        # ----- Game state -----
        # Board is a 2D list (ROWS x COLS) storing None, "red", or "gold"
        self.board = [[None for _ in range(self.COLS)] for _ in range(self.ROWS)]
        self.current_player = self.RED
        self.game_over = False
        self.win_coords = []  # list of (row, col) that form the winning line

        # Track hover column to draw a subtle highlight
        self.hover_col = None

        # Build UI and draw initial board
        self._create_ui()
        self._draw_board()

    # ---------------------- UI Construction ----------------------
    def _create_ui(self):
        """
        Build the three main UI sections:
        1) Top bar (turn label + reset button)
        2) Canvas (the game board)
        3) Status bar (small instruction/footer)
        """
        # Top bar
        self.top_frame = tk.Frame(self, height=self.TOP_BAR_H, bg="white")
        self.top_frame.pack(fill="x", padx=self.PADDING, pady=(self.PADDING, 4))

        self.turn_label = tk.Label(
            self.top_frame,
            text=self._turn_text(),
            font=("Helvetica", 16, "bold"),
            bg="white"
        )
        self.turn_label.pack(side="left")

        self.reset_btn = tk.Button(
            self.top_frame,
            text="Reset Game",
            command=self.reset_game,
            font=("Helvetica", 12),
            bg="#EAEAEA",
            activebackground="#DDDDDD"
        )
        self.reset_btn.pack(side="right")

        # Canvas for the board
        self.canvas = tk.Canvas(
            self,
            width=self.canvas_w,
            height=self.canvas_h,
            bg=self.BOARD_BG,
            highlightthickness=0
        )
        self.canvas.pack(padx=self.PADDING, pady=4)

        # Status bar (small instruction text at the bottom)
        self.status = tk.Label(
            self,
            text="Click a column to drop a disc. Press 'R' to reset.",
            font=("Helvetica", 10),
            anchor="w"
        )
        self.status.pack(fill="x", padx=self.PADDING, pady=(4, self.PADDING))

        # Mouse + keyboard bindings
        self.canvas.bind("<Button-1>", self._on_click)
        self.canvas.bind("<Motion>", self._on_motion)
        self.bind("<Key>", self._on_key)

    # ---------------------- Drawing Helpers ----------------------
    def _draw_board(self):
        """
        Redraw the entire board:
        - Clear canvas
        - Draw slots (white circles) on the blue background
        - Draw any placed discs
        - Draw hover column highlight (if any)
        - If someone won, outline those 4 discs to make it obvious
        """
        self.canvas.delete("all")

        cell_w = self.CELL
        cell_h = self.CELL

        # Optional: draw a subtle rounded rectangle as board background (visual only)
        # Here we already use a solid bg color, so slots will "punch through" as white circles.

        # Draw hover column highlight (light overlay rectangle)
        if self.hover_col is not None and not self.game_over:
            x1 = self.hover_col * cell_w
            x2 = x1 + cell_w
            self.canvas.create_rectangle(
                x1, 0, x2, self.canvas_h,
                fill="#ffffff", stipple="gray25", outline=""
            )

        # Draw the grid of slots and any discs present
        for row in range(self.ROWS):
            for col in range(self.COLS):
                x1 = col * cell_w
                y1 = row * cell_h
                x2 = x1 + cell_w
                y2 = y1 + cell_h

                # White slot (hole)
                self.canvas.create_oval(
                    x1 + self.SLOT_MARGIN, y1 + self.SLOT_MARGIN,
                    x2 - self.SLOT_MARGIN, y2 - self.SLOT_MARGIN,
                    fill="white", outline=self.BOARD_BG, width=2
                )

                # If a disc is placed here, draw it as a filled circle
                color = self.board[row][col]
                if color:
                    self.canvas.create_oval(
                        x1 + self.DISC_MARGIN, y1 + self.DISC_MARGIN,
                        x2 - self.DISC_MARGIN, y2 - self.DISC_MARGIN,
                        fill=color, outline=color
                    )

        # If there's a win, outline those four discs
        if self.win_coords:
            for (r, c) in self.win_coords:
                x1 = c * cell_w
                y1 = r * cell_h
                x2 = x1 + cell_w
                y2 = y1 + cell_h
                self.canvas.create_oval(
                    x1 + self.DISC_MARGIN, y1 + self.DISC_MARGIN,
                    x2 - self.DISC_MARGIN, y2 - self.DISC_MARGIN,
                    outline="black", width=4
                )

        # Update the turn label color to match the current player
        self.turn_label.config(text=self._turn_text(), fg=self.current_player)

    def _turn_text(self):
        """Return a user-friendly 'Player's Turn' string."""
        return f"Player's Turn: {'Red' if self.current_player == self.RED else 'Yellow'}"

    # ---------------------- Event Handlers ----------------------
    def _on_motion(self, event):
        """
        Track the mouse x-position to compute the column under the cursor.
        We use this to draw a translucent highlight for that column.
        """
        if self.game_over:
            self.hover_col = None
            self._draw_board()
            return

        # Convert mouse x coordinate to column index; also guard bounds
        col = event.x // self.CELL
        if 0 <= col < self.COLS:
            if col != self.hover_col:
                self.hover_col = col
                self._draw_board()
        else:
            # Mouse moved outside the board area (to the sides)
            if self.hover_col is not None:
                self.hover_col = None
                self._draw_board()

    def _on_key(self, event):
        """Keyboard shortcuts: 'r' to reset the game."""
        if event.char.lower() == 'r':
            self.reset_game()

    def _on_click(self, event):
        """
        Handle a left-mouse click:
        - Determine which column was clicked
        - Drop a disc to the lowest empty row in that column
        - Check for win/draw and switch players if game continues
        """
        if self.game_over:
            return

        # Determine clicked column; ignore clicks outside the board
        col = event.x // self.CELL
        if not (0 <= col < self.COLS):
            return

        # Find the lowest empty row in this column (from bottom up)
        target_row = None
        for row in range(self.ROWS - 1, -1, -1):
            if not self.board[row][col]:
                target_row = row
                break

        # Column is full
        if target_row is None:
            messagebox.showinfo("Column Full", "Try a different column.")
            return

        # Place the disc, redraw, and check for result
        self.board[target_row][col] = self.current_player
        winner, win_coords = self._check_winner(target_row, col)
        if winner:
            self.game_over = True
            self.win_coords = win_coords
            self._draw_board()
            messagebox.showinfo("Game Over", f"{'Red' if winner == self.RED else 'Yellow'} player wins!")
            return

        if self._is_board_full():
            self.game_over = True
            self._draw_board()
            messagebox.showinfo("Game Over", "It's a draw!")
            return

        # Switch player and refresh UI
        self.current_player = self.YELLOW if self.current_player == self.RED else self.RED
        self._draw_board()

    # ---------------------- Game Logic ----------------------
    def _check_winner(self, row, col):
        """
        Check if placing a disc at (row, col) creates a 4-in-a-row.
        Returns (winning_color, coords_list) or (None, []).
        """
        color = self.current_player  # we just placed this color
        directions = [
            (0, 1),   # Horizontal
            (1, 0),   # Vertical
            (1, 1),   # Diagonal down-right
            (1, -1)   # Diagonal down-left
        ]

        for dr, dc in directions:
            coords = [(row, col)]  # start with the current piece

            # Check in the positive direction (dr, dc)
            r, c = row + dr, col + dc
            while 0 <= r < self.ROWS and 0 <= c < self.COLS and self.board[r][c] == color:
                coords.append((r, c))
                r += dr
                c += dc

            # Check in the negative direction (-dr, -dc)
            r, c = row - dr, col - dc
            while 0 <= r < self.ROWS and 0 <= c < self.COLS and self.board[r][c] == color:
                coords.append((r, c))
                r -= dr
                c -= dc

            if len(coords) >= 4:
                # We found a winning line
                return color, coords

        return None, []

    def _is_board_full(self):
        """
        The board is full if the top row has no empty cells.
        We only need to check the top row for speed.
        """
        return all(self.board[0][c] is not None for c in range(self.COLS))

    def reset_game(self):
        """Reset the board and UI to start a new game."""
        self.board = [[None for _ in range(self.COLS)] for _ in range(self.ROWS)]
        self.current_player = self.RED
        self.game_over = False
        self.win_coords = []
        self.hover_col = None
        self.turn_label.config(text=self._turn_text(), fg=self.current_player)
        self._draw_board()

# ---------------------- Main Entry Point ----------------------
if __name__ == "__main__":
    game = ConnectFour()
    game.mainloop()
