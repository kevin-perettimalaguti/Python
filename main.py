import tkinter as tk
import random
import time

class MineSweeper(tk.Tk):
    def __init__(self, width, height, num_mines, difficulty):
        super().__init__()
        self.width = width
        self.height = height
        self.num_mines = num_mines
        self.difficulty = difficulty
        self.board = [[0 for _ in range(width)] for _ in range(height)]
        self.flags = [[0 for _ in range(width)] for _ in range(height)]
        self.tiles = []
        self.start_time = None
        self.timer_label = tk.Label(self, text="Time: 0")
        self.timer_label.grid(row=height, columnspan=width)
        self.colors = {"1": "blue", "2": "green", "3": "red", "4": "purple",
               "5": "maroon", "6": "turquoise", "7": "black", "8": "gray"}        
        self.create_widgets()
        self.place_mines()
        self.update_display()
        self.bind("<Button-2>", self.toggle_flag)
        self.reset_button = tk.Button(self, text="Reset", command=self.reset_game)
        self.reset_button.grid(row=height+1, columnspan=width)

    def create_widgets(self):
        for y in range(self.height):
            row = []
            for x in range(self.width):
                tile = tk.Button(self, width=2, height=1, command=lambda x=x, y=y: self.click_tile(x, y))
                tile.grid(row=y, column=x)
                row.append(tile)
            self.tiles.append(row)

    def place_mines(self):
        mines_placed = 0
        while mines_placed < self.num_mines:
            x = random.randint(0, self.width - 1)
            y = random.randint(0, self.height - 1)
            if self.board[y][x] != -1:
                self.board[y][x] = -1
                mines_placed += 1
                for dx in range(-1, 2):
                    for dy in range(-1, 2):
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < self.width and 0 <= ny < self.height and self.board[ny][nx] != -1:
                            self.board[ny][nx] += 1
                            
                            

    def click_tile(self, x, y):
        if self.start_time is None:
            self.start_time = time.time()
            self.update_timer()
        if self.flags[y][x] == 0:
            if self.board[y][x] == -1:
                self.tiles[y][x].config(text="X", state=tk.DISABLED)

                self.game_over()
            else:
                self.reveal_tile(x, y)

    def reveal_tile(self, x, y):
        if self.tiles[y][x]["state"] == tk.NORMAL:
            value = self.board[y][x]
            if value == 0:
                self.tiles[y][x].config(text="", state=tk.DISABLED)
                for dx in range(-1, 2):
                    for dy in range(-1, 2):
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < self.width and 0 <= ny < self.height:
                            self.reveal_tile(nx, ny)
            else:
                self.tiles[y][x].config(text=str(value), state=tk.DISABLED)
                self.tiles[y][x].config(disabledforeground=self.colors[str(value)])
                

                
    

    def toggle_flag(self, event):
        x, y = self.winfo_pointerxy()
        widget = self.winfo_containing(x, y)
        row, col = widget.grid_info()["row"], widget.grid_info()["column"]
        if self.tiles[row][col]["state"] == tk.NORMAL:
            if self.flags[row][col] == 0:
                self.flags[row][col] = 1
                self.tiles[row][col].config(text="F")
            elif self.flags[row][col] == 1:
                self.flags[row][col] = 2
                self.tiles[row][col].config(text="?")
            else:
                self.flags[row][col] = 0
                self.tiles[row][col].config(text="")
        self.update_display()

    def game_over(self):
        for y in range(self.height):
            for x in range(self.width):
                if self.board[y][x] == -1:
                    self.tiles[y][x].config(text="X", state=tk.DISABLED, disabledforeground="red")               
                      

        
        for row in self.tiles:
            for tile in row:
                if tile != self.timer_label:  # Ne pas désactiver le chronomètre
                    tile.config(state=tk.DISABLED)
                    
                    
                     # Créer une nouvelle fenêtre pop-up
        game_over_window = tk.Toplevel(self)
        game_over_window.title("Game Over")
        
        # Afficher le texte "Game Over" en gros
        game_over_label = tk.Label(game_over_window, text="Game Over", font=("Helvetica", 24))
        game_over_label.pack(pady=10)
        
        
        
        self.start_time = None
        
        # Add a resest button above 
        reset_button = tk.Button(game_over_window, text="Reset", command=self.reset_game)
        reset_button.pack(pady=10)
        
        # Add a quit button below
        reset_button = tk.Button(game_over_window, text="Quit", command=self.quit)
        reset_button.pack(pady=10)
                    

    def update_display(self):
        for y in range(self.height):
            for x in range(self.width):
                if self.tiles[y][x]["state"] == tk.NORMAL:
                    if self.flags[y][x] == 0:
                        self.tiles[y][x].config(text="")
                    elif self.flags[y][x] == 1:
                        self.tiles[y][x].config(text="F")
                    else:
                        self.tiles[y][x].config(text="?")
        self.after(100, self.update_display)

    def update_timer(self):
        if self.start_time is not None:
            elapsed_time = int(time.time() - self.start_time)
            self.timer_label.config(text="Time: {}".format(elapsed_time))
            self.after(1000, self.update_timer)

    def reset_game(self):
        self.destroy()
        new_game = MineSweeper(self.width, self.height, self.num_mines, self.difficulty)
        new_game.mainloop()


if __name__ == "__main__":
    difficulty_levels = {
        "Easy": {"width": 8, "height": 8, "mines_range": (10, 15)},
        "Medium": {"width": 10, "height": 10, "mines_range": (20, 30)},
        "Hard": {"width": 12, "height": 12, "mines_range": (30, 40)}
    }
    chosen_difficulty = "Medium"  # Change difficulty here
    width = difficulty_levels[chosen_difficulty]["width"]
    height = difficulty_levels[chosen_difficulty]["height"]
    min_mines, max_mines = difficulty_levels[chosen_difficulty]["mines_range"]
    num_mines = random.randint(min_mines, max_mines)
    game = MineSweeper(width=width, height=height, num_mines=num_mines, difficulty=chosen_difficulty)
    game.mainloop()