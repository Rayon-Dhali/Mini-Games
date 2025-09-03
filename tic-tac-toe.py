import tkinter as tk
from tkinter import messagebox

class TicTacToe(tk.Tk):
    """
    A simple Tic-Tac-Toe game built with Tkinter.

    Features:
    - 3x3 grid buttons for moves
    - Player turn indicator (X vs O)
    - Win detection + line highlighting
    - Draw detection
    - Reset button and keyboard shortcut ("R")
    - Beginner-friendly comments throughout
    """

    # ---------- Game Constants ----------
    SIZE = 3               # 3x3 board
    X = "X"                # Player 1 marker
    O = "O"                # Player 2 marker
    FONT = ("Helvetica", 28, "bold")  # big font for the grid
    BG_COLOR = "#f0f0f0"

    def __init__(self):
        super().__init__()

        # ----- Window Setup -----
        self.title("Tic Tac Toe")
        self.resizable(False, False)
        self.configure(bg=self.BG_COLOR)

        # ----- Game State -----
        self.current_player = self.X
        self.board = [[None for _ in range(self.SIZE)] for _ in range(self.SIZE)]
        self.game_over = False

        # ----- Build UI -----
        self._create_ui()

    # ------------------ UI ------------------
    def _create_ui(self):
        """Create the top bar, 3x3 button grid, and status bar."""
        # Top frame (turn label + reset button)
        top_frame = tk.Frame(self, bg="white", height=50)
        top_frame.pack(fill="x", padx=10, pady=5)

        self.turn_label = tk.Label(
            top_frame,
            text=self._turn_text(),
            font=("Helvetica", 16, "bold"),
            bg="white"
        )
        self.turn_label.pack(side="left", padx=10)

        reset_btn = tk.Button(
            top_frame,
            text="Reset Game",
            command=self.reset_game,
            font=("Helvetica", 12),
            bg="#EAEAEA",
            activebackground="#DDDDDD"
        )
        reset_btn.pack(side="right", padx=10)

        # Grid of buttons (the board)
        self.buttons = []
        grid_frame = tk.Frame(self, bg=self.BG_COLOR)
        grid_frame.pack(padx=10, pady=10)

        for r in range(self.SIZE):
            row_buttons = []
            for c in range(self.SIZE):
                btn = tk.Button(
                    grid_frame,
                    text="",
                    font=self.FONT,
                    width=5,
                    height=2,
                    command=lambda r=r, c=c: self._on_click(r, c)
                )
                btn.grid(row=r, column=c, padx=5, pady=5)
                row_buttons.append(btn)
            self.buttons.append(row_buttons)

        # Status bar (instructions)
        self.status = tk.Label(
            self,
            text="Click a square to make a move. Press 'R' to reset.",
            font=("Helvetica", 10),
            anchor="w",
            bg=self.BG_COLOR
        )
        self.status.pack(fill="x", padx=10, pady=(0, 10))

        # Keyboard binding
        self.bind("<Key>", self._on_key)

    # ------------------ Event Handlers ------------------
    def _on_click(self, row, col):
        """Handle a button press at (row, col)."""
        if self.game_over:
            return

        # Ignore if the cell is already filled
        if self.board[row][col] is not None:
            return

        # Place the marker (X or O)
        self.board[row][col] = self.current_player
        self.buttons[row][col].config(text=self.current_player)

        # Check for win or draw
        winner, coords = self._check_winner()
        if winner:
            self._highlight_winner(coords)
            messagebox.showinfo("Game Over", f"Player {winner} wins!")
            self.game_over = True
            return

        if self._is_board_full():
            messagebox.showinfo("Game Over", "It's a draw!")
            self.game_over = True
            return

        # Switch player and update UI
        self.current_player = self.O if self.current_player == self.X else self.X
        self.turn_label.config(text=self._turn_text())

    def _on_key(self, event):
        """Keyboard shortcuts (R = reset)."""
        if event.char.lower() == "r":
            self.reset_game()

    # ------------------ Game Logic ------------------
    def _check_winner(self):
        """
        Check rows, columns, and diagonals for a winner.
        Returns (winner, coords) where coords is list of (r,c) of the winning line.
        """
        b = self.board
        s = self.SIZE

        # Check rows
        for r in range(s):
            if b[r][0] and all(b[r][c] == b[r][0] for c in range(s)):
                return b[r][0], [(r, c) for c in range(s)]

        # Check columns
        for c in range(s):
            if b[0][c] and all(b[r][c] == b[0][c] for r in range(s)):
                return b[0][c], [(r, c) for r in range(s)]

        # Check main diagonal
        if b[0][0] and all(b[i][i] == b[0][0] for i in range(s)):
            return b[0][0], [(i, i) for i in range(s)]

        # Check anti-diagonal
        if b[0][s-1] and all(b[i][s-1-i] == b[0][s-1] for i in range(s)):
            return b[0][s-1], [(i, s-1-i) for i in range(s)]

        return None, []

    def _is_board_full(self):
        """Return True if every square is filled."""
        return all(self.board[r][c] is not None for r in range(self.SIZE) for c in range(self.SIZE))

    def _highlight_winner(self, coords):
        """Highlight the winning 3 cells with green background."""
        for (r, c) in coords:
            self.buttons[r][c].config(bg="lightgreen")

    def reset_game(self):
        """Reset the game state and clear the board."""
        self.board = [[None for _ in range(self.SIZE)] for _ in range(self.SIZE)]
        self.current_player = self.X
        self.game_over = False

        for r in range(self.SIZE):
            for c in range(self.SIZE):
                self.buttons[r][c].config(text="", bg="SystemButtonFace")

        self.turn_label.config(text=self._turn_text())

    # ------------------ Helpers ------------------
    def _turn_text(self):
        """Return a string like 'Player's Turn: X'."""
        return f"Player's Turn: {self.current_player}"

# ------------------ Main Entry Point ------------------
if __name__ == "__main__":
    game = TicTacToe()
    game.mainloop()
