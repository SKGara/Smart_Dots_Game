import tkinter as tk
import random

class SmartDotGameBacktracking:
    def __init__(self, root, grid_size=5, num_dots=8):  
        self.root = root
        self.grid_size = grid_size
        self.num_dots = num_dots
        self.grid = [[0] * grid_size for _ in range(grid_size)]
        self.row_clues = [0] * grid_size
        self.col_clues = [0] * grid_size
        self.solution = None
        self.message_label = None  # Label to show win/lose messages
        self.generate_puzzle()
        self.create_grid()
    
    def generate_puzzle(self):
        def is_valid(r, c):
            # Check if placing a dot here exceeds the row or column clues
            if self.row_clues[r] >= self.grid_size or self.col_clues[c] >= self.grid_size:
                return False
            return True

        def solve(cells, dots_left):
            if dots_left == 0:
                return True  # All dots placed
            
            if not cells:
                return False  # No more cells to consider
            
            # Choose the next cell to try
            r, c = cells.pop()

            # Try placing a dot
            if is_valid(r, c):
                self.grid[r][c] = 1
                self.row_clues[r] += 1
                self.col_clues[c] += 1
                
                if solve(cells[:], dots_left - 1):  # Pass a copy of the remaining cells
                    return True
                
                # Backtrack
                self.grid[r][c] = 0
                self.row_clues[r] -= 1
                self.col_clues[c] -= 1
            
            # Try without placing a dot
            return solve(cells[:], dots_left)
        
        # Create a list of all cells in the grid and shuffle them
        cells = [(r, c) for r in range(self.grid_size) for c in range(self.grid_size)]
        random.shuffle(cells)  # Randomize cell order
        solve(cells, self.num_dots)
        self.solution = [(r, c) for r in range(self.grid_size) for c in range(self.grid_size) if self.grid[r][c] == 1]

    def create_grid(self):
        # Add row clues with styling
        for row in range(self.grid_size):
            clue_label = tk.Label(self.root, text=str(self.row_clues[row]), font=("Arial", 14, "bold"), fg="darkblue")
            clue_label.grid(row=row + 1, column=0, padx=5, pady=5)
        
        # Add column clues with styling
        for col in range(self.grid_size):
            clue_label = tk.Label(self.root, text=str(self.col_clues[col]), font=("Arial", 14, "bold"), fg="darkblue")
            clue_label.grid(row=0, column=col + 1, padx=5, pady=5)
        
        # Add grid buttons with styling
        self.grid_buttons = {}
        for row in range(self.grid_size):
            for col in range(self.grid_size):
                button = tk.Button(
                    self.root, width=4, height=2, bg="lightgray", relief="raised",
                    command=lambda r=row, c=col: self.check_cell(r, c),
                    font=("Arial", 12, "bold")
                )
                button.grid(row=row + 1, column=col + 1, padx=2, pady=2)
                self.grid_buttons[(row, col)] = button

        # Add "Show Solution" button with styling
        show_solution_button = tk.Button(self.root, text="Show Solution", command=self.display_solution, font=("Arial", 12, "bold"), bg="orange", fg="white")
        show_solution_button.grid(row=self.grid_size + 1, column=0, columnspan=self.grid_size // 2, pady=10)

        # Add "Reset" button with styling
        reset_button = tk.Button(self.root, text="Reset", command=self.reset_game, font=("Arial", 12, "bold"), bg="green", fg="white")
        reset_button.grid(row=self.grid_size + 1, column=self.grid_size // 2, columnspan=self.grid_size // 2, pady=10)

    def check_cell(self, row, col):
        # Check if the clicked cell contains a hidden dot
        if (row, col) in self.solution:
            self.grid_buttons[(row, col)].config(text="●", bg="green", fg="white", state="disabled")
            self.solution.remove((row, col))
        else:
            # If wrong cell is clicked, display "You Lose" and disable all buttons
            self.grid_buttons[(row, col)].config(text="X", bg="red", fg="white", state="disabled")
            self.display_lose_message()
            self.disable_all_buttons()
            return
        
        # Check for win condition
        if not self.solution:
            self.display_win_message()
    
    def display_solution(self):
        # Reveal all dots in the solution
        for (row, col) in self.solution:
            self.grid_buttons[(row, col)].config(text="●", bg="blue", fg="white", state="disabled")
    
    def clear_messages(self):
        # Clear any existing win/lose message
        if self.message_label:
            self.message_label.destroy()
            self.message_label = None

    def display_win_message(self):
        self.clear_messages()  # Clear any existing message
        self.message_label = tk.Label(self.root, text="You Win!", font=("Arial", 20, "bold"), fg="blue")
        self.message_label.grid(row=self.grid_size + 2, column=0, columnspan=self.grid_size, pady=10)

    def display_lose_message(self):
        self.clear_messages()  # Clear any existing message
        self.message_label = tk.Label(self.root, text="You Lose!", font=("Arial", 20, "bold"), fg="red")
        self.message_label.grid(row=self.grid_size + 2, column=0, columnspan=self.grid_size, pady=10)

    def disable_all_buttons(self):
        # Disable all buttons on the grid
        for button in self.grid_buttons.values():
            button.config(state="disabled")

    def reset_game(self):
        # Clear existing win/lose message and reset the game grid
        self.clear_messages()
        for row in range(self.grid_size):
            for col in range(self.grid_size):
                self.grid_buttons[(row, col)].config(text="", bg="lightgray", fg="black", state="normal")
        self.row_clues = [0] * self.grid_size
        self.col_clues = [0] * self.grid_size
        self.grid = [[0] * self.grid_size for _ in range(self.grid_size)]
        self.generate_puzzle()
        self.create_grid()

# Main loop
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Smart Dot Game with Randomized Backtracking")
    root.configure(bg="lightblue")
    game = SmartDotGameBacktracking(root, grid_size=5, num_dots=8)
    root.mainloop()
