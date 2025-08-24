import tkinter as tk
import numpy as np
import random
import copy
import threading

# Colors for GUI
BACKGROUND_COLOR = "#92877d"
EMPTY_CELL_COLOR = "#9e948a"
TILE_COLORS = {
    2: "#eee4da", 4: "#ede0c8", 8: "#f2b179",
    16: "#f59563", 32: "#f67c5f", 64: "#f65e3b",
    128: "#edcf72", 256: "#edcc61", 512: "#edc850",
    1024: "#edc53f", 2048: "#edc22e"
}
TEXT_COLOR = {2: "#776e65", 4: "#776e65", 8: "#f9f6f2"}

# Initialize game board
class Board:
    def __init__(self):
        self.gridCell = np.zeros((4, 4), dtype=int)
        self.add_random_tile()
        self.add_random_tile()

    def add_random_tile(self):
        empty_cells = [(i, j) for i in range(4) for j in range(4) if self.gridCell[i][j] == 0]
        if empty_cells:
            i, j = random.choice(empty_cells)
            self.gridCell[i][j] = 2 if random.random() < 0.9 else 4

    def move(self, direction):
        rotated = False
        if direction in ["Up", "Down"]:
            self.gridCell = np.rot90(self.gridCell, 1 if direction == "Up" else 3)
            rotated = True

        moved, new_grid = self.compress_and_merge(self.gridCell)

        if rotated:
            self.gridCell = np.rot90(new_grid, 3 if direction == "Up" else 1)
        else:
            self.gridCell = new_grid

        if moved:
            self.add_random_tile()

    def compress_and_merge(self, grid):
        new_grid = np.zeros((4, 4), dtype=int)
        moved = False

        for i in range(4):
            row = grid[i][grid[i] != 0]
            new_row = []

            skip = False
            for j in range(len(row)):
                if skip:
                    skip = False
                    continue
                if j < len(row) - 1 and row[j] == row[j + 1]:
                    new_row.append(row[j] * 2)
                    skip = True
                else:
                    new_row.append(row[j])

            while len(new_row) < 4:
                new_row.append(0)

            new_grid[i] = new_row
            if not np.array_equal(grid[i], new_row):
                moved = True

        return moved, new_grid

    def is_game_over(self):
        if 0 in self.gridCell:
            return False
        for i in range(4):
            for j in range(3):
                if self.gridCell[i][j] == self.gridCell[i][j + 1]:
                    return False
        for i in range(3):
            for j in range(4):
                if self.gridCell[i][j] == self.gridCell[i + 1][j]:
                    return False
        return True

# Monte Carlo Tree Search AI
class MCTS:
    def __init__(self, board, simulations=100):
        self.board = board
        self.simulations = simulations

    def best_move(self):
        moves = ["Left", "Right", "Up", "Down"]
        scores = {move: sum(self.simulate(copy.deepcopy(self.board.gridCell), move) for _ in range(self.simulations)) for move in moves}
        return max(scores, key=scores.get)

    def simulate(self, grid, move):
        test_board = Board()
        test_board.gridCell = np.copy(grid)
        test_board.move(move)
        return np.sum(test_board.gridCell)

# Tkinter GUI
class Game2048(tk.Frame):
    def __init__(self):
        tk.Frame.__init__(self)
        self.grid()
        self.master.title("2048 MCTS AI")
        self.master.bind("<Key>", self.handle_keypress)

        self.board = Board()
        self.ai = MCTS(self.board)

        self.grid_cells = []
        self.build_grid()
        self.update_grid()

    def build_grid(self):
        background = tk.Frame(self, bg=BACKGROUND_COLOR, width=400, height=400)
        background.grid()

        for i in range(4):
            row = []
            for j in range(4):
                cell = tk.Frame(background, bg=EMPTY_CELL_COLOR, width=100, height=100)
                cell.grid(row=i, column=j, padx=5, pady=5)
                label = tk.Label(cell, text="", font=("Arial", 24, "bold"), width=4, height=2)
                label.grid()
                row.append(label)
            self.grid_cells.append(row)

    def update_grid(self):
        for i in range(4):
            for j in range(4):
                tile_value = self.board.gridCell[i][j]
                if tile_value == 0:
                    self.grid_cells[i][j].configure(text="", bg=EMPTY_CELL_COLOR)
                else:
                    self.grid_cells[i][j].configure(text=str(tile_value), bg=TILE_COLORS.get(tile_value, "#3c3a32"), fg=TEXT_COLOR.get(tile_value, "white"))

        if self.board.is_game_over():
            self.show_game_over()

        self.update_idletasks()

    def handle_keypress(self, event):
        key = event.keysym
        if key in ["Left", "Right", "Up", "Down"]:
            self.board.move(key)
            self.update_grid()
        elif key == "p":
            threading.Thread(target=self.run_ai, daemon=True).start()

    def run_ai(self):
        while not self.board.is_game_over():
            best_move = self.ai.best_move()
            self.board.move(best_move)
            self.update_grid()

    def show_game_over(self):
        game_over_frame = tk.Frame(self, width=400, height=400, bg="black")
        game_over_frame.grid()
        label = tk.Label(game_over_frame, text="Game Over!", fg="white", bg="black", font=("Arial", 24, "bold"))
        label.pack(expand=True)

# Run the game
if __name__ == "__main__":
    Game2048().mainloop()