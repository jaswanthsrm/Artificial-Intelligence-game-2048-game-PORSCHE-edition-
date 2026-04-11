import tkinter as tk
import logic
import ai
import time

# Porsche 911 Racing Theme Colors
GRID_COLOR = "#1a1a1a"
EMPTY_CELL_COLOR = "#2d2d2d"
TILE_COLORS = {
    2: "#e1e1e1", 4: "#b1b3b5", 8: "#8c8c8c", 16: "#ffcc00",
    32: "#f3a505", 64: "#d5001c", 128: "#a50013", 256: "#005f98",
    512: "#004b7b", 1024: "#1c6b54", 2048: "#cf9b67"
}

CAR_MODELS = {
    2: "Taycan", 4: "Macan", 8: "Cayenne", 16: "Panamera",
    32: "718 Cayman", 64: "911 Carrera", 128: "911 Turbo S",
    256: "911 GT3 RS", 512: "918 Spyder", 1024: "917 Racing", 2048: "MISSION X"
}

LABEL_COLORS = {2: "#1a1a1a", 4: "#1a1a1a", 16: "#1a1a1a", 32: "#1a1a1a"}
CELL_SIZE = 130
GRID_PADDING = 10

class Game2048(tk.Frame):
    def __init__(self):
        tk.Frame.__init__(self, bg=GRID_COLOR)
        self.master.title("2048 : Porsche 911 Edition")
        self.master.geometry("650x800")
        self.master.resizable(False, False)
        self.pack(fill="both", expand=True)

        self.master.bind("<Key>", self.key_down)
        self.master.bind("a", self.ai_run)

        self.score = 0
        self.move_count = 0
        self.game_over = False

        # Header: Score - Button - Moves
        header = tk.Frame(self, bg=GRID_COLOR)
        header.pack(fill="x", pady=20)

        self.score_label = tk.Label(header, text="Score : 0", font=("Helvetica", 16, "bold"), fg="white", bg=GRID_COLOR)
        self.score_label.pack(side="left", padx=20)

        restart_btn = tk.Button(header, text="RESTART ENGINE", font=("Helvetica", 10, "bold"), bg="#d5001c", fg="white",
                                command=self.reset_game, relief="flat", padx=15, pady=5)
        restart_btn.pack(side="left", expand=True)

        self.move_label = tk.Label(header, text="Moves : 0", font=("Helvetica", 16, "bold"), fg="white", bg=GRID_COLOR)
        self.move_label.pack(side="right", padx=20)

        # Board Container (Needed for the animation overlay)
        self.main_container = tk.Frame(self, bg=GRID_COLOR)
        self.main_container.pack()

        self.grid_cells = []
        self.init_grid()

        self.matrix = logic.start_game()
        self.update_grid_cells()
        self.master.focus_set()
        self.mainloop()

    def init_grid(self):
        self.background = tk.Frame(self.main_container, bg=GRID_COLOR)
        self.background.pack()
        for i in range(4):
            grid_row = []
            for j in range(4):
                cell = tk.Frame(self.background, bg=EMPTY_CELL_COLOR, width=CELL_SIZE, height=CELL_SIZE)
                cell.grid(row=i, column=j, padx=GRID_PADDING, pady=GRID_PADDING)
                cell.grid_propagate(False)
                label = tk.Label(cell, text="", bg=EMPTY_CELL_COLOR, justify="center", font=("Verdana", 14, "bold"), wraplength=CELL_SIZE - 10)
                label.place(relx=0, rely=0, relwidth=1, relheight=1)
                grid_row.append(label)
            self.grid_cells.append(grid_row)

    def show_game_over_animation(self, status="LOSE"):
        self.game_over = True
        # Create an overlay
        overlay = tk.Canvas(self.main_container, width=600, height=600, bg="#1a1a1a", highlightthickness=0)
        overlay.place(relx=0.5, rely=0.5, anchor="center")
        
        msg = "MISSION ACCOMPLISHED" if status == "WIN" else "ENGINE STALLED"
        car_icon = "🏎️💨"
        
        # Animate car moving across
        car = overlay.create_text(-50, 250, text=car_icon, font=("Arial", 40), fill="white")
        
        def animate(x):
            if x < 650:
                overlay.coords(car, x, 250)
                self.master.after(10, lambda: animate(x + 10))
            else:
                overlay.create_text(300, 300, text=msg, font=("Helvetica", 30, "bold"), fill="#d5001c")
                overlay.create_text(300, 360, text="Final Score: " + str(self.score), font=("Helvetica", 18), fill="white")

        animate(0)

    def reset_game(self):
        # Remove any game over overlays
        for widget in self.main_container.winfo_children():
            if isinstance(widget, tk.Canvas):
                widget.destroy()
        
        self.game_over = False
        self.matrix = logic.start_game()
        self.score = 0
        self.move_count = 0
        self.score_label.config(text="Score : 0")
        self.move_label.config(text="Moves : 0")
        self.update_grid_cells()
        self.master.focus_set()

    def check_status(self):
        # Check for 2048 (Win)
        if any(2048 in row for row in self.matrix):
            self.show_game_over_animation("WIN")
            return
        
        # Check if any moves are possible (Loss)
        # We try moving in all directions on a copy to see if anything changes
        import copy
        for func in [logic.move_up, logic.move_down, logic.move_left, logic.move_right]:
            _, changed, _ = func(copy.deepcopy(self.matrix))
            if changed:
                return # Still have moves
        
        self.show_game_over_animation("LOSE")

    def update_grid_cells(self):
        for i in range(4):
            for j in range(4):
                val = self.matrix[i][j]
                if val == 0:
                    self.grid_cells[i][j].configure(text="", bg=EMPTY_CELL_COLOR)
                else:
                    self.grid_cells[i][j].configure(text=f"{val}\n\n{CAR_MODELS.get(val,'Porsche')}",
                                                    bg=TILE_COLORS.get(val, "#000"), fg=LABEL_COLORS.get(val, "#fff"))
        self.update_idletasks()

    def key_down(self, event):
        if self.game_over: return
        moves = {"Up": logic.move_up, "Down": logic.move_down, "Left": logic.move_left, "Right": logic.move_right}
        if event.keysym in moves:
            self.matrix, changed, score = moves[event.keysym](self.matrix)
            if changed:
                logic.add_new_2(self.matrix)
                self.move_count += 1
                self.score += score
                self.score_label.config(text=f"Score : {self.score}")
                self.move_label.config(text=f"Moves : {self.move_count}")
                self.update_grid_cells()
                self.check_status()

    def ai_run(self, event=None):
        if self.game_over: return
        move = ai.get_best_move(self.matrix)
        if move:
            moves = {"Up": logic.move_up, "Down": logic.move_down, "Left": logic.move_left, "Right": logic.move_right}
            self.matrix, changed, score = moves[move](self.matrix)
            if changed:
                logic.add_new_2(self.matrix)
                self.move_count += 1
                self.score += score
                self.score_label.config(text=f"Score : {self.score}")
                self.move_label.config(text=f"Moves : {self.move_count}")
                self.update_grid_cells()
                self.check_status()

if __name__ == "__main__":
    Game2048()