from MineSweeper import MineSweeper
import random

def start_game():

        difficulty_levels = {
        "Easy": {"width": 8, "height": 8, "mines_range": (10, 15)},
        "Medium": {"width": 10, "height": 10, "mines_range": (20, 30)},
        "Hard": {"width": 12, "height": 12, "mines_range": (30, 40)}
        }

        chosen_difficulty = "Medium"
        width = difficulty_levels[chosen_difficulty]["width"]
        height = difficulty_levels[chosen_difficulty]["height"]
        min_mines, max_mines = difficulty_levels[chosen_difficulty]["mines_range"]
        num_mines = random.randint(min_mines, max_mines)
        game = MineSweeper(width=width, height=height, num_mines=num_mines, difficulty=chosen_difficulty)
        game.mainloop()
        
start_game()

    