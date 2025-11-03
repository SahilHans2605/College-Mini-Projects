
import tkinter as tk
from tkinter import ttk, messagebox
import random, time, math, collections, sys

# ------------------ SETTINGS ------------------
WINDOW_WIDTH, WINDOW_HEIGHT = 1100, 700
TOPBAR_HEIGHT = 70
FPS = 60

# Slightly smaller grid for better fit
GRID_ROWS, GRID_COLS = 18, 24
CELL_SIZE = 30

# Colors
BG_COLOR = "#191923"
TOPBAR_COLOR = "#282837"
BUTTON_COLOR = "#465064"
BUTTON_ACTIVE = "#6EA06E"
TEXT_COLOR = "#E6E6E6"
DIRT_COLOR = "#B47828"
OBST_COLOR = "#646464"
VAC_COLOR = "#46C8FF"
GRID_LINE = "#46464F"

# Cell states
EMPTY, DIRT, OBST = 0, 1, 2

def grid_to_center(r, c, origin, cell_size):
    x = origin[0] + c * cell_size + cell_size / 2
    y = origin[1] + r * cell_size + cell_size / 2
    return [x, y]

def world_to_grid(x, y, origin, cell_size):
    return int((y - origin[1]) // cell_size), int((x - origin[0]) // cell_size)

def in_grid(r, c, rows, cols):
    return 0 <= r < rows and 0 <= c < cols

def neighbors(r, c):
    for dr, dc in [(-1,0),(1,0),(0,-1),(0,1)]:
        yield r+dr, c+dc

def bfs_find(start, grid):
    rows, cols = len(grid), len(grid[0])
    sr, sc = start
    visited = [[False]*cols for _ in range(rows)]
    q = collections.deque([(sr, sc)])
    parent = {}
    visited[sr][sc] = True
    while q:
        r, c = q.popleft()
        if grid[r][c] == DIRT and (r, c) != (sr, sc):
            path = [(r, c)]
            while (r, c) != (sr, sc):
                r, c = parent[(r, c)]
                path.append((r, c))
            return list(reversed(path))
        for nr, nc in neighbors(r, c):
            if in_grid(nr, nc, rows, cols) and not visited[nr][nc] and grid[nr][nc] != OBST:
                visited[nr][nc] = True
                parent[(nr, nc)] = (r, c)
                q.append((nr, nc))
    return None

class VacuumApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Vacuum Cleaner Simulation (Tkinter Smooth BFS)")
        self.configure(bg=BG_COLOR)

        # Center window on screen
        screen_w = self.winfo_screenwidth()
        screen_h = self.winfo_screenheight()
        x = (screen_w - WINDOW_WIDTH)//2
        y = (screen_h - WINDOW_HEIGHT)//2
        self.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}+{x}+{y}")

        self.grid_state = [[EMPTY for _ in range(GRID_COLS)] for _ in range(GRID_ROWS)]
        self.origin = (40, TOPBAR_HEIGHT + 30)
        self.canvas_width = GRID_COLS * CELL_SIZE + self.origin[0]*2
        self.canvas_height = GRID_ROWS * CELL_SIZE + self.origin[1] + 100

        self.vacuum_grid = [GRID_ROWS//2, GRID_COLS//2]
        self.vacuum_px = grid_to_center(*self.vacuum_grid, self.origin, CELL_SIZE)
        self.path = collections.deque()
        self.cleaning = False
        self.paused = False
        self.mode = "idle"

        self.moving = False
        self.move_start_px = self.vacuum_px[:]
        self.move_end_px = self.vacuum_px[:]
        self.move_progress = 0.0
        self.move_speed = 150.0

        self.start_time = None
        self.cleaned = 0
        self.distance = 0.0

        self._build_ui()
        self._last_time = time.time()
        self.after(0, self._loop)

    def _build_ui(self):
        topbar = tk.Frame(self, bg=TOPBAR_COLOR, height=TOPBAR_HEIGHT)
        topbar.pack(fill="x", side="top")

        btn_frame = tk.Frame(topbar, bg=TOPBAR_COLOR)
        btn_frame.pack(side="left", padx=10, pady=10)

        names = [
            ("Start", self.start_clean),
            ("Pause", self.toggle_pause),
            ("Stop", self.stop_clean),
            ("Random Dirt", self.random_dirt),
            ("Add Dirt", lambda: self.set_mode("dirt")),
            ("Add Furniture", lambda: self.set_mode("obst")),
            ("Erase", lambda: self.set_mode("erase")),
            ("Reset", self.reset)
        ]
        for i, (name, cb) in enumerate(names):
            b = tk.Button(btn_frame, text=name, command=cb, bg=BUTTON_COLOR, fg=TEXT_COLOR,
                          activebackground=BUTTON_ACTIVE, relief="flat", padx=6, pady=3)
            b.grid(row=i//4, column=i%4, padx=5, pady=5)

        title = tk.Label(topbar, text="Vacuum Cleaner Simulation (Smooth BFS)", bg=TOPBAR_COLOR, fg=TEXT_COLOR,
                         font=("Consolas", 13, "bold"))
        title.pack(side="right", padx=10)

        self.canvas = tk.Canvas(self, width=self.canvas_width, height=self.canvas_height, bg=BG_COLOR, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True, padx=10, pady=10)
        self.canvas.bind("<Button-1>", self._on_canvas_click)

        self._draw_grid_static()

        self.stats_var = tk.StringVar(value="Mode: IDLE | Cleaned: 0 | Distance: 0 | Time: 0.0s")
        stats = tk.Label(self, textvariable=self.stats_var, bg=BG_COLOR, fg=TEXT_COLOR, font=("Consolas", 11))
        stats.pack(anchor="w", padx=40, pady=(5,10))

    def _on_canvas_click(self, event):
        gr, gc = world_to_grid(event.x, event.y, self.origin, CELL_SIZE)
        if in_grid(gr, gc, GRID_ROWS, GRID_COLS):
            if self.mode == "dirt":
                self.grid_state[gr][gc] = DIRT
            elif self.mode == "obst":
                if [gr, gc] != self.vacuum_grid:
                    self.grid_state[gr][gc] = OBST
                    if self.path and (gr, gc) in self.path:
                        self.path.clear()
                        self.moving = False
            elif self.mode == "erase":
                self.grid_state[gr][gc] = EMPTY
            self._draw_cell(gr, gc)

    def _draw_grid_static(self):
        self.canvas.delete("all")
        for r in range(GRID_ROWS):
            for c in range(GRID_COLS):
                x = self.origin[0] + c * CELL_SIZE
                y = self.origin[1] + r * CELL_SIZE
                self.canvas.create_rectangle(x, y, x+CELL_SIZE, y+CELL_SIZE, outline=GRID_LINE, tags=f"cell_{r}_{c}")
                self._draw_cell(r, c, True)

        vx, vy = self.vacuum_px
        radius = CELL_SIZE//2 - 3
        self.vacuum_id = self.canvas.create_oval(vx-radius, vy-radius, vx+radius, vy+radius, fill=VAC_COLOR, outline="")

    def _draw_cell(self, r, c, immediate=False):
        tag = f"content_{r}_{c}"
        self.canvas.delete(tag)
        x = self.origin[0] + c * CELL_SIZE
        y = self.origin[1] + r * CELL_SIZE
        cx = x + CELL_SIZE/2
        cy = y + CELL_SIZE/2
        if self.grid_state[r][c] == DIRT:
            rad = CELL_SIZE//4
            self.canvas.create_oval(cx-rad, cy-rad, cx+rad, cy+rad, fill=DIRT_COLOR, outline="", tags=("content", tag))
        elif self.grid_state[r][c] == OBST:
            pad = 3
            self.canvas.create_rectangle(x+pad, y+pad, x+CELL_SIZE-pad, y+CELL_SIZE-pad, fill=OBST_COLOR, outline="", tags=("content", tag))

    def start_clean(self):
        if not self.cleaning:
            self.cleaning = True
            self.paused = False
            self.start_time = time.time()
            self.cleaned = 0
            self.distance = 0.0
            self.path = collections.deque()
            self.moving = False

    def toggle_pause(self):
        if self.cleaning:
            self.paused = not self.paused

    def stop_clean(self):
        self.cleaning = False
        self.paused = False
        self.moving = False
        self.path = collections.deque()

    def random_dirt(self):
        for r in range(GRID_ROWS):
            for c in range(GRID_COLS):
                if random.random() < 0.06 and self.grid_state[r][c] == EMPTY and [r,c] != self.vacuum_grid:
                    self.grid_state[r][c] = DIRT
                    self._draw_cell(r,c)

    def reset(self):
        self.grid_state = [[EMPTY for _ in range(GRID_COLS)] for _ in range(GRID_ROWS)]
        self.cleaning = False
        self.paused = False
        self.path = collections.deque()
        self.moving = False
        self.cleaned = 0
        self.distance = 0.0
        self.start_time = None
        self._draw_grid_static()

    def set_mode(self, m):
        self.mode = m

    def _update_logic(self, dt):
        if not (self.cleaning and not self.paused):
            return

        if self.moving:
            self.move_progress += (self.move_speed * dt) / CELL_SIZE
            if self.move_progress >= 1.0:
                self.vacuum_px = self.move_end_px[:]
                self.vacuum_grid = self.next_target_cell[:]
                self.distance += CELL_SIZE
                self.moving = False
                self._update_vacuum_canvas()
                r, c = self.vacuum_grid
                if self.grid_state[r][c] == DIRT:
                    self.grid_state[r][c] = EMPTY
                    self.cleaned += 1
                    self._draw_cell(r, c)
                    self.path = collections.deque()
            else:
                sx, sy = self.move_start_px
                ex, ey = self.move_end_px
                t = self.move_progress
                self.vacuum_px = [sx + (ex - sx) * t, sy + (ey - sy) * t]
                self._update_vacuum_canvas()
        else:
            if not self.path:
                new_path = bfs_find(tuple(self.vacuum_grid), self.grid_state)
                if new_path:
                    self.path = collections.deque(new_path[1:])
                else:
                    self.cleaning = False
                    return
            if self.path:
                next_cell = self.path.popleft()
                if self.grid_state[next_cell[0]][next_cell[1]] == OBST:
                    self.path.clear()
                    return
                self.next_target_cell = list(next_cell)
                self.move_start_px = self.vacuum_px[:]
                self.move_end_px = grid_to_center(next_cell[0], next_cell[1], self.origin, CELL_SIZE)
                self.move_progress = 0.0
                self.moving = True

    def _update_vacuum_canvas(self):
        r = CELL_SIZE//2 - 3
        vx, vy = self.vacuum_px
        self.canvas.coords(self.vacuum_id, vx-r, vy-r, vx+r, vy+r)

    def _loop(self):
        now = time.time()
        dt = now - self._last_time
        self._last_time = now
        self._update_logic(dt)
        t = (time.time() - self.start_time) if self.start_time else 0
        self.stats_var.set(f"Mode: {self.mode.upper()} | Cleaned: {self.cleaned} | Distance: {int(self.distance)} | Time: {t:.1f}s")
        self.after(int(1000//FPS), self._loop)

if __name__ == "__main__":
    app = VacuumApp()
    app.mainloop()
