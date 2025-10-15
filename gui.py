import tkinter as tk
import time
from algorithms import (
    bfs_8_rooks, dfs_8_rooks, ucs_8_rooks, dls_8_rooks, ids_8_rooks,
    greedy_8_rooks, astar_8_rooks, hill_climbing_8_rooks, simulated_annealing_8_rooks,
    genetic_algorithm_8_rooks, beam_search_8_rooks, and_or_search_8_rooks,
    partially_observable_search_8_rooks, belief_state_search_8_rooks,
    backtracking_8_rooks, forward_checking_8_rooks, ac3_8_rooks, minimax_8_rooks, alpha_beta_8_rooks
)

class RookGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Game8RooksAI-NinhAnhTu-23110168")

        screen_w = self.root.winfo_screenwidth()
        screen_h = self.root.winfo_screenheight()

        self.root.geometry(f"{screen_w}x{screen_h}+0+0")
        self.root.configure(bg="#ffe6f2")

        self.n = 8
        self.cell_size = 60
        self.is_running = False
        self.selected_algo = None
        self.screen_width = screen_w
        self.screen_height = screen_h
        self.start_col = None
        self.start_row = None
        self.speed_delay = 0.3
        self.is_animating = False
        self.animation_start_time = 0
        self.runtime_update_id = None

        self.create_main_frames()

    def create_main_frames(self):
        total_w = self.screen_width
        total_h = self.screen_height

        left_w = int(total_w * 2 / 5)
        right_w = int(total_w * 3 / 5)

        self.frame_left = tk.Frame(self.root, width=left_w, height=total_h,
                                   bg="#fff0f5", relief="ridge", bd=3)
        self.frame_left.pack(side="left", fill="y")

        self.create_uninformed_buttons()
        self.create_informed_buttons()
        self.create_local_buttons()
        self.create_complexenv_buttons()
        self.create_cps_buttons()
        self.create_adversarial_buttons()

        control_frame = tk.Frame(self.frame_left, bg="#fff0f0")
        control_frame.pack(pady=20)

        btn_run = tk.Button(
            control_frame,
            text="▶ Start",
            font=("Segoe UI", 13, "bold"),
            bg="#1de491",
            fg="black",
            width=10, height=1,
            relief="raised",
            command=self.run_algorithm
        )
        btn_run.grid(row=0, column=0, padx=8, pady=5)

        btn_reset = tk.Button(
            control_frame,
            text="🔄 Reset",
            font=("Segoe UI", 13, "bold"),
            bg="#dbf20e",
            fg="#090005",
            width=10, height=1,
            relief="raised",
            command=self.reset_boards
        )
        btn_reset.grid(row=0, column=1, padx=8, pady=5)

        btn_exit = tk.Button(
            control_frame,
            text="⛔ Exit",
            font=("Segoe UI", 13, "bold"),
            bg="#f60606",
            fg="white",
            width=10, height=1,
            relief="raised",
            command=self.root.destroy
        )
        btn_exit.grid(row=0, column=2, padx=8, pady=5)

        self.frame_right = tk.Frame(self.root, width=right_w, height=total_h,
                                    bg="#fff", relief="ridge", bd=3)
        self.frame_right.pack(side="right", fill="both", expand=True)

        self.create_boards(self.frame_right)
        self.create_info_panel(self.frame_right)
        self.create_speed_control(self.frame_right)

    def run_algorithm(self):
        if not self.selected_algo:
            print("Please select an algorithm first!")
            return

        print(f"Running algorithm: {self.selected_algo}")
        
        self.var_runtime.set("0.000")
        
        start_time = time.time()
        
        h_val, g_val, f_val = 0, 0, 0
        
        try:
            if self.selected_algo == "BFS":
                steps, result, nodes_expanded, h_val, g_val, f_val = bfs_8_rooks(self.start_col)
            elif self.selected_algo == "DFS":
                steps, result, nodes_expanded, h_val, g_val, f_val = dfs_8_rooks(self.start_row, self.start_col)
            elif self.selected_algo == "UCS":
                start_pos = getattr(self, "start_row", None), getattr(self, "start_col", None)
                steps, result, nodes_expanded, h_val, g_val, f_val = ucs_8_rooks(start_pos)
            elif self.selected_algo == "DLS":
                start_pos = getattr(self, "start_row", None), getattr(self, "start_col", None)
                limit = getattr(self, "depth_limit", tk.IntVar(value=10)).get()
                steps, result, nodes_expanded, h_val, g_val, f_val = dls_8_rooks(start_pos, depth_limit=limit)
            elif self.selected_algo == "IDS":
                start_pos = getattr(self, "start_row", None), getattr(self, "start_col", None)
                steps, result, nodes_expanded, h_val, g_val, f_val = ids_8_rooks(start_pos)
            elif self.selected_algo == "Greedy":
                start_pos = getattr(self, "start_row", None), getattr(self, "start_col", None)
                steps, result, nodes_expanded, h_val, g_val, f_val = greedy_8_rooks(start_pos)
            elif self.selected_algo == "A*":
                start_pos = getattr(self, "start_row", None), getattr(self, "start_col", None)
                steps, result, nodes_expanded, h_val, g_val, f_val = astar_8_rooks(start_pos)
            elif self.selected_algo == "Hill":
                start_pos = getattr(self, "start_row", None), getattr(self, "start_col", None)
                steps, result, nodes_expanded, h_val, g_val, f_val = hill_climbing_8_rooks(start_pos)
            elif self.selected_algo == "SA":
                start_pos = getattr(self, "start_row", None), getattr(self, "start_col", None)
                steps, result, nodes_expanded, h_val, g_val, f_val = simulated_annealing_8_rooks(start_pos)
            elif self.selected_algo == "GA":
                start_pos = getattr(self, "start_row", None), getattr(self, "start_col", None)
                steps, result, nodes_expanded, h_val, g_val, f_val = genetic_algorithm_8_rooks(start_pos)
            elif self.selected_algo == "Beam":
                start_pos = getattr(self, "start_row", None), getattr(self, "start_col", None)
                steps, result, nodes_expanded, h_val, g_val, f_val = beam_search_8_rooks(start_pos)
            elif self.selected_algo == "And-Or":
                start_pos = getattr(self, "start_row", None), getattr(self, "start_col", None)
                steps, result, nodes_expanded, h_val, g_val, f_val = and_or_search_8_rooks(start_pos)
            elif self.selected_algo == "Partially":
                start_pos = getattr(self, "start_row", None), getattr(self, "start_col", None)
                steps, result, nodes_expanded, h_val, g_val, f_val = partially_observable_search_8_rooks(start_pos)
            elif self.selected_algo == "Belief":
                start_pos = getattr(self, "start_row", None), getattr(self, "start_col", None)
                steps, result, nodes_expanded, h_val, g_val, f_val = belief_state_search_8_rooks(start_pos)
            elif self.selected_algo == "Backtracking":
                start_pos = getattr(self, "start_row", None), getattr(self, "start_col", None)
                steps, result, nodes_expanded, h_val, g_val, f_val = backtracking_8_rooks(start_pos)
            elif self.selected_algo == "Forward":
                start_pos = getattr(self, "start_row", None), getattr(self, "start_col", None)
                steps, result, nodes_expanded, h_val, g_val, f_val = forward_checking_8_rooks(start_pos)
            elif self.selected_algo == "AC3":
                start_pos = getattr(self, "start_row", None), getattr(self, "start_col", None)
                steps, result, nodes_expanded, h_val, g_val, f_val = ac3_8_rooks(start_pos)
            elif self.selected_algo == "Minimax":
                start_pos = getattr(self, "start_row", None), getattr(self, "start_col", None)
                steps, result, nodes_expanded, h_val, g_val, f_val = minimax_8_rooks(start_pos)
            elif self.selected_algo == "Alpha-Beta":
                start_pos = getattr(self, "start_row", None), getattr(self, "start_col", None)
                steps, result, nodes_expanded, h_val, g_val, f_val = alpha_beta_8_rooks(start_pos)
            else:
                print(f"Algorithm {self.selected_algo} not implemented!")
                return
        except Exception as e:
            print(f"Error running algorithm {self.selected_algo}: {e}")
            import traceback
            traceback.print_exc()
            return

        end_time = time.time()
        elapsed = end_time - start_time

        self.var_time.set(f"{elapsed:.3f}")
        self.var_nodes.set(str(nodes_expanded))

        self.var_hx.set(str(h_val))
        self.var_gx.set(str(g_val))
        self.var_fx.set(str(f_val))

        print(f"Nodes expanded: {nodes_expanded} | Time: {elapsed:.3f}s")
        print(f"h(x): {h_val}, g(x): {g_val}, f(x): {f_val}")

        self.animate_process(steps)
        self.display_goal(result)

    def animate_process(self, steps):
        if not steps:
            print("No steps to display animation")
            return

        canvas = self.boards[1]
        cell = canvas._cell_size
        self.is_animating = True
        
        self.animation_start_time = time.time()
        self.update_runtime()

        print(f"Starting animation {self.selected_algo} ({len(steps)} steps)")

        def show_step(i=0):
            if not self.is_animating or i >= len(steps):
                print(f"Stopping animation {self.selected_algo}.")
                if self.runtime_update_id:
                    self.root.after_cancel(self.runtime_update_id)
                return

            step_data = steps[i]
            if isinstance(step_data, tuple) and len(step_data) == 4:
                state, h_val, g_val, f_val = step_data
                self.var_hx.set(str(h_val))
                self.var_gx.set(str(g_val))
                self.var_fx.set(str(f_val))
            else:
                state = step_data

            try:
                canvas.delete("all")
                self.draw_empty_board(canvas, cell_size=cell)
            except tk.TclError:
                return

            if state:
                for row in range(self.n):
                    col = state[row]
                    if col is not None:
                        x = col * cell + cell / 2
                        y = row * cell + cell / 2
                        canvas.create_text(x, y, text="♜", 
                                     font=("Arial", int(cell*0.6), "bold"),
                                     fill="#0A0A0A")

            canvas.after(int(self.speed_delay * 1000), lambda: show_step(i + 1))

        show_step()

    def update_runtime(self):
        if self.is_animating:
            current_time = time.time()
            elapsed = current_time - self.animation_start_time
            self.var_runtime.set(f"{elapsed:.3f}")
            
            self.runtime_update_id = self.root.after(100, self.update_runtime)

    def display_goal(self, state):
        canvas = self.boards[2]
        cell = canvas._cell_size
        canvas.delete("all")
        self.draw_empty_board(canvas, cell_size=cell)

        if not state:
            print("No result to display")
            return

        for row in range(self.n):
            col = state[row]
            if col is not None:
                x = col * cell + cell / 2
                y = row * cell + cell / 2
                canvas.create_text(x, y, text="♜", 
                             font=("Arial", int(cell*0.5), "bold"),
                             fill="#39043a")
        print("Displaying final result on Goal board")

    def handle_click_start_board(self, event):
        canvas = self.boards[0]
        cell = canvas._cell_size
        col = event.x // cell
        row = event.y // cell

        if not (0 <= col < self.n and 0 <= row < self.n):
            return

        algo = self.selected_algo

        if algo == "BFS":
            if row != 0:
                print("For BFS, only first row can be selected")
                return

        if 0 <= col < self.n and 0 <= row < self.n:
            self.start_row = row
            self.start_col = col

            print(f"Selected initial position: row {row}, column {col}")
            self.var_first_pos.set(f"({row}, {col})")

            canvas.delete("all")
            self.draw_empty_board(canvas, cell_size=cell)

            x = col * cell + cell / 2
            y = row * cell + cell / 2
            canvas.create_text(x, y, text="♜", 
                         font=("Arial", int(cell*0.5), "bold"),
                         fill="#35022C")

    def reset_boards(self):
        self.is_animating = False
        
        if self.runtime_update_id:
            self.root.after_cancel(self.runtime_update_id)
        
        self.var_runtime.set("0.000")
        self.var_time.set("0.000")
        self.var_nodes.set("0")
        self.var_first_pos.set("(?, ?)")
        self.var_hx.set("0")
        self.var_gx.set("0")
        self.var_fx.set("0")
        
        self.start_row = None
        self.start_col = None
        
        print("Reset all boards and information")
        for canvas in getattr(self, "boards", []):
            canvas.delete("all")
            cell = getattr(canvas, "_cell_size", self.cell_size)
            self.draw_empty_board(canvas, cell_size=cell)

    def create_uninformed_buttons(self):
        group_frame = tk.LabelFrame(
            self.frame_left,
            text="Uninformed Search",
            bg="#fff0f5", fg="#050103",
            font=("Segoe UI", 15, "bold"),
            labelanchor="n", padx=8, pady=6, bd=5
        )
        group_frame.pack(pady=3)

        btn_frame = tk.Frame(group_frame, bg="#fff0f5")
        btn_frame.pack(anchor="center")

        algos = ["BFS", "DFS", "UCS", "DLS", "IDS"]
        self.algo_buttons = {}

        for i, name in enumerate(algos):
            btn = tk.Button(
                btn_frame,
                text=name,
                font=("Segoe UI", 15, "bold"),
                bg="white",
                fg="#d63384",
                width=4, height=1,
                relief="ridge",
                command=lambda n=name: self.select_algorithm(n)
            )
            btn.grid(row=0, column=i, padx=6, pady=6)
            self.algo_buttons[name] = btn

    def create_informed_buttons(self):
        group_frame = tk.LabelFrame(
            self.frame_left,
            text="Informed Search",
            bg="#fff0f5", fg="#050103",
            font=("Segoe UI", 15, "bold"),
            labelanchor="n", padx=8, pady=6, bd=5
        )
        group_frame.pack(pady=3)

        btn_frame = tk.Frame(group_frame, bg="#fff0f5")
        btn_frame.pack(anchor="center")

        algos = ["A*", "Greedy"]
        self.informed_buttons = {}

        for i, name in enumerate(algos):
            btn = tk.Button(
                btn_frame,
                text=name,
                font=("Segoe UI", 15, "bold"),
                bg="white",
                fg="#d63384",
                width=6, height=1,
                relief="ridge",
                command=lambda n=name: self.select_algorithm(n)
            )
            btn.grid(row=0, column=i, padx=8, pady=6)
            self.informed_buttons[name] = btn

    def create_local_buttons(self):
        group_frame = tk.LabelFrame(
            self.frame_left,
            text="Local Search",
            bg="#fff0f5", fg="#050103",
            font=("Segoe UI", 15, "bold"),
            labelanchor="n", padx=8, pady=6, bd=5
        )
        group_frame.pack(pady=3)

        btn_frame = tk.Frame(group_frame, bg="#fff0f5")
        btn_frame.pack(anchor="center")

        algos = ["Hill", "SA", "GA", "Beam"]
        self.local_buttons = {}

        for i, name in enumerate(algos):
            btn = tk.Button(
                btn_frame,
                text=name,
                font=("Segoe UI", 15, "bold"),
                bg="white", fg="#d63384",
                width=5, height=1, relief="ridge",
                command=lambda n=name: self.select_algorithm(n)
            )
            btn.grid(row=0, column=i, padx=6, pady=6)
            self.local_buttons[name] = btn

    def create_complexenv_buttons(self):
        group_frame = tk.LabelFrame(
            self.frame_left,
            text="Complex Environment",
            bg="#fff0f5", fg="#050103",
            font=("Segoe UI", 15, "bold"),
            labelanchor="n", padx=8, pady=6, bd=5
        )
        group_frame.pack(pady=3)

        btn_frame = tk.Frame(group_frame, bg="#fff0f5")
        btn_frame.pack(anchor="center")

        algos = ["And-Or", "Partially", "Belief"]
        self.complexenv_buttons = {}

        for i, name in enumerate(algos):
            btn = tk.Button(
                btn_frame,
                text=name,
                font=("Segoe UI", 15, "bold"),
                bg="white", fg="#d63384",
                width=8, height=1, relief="ridge",
                command=lambda n=name: self.select_algorithm(n)
            )
            btn.grid(row=0, column=i, padx=6, pady=6)
            self.complexenv_buttons[name] = btn

    def create_cps_buttons(self):
        group_frame = tk.LabelFrame(
            self.frame_left,
            text="CPS / CSP",
            bg="#fff0f5", fg="#050103",
            font=("Segoe UI", 15, "bold"),
            labelanchor="n", padx=8, pady=6, bd=5
        )
        group_frame.pack(pady=3)

        btn_frame = tk.Frame(group_frame, bg="#fff0f5")
        btn_frame.pack(anchor="center")

        algos = ["Backtracking", "Forward", "AC3"]
        self.cps_buttons = {}

        for i, name in enumerate(algos):
            btn = tk.Button(
                btn_frame,
                text=name,
                font=("Segoe UI", 14, "bold"),
                bg="white", fg="#d63384",
                width=11, height=1, relief="ridge",
                command=lambda n=name: self.select_algorithm(n)
            )
            btn.grid(row=0, column=i, padx=6, pady=6)
            self.cps_buttons[name] = btn

    def create_adversarial_buttons(self):
        group_frame = tk.LabelFrame(
            self.frame_left,
            text="Adversarial Search",
            bg="#fff0f5", fg="#050103",
            font=("Segoe UI", 15, "bold"),
            labelanchor="n", padx=8, pady=6, bd=5
        )
        group_frame.pack(pady=3)

        btn_frame = tk.Frame(group_frame, bg="#fff0f5")
        btn_frame.pack(anchor="center")

        algos = ["Minimax", "Alpha-Beta"]
        self.adversarial_buttons = {}

        for i, name in enumerate(algos):
            btn = tk.Button(
                btn_frame,
                text=name,
                font=("Segoe UI", 15, "bold"),
                bg="white", fg="#d63384",
                width=10, height=1, relief="ridge",
                command=lambda n=name: self.select_algorithm(n)
            )
            btn.grid(row=0, column=i, padx=6, pady=6)
            self.adversarial_buttons[name] = btn

    def select_algorithm(self, name):
        self.selected_algo = name
        print(f"Selected algorithm: {name}")

        for group in [
            "algo_buttons",
            "informed_buttons",
            "local_buttons",
            "complexenv_buttons",
            "cps_buttons",
            "adversarial_buttons"
        ]:
            for _, btn in getattr(self, group, {}).items():
                btn.config(bg="white", fg="#d63384")

        for group in [
            "algo_buttons",
            "informed_buttons",
            "local_buttons",
            "complexenv_buttons",
            "cps_buttons",
            "adversarial_buttons" 
        ]:
            if name in getattr(self, group, {}):
                getattr(self, group)[name].config(bg="#d63384", fg="white")
                break

    def update_speed(self, value):
        try:
            self.speed_delay = float(value)
            print(f"Display speed: {self.speed_delay:.2f}s per step")
        except ValueError:
            pass

    def create_boards(self, parent):
        parent.configure(bg="white")

        tk.Label(parent, text="",
                bg="white", fg="#d63384",
                font=("Segoe UI", 24, "bold")).pack(pady=20)

        main_frame = tk.Frame(parent, bg="white")
        main_frame.pack(fill="both", expand=True, pady=10)

        board_area = tk.Frame(main_frame, bg="white")
        board_area.pack(side="right", padx=80, anchor="n")

        big_cell = 40
        big_canvas = tk.Canvas(board_area,
                            width=self.n * big_cell,
                            height=self.n * big_cell,
                            bg="#fce4ec",
                            highlightthickness=4,
                            highlightbackground="#d63384")
        big_canvas._cell_size = big_cell  
        big_canvas.pack()
        self.draw_empty_board(big_canvas, cell_size=big_cell)

        tk.Label(board_area, text="Animation",
                bg="white", fg="#b30059",
                font=("Segoe UI", 16, "bold")).pack(pady=5)

        bottom_frame = tk.Frame(board_area, bg="white")
        bottom_frame.pack(pady=(30, 0), anchor="w", padx=40)

        self.boards = []
        small_cell = 25
        titles = ["Start", "Goal"]

        for i, title in enumerate(titles):
            sub = tk.Frame(bottom_frame, bg="white", padx=20, pady=10)
            sub.grid(row=0, column=i, padx=30)

            tk.Label(sub, text=title, bg="white", fg="#d63384",
                    font=("Segoe UI", 14, "bold")).pack(pady=5)

            canvas = tk.Canvas(sub,
                            width=self.n * small_cell,
                            height=self.n * small_cell,
                            bg="#fce4ec",
                            highlightthickness=3,
                            highlightbackground="#d63384")
            canvas._cell_size = small_cell
            canvas.pack()
            self.draw_empty_board(canvas, cell_size=small_cell)
            self.boards.append(canvas)

            if i == 0:
                canvas.bind("<Button-1>", self.handle_click_start_board)

        self.boards.insert(1, big_canvas)

    def create_info_panel(self, parent):
        info_frame = tk.LabelFrame(
            parent,
            text="Information Algorithms",
            bg="white", fg="#ed0c1b",
            font=("Segoe UI", 15, "bold"),
            labelanchor="n", padx=15, pady=10, bd=5
        )
        info_frame.place(relx=0.01, rely=0.01, relwidth=0.28, relheight=0.40)

        font_label = ("Segoe UI", 14, "bold")
        font_value = ("Consolas", 14)

        tk.Label(info_frame, text="Start:", bg="white", fg="#ed0c1b", font=font_label)\
            .grid(row=0, column=0, sticky="w", pady=5)
        self.var_first_pos = tk.StringVar(value="(?, ?)")
        tk.Label(info_frame, textvariable=self.var_first_pos, bg="white", fg="black", font=font_value)\
            .grid(row=0, column=1, sticky="w")

        tk.Label(info_frame, text="Nodes:", bg="white", fg="#ed0c1b", font=font_label)\
            .grid(row=1, column=0, sticky="w", pady=5)
        self.var_nodes = tk.StringVar(value="0")
        tk.Label(info_frame, textvariable=self.var_nodes, bg="white", fg="black", font=font_value)\
            .grid(row=1, column=1, sticky="w")

        tk.Label(info_frame, text="Time(s):", bg="white", fg="#ed0c1b", font=font_label)\
            .grid(row=2, column=0, sticky="w", pady=5)
        self.var_time = tk.StringVar(value="0.000")
        tk.Label(info_frame, textvariable=self.var_time, bg="white", fg="black", font=font_value)\
            .grid(row=2, column=1, sticky="w")

        tk.Label(info_frame, text="Runtime(s):", bg="white", fg="#ed0c1b", font=font_label)\
            .grid(row=3, column=0, sticky="w", pady=5)
        self.var_runtime = tk.StringVar(value="0.000")
        tk.Label(info_frame, textvariable=self.var_runtime, bg="white", fg="black", font=font_value)\
            .grid(row=3, column=1, sticky="w")

        tk.Label(info_frame, text="h(x):", bg="white", fg="#ed0c1b", font=font_label)\
            .grid(row=4, column=0, sticky="w", pady=5)
        self.var_hx = tk.StringVar(value="0")
        tk.Label(info_frame, textvariable=self.var_hx, bg="white", fg="black", font=font_value)\
            .grid(row=4, column=1, sticky="w")

        tk.Label(info_frame, text="g(x):", bg="white", fg="#ed0c1b", font=font_label)\
            .grid(row=5, column=0, sticky="w", pady=5)
        self.var_gx = tk.StringVar(value="0")
        tk.Label(info_frame, textvariable=self.var_gx, bg="white", fg="black", font=font_value)\
            .grid(row=5, column=1, sticky="w")

        tk.Label(info_frame, text="f(x):", bg="white", fg="#ed0c1b", font=font_label)\
            .grid(row=6, column=0, sticky="w", pady=5)
        self.var_fx = tk.StringVar(value="0")
        tk.Label(info_frame, textvariable=self.var_fx, bg="white", fg="black", font=font_value)\
            .grid(row=6, column=1, sticky="w")

    def create_speed_control(self, parent):
        speed_frame = tk.Frame(parent, bg="white")
        speed_frame.place(relx=0.01, rely=0.42, relwidth=0.30, relheight=0.10)

        tk.Label(speed_frame, text="Speed:",
                bg="white", fg="#1010ed", font=("Segoe UI", 12, "bold"))\
            .pack(anchor="w", pady=(0, 3))

        self.speed_scale = tk.Scale(
            speed_frame,
            from_=0.01, to=1,
            orient="horizontal", resolution=0.05,
            length=260,
            bg="white", fg="#b30059",
            highlightthickness=0,
            troughcolor="#ffe6f2",
            activebackground="#ffb6c1",
            command=self.update_speed
        )
        self.speed_scale.set(self.speed_delay)
        self.speed_scale.pack(anchor="center", pady=(0, 10))

    def draw_empty_board(self, canvas, cell_size=None):
        if cell_size is None:
            cell_size = self.cell_size
        for i in range(self.n):
            for j in range(self.n):
                x1 = j * cell_size
                y1 = i * cell_size
                x2 = x1 + cell_size
                y2 = y1 + cell_size
                color = "#f8bbd0" if (i + j) % 2 == 0 else "#ffffff"
                canvas.create_rectangle(x1, y1, x2, y2,
                                        fill=color, outline="#d63384", width=1)

    def exit_fullscreen(self):
        self.root.attributes("-fullscreen", False)