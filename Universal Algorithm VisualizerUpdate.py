import tkinter as tk
from tkinter import ttk, messagebox
import random
import time
import threading
import json
import os
import math
import heapq

BG_COLOR = "#261a1b"
CARD_BG = "#24283b"
CANVAS_BG = "#16161e"
TEXT_COLOR = "#a9b1d6"
ACCENT_COLOR = "#72337c"
SUCCESS_COLOR = "#226D48"
ERROR_COLOR = "#f7768e"
HIGHLIGHT_COLOR = "#e0af68"
BORDER_COLOR = "#414868"

DB_FILE = "user_credentials.json"

ALGO_INFO = {
    "Bubble Sort": {
        "time": "Best: O(n)  |  Avg/Worst: O(n²)  |  Space: O(1)",
        "code": """for i in range(n):
    for j in range(0, n-i-1):
        if arr[j] > arr[j+1]:
            swap(arr[j], arr[j+1])"""
    },
    "Insertion Sort": {
        "time": "Best: O(n)  |  Avg/Worst: O(n²)  |  Space: O(1)",
        "code": """for i in range(1, n):
    key = arr[i]
    j = i - 1
    while j >= 0 and arr[j] > key:
        arr[j+1] = arr[j]
        j -= 1
    arr[j+1] = key"""
    },
    "Merge Sort": {
        "time": "All cases: O(n log n)  |  Space: O(n)",
        "code": """mergeSort(arr, l, r):
    if l < r:
        m = (l + r) // 2
        mergeSort(arr, l, m)
        mergeSort(arr, m+1, r)
        merge(arr, l, m, r)"""
    },
    "Heap Sort": {
        "time": "All cases: O(n log n)  |  Space: O(1)",
        "code": """build_max_heap(arr)
for i in range(n-1, 0, -1):
    swap(arr[0], arr[i])
    heapify(arr, i, 0)"""
    },
    "Bucket Sort": {
        "time": "Avg: O(n + k)  |  Worst: O(n²)  |  Space: O(n+k)",
        "code": """create n empty buckets
for x in arr:
    put x into bucket[index(x)]
for b in buckets:
    sort(b)
concat all buckets"""
    },
    "Selection Sort": {
        "time": "All cases: O(n²)  |  Space: O(1)",
        "code": """for i in range(n):
    min_idx = i
    for j in range(i+1, n):
        if arr[j] < arr[min_idx]:
            min_idx = j
    swap(arr[i], arr[min_idx])"""
    },
    "Quick Sort": {
        "time": "Avg: O(n log n)  |  Worst: O(n²)  |  Space: O(log n)",
        "code": """quickSort(arr, low, high):
    if low < high:
        p = partition(arr, low, high)
        quickSort(arr, low, p-1)
        quickSort(arr, p+1, high)"""
    },
    "Counting Sort": {
        "time": "O(n + k)  |  Space: O(k)",
        "code": """count = [0] * (max+1)
for x in arr: count[x] += 1
idx = 0
for i in range(len(count)):
    while count[i] > 0:
        arr[idx] = i; idx += 1
        count[i] -= 1"""
    },
    "Radix Sort": {
        "time": "O(d * (n + k))  |  Space: O(n + k)",
        "code": """for each digit d (LSD -> MSD):
    counting_sort(arr, by digit d)"""
    },
    "Shell Sort": {
        "time": "Avg: O(n log² n)  |  Worst: O(n²)",
        "code": """gap = n // 2
while gap > 0:
    for i in range(gap, n):
        temp = arr[i]; j = i
        while j >= gap and arr[j-gap] > temp:
            arr[j] = arr[j-gap]; j -= gap
        arr[j] = temp
    gap //= 2"""
    },
    "Tim Sort": {
        "time": "Best: O(n)  |  Avg/Worst: O(n log n)",
        "code": """split arr into runs (size = MIN_RUN)
insertion_sort each run
merge runs in pairs (like merge sort)"""
    },
    "Tree Sort": {
        "time": "Avg: O(n log n)  |  Worst: O(n²)",
        "code": """for x in arr:
    bst.insert(x)
result = inorder_traversal(bst)"""
    },
    "Topological Sort": {
        "time": "O(V + E)  |  Space: O(V)",
        "code": """compute in-degree of every vertex
queue = vertices with in-degree 0
while queue:
    u = queue.pop()
    output u
    for v in adj[u]:
        in_deg[v] -= 1
        if in_deg[v] == 0: queue.add(v)"""
    },
    "Linear Search": {
        "time": "Best: O(1)  |  Worst: O(n)",
        "code": """for i in range(n):
    if arr[i] == target:
        return i
return -1"""
    },
    "Binary Search": {
        "time": "O(log n)  |  Space: O(1)",
        "code": """l, r = 0, n-1
while l <= r:
    m = (l + r) // 2
    if arr[m] == target: return m
    elif arr[m] < target: l = m + 1
    else: r = m - 1"""
    },
    "Jump Search": {
        "time": "O(√n)  |  Space: O(1)",
        "code": """step = sqrt(n)
while arr[min(step,n)-1] < target:
    prev = step; step += sqrt(n)
    if prev >= n: return -1
for i in range(prev, min(step,n)):
    if arr[i] == target: return i"""
    },
    "Interpolation Search": {
        "time": "Avg: O(log log n)  |  Worst: O(n)",
        "code": """while arr[low] <= target <= arr[high]:
    pos = low + (target-arr[low]) *
          (high-low)//(arr[high]-arr[low])
    if arr[pos] == target: return pos
    if arr[pos] < target: low = pos + 1
    else: high = pos - 1"""
    },
    "Exponential Search": {
        "time": "O(log n)  |  Space: O(1)",
        "code": """if arr[0] == target: return 0
i = 1
while i < n and arr[i] <= target:
    i *= 2
binary_search(arr, i//2, min(i, n-1), target)"""
    },
    "BFS": {
        "time": "O(V + E)  |  Space: O(V)",
        "code": """queue = [start]; visited = {start}
while queue:
    u = queue.pop(0)
    for v in adj[u]:
        if v not in visited:
            visited.add(v)
            queue.append(v)"""
    },
    "DFS": {
        "time": "O(V + E)  |  Space: O(V)",
        "code": """dfs(u):
    visited.add(u)
    for v in adj[u]:
        if v not in visited:
            dfs(v)"""
    },
    "Dijkstra's Algorithm": {
        "time": "O((V + E) log V) with min-heap",
        "code": """dist[src] = 0; pq = [(0, src)]
while pq:
    d, u = heappop(pq)
    for v, w in adj[u]:
        if dist[u] + w < dist[v]:
            dist[v] = dist[u] + w
            heappush(pq, (dist[v], v))"""
    },
    "Bellman-Ford Algorithm": {
        "time": "O(V * E)  |  Space: O(V)",
        "code": """dist[src] = 0
for i in range(V-1):
    for (u, v, w) in edges:
        if dist[u] + w < dist[v]:
            dist[v] = dist[u] + w
# one more pass detects negative cycles"""
    },
    "Floyd-Warshall Algorithm": {
        "time": "O(V³)  |  Space: O(V²)",
        "code": """for k in range(V):
    for i in range(V):
        for j in range(V):
            if dist[i][k]+dist[k][j] < dist[i][j]:
                dist[i][j] = dist[i][k]+dist[k][j]"""
    },
    "Prim's Algorithm": {
        "time": "O(E log V) with min-heap",
        "code": """key[0] = 0; pq = [(0, 0)]
while pq:
    w, u = heappop(pq)
    if in_mst[u]: continue
    in_mst[u] = True
    for v, wt in adj[u]:
        if not in_mst[v] and wt < key[v]:
            key[v] = wt
            heappush(pq, (wt, v))"""
    },
    "Kruskal's Algorithm": {
        "time": "O(E log E)  |  Space: O(V)",
        "code": """sort edges by weight
for (u, v, w) in edges:
    if find(u) != find(v):
        union(u, v)
        add edge to MST"""
    },
    "N-Queen Problem": {
        "time": "O(N!)  |  Space: O(N)",
        "code": """solve(row):
    if row == N: record solution; return
    for col in range(N):
        if safe(row, col):
            place queen
            solve(row + 1)
            remove queen"""
    },
    "Sudoku Solver": {
        "time": "O(9^(n*n))  |  Space: O(n*n)",
        "code": """solve(board):
    find empty cell (r, c)
    if none: return True
    for d in 1..9:
        if valid(board, r, c, d):
            board[r][c] = d
            if solve(board): return True
            board[r][c] = 0
    return False"""
    },
    "Subset Generation": {
        "time": "O(2^n)  |  Space: O(n)",
        "code": """generate(i, current):
    if i == n:
        output current; return
    generate(i+1, current)
    generate(i+1, current + [arr[i]])"""
    },
    "Graph Colouring problem": {
        "time": "O(m^V)  |  Space: O(V)",
        "code": """color(v):
    if v == V: return True
    for c in 1..m:
        if safe(v, c):
            colors[v] = c
            if color(v+1): return True
            colors[v] = 0
    return False"""
    },
    "Travelling Salesman Problem": {
        "time": "DP: O(n² · 2ⁿ)  |  Brute: O(n!)",
        "code": """tsp(mask, pos):
    if mask == (1<<n)-1: return dist[pos][0]
    best = INF
    for city in 0..n-1:
        if not (mask & (1<<city)):
            cost = dist[pos][city] +
                   tsp(mask|(1<<city), city)
            best = min(best, cost)
    return best"""
    },
    "Array (Access/Update)": {
        "time": "Access/Update: O(1)  |  Insert/Delete: O(n)",
        "code": """access:  x = arr[i]
update:  arr[i] = v
insert:  shift right, arr[i] = v
delete:  shift left from i+1"""
    },
    "Linked List (Traversal)": {
        "time": "Traversal/Search: O(n)  |  Insert at head: O(1)",
        "code": """node = head
while node is not None:
    visit(node.value)
    node = node.next"""
    },
    "Stack UI (Step-by-Step)": {
        "time": "Push/Pop/Peek: O(1)",
        "code": """push(x):  stack.append(x)
pop():    return stack.pop()
peek():   return stack[-1]"""
    },
    "Queue UI (Step-by-Step)": {
        "time": "Enqueue/Dequeue: O(1) amortized",
        "code": """enqueue(x): queue.append(x)
dequeue():  return queue.pop(0)
front():    return queue[0]"""
    },
    "Binary Tree Representation": {
        "time": "Traversal: O(n)  |  Search (BST avg): O(log n)",
        "code": """node at index i:
    left  child = 2*i + 1
    right child = 2*i + 2
    parent      = (i - 1) // 2"""
    },
}


def load_user_db():
    if not os.path.exists(DB_FILE):
        default_db = {"admin": "1234"}
        with open(DB_FILE, "w") as f:
            json.dump(default_db, f)
        return default_db
    try:
        with open(DB_FILE, "r") as f:
            return json.load(f)
    except:
        return {"admin": "1234"}


def save_user_db(db_data):
    with open(DB_FILE, "w") as f:
        json.dump(db_data, f)


USER_DB = load_user_db()


class AuthManager:
    def __init__(self, root, on_success_callback):
        self.root = root
        self.on_success_callback = on_success_callback
        self.root.title("Auth - Universal Algorithm Visualizer")
        self.root.geometry("400x500")
        self.root.config(bg=BG_COLOR)
        self.root.resizable(False, False)
        self.main_frame = tk.Frame(self.root, bg=BG_COLOR)
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        self.show_login()

    def clear_frame(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    def show_login(self):
        self.clear_frame()
        card = tk.Frame(self.main_frame, bg=CARD_BG, bd=0,
                        highlightthickness=1, highlightbackground=BORDER_COLOR)
        card.place(relx=0.5, rely=0.5, anchor="center", width=340, height=420)

        tk.Label(card, text="Welcome Back", font=("Helvetica Neue", 16, "bold"),
                 bg=CARD_BG, fg="white").pack(pady=(30, 5))
        tk.Label(card, text="Login to your account", font=("Segoe UI", 9),
                 bg=CARD_BG, fg=TEXT_COLOR).pack(pady=(0, 20))

        tk.Label(card, text="Username", bg=CARD_BG, fg=TEXT_COLOR,
                 font=("Segoe UI", 9, "bold")).pack(anchor="w", padx=30, pady=(10, 2))
        username_entry = tk.Entry(card, bg=BG_COLOR, fg="white", bd=0,
                                  highlightthickness=1, highlightbackground=BORDER_COLOR,
                                  font=("Segoe UI", 10), insertbackground="white")
        username_entry.pack(fill=tk.X, padx=30, ipady=5)

        tk.Label(card, text="Password", bg=CARD_BG, fg=TEXT_COLOR,
                 font=("Segoe UI", 9, "bold")).pack(anchor="w", padx=30, pady=(10, 2))
        password_entry = tk.Entry(card, show="•", bg=BG_COLOR, fg="white", bd=0,
                                  highlightthickness=1, highlightbackground=BORDER_COLOR,
                                  font=("Segoe UI", 10), insertbackground="white")
        password_entry.pack(fill=tk.X, padx=30, ipady=5)

        def handle_login():
            global USER_DB
            USER_DB = load_user_db()
            uname = username_entry.get().strip()
            pw = password_entry.get().strip()
            if uname in USER_DB and USER_DB[uname] == pw:
                self.main_frame.pack_forget()
                self.on_success_callback()
            else:
                messagebox.showerror("Error", "Invalid username or password!", parent=self.root)

        tk.Button(card, text="Login", command=handle_login, bg=ACCENT_COLOR,
                  fg=BG_COLOR, font=("Segoe UI", 10, "bold"),
                  relief=tk.FLAT, cursor="hand2").pack(fill=tk.X, padx=30, pady=25, ipady=4)

        tk.Button(card, text="Don't have an account? Sign Up",
                  command=self.show_signup, bg=CARD_BG, fg=ACCENT_COLOR, bd=0,
                  font=("Segoe UI", 9, "underline"),
                  activebackground=CARD_BG, activeforeground=ACCENT_COLOR,
                  cursor="hand2").pack(pady=10)

    def show_signup(self):
        self.clear_frame()
        card = tk.Frame(self.main_frame, bg=CARD_BG, bd=0,
                        highlightthickness=1, highlightbackground=BORDER_COLOR)
        card.place(relx=0.5, rely=0.5, anchor="center", width=340, height=420)

        tk.Label(card, text="Create Account", font=("Helvetica Neue", 16, "bold"),
                 bg=CARD_BG, fg="white").pack(pady=(30, 5))
        tk.Label(card, text="Choose Username", bg=CARD_BG, fg=TEXT_COLOR,
                 font=("Segoe UI", 9, "bold")).pack(anchor="w", padx=30, pady=(10, 2))
        username_entry = tk.Entry(card, bg=BG_COLOR, fg="white", bd=0,
                                  highlightthickness=1, highlightbackground=BORDER_COLOR,
                                  font=("Segoe UI", 10), insertbackground="white")
        username_entry.pack(fill=tk.X, padx=30, ipady=5)

        tk.Label(card, text="Create Password", bg=CARD_BG, fg=TEXT_COLOR,
                 font=("Segoe UI", 9, "bold")).pack(anchor="w", padx=30, pady=(10, 2))
        password_entry = tk.Entry(card, show="•", bg=BG_COLOR, fg="white", bd=0,
                                  highlightthickness=1, highlightbackground=BORDER_COLOR,
                                  font=("Segoe UI", 10), insertbackground="white")
        password_entry.pack(fill=tk.X, padx=30, ipady=5)

        def handle_signup():
            global USER_DB
            uname = username_entry.get().strip()
            pw = password_entry.get().strip()
            if not uname or not pw:
                messagebox.showerror("Error", "Fields cannot be empty!", parent=self.root)
                return
            USER_DB = load_user_db()
            if uname in USER_DB:
                messagebox.showerror("Error", "Username already exists!", parent=self.root)
            else:
                USER_DB[uname] = pw
                save_user_db(USER_DB)
                messagebox.showinfo("Success", "Account created! Login now.", parent=self.root)
                self.show_login()

        tk.Button(card, text="Sign Up", command=handle_signup, bg=SUCCESS_COLOR,
                  fg=BG_COLOR, font=("Segoe UI", 10, "bold"),
                  relief=tk.FLAT).pack(fill=tk.X, padx=30, pady=25, ipady=4)
        tk.Button(card, text="Back to Login", command=self.show_login,
                  bg=CARD_BG, fg=ACCENT_COLOR, bd=0).pack()


class UltimateSimulator:
    def __init__(self, root):
        self.root = root
        self.root.title("Universal Algorithm Visualizer")
        self.root.geometry("1380x820")
        self.root.config(bg=BG_COLOR)
        self.data = []
        self.is_paused = False
        self.apply_ttk_styles()
        self.setup_ui()

    def apply_ttk_styles(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TCombobox", fieldbackground=CARD_BG,
                        background=BORDER_COLOR, foreground="white")

    def setup_ui(self):
        self.header_frame = tk.Frame(self.root, bg=CARD_BG, height=65)
        self.header_frame.pack(fill=tk.X, side=tk.TOP)
        tk.Label(self.header_frame, text="Universal Algorithm Visualizer",
                 bg=CARD_BG, fg="white",
                 font=("Helvetica Neue", 18, "bold")).pack(side=tk.LEFT, padx=35, pady=18)

        self.ctrl_frame = tk.Frame(self.root, bg=CARD_BG, bd=0,
                                   highlightthickness=1, highlightbackground=BORDER_COLOR)
        self.ctrl_frame.pack(fill=tk.X, side=tk.TOP, padx=30, pady=20)

        tk.Label(self.ctrl_frame, text="📂 Category",
                 bg=CARD_BG, fg=TEXT_COLOR).grid(row=0, column=0, padx=10, pady=15)
        self.cat_menu = ttk.Combobox(
            self.ctrl_frame,
            values=["Sorting", "Searching", "Data Structures", "Graph", "Backtracking"],
            state="readonly", width=15)
        self.cat_menu.current(0)
        self.cat_menu.grid(row=0, column=1)
        self.cat_menu.bind("<<ComboboxSelected>>", self.update_algo_list)

        tk.Label(self.ctrl_frame, text="⚙️ Algorithm",
                 bg=CARD_BG, fg=TEXT_COLOR).grid(row=0, column=2, padx=10)
        self.algo_menu = ttk.Combobox(self.ctrl_frame, state="readonly", width=25)
        self.algo_menu.grid(row=0, column=3)
        self.algo_menu.bind("<<ComboboxSelected>>", lambda e: self.update_pseudocode_panel())
        self.update_algo_list()

        tk.Label(self.ctrl_frame, text="🔢 Size",
                 bg=CARD_BG, fg=TEXT_COLOR).grid(row=0, column=4, padx=10)
        self.size_entry = tk.Entry(self.ctrl_frame, width=5, bg=BG_COLOR,
                                   fg="white", insertbackground="white")
        self.size_entry.insert(0, "15")
        self.size_entry.grid(row=0, column=5)

        tk.Button(self.ctrl_frame, text="Generate", command=self.generate_data,
                  bg=ACCENT_COLOR, fg=BG_COLOR).grid(row=0, column=6, padx=15)

        self.play_btn = tk.Button(self.ctrl_frame, text="▶ Run",
                                  command=self.start_thread,
                                  bg=SUCCESS_COLOR, fg=BG_COLOR, width=10)
        self.play_btn.grid(row=0, column=7, padx=10)

        tk.Button(self.ctrl_frame, text="⏸ Pause",
                  command=self.toggle_pause,
                  bg="#ff9e64").grid(row=0, column=8)

        self.speed_scale = tk.Scale(self.ctrl_frame, from_=0.01, to=1.5,
                                    resolution=0.05, orient=tk.HORIZONTAL,
                                    bg=CARD_BG, fg=TEXT_COLOR, label="Speed")
        self.speed_scale.set(0.3)
        self.speed_scale.grid(row=0, column=9, padx=20)

        body = tk.Frame(self.root, bg=BG_COLOR)
        body.pack(fill=tk.BOTH, expand=True, padx=30, pady=5)

        self.canvas = tk.Canvas(body, bg=CANVAS_BG, highlightthickness=0)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.side_panel = tk.Frame(body, bg=CARD_BG, bd=0,
                                   highlightthickness=1,
                                   highlightbackground=BORDER_COLOR, width=360)
        self.side_panel.pack(side=tk.RIGHT, fill=tk.Y, padx=(15, 0))
        self.side_panel.pack_propagate(False)

        tk.Label(self.side_panel, text="📘 Pseudocode",
                 bg=CARD_BG, fg="white",
                 font=("Helvetica Neue", 13, "bold")).pack(anchor="w", padx=15, pady=(15, 5))

        self.algo_title_var = tk.StringVar(value="—")
        tk.Label(self.side_panel, textvariable=self.algo_title_var,
                 bg=CARD_BG, fg=HIGHLIGHT_COLOR,
                 font=("Segoe UI", 11, "bold")).pack(anchor="w", padx=15)

        tk.Label(self.side_panel, text="Time / Space Complexity",
                 bg=CARD_BG, fg=TEXT_COLOR,
                 font=("Segoe UI", 9, "bold")).pack(anchor="w", padx=15, pady=(12, 2))

        self.complexity_label_var = tk.StringVar(value="—")
        tk.Label(self.side_panel, textvariable=self.complexity_label_var,
                 bg=CARD_BG, fg=SUCCESS_COLOR,
                 font=("Consolas", 10), wraplength=320,
                 justify="left").pack(anchor="w", padx=15)

        tk.Label(self.side_panel, text="Pseudocode",
                 bg=CARD_BG, fg=TEXT_COLOR,
                 font=("Segoe UI", 9, "bold")).pack(anchor="w", padx=15, pady=(15, 4))

        code_wrap = tk.Frame(self.side_panel, bg=CARD_BG)
        code_wrap.pack(fill=tk.BOTH, expand=True, padx=15, pady=(0, 15))

        self.code_text = tk.Text(code_wrap, bg=BG_COLOR, fg="white",
                                 font=("Consolas", 10), bd=0,
                                 highlightthickness=1, highlightbackground=BORDER_COLOR,
                                 wrap="none", insertbackground="white")
        self.code_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scroll = tk.Scrollbar(code_wrap, command=self.code_text.yview)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.code_text.config(yscrollcommand=scroll.set, state="disabled")

        self.info_frame = tk.Frame(self.root, bg=CARD_BG)
        self.info_frame.pack(fill=tk.X, side=tk.BOTTOM, padx=30, pady=20)
        self.complexity_var = tk.StringVar(value="Ready to Visualize")
        tk.Label(self.info_frame, textvariable=self.complexity_var,
                 bg=CARD_BG, fg=TEXT_COLOR,
                 font=("Consolas", 11)).pack(pady=10)

        self.update_pseudocode_panel()

    def update_pseudocode_panel(self):
        algo = self.algo_menu.get()
        info = ALGO_INFO.get(algo)
        self.algo_title_var.set(algo if algo else "—")
        self.code_text.config(state="normal")
        self.code_text.delete("1.0", tk.END)
        if info:
            self.complexity_label_var.set(info["time"])
            self.code_text.insert("1.0", info["code"])
        else:
            self.complexity_label_var.set("—")
            self.code_text.insert("1.0", "Pseudocode not available.")
        self.code_text.config(state="disabled")

    def update_algo_list(self, event=None):
        cat = self.cat_menu.get()
        if cat == "Sorting":
            list_val = ["Bubble Sort", "Insertion Sort", "Merge Sort", "Heap Sort",
                        "Bucket Sort", "Selection Sort", "Quick Sort", "Counting Sort",
                        "Radix Sort", "Shell Sort", "Tim Sort", "Tree Sort", "Topological Sort"]
        elif cat == "Searching":
            list_val = ["Linear Search", "Binary Search", "Jump Search",
                        "Interpolation Search", "Exponential Search"]
        elif cat == "Graph":
            list_val = ["BFS", "DFS", "Dijkstra's Algorithm", "Bellman-Ford Algorithm",
                        "Floyd-Warshall Algorithm", "Prim's Algorithm", "Kruskal's Algorithm"]
        elif cat == "Backtracking":
            list_val = ["N-Queen Problem", "Sudoku Solver", "Subset Generation",
                        "Graph Colouring problem", "Travelling Salesman Problem"]
        else:
            list_val = ["Array (Access/Update)", "Linked List (Traversal)",
                        "Stack UI (Step-by-Step)", "Queue UI (Step-by-Step)",
                        "Binary Tree Representation"]

        self.algo_menu['values'] = list_val
        self.algo_menu.current(0)
        if hasattr(self, "code_text"):
            self.update_pseudocode_panel()

    def generate_data(self):
        try:
            size = int(self.size_entry.get())
        except:
            size = 15
        if size > 30:
            size = 30
        self.data = [random.randint(10, 99) for _ in range(size)]
        self.draw_bars(self.data, [ACCENT_COLOR] * len(self.data))

    def draw_bars(self, data, color_list):
        self.canvas.delete("all")
        c_height = 400
        c_width = max(self.canvas.winfo_width(), 600)
        x_width = c_width / (len(data) + 1)
        offset = 30
        for i, val in enumerate(data):
            x0 = i * x_width + offset
            y0 = c_height - (val * 3)
            x1 = (i + 1) * x_width + offset
            y1 = c_height
            self.canvas.create_rectangle(x0, y0, x1, y1,
                                         fill=color_list[i], outline=BORDER_COLOR)
            self.canvas.create_text(x0 + (x_width / 2), y0 - 15,
                                    text=str(val), fill="white",
                                    font=("Arial", 10, "bold"))
        self.root.update_idletasks()

    def toggle_pause(self):
        self.is_paused = not self.is_paused

    def check_sim_state(self):
        while self.is_paused:
            time.sleep(0.1)
        time.sleep(self.speed_scale.get())

    def start_thread(self):
        algo = self.algo_menu.get()
        self.update_pseudocode_panel()
        target_map = {
            "Bubble Sort": self.bubble_sort,
            "Insertion Sort": self.insertion_sort,
            "Merge Sort": self.merge_sort_start,
            "Heap Sort": self.heap_sort,
            "Bucket Sort": self.bucket_sort,
            "Selection Sort": self.selection_sort,
            "Quick Sort": self.quick_sort_start,
            "Counting Sort": self.counting_sort,
            "Radix Sort": self.radix_sort,
            "Shell Sort": self.shell_sort,
            "Tim Sort": self.tim_sort,
            "Tree Sort": self.tree_sort,
            "Topological Sort": self.topological_sort_viz,
            "Linear Search": self.linear_search,
            "Binary Search": self.binary_search,
            "Jump Search": self.jump_search,
            "Interpolation Search": self.interpolation_search,
            "Exponential Search": self.exponential_search,
            "BFS": self.bfs_viz,
            "DFS": self.dfs_viz,
            "Dijkstra's Algorithm": self.dijkstra_viz,
            "Bellman-Ford Algorithm": self.bellman_ford_viz,
            "Floyd-Warshall Algorithm": self.floyd_warshall_viz,
            "Prim's Algorithm": self.prim_viz,
            "Kruskal's Algorithm": self.kruskal_viz,
            "N-Queen Problem": self.n_queens_viz,
            "Sudoku Solver": self.sudoku_viz,
            "Subset Generation": self.subset_gen_viz,
            "Graph Colouring problem": self.graph_coloring_viz,
            "Travelling Salesman Problem": self.tsp_viz,
            "Array (Access/Update)": self.visualize_array_ops,
            "Linked List (Traversal)": self.visualize_linked_list,
            "Stack UI (Step-by-Step)": self.visualize_stack_step,
            "Queue UI (Step-by-Step)": self.visualize_queue_step,
            "Binary Tree Representation": self.draw_tree_viz,
        }
        if algo in target_map:
            threading.Thread(target=target_map[algo], daemon=True).start()
        else:
            messagebox.showinfo("Note", f"{algo} visualization not yet implemented.")

    # ─────────────────────────────────────────────
    # GRAPH SHARED NODES/EDGES (used by BFS, DFS, Dijkstra, Bellman-Ford)
    # ─────────────────────────────────────────────
    def _get_graph(self):
        nodes = {
            0: (310, 80),
            1: (150, 200),
            2: (470, 200),
            3: (100, 360),
            4: (300, 380),
            5: (520, 360),
        }
        edges = [
            (0, 1, 4), (0, 2, 3),
            (1, 2, 5), (1, 3, 6),
            (1, 4, 7), (2, 4, 8),
            (2, 5, 2), (3, 4, 9),
            (4, 5, 1),
        ]
        return nodes, edges

    def _draw_graph_state(self, nodes, edges, visited=set(),
                          active_node=-1, active_edge=None,
                          dist_labels=None, edge_colors=None):
        self.canvas.delete("all")
        for u, v, w in edges:
            x1, y1 = nodes[u]
            x2, y2 = nodes[v]
            ek = (min(u, v), max(u, v))
            if edge_colors and ek in edge_colors:
                color, width = edge_colors[ek]
            elif active_edge and active_edge == ek:
                color, width = HIGHLIGHT_COLOR, 3
            else:
                color, width = BORDER_COLOR, 1
            self.canvas.create_line(x1, y1, x2, y2, fill=color, width=width)
            mx, my = (x1 + x2) // 2, (y1 + y2) // 2
            self.canvas.create_text(mx, my - 10, text=str(w),
                                    fill=HIGHLIGHT_COLOR, font=("Consolas", 10))

        for i, (x, y) in nodes.items():
            if i == active_node:
                fill = HIGHLIGHT_COLOR
            elif i in visited:
                fill = SUCCESS_COLOR
            else:
                fill = ACCENT_COLOR
            self.canvas.create_oval(x - 20, y - 20, x + 20, y + 20,
                                    fill=fill, outline="white", width=2)
            self.canvas.create_text(x, y, text=str(i),
                                    fill="white", font=("Arial", 11, "bold"))
            if dist_labels and i in dist_labels:
                lbl = "∞" if dist_labels[i] == 999999 else str(dist_labels[i])
                self.canvas.create_text(x, y + 32, text=f"d={lbl}",
                                        fill=HIGHLIGHT_COLOR,
                                        font=("Consolas", 9))
        self.root.update()

    # ─────────────────────────────────────────────
    # BFS
    # ─────────────────────────────────────────────
    def bfs_viz(self):
        self.complexity_var.set("BFS: Level-order Traversal  O(V + E)")
        nodes, edges = self._get_graph()
        adj = {i: [] for i in nodes}
        for u, v, w in edges:
            adj[u].append(v)
            adj[v].append(u)

        visited = set()
        queue = [0]
        visited.add(0)
        self._draw_graph_state(nodes, edges, visited, active_node=0)
        self.check_sim_state()

        while queue:
            u = queue.pop(0)
            self._draw_graph_state(nodes, edges, visited, active_node=u)
            self.check_sim_state()
            for v in adj[u]:
                if v not in visited:
                    visited.add(v)
                    queue.append(v)
                    self._draw_graph_state(nodes, edges, visited,
                                           active_node=v,
                                           active_edge=(min(u, v), max(u, v)))
                    self.check_sim_state()

        self._draw_graph_state(nodes, edges, visited)
        self.complexity_var.set("BFS: Complete!")

    # ─────────────────────────────────────────────
    # DFS
    # ─────────────────────────────────────────────
    def dfs_viz(self):
        self.complexity_var.set("DFS: Depth-first Traversal  O(V + E)")
        nodes, edges = self._get_graph()
        adj = {i: [] for i in nodes}
        for u, v, w in edges:
            adj[u].append(v)
            adj[v].append(u)

        visited = set()

        def dfs(u):
            visited.add(u)
            self._draw_graph_state(nodes, edges, visited, active_node=u)
            self.check_sim_state()
            for v in adj[u]:
                if v not in visited:
                    self._draw_graph_state(nodes, edges, visited,
                                           active_node=v,
                                           active_edge=(min(u, v), max(u, v)))
                    self.check_sim_state()
                    dfs(v)

        dfs(0)
        self._draw_graph_state(nodes, edges, visited)
        self.complexity_var.set("DFS: Complete!")

    # ─────────────────────────────────────────────
    # DIJKSTRA
    # ─────────────────────────────────────────────
    def dijkstra_viz(self):
        self.complexity_var.set("Dijkstra's Algorithm: Shortest Path")
        nodes, edges = self._get_graph()
        adj = {i: [] for i in nodes}
        for u, v, w in edges:
            adj[u].append((v, w))
            adj[v].append((u, w))

        INF = 999999
        dist = {i: INF for i in nodes}
        dist[0] = 0
        pq = [(0, 0)]
        visited = set()

        self._draw_graph_state(nodes, edges, visited, dist_labels=dist)
        self.check_sim_state()

        while pq:
            d, u = heapq.heappop(pq)
            if u in visited:
                continue
            visited.add(u)
            self._draw_graph_state(nodes, edges, visited,
                                   active_node=u, dist_labels=dist)
            self.check_sim_state()
            for v, w in adj[u]:
                if dist[u] + w < dist[v]:
                    dist[v] = dist[u] + w
                    heapq.heappush(pq, (dist[v], v))
                    self._draw_graph_state(nodes, edges, visited,
                                           active_node=v,
                                           active_edge=(min(u, v), max(u, v)),
                                           dist_labels=dist)
                    self.check_sim_state()

        self._draw_graph_state(nodes, edges, visited, dist_labels=dist)
        self.complexity_var.set("Dijkstra's: Complete!")

    # ─────────────────────────────────────────────
    # BELLMAN-FORD
    # ─────────────────────────────────────────────
    def bellman_ford_viz(self):
        self.complexity_var.set("Bellman-Ford: Shortest Path with Neg Weights  O(VE)")
        nodes, edges = self._get_graph()

        INF = 999999
        dist = {i: INF for i in nodes}
        dist[0] = 0
        edge_colors = {}

        self._draw_graph_state(nodes, edges, dist_labels=dist)
        self.check_sim_state()

        for iteration in range(len(nodes) - 1):
            updated = False
            for u, v, w in edges:
                ek = (min(u, v), max(u, v))
                # highlight current edge being relaxed
                edge_colors[ek] = (HIGHLIGHT_COLOR, 2)
                self._draw_graph_state(nodes, edges,
                                       active_edge=ek,
                                       dist_labels=dist,
                                       edge_colors=edge_colors)
                time.sleep(self.speed_scale.get() * 0.4)

                relaxed = False
                if dist[u] != INF and dist[u] + w < dist[v]:
                    dist[v] = dist[u] + w
                    relaxed = True
                    updated = True
                if dist[v] != INF and dist[v] + w < dist[u]:
                    dist[u] = dist[v] + w
                    relaxed = True
                    updated = True

                if relaxed:
                    edge_colors[ek] = (SUCCESS_COLOR, 2)
                else:
                    del edge_colors[ek]

                self._draw_graph_state(nodes, edges, dist_labels=dist,
                                       edge_colors=edge_colors)
                self.check_sim_state()

            if not updated:
                break

        self._draw_graph_state(nodes, edges,
                               visited=set(nodes.keys()),
                               dist_labels=dist)
        self.complexity_var.set("Bellman-Ford: Complete!")

    # ─────────────────────────────────────────────
    # FLOYD-WARSHALL  (fixed: real values, animated updates)
    # ─────────────────────────────────────────────
    def floyd_warshall_viz(self):
        self.canvas.delete("all")
        self.complexity_var.set("Floyd-Warshall: All-Pairs Shortest Path  O(V³)")

        V = 4
        INF = 999

        dist = [
            [0,   3, INF,   7],
            [8,   0,   2, INF],
            [5, INF,   0,   1],
            [2, INF, INF,   0],
        ]

        cell_size = 55
        start_x = 220
        start_y = 100

        def draw_matrix(hi=-1, hj=-1, hk=-1):
            self.canvas.delete("all")
            self.complexity_var.set(
                f"Floyd-Warshall: k={hk}  i={hi}  j={hj}" if hk >= 0
                else "Floyd-Warshall: Initial matrix")

            # Title
            self.canvas.create_text(
                start_x + V * cell_size // 2, start_y - 50,
                text="Distance Matrix",
                fill="white", font=("Helvetica Neue", 13, "bold"))

            # Column headers
            for j in range(V):
                self.canvas.create_text(
                    start_x + j * cell_size + cell_size // 2,
                    start_y - 22,
                    text=str(j), fill=HIGHLIGHT_COLOR,
                    font=("Consolas", 11, "bold"))

            # Row headers + cells
            for i in range(V):
                self.canvas.create_text(
                    start_x - 22,
                    start_y + i * cell_size + cell_size // 2,
                    text=str(i), fill=HIGHLIGHT_COLOR,
                    font=("Consolas", 11, "bold"))

                for j in range(V):
                    x = start_x + j * cell_size
                    y = start_y + i * cell_size

                    # Background color of cell
                    if i == hi and j == hj:
                        bg = SUCCESS_COLOR
                    elif i == hi or j == hj:
                        bg = "#3a3f5c"
                    elif hk >= 0 and (i == hk or j == hk):
                        bg = "#2d3250"
                    else:
                        bg = CARD_BG

                    self.canvas.create_rectangle(
                        x, y, x + cell_size, y + cell_size,
                        fill=bg, outline=BORDER_COLOR, width=1)

                    val = dist[i][j]
                    text_val = "∞" if val >= INF else str(val)
                    color = ERROR_COLOR if val >= INF else "white"
                    self.canvas.create_text(
                        x + cell_size // 2, y + cell_size // 2,
                        text=text_val, fill=color,
                        font=("Consolas", 12, "bold"))

            self.root.update()

        # Show initial matrix
        draw_matrix()
        self.check_sim_state()

        # Main Floyd-Warshall loop
        for k in range(V):
            for i in range(V):
                for j in range(V):
                    if dist[i][k] + dist[k][j] < dist[i][j]:
                        dist[i][j] = dist[i][k] + dist[k][j]
                        draw_matrix(hi=i, hj=j, hk=k)
                        self.check_sim_state()
                    else:
                        draw_matrix(hi=i, hj=j, hk=k)
                        time.sleep(self.speed_scale.get() * 0.2)

        draw_matrix()
        self.complexity_var.set("Floyd-Warshall: Complete! ✓")

    # ─────────────────────────────────────────────
    # PRIM'S  (fixed: real graph, not tree)
    # ─────────────────────────────────────────────
    def prim_viz(self):
        self.canvas.delete("all")
        self.complexity_var.set("Prim's Algorithm: Minimum Spanning Tree  O(E log V)")

        nodes, edges = self._get_graph()
        adj = {i: [] for i in nodes}
        for u, v, w in edges:
            adj[u].append((w, v))
            adj[v].append((w, u))

        visited = set()
        mst_edges = set()
        start = 0
        visited.add(start)
        pq = []
        for w, v in adj[start]:
            heapq.heappush(pq, (w, start, v))

        self._draw_prim_kruskal(nodes, edges, mst_edges, visited)
        self.check_sim_state()

        total_cost = 0
        while pq and len(visited) < len(nodes):
            w, u, v = heapq.heappop(pq)
            if v in visited:
                continue
            # Highlight candidate edge
            ek = (min(u, v), max(u, v))
            self._draw_prim_kruskal(nodes, edges, mst_edges, visited,
                                    active_edge=ek)
            self.check_sim_state()

            visited.add(v)
            mst_edges.add(ek)
            total_cost += w

            for nw, nv in adj[v]:
                if nv not in visited:
                    heapq.heappush(pq, (nw, v, nv))

            self._draw_prim_kruskal(nodes, edges, mst_edges, visited)
            self.check_sim_state()

        self._draw_prim_kruskal(nodes, edges, mst_edges, visited)
        self.complexity_var.set(f"Prim's: MST Complete!  Total Cost = {total_cost}")

    # ─────────────────────────────────────────────
    # KRUSKAL'S  (fixed: real graph, not tree)
    # ─────────────────────────────────────────────
    def kruskal_viz(self):
        self.canvas.delete("all")
        self.complexity_var.set("Kruskal's Algorithm: Minimum Spanning Tree  O(E log E)")

        nodes, edges = self._get_graph()

        # Sort edges by weight
        sorted_edges = sorted(edges, key=lambda e: e[2])

        parent = {i: i for i in nodes}
        rank   = {i: 0 for i in nodes}

        def find(x):
            while parent[x] != x:
                parent[x] = parent[parent[x]]
                x = parent[x]
            return x

        def union(a, b):
            ra, rb = find(a), find(b)
            if ra == rb:
                return False
            if rank[ra] < rank[rb]:
                ra, rb = rb, ra
            parent[rb] = ra
            if rank[ra] == rank[rb]:
                rank[ra] += 1
            return True

        mst_edges = set()
        rejected  = set()
        total_cost = 0

        self._draw_prim_kruskal(nodes, edges, mst_edges, set(), rejected=rejected)
        self.check_sim_state()

        for u, v, w in sorted_edges:
            ek = (min(u, v), max(u, v))
            # Highlight candidate
            self._draw_prim_kruskal(nodes, edges, mst_edges, set(),
                                    active_edge=ek, rejected=rejected)
            self.check_sim_state()

            if union(u, v):
                mst_edges.add(ek)
                total_cost += w
            else:
                rejected.add(ek)

            self._draw_prim_kruskal(nodes, edges, mst_edges, set(),
                                    rejected=rejected)
            self.check_sim_state()

            if len(mst_edges) == len(nodes) - 1:
                break

        # Final: color MST nodes
        mst_nodes = set()
        for u, v in mst_edges:
            mst_nodes.add(u)
            mst_nodes.add(v)
        self._draw_prim_kruskal(nodes, edges, mst_edges, mst_nodes,
                                rejected=rejected)
        self.complexity_var.set(f"Kruskal's: MST Complete!  Total Cost = {total_cost}")

    def _draw_prim_kruskal(self, nodes, edges, mst_edges, visited,
                           active_edge=None, rejected=None):
        """Shared graph draw for Prim and Kruskal."""
        self.canvas.delete("all")
        if rejected is None:
            rejected = set()

        for u, v, w in edges:
            x1, y1 = nodes[u]
            x2, y2 = nodes[v]
            ek = (min(u, v), max(u, v))

            if active_edge and active_edge == ek:
                color, width = HIGHLIGHT_COLOR, 3
            elif ek in mst_edges:
                color, width = SUCCESS_COLOR, 3
            elif ek in rejected:
                color, width = ERROR_COLOR, 1
            else:
                color, width = BORDER_COLOR, 1

            self.canvas.create_line(x1, y1, x2, y2, fill=color, width=width)
            mx, my = (x1 + x2) // 2, (y1 + y2) // 2
            self.canvas.create_text(mx, my - 10, text=str(w),
                                    fill=HIGHLIGHT_COLOR, font=("Consolas", 10))

        mst_nodes = set()
        for a, b in mst_edges:
            mst_nodes.add(a)
            mst_nodes.add(b)

        for i, (x, y) in nodes.items():
            if i in visited or i in mst_nodes:
                fill = SUCCESS_COLOR
            else:
                fill = ACCENT_COLOR
            self.canvas.create_oval(x - 20, y - 20, x + 20, y + 20,
                                    fill=fill, outline="white", width=2)
            self.canvas.create_text(x, y, text=str(i),
                                    fill="white", font=("Arial", 11, "bold"))
        self.root.update()

    # ─────────────────────────────────────────────
    # BACKTRACKING
    # ─────────────────────────────────────────────
    def n_queens_viz(self):
        self.canvas.delete("all")
        self.complexity_var.set("N-Queen: Backtracking  O(N!)")
        try:
            N = int(self.size_entry.get())
        except:
            N = 6
        N = max(4, min(N, 10))
        board = [[0] * N for _ in range(N)]

        def draw_grid(b):
            self.canvas.delete("all")
            grid_size = min(50, 300 // N)
            start_x = 350 - (N * grid_size) // 2
            start_y = 150
            for r in range(N):
                for c in range(N):
                    x0 = start_x + c * grid_size
                    y0 = start_y + r * grid_size
                    fill = "#2d3250" if (r + c) % 2 == 0 else CANVAS_BG
                    self.canvas.create_rectangle(x0, y0, x0 + grid_size,
                                                 y0 + grid_size,
                                                 outline=BORDER_COLOR, fill=fill)
                    if b[r][c] == 1:
                        self.canvas.create_text(
                            x0 + grid_size // 2, y0 + grid_size // 2,
                            text="♛", fill=HIGHLIGHT_COLOR,
                            font=("Arial", grid_size // 2, "bold"))
            self.root.update()

        def is_safe(b, row, col):
            for i in range(row):
                if b[i][col] == 1:
                    return False
                if col - (row - i) >= 0 and b[i][col - (row - i)] == 1:
                    return False
                if col + (row - i) < N and b[i][col + (row - i)] == 1:
                    return False
            return True

        def solve(row):
            if row == N:
                return True
            for col in range(N):
                if is_safe(board, row, col):
                    board[row][col] = 1
                    draw_grid(board)
                    self.check_sim_state()
                    if solve(row + 1):
                        return True
                    board[row][col] = 0
                    draw_grid(board)
            return False

        solve(0)
        self.complexity_var.set("N-Queen: Solution found!")

    def sudoku_viz(self):
        self.canvas.delete("all")
        self.complexity_var.set("Sudoku: Backtracking Algorithm")

        board = [
            [5, 3, 0, 0, 7, 0, 0, 0, 0],
            [6, 0, 0, 1, 9, 5, 0, 0, 0],
            [0, 9, 8, 0, 0, 0, 0, 6, 0],
            [8, 0, 0, 0, 6, 0, 0, 0, 3],
            [4, 0, 0, 8, 0, 3, 0, 0, 1],
            [7, 0, 0, 0, 2, 0, 0, 0, 6],
            [0, 6, 0, 0, 0, 0, 2, 8, 0],
            [0, 0, 0, 4, 1, 9, 0, 0, 5],
            [0, 0, 0, 0, 8, 0, 0, 7, 9],
        ]
        original = [row[:] for row in board]

        def draw_board(b, active_r=-1, active_c=-1):
            self.canvas.delete("all")
            gs = 40
            sx, sy = 280, 80
            for r in range(9):
                for c in range(9):
                    x0 = sx + c * gs
                    y0 = sy + r * gs
                    is_active = (r == active_r and c == active_c)
                    fill = HIGHLIGHT_COLOR if is_active else (
                        "#2d3250" if (r // 3 + c // 3) % 2 == 0 else CARD_BG)
                    self.canvas.create_rectangle(x0, y0, x0 + gs, y0 + gs,
                                                 outline=BORDER_COLOR, fill=fill)
                    if b[r][c] != 0:
                        orig = original[r][c] != 0
                        color = TEXT_COLOR if orig else SUCCESS_COLOR
                        self.canvas.create_text(
                            x0 + 20, y0 + 20, text=str(b[r][c]),
                            fill=color, font=("Arial", 14, "bold"))

            # Bold 3x3 borders
            for i in range(4):
                lw = 3 if i % 3 == 0 else 1
                self.canvas.create_line(sx + i * 3 * gs, sy,
                                        sx + i * 3 * gs, sy + 9 * gs,
                                        fill="white", width=lw)
                self.canvas.create_line(sx, sy + i * 3 * gs,
                                        sx + 9 * gs, sy + i * 3 * gs,
                                        fill="white", width=lw)
            self.root.update()

        def is_valid(b, r, c, n):
            for i in range(9):
                if b[r][i] == n or b[i][c] == n:
                    return False
            sr, sc = 3 * (r // 3), 3 * (c // 3)
            for i in range(3):
                for j in range(3):
                    if b[sr + i][sc + j] == n:
                        return False
            return True

        def solve(b):
            for r in range(9):
                for c in range(9):
                    if b[r][c] == 0:
                        for n in range(1, 10):
                            if is_valid(b, r, c, n):
                                b[r][c] = n
                                draw_board(b, r, c)
                                self.check_sim_state()
                                if solve(b):
                                    return True
                                b[r][c] = 0
                        return False
            return True

        draw_board(board)   
        solve(board)
        self.complexity_var.set("Sudoku: Solved!")

    def subset_gen_viz(self):
        self.complexity_var.set("Subset Generation: O(2^n)")
        if not self.data:
            self.generate_data()
        n = len(self.data)
        for i in range(min(n, 8)):
            self.draw_bars(self.data,
                           [SUCCESS_COLOR if k <= i else ACCENT_COLOR for k in range(n)])
            self.check_sim_state()
        self.draw_bars(self.data, [SUCCESS_COLOR] * n)

    def graph_coloring_viz(self):
        self.complexity_var.set("Graph Coloring: Backtracking  O(m^V)")
        nodes, edges = self._get_graph()
        adj = {i: [] for i in nodes}
        for u, v, w in edges:
            adj[u].append(v)
            adj[v].append(u)

        COLORS = ["#e0af68", "#7aa2f7", "#9ece6a", "#f7768e", "#bb9af7", "#2ac3de"]
        color_map = {}

        def draw_coloring():
            self.canvas.delete("all")
            for u, v, w in edges:
                x1, y1 = nodes[u]
                x2, y2 = nodes[v]
                self.canvas.create_line(x1, y1, x2, y2,
                                        fill=BORDER_COLOR, width=1)
            for i, (x, y) in nodes.items():
                fill = color_map.get(i, ACCENT_COLOR)
                self.canvas.create_oval(x - 20, y - 20, x + 20, y + 20,
                                        fill=fill, outline="white", width=2)
                self.canvas.create_text(x, y, text=str(i),
                                        fill="white", font=("Arial", 11, "bold"))
            self.root.update()

        def is_safe(v, c):
            return all(color_map.get(nb) != c for nb in adj[v])

        def color_graph(v):
            if v == len(nodes):
                return True
            for c in COLORS:
                if is_safe(v, c):
                    color_map[v] = c
                    draw_coloring()
                    self.check_sim_state()
                    if color_graph(v + 1):
                        return True
                    del color_map[v]
            return False

        color_graph(0)
        draw_coloring()
        self.complexity_var.set("Graph Coloring: Complete!")

    def tsp_viz(self):
        self.canvas.delete("all")
        self.complexity_var.set("Travelling Salesman Problem  (Nearest Neighbour heuristic)")

        cities = {
            0: (310, 100),
            1: (150, 220),
            2: (470, 220),
            3: (200, 380),
            4: (420, 380),
        }

        def dist(a, b):
            x1, y1 = cities[a]
            x2, y2 = cities[b]
            return math.hypot(x2 - x1, y2 - y1)

        def draw_tour(tour, active_edge=None):
            self.canvas.delete("all")
            # All edges
            for i in range(len(tour)):
                u = tour[i]
                v = tour[(i + 1) % len(tour)]
                x1, y1 = cities[u]
                x2, y2 = cities[v]
                ek = (min(u, v), max(u, v))
                color = HIGHLIGHT_COLOR if active_edge == ek else SUCCESS_COLOR
                self.canvas.create_line(x1, y1, x2, y2, fill=color, width=2)

            for i, (x, y) in cities.items():
                self.canvas.create_oval(x - 20, y - 20, x + 20, y + 20,
                                        fill=ACCENT_COLOR, outline="white", width=2)
                self.canvas.create_text(x, y, text=str(i),
                                        fill="white", font=("Arial", 11, "bold"))
            self.root.update()

        # Nearest neighbour heuristic
        unvisited = set(cities.keys())
        tour = [0]
        unvisited.remove(0)

        while unvisited:
            last = tour[-1]
            nearest = min(unvisited, key=lambda c: dist(last, c))
            ek = (min(last, nearest), max(last, nearest))
            draw_tour(tour + [nearest], active_edge=ek)
            self.check_sim_state()
            tour.append(nearest)
            unvisited.remove(nearest)

        total = sum(dist(tour[i], tour[(i + 1) % len(tour)])
                    for i in range(len(tour)))
        draw_tour(tour)
        self.complexity_var.set(f"TSP: Tour found!  Cost ≈ {int(total)}")

    # ─────────────────────────────────────────────
    # SEARCHING
    # ─────────────────────────────────────────────
    def linear_search(self):
        if not self.data:
            self.generate_data()
        target = random.choice(self.data)
        self.complexity_var.set(f"Searching for: {target}  |  Time: O(n)")
        for i in range(len(self.data)):
            colors = [HIGHLIGHT_COLOR if k == i else ACCENT_COLOR
                      for k in range(len(self.data))]
            self.draw_bars(self.data, colors)
            self.check_sim_state()
            if self.data[i] == target:
                self.complexity_var.set(f"FOUND {target} at Index {i}!")
                self.draw_bars(self.data,
                               [SUCCESS_COLOR if k == i else ACCENT_COLOR
                                for k in range(len(self.data))])
                return
        self.complexity_var.set(f"Element {target} not found.")

    def binary_search(self):
        self.data.sort()
        target = random.choice(self.data)
        l, r = 0, len(self.data) - 1
        self.complexity_var.set(f"Binary Search: Target = {target}")
        while l <= r:
            mid = (l + r) // 2
            colors = [ACCENT_COLOR] * len(self.data)
            if l < len(self.data):
                colors[l] = "#bb9af2"
            if r < len(self.data):
                colors[r] = "#ff9e64"
            colors[mid] = ERROR_COLOR
            self.draw_bars(self.data, colors)
            self.check_sim_state()
            if self.data[mid] == target:
                self.draw_bars(self.data,
                               [SUCCESS_COLOR if k == mid else ACCENT_COLOR
                                for k in range(len(self.data))])
                self.complexity_var.set(f"FOUND {target} at Index {mid}!")
                return
            if self.data[mid] < target:
                l = mid + 1
            else:
                r = mid - 1
        self.complexity_var.set("Not found.")

    def jump_search(self):
        self.data.sort()
        n = len(self.data)
        target = random.choice(self.data)
        step = max(1, int(math.sqrt(n)))
        prev = 0
        self.complexity_var.set(f"Jump Search: Target {target}  |  Step {step}")
        while self.data[min(step, n) - 1] < target:
            colors = [HIGHLIGHT_COLOR if k < step else ACCENT_COLOR
                      for k in range(n)]
            self.draw_bars(self.data, colors)
            self.check_sim_state()
            prev = step
            step += int(math.sqrt(n))
            if prev >= n:
                break
        for i in range(prev, min(step, n)):
            colors = [HIGHLIGHT_COLOR if k == i else ACCENT_COLOR
                      for k in range(n)]
            self.draw_bars(self.data, colors)
            self.check_sim_state()
            if self.data[i] == target:
                self.draw_bars(self.data,
                               [SUCCESS_COLOR if k == i else ACCENT_COLOR
                                for k in range(n)])
                self.complexity_var.set(f"FOUND {target} at Index {i}!")
                return
        self.complexity_var.set("Not found.")

    def interpolation_search(self):
        self.data.sort()
        n = len(self.data)
        target = random.choice(self.data)
        low, high = 0, n - 1
        self.complexity_var.set(f"Interpolation Search: Target {target}")
        while (low <= high and
               self.data[low] <= target <= self.data[high] and
               self.data[high] != self.data[low]):
            pos = low + int(((target - self.data[low]) * (high - low))
                            / (self.data[high] - self.data[low]))
            pos = max(low, min(pos, high))
            colors = [HIGHLIGHT_COLOR if k == pos else ACCENT_COLOR
                      for k in range(n)]
            self.draw_bars(self.data, colors)
            self.check_sim_state()
            if self.data[pos] == target:
                self.draw_bars(self.data,
                               [SUCCESS_COLOR if k == pos else ACCENT_COLOR
                                for k in range(n)])
                self.complexity_var.set(f"FOUND {target} at Index {pos}!")
                return
            if self.data[pos] < target:
                low = pos + 1
            else:
                high = pos - 1
        self.complexity_var.set("Not found.")

    def exponential_search(self):
        self.data.sort()
        n = len(self.data)
        target = random.choice(self.data)
        self.complexity_var.set(f"Exponential Search: Target {target}")
        if self.data[0] == target:
            self.draw_bars(self.data,
                           [SUCCESS_COLOR] + [ACCENT_COLOR] * (n - 1))
            return
        i = 1
        while i < n and self.data[i] <= target:
            colors = [HIGHLIGHT_COLOR if k <= i else ACCENT_COLOR
                      for k in range(n)]
            self.draw_bars(self.data, colors)
            self.check_sim_state()
            i *= 2
        l, r = i // 2, min(i, n - 1)
        while l <= r:
            mid = (l + r) // 2
            self.draw_bars(self.data,
                           [HIGHLIGHT_COLOR if k == mid else ACCENT_COLOR
                            for k in range(n)])
            self.check_sim_state()
            if self.data[mid] == target:
                self.draw_bars(self.data,
                               [SUCCESS_COLOR if k == mid else ACCENT_COLOR
                                for k in range(n)])
                self.complexity_var.set(f"FOUND {target} at Index {mid}!")
                return
            if self.data[mid] < target:
                l = mid + 1
            else:
                r = mid - 1
        self.complexity_var.set("Not found.")

    # ─────────────────────────────────────────────
    # SORTING
    # ─────────────────────────────────────────────
    def bubble_sort(self):
        n = len(self.data)
        for i in range(n):
            for j in range(n - i - 1):
                if self.data[j] > self.data[j + 1]:
                    self.data[j], self.data[j + 1] = self.data[j + 1], self.data[j]
                    self.draw_bars(self.data,
                                   [ERROR_COLOR if k == j or k == j + 1
                                    else ACCENT_COLOR for k in range(n)])
                    self.check_sim_state()
        self.draw_bars(self.data, [SUCCESS_COLOR] * n)

    def insertion_sort(self):
        for i in range(1, len(self.data)):
            key, j = self.data[i], i - 1
            while j >= 0 and self.data[j] > key:
                self.draw_bars(self.data,
                               [HIGHLIGHT_COLOR if k == j else ACCENT_COLOR
                                for k in range(len(self.data))])
                self.check_sim_state()
                self.data[j + 1] = self.data[j]
                j -= 1
            self.data[j + 1] = key
        self.draw_bars(self.data, [SUCCESS_COLOR] * len(self.data))

    def merge_sort_start(self):
        self.merge_sort(0, len(self.data) - 1)
        self.draw_bars(self.data, [SUCCESS_COLOR] * len(self.data))

    def merge_sort(self, l, r):
        if l < r:
            mid = (l + r) // 2
            self.merge_sort(l, mid)
            self.merge_sort(mid + 1, r)
            self.merge(l, mid, r)

    def merge(self, l, m, r):
        left = self.data[l:m + 1]
        right = self.data[m + 1:r + 1]
        i = j = 0
        k = l
        while i < len(left) and j < len(right):
            self.draw_bars(self.data,
                           [HIGHLIGHT_COLOR if x == k else ACCENT_COLOR
                            for x in range(len(self.data))])
            self.check_sim_state()
            if left[i] <= right[j]:
                self.data[k] = left[i]
                i += 1
            else:
                self.data[k] = right[j]
                j += 1
            k += 1
        while i < len(left):
            self.data[k] = left[i]; i += 1; k += 1
        while j < len(right):
            self.data[k] = right[j]; j += 1; k += 1

    def heap_sort(self):
        n = len(self.data)
        for i in range(n // 2 - 1, -1, -1):
            self.heapify(n, i)
        for i in range(n - 1, 0, -1):
            self.data[i], self.data[0] = self.data[0], self.data[i]
            self.heapify(i, 0)
            self.draw_bars(self.data,
                           [HIGHLIGHT_COLOR if k == i else ACCENT_COLOR
                            for k in range(n)])
            self.check_sim_state()
        self.draw_bars(self.data, [SUCCESS_COLOR] * n)

    def heapify(self, n, i):
        largest, l, r = i, 2 * i + 1, 2 * i + 2
        if l < n and self.data[i] < self.data[l]:
            largest = l
        if r < n and self.data[largest] < self.data[r]:
            largest = r
        if largest != i:
            self.data[i], self.data[largest] = self.data[largest], self.data[i]
            self.heapify(n, largest)

    def bucket_sort(self):
        if not self.data:
            self.generate_data()
        max_v, n = max(self.data), len(self.data)
        buckets = [[] for _ in range(n)]
        for x in self.data:
            idx = int(n * x / (max_v + 1))
            buckets[idx].append(x)
        self.data.clear()
        for b in buckets:
            b.sort()
            for x in b:
                self.data.append(x)
                pad = [0] * (n - len(self.data))
                self.draw_bars(
                    self.data + pad,
                    [HIGHLIGHT_COLOR] * len(self.data) + [ACCENT_COLOR] * len(pad))
                self.check_sim_state()
        self.draw_bars(self.data, [SUCCESS_COLOR] * n)

    def selection_sort(self):
        n = len(self.data)
        for i in range(n):
            m_idx = i
            for j in range(i + 1, n):
                if self.data[j] < self.data[m_idx]:
                    m_idx = j
            self.data[i], self.data[m_idx] = self.data[m_idx], self.data[i]
            self.draw_bars(self.data,
                           [SUCCESS_COLOR if k <= i else ACCENT_COLOR
                            for k in range(n)])
            self.check_sim_state()

    def quick_sort_start(self):
        self.quick_sort(0, len(self.data) - 1)
        self.draw_bars(self.data, [SUCCESS_COLOR] * len(self.data))

    def quick_sort(self, low, high):
        if low < high:
            pivot = self.data[high]
            i = low - 1
            for j in range(low, high):
                if self.data[j] < pivot:
                    i += 1
                    self.data[i], self.data[j] = self.data[j], self.data[i]
            self.data[i + 1], self.data[high] = self.data[high], self.data[i + 1]
            p = i + 1
            self.quick_sort(low, p - 1)
            self.quick_sort(p + 1, high)

    def counting_sort(self):
        if not self.data:
            self.generate_data()
        max_val = max(self.data)
        count = [0] * (max_val + 1)
        for x in self.data:
            count[x] += 1
        idx = 0
        for i in range(len(count)):
            while count[i] > 0:
                self.data[idx] = i
                count[i] -= 1
                idx += 1
                self.draw_bars(self.data,
                               [HIGHLIGHT_COLOR if k == idx - 1 else ACCENT_COLOR
                                for k in range(len(self.data))])
                self.check_sim_state()
        self.draw_bars(self.data, [SUCCESS_COLOR] * len(self.data))

    def radix_sort(self):
        if not self.data:
            self.generate_data()
        max_v = max(self.data)
        exp = 1
        while max_v // exp > 0:
            n = len(self.data)
            output = [0] * n
            count = [0] * 10
            for i in range(n):
                count[(self.data[i] // exp) % 10] += 1
            for i in range(1, 10):
                count[i] += count[i - 1]
            for i in range(n - 1, -1, -1):
                idx = (self.data[i] // exp) % 10
                output[count[idx] - 1] = self.data[i]
                count[idx] -= 1
            for i in range(n):
                self.data[i] = output[i]
                self.draw_bars(self.data,
                               [HIGHLIGHT_COLOR if k == i else ACCENT_COLOR
                                for k in range(n)])
                self.check_sim_state()
            exp *= 10
        self.draw_bars(self.data, [SUCCESS_COLOR] * len(self.data))

    def shell_sort(self):
        n = len(self.data)
        gap = n // 2
        while gap > 0:
            for i in range(gap, n):
                temp = self.data[i]
                j = i
                while j >= gap and self.data[j - gap] > temp:
                    self.data[j] = self.data[j - gap]
                    j -= gap
                    self.draw_bars(self.data,
                                   [ERROR_COLOR if k == j else ACCENT_COLOR
                                    for k in range(n)])
                    self.check_sim_state()
                self.data[j] = temp
            gap //= 2
        self.draw_bars(self.data, [SUCCESS_COLOR] * n)

    def tim_sort(self):
        self.data.sort()
        self.draw_bars(self.data, [SUCCESS_COLOR] * len(self.data))
        self.complexity_var.set("Tim Sort: Complete!")

    def tree_sort(self):
        self.draw_tree_viz()
        time.sleep(1)
        self.data.sort()
        self.draw_bars(self.data, [SUCCESS_COLOR] * len(self.data))
        self.complexity_var.set("Tree Sort: Complete!")

    def topological_sort_viz(self):
        self.complexity_var.set("Topological Sort: DAG linear ordering  O(V + E)")
        self.canvas.delete("all")

        # Simple DAG
        dag_nodes = {
            0: (100, 200), 1: (250, 100), 2: (250, 300),
            3: (400, 100), 4: (400, 300), 5: (550, 200),
        }
        dag_edges = [(0, 1), (0, 2), (1, 3), (2, 4), (3, 5), (4, 5)]
        in_degree = {i: 0 for i in dag_nodes}
        adj = {i: [] for i in dag_nodes}
        for u, v in dag_edges:
            adj[u].append(v)
            in_degree[v] += 1

        order = []
        queue = [n for n in dag_nodes if in_degree[n] == 0]

        def draw_dag(active=-1):
            self.canvas.delete("all")
            for u, v in dag_edges:
                x1, y1 = dag_nodes[u]
                x2, y2 = dag_nodes[v]
                self.canvas.create_line(x1, y1, x2, y2, fill=BORDER_COLOR,
                                        width=1, arrow=tk.LAST)
            for i, (x, y) in dag_nodes.items():
                if i in order:
                    fill = SUCCESS_COLOR
                elif i == active:
                    fill = HIGHLIGHT_COLOR
                else:
                    fill = ACCENT_COLOR
                self.canvas.create_oval(x - 20, y - 20, x + 20, y + 20,
                                        fill=fill, outline="white", width=2)
                self.canvas.create_text(x, y, text=str(i),
                                        fill="white", font=("Arial", 11, "bold"))

            if order:
                self.canvas.create_text(
                    330, 430,
                    text="Order: " + " → ".join(str(o) for o in order),
                    fill=HIGHLIGHT_COLOR, font=("Consolas", 12))
            self.root.update()

        draw_dag()
        self.check_sim_state()

        while queue:
            u = queue.pop(0)
            draw_dag(active=u)
            self.check_sim_state()
            order.append(u)
            for v in adj[u]:
                in_degree[v] -= 1
                if in_degree[v] == 0:
                    queue.append(v)
            draw_dag()

        self.complexity_var.set("Topological Sort: " + " → ".join(str(o) for o in order))

    # ─────────────────────────────────────────────
    # DATA STRUCTURES
    # ─────────────────────────────────────────────
    def draw_tree_viz(self):
        self.canvas.delete("all")
        if not self.data:
            self.generate_data()
        n = len(self.data)
        cx = max(self.canvas.winfo_width() // 2, 350)

        def draw_node(idx, x, y, dx):
            if idx >= n:
                return
            if 2 * idx + 1 < n:
                self.canvas.create_line(x, y, x - dx, y + 60,
                                        fill="white", width=2)
                draw_node(2 * idx + 1, x - dx, y + 60, max(dx / 2, 20))
            if 2 * idx + 2 < n:
                self.canvas.create_line(x, y, x + dx, y + 60,
                                        fill="white", width=2)
                draw_node(2 * idx + 2, x + dx, y + 60, max(dx / 2, 20))
            self.canvas.create_oval(x - 18, y - 18, x + 18, y + 18,
                                    fill="#4CAF50", outline="white")
            self.canvas.create_text(x, y, text=str(self.data[idx]),
                                    fill="black", font=("Arial", 10, "bold"))

        draw_node(0, cx, 50, 200)
        self.root.update_idletasks()

    def visualize_array_ops(self):
        size = 8
        self.data = [random.randint(10, 99) for _ in range(size)]
        for i in range(size):
            self.draw_array_boxes(i, "Accessing...")
            self.check_sim_state()
        self.data[3] = 99
        self.draw_array_boxes(3, "Updated index 3 → 99")
        self.complexity_var.set("Array: Access O(1) | Update O(1) | Complete!")

    def draw_array_boxes(self, highlight_idx=-1, status=""):
        self.canvas.delete("all")
        box_size, start_x, y = 70, 100, 200
        for i, val in enumerate(self.data):
            color = HIGHLIGHT_COLOR if i == highlight_idx else CARD_BG
            self.canvas.create_rectangle(start_x + i * box_size, y,
                                         start_x + (i + 1) * box_size, y + box_size,
                                         fill=color, outline=BORDER_COLOR)
            self.canvas.create_text(start_x + i * box_size + 35, y + 35,
                                    text=str(val), fill="white",
                                    font=("Arial", 12, "bold"))
            self.canvas.create_text(start_x + i * box_size + 35, y + box_size + 15,
                                    text=f"[{i}]", fill=TEXT_COLOR,
                                    font=("Arial", 9))
        if status:
            self.canvas.create_text(400, 350, text=status,
                                    fill=SUCCESS_COLOR, font=("Arial", 14))

    def visualize_linked_list(self):
        self.data = [random.randint(10, 99) for _ in range(6)]
        for i in range(len(self.data)):
            self.draw_linked_nodes(i)
            self.check_sim_state()
        self.complexity_var.set("Linked List: Traversal Complete!")

    def draw_linked_nodes(self, active_idx=-1):
        self.canvas.delete("all")
        x, y, node_w, node_h, gap = 60, 200, 60, 40, 60
        for i, val in enumerate(self.data):
            color = HIGHLIGHT_COLOR if i == active_idx else ACCENT_COLOR
            self.canvas.create_rectangle(x, y, x + node_w, y + node_h,
                                         fill=color, outline="white", width=2)
            self.canvas.create_text(x + 30, y + 20, text=str(val),
                                    fill=BG_COLOR, font=("Arial", 10, "bold"))
            if i < len(self.data) - 1:
                self.canvas.create_line(x + node_w, y + 20,
                                        x + node_w + gap, y + 20,
                                        fill=TEXT_COLOR, arrow=tk.LAST, width=2)
            x += node_w + gap
        # NULL terminator
        self.canvas.create_text(x + 20, y + 20, text="NULL",
                                fill=ERROR_COLOR, font=("Consolas", 10))

    def visualize_stack_step(self):
        self.data = []
        self.complexity_var.set("Stack: Pushing elements...")
        for i in range(5):
            self.data.append(random.randint(20, 90))
            self.draw_bars(self.data, [HIGHLIGHT_COLOR] * len(self.data))
            self.check_sim_state()
        self.complexity_var.set("Stack: Popping elements...")
        for i in range(5):
            if self.data:
                self.data.pop()
            self.draw_bars(self.data if self.data else [0],
                           [ERROR_COLOR] * max(len(self.data), 1))
            self.check_sim_state()
        self.complexity_var.set("Stack: Push/Pop O(1) — Complete!")

    def visualize_queue_step(self):
        self.data = []
        self.complexity_var.set("Queue: Enqueuing elements...")
        for i in range(5):
            self.data.append(random.randint(20, 90))
            self.draw_bars(self.data, [HIGHLIGHT_COLOR] * len(self.data))
            self.check_sim_state()
        self.complexity_var.set("Queue: Dequeuing elements...")
        for i in range(5):
            if self.data:
                self.data.pop(0)
            self.draw_bars(self.data if self.data else [0],
                           [ERROR_COLOR] * max(len(self.data), 1))
            self.check_sim_state()
        self.complexity_var.set("Queue: Enqueue/Dequeue O(1) — Complete!")


if __name__ == "__main__":
    root = tk.Tk()

    def load_app():
        UltimateSimulator(root)

    auth = AuthManager(root, load_app)
    root.mainloop()