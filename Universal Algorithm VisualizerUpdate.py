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
    # ─────────────── RECURSION ───────────────
    "Tower of Hanoi": {
        "time": "O(2ⁿ)  |  Space: O(n)",
        "code": """hanoi(n, src, aux, dest):
    if n == 1:
        move disk from src → dest
        return
    hanoi(n-1, src, dest, aux)
    move disk from src → dest
    hanoi(n-1, aux, src, dest)"""
    },
    "Josephus Problem": {
        "time": "O(n)  |  Space: O(n)",
        "code": """josephus(n, k):
    if n == 1: return 0
    return (josephus(n-1, k) + k) % n
# or iterative circle elimination"""
    },
    "Lines in the Plane": {
        "time": "O(n)  |  Space: O(1)",
        "code": """regions(n):
    if n == 0: return 1
    return regions(n-1) + n
# Maximum regions by n lines:
# R(n) = 1 + n(n+1)/2"""
    },
    "Fibonacci (Recursive)": {
        "time": "O(2ⁿ)  |  Space: O(n)",
        "code": """fib(n):
    if n <= 1: return n
    return fib(n-1) + fib(n-2)"""
    },
    "Fibonacci (Iterative)": {
        "time": "O(n)  |  Space: O(1)",
        "code": """fib(n):
    if n <= 1: return n
    a, b = 0, 1
    for i in range(2, n+1):
        a, b = b, a + b
    return b"""
    },
    "Fibonacci (Matrix Expo)": {
        "time": "O(log n)  |  Space: O(1)",
        "code": """M = [[1, 1], [1, 0]]
# F(n) = (M^(n-1))[0][0]
mat_pow(base, exp):
    result = Identity
    while exp > 0:
        if exp odd: result *= base
        base *= base
        exp //= 2
    return result"""
    },
    "Factorial (Recursive)": {
        "time": "O(n)  |  Space: O(n)",
        "code": """fact(n):
    if n <= 1: return 1
    return n * fact(n-1)"""
    },
    "Binary Search (Recursive)": {
        "time": "O(log n)  |  Space: O(log n)",
        "code": """bin_search(arr, l, r, target):
    if l > r: return -1
    mid = (l + r) // 2
    if arr[mid] == target: return mid
    if arr[mid] < target:
        return bin_search(arr, mid+1, r, target)
    return bin_search(arr, l, mid-1, target)"""
    },
    "Permutations (Recursive)": {
        "time": "O(n!)  |  Space: O(n)",
        "code": """permute(arr, l, r):
    if l == r:
        output arr
        return
    for i in range(l, r+1):
        swap(arr[l], arr[i])
        permute(arr, l+1, r)
        swap(arr[l], arr[i])  # backtrack"""
    },
    # ─────────────── DYNAMIC PROGRAMMING ───────────────
    "Fibonacci (DP)": {
        "time": "O(n)  |  Space: O(n) or O(1)",
        "code": """dp[0]=0; dp[1]=1
for i in range(2, n+1):
    dp[i] = dp[i-1] + dp[i-2]
return dp[n]"""
    },
    "0/1 Knapsack": {
        "time": "O(nW)  |  Space: O(nW)",
        "code": """for i in 1..n:
    for w in 0..W:
        if wt[i] <= w:
            dp[i][w] = max(dp[i-1][w],
                           val[i] + dp[i-1][w-wt[i]])
        else:
            dp[i][w] = dp[i-1][w]"""
    },
    "Longest Common Subsequence": {
        "time": "O(mn)  |  Space: O(mn)",
        "code": """for i in 1..m:
    for j in 1..n:
        if X[i]==Y[j]:
            dp[i][j] = dp[i-1][j-1] + 1
        else:
            dp[i][j] = max(dp[i-1][j], dp[i][j-1])"""
    },
    "Coin Change": {
        "time": "O(n*amount)  |  Space: O(amount)",
        "code": """dp[0] = 0
for a in 1..amount:
    dp[a] = INF
    for coin in coins:
        if coin <= a:
            dp[a] = min(dp[a], 1 + dp[a-coin])"""
    },
    "Edit Distance": {
        "time": "O(mn)  |  Space: O(mn)",
        "code": """for i in 0..m:
    for j in 0..n:
        if i==0: dp[i][j] = j
        elif j==0: dp[i][j] = i
        elif s1[i]==s2[j]:
            dp[i][j] = dp[i-1][j-1]
        else:
            dp[i][j] = 1 + min(dp[i-1][j],
                               dp[i][j-1],
                               dp[i-1][j-1])"""
    },
    "Longest Increasing Subsequence": {
        "time": "O(n²)  |  Space: O(n)",
        "code": """dp[i] = 1
for i in 1..n-1:
    for j in 0..i-1:
        if arr[j] < arr[i]:
            dp[i] = max(dp[i], dp[j]+1)
return max(dp)"""
    },
    "Climbing Stairs": {
        "time": "O(n)  |  Space: O(1)",
        "code": """# ways to climb n stairs (1 or 2 steps)
a, b = 1, 1
for i in range(2, n+1):
    a, b = b, a + b
return b"""
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
        self.step_count = 0
        self.total_steps = 0
        # Modify mode state (never mutates original ALGO_INFO)
        self.custom_pseudocode = {}      # algo -> edited code string
        self.applied_pseudocode = {}     # algo -> last applied code
        self.sort_ascending = True       # derived from modified comparison
        self.modify_active = False
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
            values=["Sorting", "Searching", "Data Structures", "Graph", "Backtracking", "Recursion", "Dynamic Programming"],
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

        tk.Button(self.ctrl_frame, text="✎ Modify",
                  command=self.open_modify_dialog,
                  bg="#7aa2f7", fg=BG_COLOR,
                  font=("Segoe UI", 9, "bold")).grid(row=0, column=9, padx=8)

        self.speed_scale = tk.Scale(self.ctrl_frame, from_=0.01, to=1.5,
                                    resolution=0.05, orient=tk.HORIZONTAL,
                                    bg=CARD_BG, fg=TEXT_COLOR, label="Speed")
        self.speed_scale.set(0.3)
        self.speed_scale.grid(row=0, column=10, padx=20)

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
                 font=("Consolas", 11)).pack(side=tk.LEFT, padx=20, pady=10)
        self.step_var = tk.StringVar(value="Steps: 0")
        tk.Label(self.info_frame, textvariable=self.step_var,
                 bg=CARD_BG, fg=HIGHLIGHT_COLOR,
                 font=("Consolas", 11, "bold")).pack(side=tk.RIGHT, padx=20, pady=10)

        self.update_pseudocode_panel()

    def update_pseudocode_panel(self):
        algo = self.algo_menu.get()
        info = ALGO_INFO.get(algo)
        self.algo_title_var.set(algo if algo else "—")
        self.code_text.config(state="normal")
        self.code_text.delete("1.0", tk.END)
        # Prefer applied/custom pseudocode without mutating original ALGO_INFO
        if algo in self.applied_pseudocode:
            self.complexity_label_var.set(info["time"] if info else "—")
            self.code_text.insert("1.0", self.applied_pseudocode[algo])
        elif algo in self.custom_pseudocode:
            self.complexity_label_var.set(info["time"] if info else "—")
            self.code_text.insert("1.0", self.custom_pseudocode[algo])
        elif info:
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
        elif cat == "Recursion":
            list_val = ["Tower of Hanoi", "Josephus Problem", "Lines in the Plane",
                        "Fibonacci (Recursive)", "Fibonacci (Iterative)",
                        "Fibonacci (Matrix Expo)", "Factorial (Recursive)",
                        "Binary Search (Recursive)", "Permutations (Recursive)"]
        elif cat == "Dynamic Programming":
            list_val = ["Fibonacci (DP)", "0/1 Knapsack", "Longest Common Subsequence",
                        "Coin Change", "Edit Distance", "Longest Increasing Subsequence",
                        "Climbing Stairs"]
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

    # ─────────────────────────────────────────────
    # MODIFY FEATURE
    # ─────────────────────────────────────────────
    def _analyze_sort_direction(self, code_text):
        """Infer ascending/descending from comparison operators in pseudocode.
        Returns True for ascending, False for descending.
        """
        code = code_text.lower()
        # Count ascending-style vs descending-style comparisons
        # Ascending bubble: arr[j] > arr[j+1]  → swap
        # Descending:       arr[j] < arr[j+1]  → swap
        asc_hints = code.count(">") - code.count(">=")
        desc_hints = code.count("<") - code.count("<=")
        # Prefer the dominant swap-trigger style
        if "arr[j] < arr[j+1]" in code or "arr[j]<arr[j+1]" in code.replace(" ", ""):
            return False
        if "arr[j] > arr[j+1]" in code or "arr[j]>arr[j+1]" in code.replace(" ", ""):
            return True
        if "descending" in code or "desc" in code:
            return False
        if "ascending" in code or "asc" in code:
            return True
        # Fallback: more < than > in comparison context → descending
        if desc_hints > asc_hints:
            return False
        return True

    def _validate_pseudocode(self, code, algo):
        """Lightweight validation — no eval/exec. Returns (ok, message)."""
        if not code or not code.strip():
            return False, "Pseudocode is empty."
        lines = [ln.strip() for ln in code.splitlines() if ln.strip()]
        if not lines:
            return False, "Pseudocode has no statements."
        # Reject obvious dangerous patterns
        banned = ["import ", "exec(", "eval(", "open(", "__", "os.", "sys.",
                  "subprocess", "socket", "file("]
        low = code.lower()
        for b in banned:
            if b in low:
                return False, f"Unsupported/unsafe construct: '{b.strip()}'"
        # Sorting algorithms: require some recognizable structure
        sorting = {"Bubble Sort", "Insertion Sort", "Selection Sort",
                   "Quick Sort", "Merge Sort", "Heap Sort", "Shell Sort"}
        if algo in sorting:
            has_loop = any(k in low for k in ("for ", "while "))
            has_compare = (">" in code or "<" in code)
            if not has_loop:
                return False, "Sorting pseudocode should contain a loop (for/while)."
            if not has_compare:
                return False, "Sorting pseudocode should contain a comparison (>, <)."
        return True, "Pseudocode looks valid."

    def open_modify_dialog(self):
        """Full Modify panel: dynamic inputs, original + editable pseudocode."""
        algo = self.algo_menu.get()
        info = ALGO_INFO.get(algo, {})
        original_code = info.get("code", "—")
        current_edit = self.custom_pseudocode.get(
            algo, self.applied_pseudocode.get(algo, original_code))

        win = tk.Toplevel(self.root)
        win.title(f"Modify — {algo}")
        win.geometry("640x720")
        win.config(bg=BG_COLOR)
        win.transient(self.root)
        win.grab_set()
        win.resizable(True, True)

        # Scrollable outer
        canvas_outer = tk.Canvas(win, bg=BG_COLOR, highlightthickness=0)
        scroll_y = tk.Scrollbar(win, orient="vertical", command=canvas_outer.yview)
        canvas_outer.configure(yscrollcommand=scroll_y.set)
        scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        canvas_outer.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        form = tk.Frame(canvas_outer, bg=BG_COLOR)
        canvas_outer.create_window((0, 0), window=form, anchor="nw")

        def _on_form_configure(_e=None):
            canvas_outer.configure(scrollregion=canvas_outer.bbox("all"))
        form.bind("<Configure>", _on_form_configure)

        tk.Label(form, text="✎ Modify Input & Pseudocode",
                 bg=BG_COLOR, fg="white",
                 font=("Helvetica Neue", 14, "bold")).pack(pady=(16, 4))
        tk.Label(form, text=f"Algorithm: {algo}",
                 bg=BG_COLOR, fg=HIGHLIGHT_COLOR,
                 font=("Segoe UI", 10)).pack(pady=(0, 10))

        card = tk.Frame(form, bg=CARD_BG, bd=0,
                        highlightthickness=1, highlightbackground=BORDER_COLOR)
        card.pack(fill=tk.BOTH, expand=True, padx=18, pady=6)

        # ── 1) Array size ──
        tk.Label(card, text="1) Array Size (N)",
                 bg=CARD_BG, fg=TEXT_COLOR,
                 font=("Segoe UI", 9, "bold")).pack(anchor="w", padx=16, pady=(12, 2))
        size_row = tk.Frame(card, bg=CARD_BG)
        size_row.pack(fill=tk.X, padx=16)
        size_var = tk.StringVar(value=str(len(self.data) if self.data else 5))
        size_ent = tk.Entry(size_row, textvariable=size_var, width=6,
                            bg=BG_COLOR, fg="white", insertbackground="white",
                            bd=0, highlightthickness=1, highlightbackground=BORDER_COLOR,
                            font=("Segoe UI", 10))
        size_ent.pack(side=tk.LEFT, ipady=3)
        tk.Label(size_row, text="  (1–30)", bg=CARD_BG, fg=TEXT_COLOR,
                 font=("Segoe UI", 8)).pack(side=tk.LEFT)

        # ── 2) Dynamic value fields ──
        tk.Label(card, text="2) Input Values (one field per element)",
                 bg=CARD_BG, fg=TEXT_COLOR,
                 font=("Segoe UI", 9, "bold")).pack(anchor="w", padx=16, pady=(12, 2))
        fields_frame = tk.Frame(card, bg=CARD_BG)
        fields_frame.pack(fill=tk.X, padx=12, pady=4)
        value_entries = []

        def rebuild_fields(preserve=True):
            nonlocal value_entries
            old_vals = []
            if preserve:
                for e in value_entries:
                    old_vals.append(e.get().strip())
            for w in fields_frame.winfo_children():
                w.destroy()
            value_entries = []
            try:
                n = int(size_var.get().strip())
                n = max(1, min(n, 30))
            except Exception:
                n = 5
                size_var.set("5")
            # seed from existing data / old fields
            seeds = old_vals if old_vals else [str(x) for x in self.data]
            for i in range(n):
                row = tk.Frame(fields_frame, bg=CARD_BG)
                row.pack(fill=tk.X, pady=2)
                tk.Label(row, text=f"[{i}]", bg=CARD_BG, fg=HIGHLIGHT_COLOR,
                         font=("Consolas", 9), width=4).pack(side=tk.LEFT)
                ent = tk.Entry(row, bg=BG_COLOR, fg="white", insertbackground="white",
                               bd=0, highlightthickness=1, highlightbackground=BORDER_COLOR,
                               font=("Segoe UI", 10), width=12)
                default = seeds[i] if i < len(seeds) else str(random.randint(1, 99))
                ent.insert(0, default)
                ent.pack(side=tk.LEFT, padx=4, ipady=2)
                value_entries.append(ent)
            _on_form_configure()

        tk.Button(size_row, text="Update Fields", command=lambda: rebuild_fields(True),
                  bg=ACCENT_COLOR, fg=BG_COLOR, font=("Segoe UI", 8, "bold"),
                  relief=tk.FLAT, cursor="hand2").pack(side=tk.LEFT, padx=10)
        rebuild_fields(False)

        # ── 3) Original pseudocode (read-only) ──
        tk.Label(card, text="3) Original Pseudocode (read-only)",
                 bg=CARD_BG, fg=HIGHLIGHT_COLOR,
                 font=("Segoe UI", 9, "bold")).pack(anchor="w", padx=16, pady=(14, 2))
        orig_box = tk.Text(card, height=5, bg="#1a1b26", fg=TEXT_COLOR,
                           font=("Consolas", 9), bd=0, highlightthickness=1,
                           highlightbackground=BORDER_COLOR, wrap="none")
        orig_box.pack(fill=tk.X, padx=16, pady=2)
        orig_box.insert("1.0", original_code)
        orig_box.config(state="disabled")

        # ── 4) Modified pseudocode (editable) ──
        tk.Label(card, text="4) Modified Pseudocode (editable)",
                 bg=CARD_BG, fg=SUCCESS_COLOR,
                 font=("Segoe UI", 9, "bold")).pack(anchor="w", padx=16, pady=(10, 2))
        mod_box = tk.Text(card, height=8, bg=BG_COLOR, fg="white",
                          font=("Consolas", 9), bd=0, highlightthickness=1,
                          highlightbackground=BORDER_COLOR, wrap="none",
                          insertbackground="white")
        mod_box.pack(fill=tk.BOTH, expand=True, padx=16, pady=2)
        mod_box.insert("1.0", current_edit)

        status_var = tk.StringVar(value="")
        tk.Label(card, textvariable=status_var, bg=CARD_BG, fg=ERROR_COLOR,
                 font=("Segoe UI", 9), wraplength=560, justify="left").pack(
                     anchor="w", padx=16, pady=(6, 4))

        tip = ("Tip: For Bubble/Insertion/Selection Sort, change '>' to '<' "
               "(or vice versa) to switch ascending ↔ descending. "
               "Arbitrary full rewrites are validated but only supported "
               "comparison-direction changes alter execution.")
        tk.Label(card, text=tip, bg=CARD_BG, fg=TEXT_COLOR,
                 font=("Segoe UI", 8), wraplength=560, justify="left").pack(
                     anchor="w", padx=16, pady=(0, 8))

        def do_validate():
            code = mod_box.get("1.0", tk.END).rstrip()
            ok, msg = self._validate_pseudocode(code, algo)
            status_var.set(("✓ " if ok else "✗ ") + msg)
            return ok, code

        def do_reset():
            mod_box.delete("1.0", tk.END)
            mod_box.insert("1.0", original_code)
            status_var.set("Reset to original pseudocode.")

        def do_cancel():
            win.destroy()

        def _collect_and_apply(silent=False):
            """Validate + apply data/pseudocode. Returns True on success."""
            ok, code = do_validate()
            if not ok:
                messagebox.showerror("Validation Failed", status_var.get(), parent=win)
                return False
            nums = []
            for i, e in enumerate(value_entries):
                raw = e.get().strip()
                if raw == "":
                    messagebox.showerror("Invalid Input",
                                         f"Field [{i}] is empty.", parent=win)
                    return False
                try:
                    nums.append(int(raw))
                except ValueError:
                    messagebox.showerror("Invalid Input",
                                         f"Field [{i}] is not an integer: '{raw}'",
                                         parent=win)
                    return False
            if not nums:
                messagebox.showerror("Invalid Input", "Need at least one number.", parent=win)
                return False

            self.data = nums[:]
            self.size_entry.delete(0, tk.END)
            self.size_entry.insert(0, str(len(nums)))
            self.custom_pseudocode[algo] = code
            self.applied_pseudocode[algo] = code
            self.sort_ascending = self._analyze_sort_direction(code)
            self.modify_active = True
            self.step_count = 0
            self.step_var.set("Steps: 0")
            self.update_pseudocode_panel()
            self.draw_bars(self.data, [ACCENT_COLOR] * len(self.data))
            order = "ascending" if self.sort_ascending else "descending"
            self.complexity_var.set(
                f"Modified applied ({len(nums)} elements, sort={order})")
            status_var.set(f"✓ Applied ({order}).")
            if not silent:
                messagebox.showinfo(
                    "Applied",
                    f"Data & pseudocode applied.\n"
                    f"Elements: {nums}\n"
                    f"Detected sort order: {order}",
                    parent=win)
            return True

        def do_apply():
            if _collect_and_apply(silent=False):
                win.destroy()

        def do_apply_and_run():
            if _collect_and_apply(silent=True):
                win.destroy()
                self.root.after(80, self.start_thread)

        btn_row = tk.Frame(form, bg=BG_COLOR)
        btn_row.pack(fill=tk.X, padx=18, pady=12)
        tk.Button(btn_row, text="Validate", command=do_validate,
                  bg="#7aa2f7", fg=BG_COLOR, font=("Segoe UI", 9, "bold"),
                  relief=tk.FLAT, cursor="hand2").pack(side=tk.LEFT, padx=3, ipadx=6, ipady=3)
        tk.Button(btn_row, text="Reset", command=do_reset,
                  bg=CARD_BG, fg=TEXT_COLOR, font=("Segoe UI", 9),
                  relief=tk.FLAT, cursor="hand2").pack(side=tk.LEFT, padx=3, ipadx=6, ipady=3)
        tk.Button(btn_row, text="Apply Changes", command=do_apply,
                  bg=SUCCESS_COLOR, fg=BG_COLOR, font=("Segoe UI", 9, "bold"),
                  relief=tk.FLAT, cursor="hand2").pack(side=tk.LEFT, padx=3, ipadx=6, ipady=3)
        tk.Button(btn_row, text="▶ Apply & Run", command=do_apply_and_run,
                  bg=ACCENT_COLOR, fg="white", font=("Segoe UI", 9, "bold"),
                  relief=tk.FLAT, cursor="hand2").pack(side=tk.LEFT, padx=3, ipadx=6, ipady=3)
        tk.Button(btn_row, text="Cancel", command=do_cancel,
                  bg=ERROR_COLOR, fg="white", font=("Segoe UI", 9),
                  relief=tk.FLAT, cursor="hand2").pack(side=tk.RIGHT, padx=3, ipadx=6, ipady=3)

    def draw_bars(self, data, color_list):
        self.canvas.delete("all")
        if not data:
            self.root.update_idletasks()
            return
        c_height = 300
        c_width = max(self.canvas.winfo_width(), 600)
        # Narrower bars with more spacing
        x_width = c_width / (len(data) + 1.5)
        bar_width = x_width * 0.55
        offset = 40
        max_abs = max(abs(v) for v in data) or 1
        # Smaller max height (~150px)
        scale = min(1.5, 150.0 / max_abs)
        base_y = c_height - 8
        for i, val in enumerate(data):
            cx = offset + i * x_width + x_width / 2
            bar_h = max(4, abs(val) * scale)
            if val >= 0:
                y0 = base_y - bar_h
                y1 = base_y
            else:
                y0 = base_y
                y1 = base_y + min(bar_h, 35)
            x0 = cx - bar_width / 2
            x1 = cx + bar_width / 2
            fill = color_list[i] if i < len(color_list) else ACCENT_COLOR
            self.canvas.create_rectangle(x0, y0, x1, y1,
                                         fill=fill, outline=BORDER_COLOR)
            label_y = y0 - 10 if val >= 0 else y1 + 10
            self.canvas.create_text(cx, label_y,
                                    text=str(val), fill="white",
                                    font=("Arial", 9, "bold"))
        self.root.update_idletasks()

    def toggle_pause(self):
        self.is_paused = not self.is_paused

    def check_sim_state(self):
        self.step_count += 1
        self.step_var.set(f"Steps: {self.step_count}")
        while self.is_paused:
            time.sleep(0.1)
        time.sleep(self.speed_scale.get())

    def start_thread(self):
        algo = self.algo_menu.get()
        self.step_count = 0
        self.step_var.set("Steps: 0")
        self.update_pseudocode_panel()
        if not self.data and algo in (
            "Bubble Sort", "Insertion Sort", "Merge Sort", "Heap Sort",
            "Bucket Sort", "Selection Sort", "Quick Sort", "Counting Sort",
            "Radix Sort", "Shell Sort", "Tim Sort", "Tree Sort",
            "Linear Search", "Binary Search", "Jump Search",
            "Interpolation Search", "Exponential Search",
            "Longest Increasing Subsequence",
        ):
            self.generate_data()
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
            # Recursion
            "Tower of Hanoi": self.tower_of_hanoi_viz,
            "Josephus Problem": self.josephus_viz,
            "Lines in the Plane": self.lines_in_plane_viz,
            "Fibonacci (Recursive)": self.fibonacci_viz,
            "Fibonacci (Iterative)": self.fibonacci_iterative_viz,
            "Fibonacci (Matrix Expo)": self.fibonacci_matrix_viz,
            "Factorial (Recursive)": self.factorial_viz,
            "Binary Search (Recursive)": self.binary_search_recursive_viz,
            "Permutations (Recursive)": self.permutations_viz,
            # Dynamic Programming
            "Fibonacci (DP)": self.fibonacci_dp_viz,
            "0/1 Knapsack": self.knapsack_viz,
            "Longest Common Subsequence": self.lcs_viz,
            "Coin Change": self.coin_change_viz,
            "Edit Distance": self.edit_distance_viz,
            "Longest Increasing Subsequence": self.lis_viz,
            "Climbing Stairs": self.climbing_stairs_viz,
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
        asc = self.sort_ascending
        for i in range(n):
            for j in range(n - i - 1):
                should_swap = (self.data[j] > self.data[j + 1]) if asc else (self.data[j] < self.data[j + 1])
                if should_swap:
                    self.data[j], self.data[j + 1] = self.data[j + 1], self.data[j]
                    self.draw_bars(self.data,
                                   [ERROR_COLOR if k == j or k == j + 1
                                    else ACCENT_COLOR for k in range(n)])
                    self.check_sim_state()
                else:
                    # still count comparison steps for accurate step count
                    self.draw_bars(self.data,
                                   [HIGHLIGHT_COLOR if k == j or k == j + 1
                                    else ACCENT_COLOR for k in range(n)])
                    self.check_sim_state()
        self.draw_bars(self.data, [SUCCESS_COLOR] * n)
        order = "ascending" if asc else "descending"
        self.complexity_var.set(f"Bubble Sort complete ({order}) — Steps: {self.step_count}")

    def insertion_sort(self):
        asc = self.sort_ascending
        for i in range(1, len(self.data)):
            key, j = self.data[i], i - 1
            while j >= 0 and ((self.data[j] > key) if asc else (self.data[j] < key)):
                self.draw_bars(self.data,
                               [HIGHLIGHT_COLOR if k == j else ACCENT_COLOR
                                for k in range(len(self.data))])
                self.check_sim_state()
                self.data[j + 1] = self.data[j]
                j -= 1
            self.data[j + 1] = key
        self.draw_bars(self.data, [SUCCESS_COLOR] * len(self.data))
        order = "ascending" if asc else "descending"
        self.complexity_var.set(f"Insertion Sort complete ({order}) — Steps: {self.step_count}")

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
        asc = self.sort_ascending
        for i in range(n):
            m_idx = i
            for j in range(i + 1, n):
                better = (self.data[j] < self.data[m_idx]) if asc else (self.data[j] > self.data[m_idx])
                if better:
                    m_idx = j
            self.data[i], self.data[m_idx] = self.data[m_idx], self.data[i]
            self.draw_bars(self.data,
                           [SUCCESS_COLOR if k <= i else ACCENT_COLOR
                            for k in range(n)])
            self.check_sim_state()
        order = "ascending" if asc else "descending"
        self.complexity_var.set(f"Selection Sort complete ({order}) — Steps: {self.step_count}")

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

    # ─────────────────────────────────────────────
    # RECURSION VISUALIZATIONS
    # ─────────────────────────────────────────────
    def tower_of_hanoi_viz(self):
        self.canvas.delete("all")
        try:
            n = int(self.size_entry.get())
        except:
            n = 4
        n = max(2, min(n, 7))
        self.complexity_var.set(f"Tower of Hanoi: {n} disks  |  Moves: {2**n - 1}")

        # Peg positions
        pegs_x = [200, 400, 600]
        peg_y_base = 420
        peg_height = 220
        disk_height = 18
        max_width = 140

        # State: list of lists (bottom → top)
        towers = [list(range(n, 0, -1)), [], []]  # disk sizes

        def draw_state(moving_disk=None, from_peg=None, to_peg=None, mid_y=None):
            self.canvas.delete("all")
            # Draw base
            self.canvas.create_rectangle(80, peg_y_base, 720, peg_y_base + 15,
                                         fill=BORDER_COLOR, outline="")
            # Draw pegs
            for i, x in enumerate(pegs_x):
                self.canvas.create_rectangle(x - 6, peg_y_base - peg_height,
                                             x + 6, peg_y_base,
                                             fill="#565f89", outline="white")
                self.canvas.create_text(x, peg_y_base + 30,
                                        text=["A (Src)", "B (Aux)", "C (Dest)"][i],
                                        fill=TEXT_COLOR, font=("Segoe UI", 10, "bold"))

            # Draw disks on pegs
            for p_idx, peg in enumerate(towers):
                for d_idx, size in enumerate(peg):
                    w = 30 + size * (max_width // n)
                    x = pegs_x[p_idx]
                    y = peg_y_base - (d_idx + 1) * disk_height
                    color = HIGHLIGHT_COLOR if (moving_disk == size and mid_y is None) else ACCENT_COLOR
                    self.canvas.create_rectangle(x - w // 2, y,
                                                 x + w // 2, y + disk_height - 2,
                                                 fill=color, outline="white", width=1)
                    self.canvas.create_text(x, y + disk_height // 2 - 1,
                                            text=str(size), fill="white",
                                            font=("Arial", 9, "bold"))

            # Draw moving disk in air
            if moving_disk is not None and mid_y is not None and from_peg is not None:
                w = 30 + moving_disk * (max_width // n)
                x = (pegs_x[from_peg] + pegs_x[to_peg]) // 2
                self.canvas.create_rectangle(x - w // 2, mid_y,
                                             x + w // 2, mid_y + disk_height - 2,
                                             fill=HIGHLIGHT_COLOR, outline="white", width=2)
                self.canvas.create_text(x, mid_y + disk_height // 2 - 1,
                                        text=str(moving_disk), fill="white",
                                        font=("Arial", 9, "bold"))

            self.root.update()

        def move_disk(src, dest):
            disk = towers[src].pop()
            # Animate lift
            for step in range(8):
                mid_y = peg_y_base - peg_height - 30 - step * 8
                draw_state(moving_disk=disk, from_peg=src, to_peg=dest, mid_y=mid_y)
                time.sleep(self.speed_scale.get() * 0.15)
            # Move sideways
            for step in range(10):
                t = step / 9
                mid_x = pegs_x[src] + (pegs_x[dest] - pegs_x[src]) * t
                mid_y = peg_y_base - peg_height - 90
                self.canvas.delete("all")
                # redraw static
                self.canvas.create_rectangle(80, peg_y_base, 720, peg_y_base + 15,
                                             fill=BORDER_COLOR, outline="")
                for i, x in enumerate(pegs_x):
                    self.canvas.create_rectangle(x - 6, peg_y_base - peg_height,
                                                 x + 6, peg_y_base,
                                                 fill="#565f89", outline="white")
                    self.canvas.create_text(x, peg_y_base + 30,
                                            text=["A (Src)", "B (Aux)", "C (Dest)"][i],
                                            fill=TEXT_COLOR, font=("Segoe UI", 10, "bold"))
                for p_idx, peg in enumerate(towers):
                    for d_idx, size in enumerate(peg):
                        w = 30 + size * (max_width // n)
                        x = pegs_x[p_idx]
                        y = peg_y_base - (d_idx + 1) * disk_height
                        self.canvas.create_rectangle(x - w // 2, y,
                                                     x + w // 2, y + disk_height - 2,
                                                     fill=ACCENT_COLOR, outline="white")
                        self.canvas.create_text(x, y + disk_height // 2 - 1,
                                                text=str(size), fill="white",
                                                font=("Arial", 9, "bold"))
                w = 30 + disk * (max_width // n)
                self.canvas.create_rectangle(mid_x - w // 2, mid_y,
                                             mid_x + w // 2, mid_y + disk_height - 2,
                                             fill=HIGHLIGHT_COLOR, outline="white", width=2)
                self.canvas.create_text(mid_x, mid_y + disk_height // 2 - 1,
                                        text=str(disk), fill="white",
                                        font=("Arial", 9, "bold"))
                self.root.update()
                time.sleep(self.speed_scale.get() * 0.12)

            towers[dest].append(disk)
            draw_state()
            self.check_sim_state()

        def hanoi(k, src, aux, dest):
            if k == 1:
                move_disk(src, dest)
                return
            hanoi(k - 1, src, dest, aux)
            move_disk(src, dest)
            hanoi(k - 1, aux, src, dest)

        draw_state()
        self.check_sim_state()
        hanoi(n, 0, 1, 2)
        self.complexity_var.set(f"Tower of Hanoi: Complete!  ({2**n - 1} moves)")

    def josephus_viz(self):
        self.canvas.delete("all")
        try:
            n = int(self.size_entry.get())
        except:
            n = 10
        n = max(5, min(n, 20))
        k = 2  # every 2nd person (classic)
        self.complexity_var.set(f"Josephus Problem: n={n}, k={k}")

        people = list(range(n))
        cx, cy, radius = 400, 260, 160

        def draw_circle(alive, current=None, eliminated=None):
            self.canvas.delete("all")
            # Circle guide
            self.canvas.create_oval(cx - radius - 10, cy - radius - 10,
                                    cx + radius + 10, cy + radius + 10,
                                    outline=BORDER_COLOR, width=1)
            angle_step = 2 * math.pi / n
            for i in range(n):
                angle = -math.pi / 2 + i * angle_step
                x = cx + radius * math.cos(angle)
                y = cy + radius * math.sin(angle)
                if i not in alive:
                    continue
                if i == eliminated:
                    fill = ERROR_COLOR
                elif i == current:
                    fill = HIGHLIGHT_COLOR
                else:
                    fill = ACCENT_COLOR
                self.canvas.create_oval(x - 18, y - 18, x + 18, y + 18,
                                        fill=fill, outline="white", width=2)
                self.canvas.create_text(x, y, text=str(i),
                                        fill="white", font=("Arial", 10, "bold"))
            remaining = sorted(alive)
            self.canvas.create_text(400, 460,
                                    text="Alive: " + ", ".join(map(str, remaining)),
                                    fill=TEXT_COLOR, font=("Consolas", 11))
            self.root.update()

        alive = set(range(n))
        idx = 0
        draw_circle(alive)
        self.check_sim_state()

        while len(alive) > 1:
            # Count k people
            count = 0
            while count < k:
                if idx in alive:
                    count += 1
                    if count == k:
                        break
                idx = (idx + 1) % n
            # Eliminate
            eliminated = idx
            draw_circle(alive, current=idx, eliminated=eliminated)
            self.check_sim_state()
            alive.remove(eliminated)
            # Move to next
            idx = (idx + 1) % n
            while idx not in alive and alive:
                idx = (idx + 1) % n
            draw_circle(alive, current=idx)
            self.check_sim_state()

        survivor = list(alive)[0]
        draw_circle(alive)
        self.complexity_var.set(f"Josephus: Survivor is person {survivor}!")

    def lines_in_plane_viz(self):
        self.canvas.delete("all")
        try:
            n = int(self.size_entry.get())
        except:
            n = 6
        n = max(1, min(n, 12))
        self.complexity_var.set(f"Lines in the Plane: Maximum regions with {n} lines")

        # Classic formula visualization + simple line drawing
        # R(n) = R(n-1) + n , R(0)=1
        regions = [1]
        for i in range(1, n + 1):
            regions.append(regions[-1] + i)

        def draw_step(step):
            self.canvas.delete("all")
            # Title & formula
            self.canvas.create_text(400, 40,
                                    text=f"Maximum Regions by {step} Lines",
                                    fill="white", font=("Helvetica Neue", 14, "bold"))
            self.canvas.create_text(400, 70,
                                    text=f"R({step}) = R({step-1}) + {step} = {regions[step]}",
                                    fill=HIGHLIGHT_COLOR, font=("Consolas", 13))

            # Draw lines (simple arrangement that maximizes regions)
            # We draw lines with different slopes/intercepts
            margin = 80
            width, height = 640, 320
            base_x, base_y = 80, 100

            # Background
            self.canvas.create_rectangle(base_x, base_y,
                                         base_x + width, base_y + height,
                                         fill=CANVAS_BG, outline=BORDER_COLOR)

            # Draw the lines one by one
            colors = [ACCENT_COLOR, HIGHLIGHT_COLOR, SUCCESS_COLOR, ERROR_COLOR,
                      "#7aa2f7", "#bb9af7", "#2ac3de", "#e0af68"]
            for i in range(step):
                # Vary angle and position
                angle = (i * 25 + 10) * math.pi / 180
                # Parametric line through center with offset
                cx = base_x + width / 2 + (i - step / 2) * 15
                cy = base_y + height / 2 + (i % 3 - 1) * 20
                dx = math.cos(angle) * 400
                dy = math.sin(angle) * 400
                x1, y1 = cx - dx, cy - dy
                x2, y2 = cx + dx, cy + dy
                # Clip roughly to box
                self.canvas.create_line(x1, y1, x2, y2,
                                        fill=colors[i % len(colors)], width=2)

            # Show recurrence table
            table_x = 100
            self.canvas.create_text(table_x, base_y + height + 40,
                                    text="Recurrence:",
                                    fill=TEXT_COLOR, font=("Segoe UI", 10, "bold"),
                                    anchor="w")
            for i in range(min(step + 1, 9)):
                txt = f"R({i}) = {regions[i]}"
                color = SUCCESS_COLOR if i == step else TEXT_COLOR
                self.canvas.create_text(table_x + i * 70, base_y + height + 65,
                                        text=txt, fill=color,
                                        font=("Consolas", 10))

            self.root.update()

        for s in range(0, n + 1):
            draw_step(s)
            self.check_sim_state()

        self.complexity_var.set(f"Lines in the Plane: R({n}) = {regions[n]} regions")

    def fibonacci_viz(self):
        self.canvas.delete("all")
        try:
            n = int(self.size_entry.get())
        except:
            n = 7
        # Full tree only readable up to ~6; for larger n we use stack + sequence view
        n = max(1, min(n, 20))
        self.complexity_var.set(f"Fibonacci Recursive: fib({n})")

        call_count = [0]
        max_depth = [0]
        stack = []          # current call stack of k values
        computed = {}       # memo of results we have finished

        def draw_state(current_k=None, returning=None):
            self.canvas.delete("all")
            # Title
            self.canvas.create_text(400, 25,
                                    text=f"Fibonacci Recursive  —  fib({n})",
                                    fill="white", font=("Helvetica Neue", 14, "bold"))
            # Stats
            self.canvas.create_text(400, 52,
                                    text=f"Calls so far: {call_count[0]}   |   Max depth: {max_depth[0]}",
                                    fill=HIGHLIGHT_COLOR, font=("Consolas", 11))

            # ---- Call Stack (left side) ----
            self.canvas.create_text(160, 90,
                                    text="Call Stack",
                                    fill=TEXT_COLOR, font=("Segoe UI", 11, "bold"))
            box_w, box_h = 140, 28
            for i, k in enumerate(reversed(stack)):
                y = 110 + i * (box_h + 6)
                is_top = (i == 0)
                fill = HIGHLIGHT_COLOR if is_top else ACCENT_COLOR
                self.canvas.create_rectangle(90, y, 90 + box_w, y + box_h,
                                             fill=fill, outline="white", width=1)
                self.canvas.create_text(160, y + box_h // 2,
                                        text=f"fib({k})",
                                        fill="white", font=("Consolas", 11, "bold"))
            if returning is not None:
                self.canvas.create_text(160, 110 + len(stack) * (box_h + 6) + 20,
                                        text=f"← return {returning}",
                                        fill=SUCCESS_COLOR, font=("Consolas", 11, "bold"))

            # ---- Sequence / Results (right side) ----
            self.canvas.create_text(520, 90,
                                    text="Computed Values",
                                    fill=TEXT_COLOR, font=("Segoe UI", 11, "bold"))
            # Show fib(0) … fib(n) as boxes
            cols = 8
            start_x, start_y = 340, 115
            box = 48
            for i in range(n + 1):
                col = i % cols
                row = i // cols
                x = start_x + col * (box + 8)
                y = start_y + row * (box + 18)
                if i in computed:
                    fill = SUCCESS_COLOR
                    txt = str(computed[i])
                elif i == current_k:
                    fill = HIGHLIGHT_COLOR
                    txt = "?"
                else:
                    fill = CARD_BG
                    txt = "?"
                self.canvas.create_rectangle(x, y, x + box, y + box,
                                             fill=fill, outline=BORDER_COLOR)
                self.canvas.create_text(x + box // 2, y + box // 2 - 4,
                                        text=txt, fill="white",
                                        font=("Consolas", 10, "bold"))
                self.canvas.create_text(x + box // 2, y + box + 9,
                                        text=f"f({i})", fill=TEXT_COLOR,
                                        font=("Arial", 8))

            # Big result at bottom when finished
            if n in computed:
                self.canvas.create_text(400, 420,
                                        text=f"fib({n}) = {computed[n]}",
                                        fill=SUCCESS_COLOR,
                                        font=("Consolas", 18, "bold"))
            self.root.update()

        def fib(k, depth=0):
            call_count[0] += 1
            max_depth[0] = max(max_depth[0], depth)
            stack.append(k)
            draw_state(current_k=k)
            self.check_sim_state()

            if k <= 1:
                res = k
            else:
                res = fib(k - 1, depth + 1) + fib(k - 2, depth + 1)

            computed[k] = res
            stack.pop()
            draw_state(returning=res)
            self.check_sim_state()
            return res

        result = fib(n)
        draw_state()
        self.complexity_var.set(
            f"Fibonacci: fib({n}) = {result}   |   Total calls: {call_count[0]}   |   Max depth: {max_depth[0]}")

    def fibonacci_iterative_viz(self):
        """O(n) iterative Fibonacci – contrast with the exponential recursive version."""
        self.canvas.delete("all")
        try:
            n = int(self.size_entry.get())
        except:
            n = 10
        n = max(0, min(n, 30))
        self.complexity_var.set(f"Fibonacci Iterative (Optimized): fib({n})  O(n) time, O(1) space")

        # Pre-compute nothing – animate step by step
        a, b = 0, 1
        sequence = [0]
        if n >= 1:
            sequence.append(1)

        def draw_state(i, a_val, b_val, just_updated=False):
            self.canvas.delete("all")
            # Title
            self.canvas.create_text(400, 25,
                                    text=f"Iterative Fibonacci  —  fib({n})",
                                    fill="white", font=("Helvetica Neue", 14, "bold"))
            self.canvas.create_text(400, 52,
                                    text="Only two variables needed  →  O(1) extra space",
                                    fill=HIGHLIGHT_COLOR, font=("Consolas", 11))

            # Current variables a & b
            self.canvas.create_text(200, 100, text="a (prev)", fill=TEXT_COLOR,
                                    font=("Segoe UI", 10, "bold"))
            self.canvas.create_rectangle(130, 115, 270, 165,
                                         fill=ACCENT_COLOR, outline="white", width=2)
            self.canvas.create_text(200, 140, text=str(a_val),
                                    fill="white", font=("Consolas", 16, "bold"))

            self.canvas.create_text(400, 100, text="b (current)", fill=TEXT_COLOR,
                                    font=("Segoe UI", 10, "bold"))
            fill_b = SUCCESS_COLOR if just_updated else HIGHLIGHT_COLOR
            self.canvas.create_rectangle(330, 115, 470, 165,
                                         fill=fill_b, outline="white", width=2)
            self.canvas.create_text(400, 140, text=str(b_val),
                                    fill="white", font=("Consolas", 16, "bold"))

            # Arrow / formula
            self.canvas.create_text(400, 195,
                                    text="next = a + b    then    a, b = b, next",
                                    fill=TEXT_COLOR, font=("Consolas", 12))

            # Progress bar
            bar_x, bar_y, bar_w, bar_h = 100, 230, 600, 18
            progress = 0 if n == 0 else min(i / n, 1.0)
            self.canvas.create_rectangle(bar_x, bar_y, bar_x + bar_w, bar_y + bar_h,
                                         fill=CARD_BG, outline=BORDER_COLOR)
            self.canvas.create_rectangle(bar_x, bar_y,
                                         bar_x + int(bar_w * progress), bar_y + bar_h,
                                         fill=SUCCESS_COLOR, outline="")
            self.canvas.create_text(400, bar_y + 35,
                                    text=f"Step {i} / {n}",
                                    fill=TEXT_COLOR, font=("Consolas", 11))

            # Sequence so far
            self.canvas.create_text(400, 290,
                                    text="Sequence built so far:",
                                    fill=TEXT_COLOR, font=("Segoe UI", 10, "bold"))
            cols = 10
            box = 48
            start_x = 80
            start_y = 315
            for idx, val in enumerate(sequence):
                col = idx % cols
                row = idx // cols
                x = start_x + col * (box + 6)
                y = start_y + row * (box + 16)
                is_latest = (idx == len(sequence) - 1)
                fill = SUCCESS_COLOR if is_latest else CARD_BG
                self.canvas.create_rectangle(x, y, x + box, y + box,
                                             fill=fill, outline=BORDER_COLOR)
                self.canvas.create_text(x + box // 2, y + box // 2 - 3,
                                        text=str(val), fill="white",
                                        font=("Consolas", 9, "bold"))
                self.canvas.create_text(x + box // 2, y + box + 8,
                                        text=f"f({idx})", fill=TEXT_COLOR,
                                        font=("Arial", 7))

            if i >= n:
                self.canvas.create_text(400, 460,
                                        text=f"fib({n}) = {b_val}",
                                        fill=SUCCESS_COLOR,
                                        font=("Consolas", 18, "bold"))
            self.root.update()

        # Special cases
        if n == 0:
            draw_state(0, 0, 0, True)
            self.complexity_var.set("Fibonacci Iterative: fib(0) = 0")
            return
        if n == 1:
            draw_state(1, 0, 1, True)
            self.complexity_var.set("Fibonacci Iterative: fib(1) = 1")
            return

        draw_state(1, a, b)
        self.check_sim_state()

        for i in range(2, n + 1):
            a, b = b, a + b
            sequence.append(b)
            draw_state(i, a, b, just_updated=True)
            self.check_sim_state()

        self.complexity_var.set(
            f"Fibonacci Iterative: fib({n}) = {b}   |   Only {n-1} additions  |  O(1) space")

    def fibonacci_matrix_viz(self):
        """Fibonacci via Matrix Exponentiation – O(log n)."""
        self.canvas.delete("all")
        try:
            n = int(self.size_entry.get())
        except:
            n = 10
        n = max(0, min(n, 40))
        self.complexity_var.set(f"Matrix Exponentiation: fib({n})  O(log n)")

        def mat_mul(A, B):
            return [
                [A[0][0]*B[0][0] + A[0][1]*B[1][0],
                 A[0][0]*B[0][1] + A[0][1]*B[1][1]],
                [A[1][0]*B[0][0] + A[1][1]*B[1][0],
                 A[1][0]*B[0][1] + A[1][1]*B[1][1]]
            ]

        def identity():
            return [[1, 0], [0, 1]]

        def draw_matrix(mat, title, x, y, highlight=False):
            cell = 52
            bg = HIGHLIGHT_COLOR if highlight else CARD_BG
            self.canvas.create_text(x + cell, y - 18, text=title,
                                    fill=TEXT_COLOR, font=("Segoe UI", 10, "bold"))
            for i in range(2):
                for j in range(2):
                    cx = x + j * cell
                    cy = y + i * cell
                    self.canvas.create_rectangle(cx, cy, cx + cell, cy + cell,
                                                 fill=bg, outline=BORDER_COLOR, width=1)
                    val = mat[i][j]
                    # Keep numbers readable
                    txt = str(val) if abs(val) < 10**12 else f"{val:.2e}"
                    self.canvas.create_text(cx + cell//2, cy + cell//2,
                                            text=txt, fill="white",
                                            font=("Consolas", 10, "bold"))

        steps = []  # list of (base, exp, result, action)

        def mat_pow(base, exp):
            result = identity()
            orig_exp = exp
            step = 0
            while exp > 0:
                action = ""
                if exp & 1:
                    result = mat_mul(result, base)
                    action = f"exp odd → result *= base"
                steps.append(( [row[:] for row in base],
                               exp,
                               [row[:] for row in result],
                               action or "skip multiply",
                               step ))
                base = mat_mul(base, base)
                exp //= 2
                step += 1
                # also record the square
                steps.append(( [row[:] for row in base],
                               exp,
                               [row[:] for row in result],
                               "base = base²",
                               step ))
                step += 1
            return result

        if n == 0:
            self.canvas.create_text(400, 250, text="fib(0) = 0",
                                    fill=SUCCESS_COLOR, font=("Consolas", 20, "bold"))
            self.complexity_var.set("Matrix Expo: fib(0) = 0")
            return
        if n == 1:
            self.canvas.create_text(400, 250, text="fib(1) = 1",
                                    fill=SUCCESS_COLOR, font=("Consolas", 20, "bold"))
            self.complexity_var.set("Matrix Expo: fib(1) = 1")
            return

        # M = [[1,1],[1,0]], we need M^(n-1), then F(n) = result[0][0]
        M = [[1, 1], [1, 0]]
        result_mat = mat_pow([row[:] for row in M], n - 1)
        fib_n = result_mat[0][0]

        # Animate the recorded steps
        for base, exp, res, action, step_no in steps:
            self.canvas.delete("all")
            self.canvas.create_text(400, 22,
                                    text=f"Matrix Exponentiation  —  fib({n})",
                                    fill="white", font=("Helvetica Neue", 14, "bold"))
            self.canvas.create_text(400, 48,
                                    text=f"Computing M^({n-1})   |   step {step_no}",
                                    fill=HIGHLIGHT_COLOR, font=("Consolas", 11))

            # Formula reminder
            self.canvas.create_text(400, 78,
                                    text="[[F(k+1), F(k)], [F(k), F(k-1)]]  =  [[1,1],[1,0]]^k",
                                    fill=TEXT_COLOR, font=("Consolas", 10))

            draw_matrix(base, "current base", 80, 120)
            draw_matrix(res, "result so far", 320, 120, highlight=True)

            # Exponent info
            self.canvas.create_text(600, 140, text=f"exp = {exp}",
                                    fill=HIGHLIGHT_COLOR, font=("Consolas", 12, "bold"))
            self.canvas.create_text(600, 170, text=action,
                                    fill=SUCCESS_COLOR, font=("Consolas", 11))

            # Binary of original exponent
            self.canvas.create_text(400, 280,
                                    text=f"Original exponent {n-1} in binary: {bin(n-1)[2:]}",
                                    fill=TEXT_COLOR, font=("Consolas", 11))

            # Progress
            total_bits = max(1, (n-1).bit_length())
            self.canvas.create_text(400, 310,
                                    text=f"Only ~{total_bits} iterations (log₂({n-1}))",
                                    fill=TEXT_COLOR, font=("Segoe UI", 10))

            self.root.update()
            self.check_sim_state()

        # Final result
        self.canvas.delete("all")
        self.canvas.create_text(400, 40,
                                text=f"Matrix Exponentiation Complete",
                                fill="white", font=("Helvetica Neue", 14, "bold"))
        draw_matrix(result_mat, f"M^({n-1})", 280, 100, highlight=True)
        self.canvas.create_text(400, 240,
                                text=f"fib({n}) = result[0][0] = {fib_n}",
                                fill=SUCCESS_COLOR, font=("Consolas", 16, "bold"))
        self.canvas.create_text(400, 290,
                                text=f"Time complexity: O(log n)  ≈  {(n-1).bit_length()} multiplications of 2×2 matrices",
                                fill=TEXT_COLOR, font=("Consolas", 11))
        self.complexity_var.set(
            f"Matrix Expo: fib({n}) = {fib_n}   |   O(log n)  |  ~{(n-1).bit_length()} steps")
        self.root.update()

    def factorial_viz(self):
        self.canvas.delete("all")
        try:
            n = int(self.size_entry.get())
        except:
            n = 6
        n = max(1, min(n, 12))
        self.complexity_var.set(f"Factorial Recursive: {n}!")

        stack = []  # for visualization of call stack

        def fact(k):
            stack.append(k)
            self._draw_fact_stack(stack, None)
            self.check_sim_state()
            if k <= 1:
                res = 1
            else:
                res = k * fact(k - 1)
            stack.pop()
            self._draw_fact_stack(stack, res)
            self.check_sim_state()
            return res

        result = fact(n)
        self.complexity_var.set(f"Factorial: {n}! = {result}")

    def _draw_fact_stack(self, stack, returning):
        self.canvas.delete("all")
        self.canvas.create_text(400, 40,
                                text="Factorial Call Stack",
                                fill="white", font=("Helvetica Neue", 14, "bold"))
        if not stack and returning is not None:
            self.canvas.create_text(400, 200,
                                    text=f"Result = {returning}",
                                    fill=SUCCESS_COLOR,
                                    font=("Consolas", 20, "bold"))
            self.root.update()
            return

        box_w, box_h = 180, 40
        start_y = 100
        for i, val in enumerate(reversed(stack)):
            y = start_y + i * (box_h + 12)
            color = HIGHLIGHT_COLOR if i == 0 else ACCENT_COLOR
            self.canvas.create_rectangle(310, y, 310 + box_w, y + box_h,
                                         fill=color, outline="white", width=2)
            self.canvas.create_text(400, y + box_h // 2,
                                    text=f"fact({val})",
                                    fill="white", font=("Consolas", 12, "bold"))
        if returning is not None:
            self.canvas.create_text(400, start_y + len(stack) * (box_h + 12) + 30,
                                    text=f"← returning {returning}",
                                    fill=SUCCESS_COLOR, font=("Consolas", 12))
        self.root.update()

    def binary_search_recursive_viz(self):
        if not self.data:
            self.generate_data()
        self.data.sort()
        target = random.choice(self.data)
        self.complexity_var.set(f"Recursive Binary Search: Target = {target}")

        def bin_search(l, r, depth=0):
            if l > r:
                return -1
            mid = (l + r) // 2
            colors = [ACCENT_COLOR] * len(self.data)
            for i in range(l, r + 1):
                colors[i] = "#3a3f5c"
            colors[mid] = HIGHLIGHT_COLOR
            if l < len(self.data):
                colors[l] = "#bb9af2"
            if r < len(self.data):
                colors[r] = "#ff9e64"
            self.draw_bars(self.data, colors)
            self.complexity_var.set(
                f"Recursive Binary Search  depth={depth}  mid={mid}  target={target}")
            self.check_sim_state()
            if self.data[mid] == target:
                self.draw_bars(self.data,
                               [SUCCESS_COLOR if k == mid else ACCENT_COLOR
                                for k in range(len(self.data))])
                return mid
            if self.data[mid] < target:
                return bin_search(mid + 1, r, depth + 1)
            return bin_search(l, mid - 1, depth + 1)

        idx = bin_search(0, len(self.data) - 1)
        if idx != -1:
            self.complexity_var.set(f"FOUND {target} at Index {idx} (recursive)!")
        else:
            self.complexity_var.set("Not found.")

    def permutations_viz(self):
        self.canvas.delete("all")
        try:
            n = int(self.size_entry.get())
        except:
            n = 3
        n = max(2, min(n, 4))  # keep small
        arr = list(range(1, n + 1))
        self.complexity_var.set(f"Permutations of {arr}  (n! = {math.factorial(n)})")

        results = []

        def draw_current(current, depth):
            self.canvas.delete("all")
            self.canvas.create_text(400, 30,
                                    text=f"Generating Permutations (depth {depth})",
                                    fill="white", font=("Helvetica Neue", 13, "bold"))
            # Current partial
            self.canvas.create_text(400, 70,
                                    text="Current: " + " ".join(map(str, current)),
                                    fill=HIGHLIGHT_COLOR, font=("Consolas", 14))
            # All found so far
            y = 120
            for i, p in enumerate(results[-12:]):  # show last few
                self.canvas.create_text(400, y + i * 22,
                                        text=str(p),
                                        fill=SUCCESS_COLOR, font=("Consolas", 11))
            self.root.update()

        def permute(a, l):
            if l == len(a):
                results.append(a[:])
                draw_current(a, l)
                self.check_sim_state()
                return
            for i in range(l, len(a)):
                a[l], a[i] = a[i], a[l]
                draw_current(a[:l + 1], l)
                self.check_sim_state()
                permute(a, l + 1)
                a[l], a[i] = a[i], a[l]  # backtrack

        permute(arr, 0)
        self.complexity_var.set(f"Permutations: Generated {len(results)} permutations")

    # ─────────────────────────────────────────────
    # DYNAMIC PROGRAMMING VISUALIZATIONS
    # ─────────────────────────────────────────────
    def fibonacci_dp_viz(self):
        """Bottom-up DP table for Fibonacci."""
        self.canvas.delete("all")
        try:
            n = int(self.size_entry.get())
        except:
            n = 10
        n = max(0, min(n, 25))
        self.complexity_var.set(f"Fibonacci DP (Bottom-Up): fib({n})")

        dp = [0] * (n + 1)
        if n >= 1:
            dp[1] = 1

        def draw_table(current=None):
            self.canvas.delete("all")
            self.canvas.create_text(400, 25,
                                    text=f"Fibonacci DP Table  —  fib({n})",
                                    fill="white", font=("Helvetica Neue", 14, "bold"))
            cols = 10
            box = 52
            start_x, start_y = 80, 80
            for i in range(n + 1):
                col = i % cols
                row = i // cols
                x = start_x + col * (box + 8)
                y = start_y + row * (box + 22)
                if i == current:
                    fill = HIGHLIGHT_COLOR
                elif i <= (current or -1):
                    fill = SUCCESS_COLOR
                else:
                    fill = CARD_BG
                self.canvas.create_rectangle(x, y, x + box, y + box,
                                             fill=fill, outline=BORDER_COLOR)
                val = dp[i] if i <= (current or -1) or (current is None and i <= n) else "?"
                if current is None:
                    val = dp[i]
                self.canvas.create_text(x + box//2, y + box//2 - 4,
                                        text=str(val), fill="white",
                                        font=("Consolas", 11, "bold"))
                self.canvas.create_text(x + box//2, y + box + 10,
                                        text=f"dp[{i}]", fill=TEXT_COLOR,
                                        font=("Arial", 8))
            if current is not None and current >= 2:
                self.canvas.create_text(400, 380,
                                        text=f"dp[{current}] = dp[{current-1}] + dp[{current-2}] = {dp[current-1]} + {dp[current-2]}",
                                        fill=HIGHLIGHT_COLOR, font=("Consolas", 12))
            self.root.update()

        draw_table(-1)
        self.check_sim_state()
        for i in range(2, n + 1):
            dp[i] = dp[i-1] + dp[i-2]
            draw_table(i)
            self.check_sim_state()
        draw_table(None)
        self.complexity_var.set(f"Fibonacci DP: fib({n}) = {dp[n]}")

    def knapsack_viz(self):
        """0/1 Knapsack DP table animation."""
        self.canvas.delete("all")
        # Fixed small example for clear visualization
        values = [60, 100, 120]
        weights = [10, 20, 30]
        W = 50
        n = len(values)
        self.complexity_var.set(f"0/1 Knapsack: n={n}, W={W}")

        dp = [[0] * (W + 1) for _ in range(n + 1)]

        def draw_dp(hi=-1, hw=-1):
            self.canvas.delete("all")
            self.canvas.create_text(400, 20,
                                    text="0/1 Knapsack DP Table",
                                    fill="white", font=("Helvetica Neue", 13, "bold"))
            self.canvas.create_text(400, 42,
                                    text=f"Items: val={values}  wt={weights}  Capacity={W}",
                                    fill=TEXT_COLOR, font=("Consolas", 10))

            # Draw a compact version (show every 5 capacity for space)
            cell_w, cell_h = 28, 22
            start_x, start_y = 60, 70
            # Header
            for w in range(0, W + 1, 5):
                self.canvas.create_text(start_x + (w // 5) * cell_w + cell_w//2, start_y - 12,
                                        text=str(w), fill=HIGHLIGHT_COLOR, font=("Arial", 7))
            for i in range(n + 1):
                self.canvas.create_text(start_x - 20, start_y + i * cell_h + cell_h//2,
                                        text=str(i), fill=HIGHLIGHT_COLOR, font=("Arial", 8))
                for w_idx, w in enumerate(range(0, W + 1, 5)):
                    x = start_x + w_idx * cell_w
                    y = start_y + i * cell_h
                    if i == hi and w == hw:
                        fill = HIGHLIGHT_COLOR
                    elif i <= hi:
                        fill = SUCCESS_COLOR if dp[i][w] > 0 else CARD_BG
                    else:
                        fill = CARD_BG
                    self.canvas.create_rectangle(x, y, x + cell_w, y + cell_h,
                                                 fill=fill, outline=BORDER_COLOR)
                    self.canvas.create_text(x + cell_w//2, y + cell_h//2,
                                            text=str(dp[i][w]), fill="white",
                                            font=("Arial", 7))
            self.root.update()

        for i in range(1, n + 1):
            for w in range(W + 1):
                if weights[i-1] <= w:
                    dp[i][w] = max(dp[i-1][w],
                                   values[i-1] + dp[i-1][w - weights[i-1]])
                else:
                    dp[i][w] = dp[i-1][w]
                if w % 5 == 0:
                    draw_dp(i, w)
                    self.check_sim_state()

        draw_dp()
        self.complexity_var.set(f"0/1 Knapsack: Maximum value = {dp[n][W]}")

    def lcs_viz(self):
        """Longest Common Subsequence DP table."""
        self.canvas.delete("all")
        X = "AGGTAB"
        Y = "GXTXAYB"
        m, n = len(X), len(Y)
        self.complexity_var.set(f"LCS: '{X}' vs '{Y}'")

        dp = [[0] * (n + 1) for _ in range(m + 1)]

        def draw_table(hi=-1, hj=-1):
            self.canvas.delete("all")
            self.canvas.create_text(400, 20,
                                    text="Longest Common Subsequence",
                                    fill="white", font=("Helvetica Neue", 13, "bold"))
            self.canvas.create_text(400, 42,
                                    text=f"X = {X}    Y = {Y}",
                                    fill=TEXT_COLOR, font=("Consolas", 11))

            cell = 36
            sx, sy = 120, 80
            # Column headers (Y)
            for j in range(n):
                self.canvas.create_text(sx + (j+1)*cell + cell//2, sy - 12,
                                        text=Y[j], fill=HIGHLIGHT_COLOR,
                                        font=("Consolas", 11, "bold"))
            for i in range(m + 1):
                if i > 0:
                    self.canvas.create_text(sx - 15, sy + i*cell + cell//2,
                                            text=X[i-1], fill=HIGHLIGHT_COLOR,
                                            font=("Consolas", 11, "bold"))
                for j in range(n + 1):
                    x = sx + j * cell
                    y = sy + i * cell
                    if i == hi and j == hj:
                        fill = HIGHLIGHT_COLOR
                    elif i <= hi and j <= hj:
                        fill = SUCCESS_COLOR if dp[i][j] > 0 else CARD_BG
                    else:
                        fill = CARD_BG
                    self.canvas.create_rectangle(x, y, x+cell, y+cell,
                                                 fill=fill, outline=BORDER_COLOR)
                    self.canvas.create_text(x+cell//2, y+cell//2,
                                            text=str(dp[i][j]), fill="white",
                                            font=("Consolas", 10, "bold"))
            self.root.update()

        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if X[i-1] == Y[j-1]:
                    dp[i][j] = dp[i-1][j-1] + 1
                else:
                    dp[i][j] = max(dp[i-1][j], dp[i][j-1])
                draw_table(i, j)
                self.check_sim_state()

        draw_table()
        self.complexity_var.set(f"LCS Length = {dp[m][n]}")

    def coin_change_viz(self):
        """Minimum coins DP."""
        self.canvas.delete("all")
        coins = [1, 3, 4]
        amount = 10
        try:
            amount = min(int(self.size_entry.get()), 20)
        except:
            pass
        self.complexity_var.set(f"Coin Change: coins={coins}, amount={amount}")

        INF = 999
        dp = [INF] * (amount + 1)
        dp[0] = 0

        def draw_state(curr_a=-1):
            self.canvas.delete("all")
            self.canvas.create_text(400, 25,
                                    text=f"Coin Change (Min Coins)  —  amount={amount}",
                                    fill="white", font=("Helvetica Neue", 13, "bold"))
            self.canvas.create_text(400, 50,
                                    text=f"Coins: {coins}",
                                    fill=TEXT_COLOR, font=("Consolas", 11))

            box = 48
            cols = 10
            for a in range(amount + 1):
                col = a % cols
                row = a // cols
                x = 80 + col * (box + 8)
                y = 90 + row * (box + 20)
                if a == curr_a:
                    fill = HIGHLIGHT_COLOR
                elif dp[a] < INF:
                    fill = SUCCESS_COLOR
                else:
                    fill = CARD_BG
                self.canvas.create_rectangle(x, y, x+box, y+box,
                                             fill=fill, outline=BORDER_COLOR)
                txt = str(dp[a]) if dp[a] < INF else "∞"
                self.canvas.create_text(x+box//2, y+box//2-3,
                                        text=txt, fill="white",
                                        font=("Consolas", 11, "bold"))
                self.canvas.create_text(x+box//2, y+box+9,
                                        text=f"a={a}", fill=TEXT_COLOR, font=("Arial", 8))
            self.root.update()

        draw_state()
        self.check_sim_state()
        for a in range(1, amount + 1):
            for c in coins:
                if c <= a and dp[a - c] + 1 < dp[a]:
                    dp[a] = dp[a - c] + 1
            draw_state(a)
            self.check_sim_state()

        result = dp[amount] if dp[amount] < INF else -1
        self.complexity_var.set(f"Coin Change: Min coins for {amount} = {result}")

    def edit_distance_viz(self):
        """Levenshtein Edit Distance DP."""
        self.canvas.delete("all")
        s1, s2 = "kitten", "sitting"
        m, n = len(s1), len(s2)
        self.complexity_var.set(f"Edit Distance: '{s1}' → '{s2}'")

        dp = [[0] * (n + 1) for _ in range(m + 1)]
        for i in range(m + 1):
            dp[i][0] = i
        for j in range(n + 1):
            dp[0][j] = j

        def draw_table(hi=-1, hj=-1):
            self.canvas.delete("all")
            self.canvas.create_text(400, 18,
                                    text="Edit Distance (Levenshtein)",
                                    fill="white", font=("Helvetica Neue", 13, "bold"))
            self.canvas.create_text(400, 40,
                                    text=f"'{s1}'  →  '{s2}'",
                                    fill=TEXT_COLOR, font=("Consolas", 11))

            cell = 34
            sx, sy = 100, 70
            for j in range(n):
                self.canvas.create_text(sx + (j+1)*cell + cell//2, sy - 12,
                                        text=s2[j], fill=HIGHLIGHT_COLOR,
                                        font=("Consolas", 10, "bold"))
            for i in range(m + 1):
                if i > 0:
                    self.canvas.create_text(sx - 14, sy + i*cell + cell//2,
                                            text=s1[i-1], fill=HIGHLIGHT_COLOR,
                                            font=("Consolas", 10, "bold"))
                for j in range(n + 1):
                    x = sx + j * cell
                    y = sy + i * cell
                    if i == hi and j == hj:
                        fill = HIGHLIGHT_COLOR
                    else:
                        fill = CARD_BG
                    self.canvas.create_rectangle(x, y, x+cell, y+cell,
                                                 fill=fill, outline=BORDER_COLOR)
                    self.canvas.create_text(x+cell//2, y+cell//2,
                                            text=str(dp[i][j]), fill="white",
                                            font=("Consolas", 9, "bold"))
            self.root.update()

        draw_table()
        self.check_sim_state()
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if s1[i-1] == s2[j-1]:
                    dp[i][j] = dp[i-1][j-1]
                else:
                    dp[i][j] = 1 + min(dp[i-1][j], dp[i][j-1], dp[i-1][j-1])
                draw_table(i, j)
                self.check_sim_state()

        draw_table()
        self.complexity_var.set(f"Edit Distance = {dp[m][n]}")

    def lis_viz(self):
        """Longest Increasing Subsequence O(n²) DP."""
        self.canvas.delete("all")
        if not self.data:
            self.generate_data()
        arr = self.data[:12]  # keep small
        n = len(arr)
        self.complexity_var.set(f"LIS: array = {arr}")

        dp = [1] * n
        parent = [-1] * n

        def draw_state(curr=-1):
            self.canvas.delete("all")
            self.canvas.create_text(400, 25,
                                    text="Longest Increasing Subsequence",
                                    fill="white", font=("Helvetica Neue", 13, "bold"))
            # Draw array bars with dp values
            bar_w = min(40, 600 // n)
            for i, val in enumerate(arr):
                x = 80 + i * (bar_w + 10)
                h = val * 2
                y = 320 - h
                if i == curr:
                    fill = HIGHLIGHT_COLOR
                else:
                    fill = ACCENT_COLOR
                self.canvas.create_rectangle(x, y, x + bar_w, 320,
                                             fill=fill, outline=BORDER_COLOR)
                self.canvas.create_text(x + bar_w//2, y - 12,
                                        text=str(val), fill="white",
                                        font=("Arial", 9, "bold"))
                # dp value under
                self.canvas.create_text(x + bar_w//2, 340,
                                        text=f"dp={dp[i]}", fill=SUCCESS_COLOR,
                                        font=("Consolas", 9))
            self.root.update()

        draw_state()
        self.check_sim_state()
        for i in range(1, n):
            for j in range(i):
                if arr[j] < arr[i] and dp[j] + 1 > dp[i]:
                    dp[i] = dp[j] + 1
                    parent[i] = j
            draw_state(i)
            self.check_sim_state()

        lis_len = max(dp)
        draw_state()
        self.complexity_var.set(f"LIS Length = {lis_len}")

    def climbing_stairs_viz(self):
        """Climbing Stairs – classic DP (same recurrence as Fibonacci)."""
        self.canvas.delete("all")
        try:
            n = int(self.size_entry.get())
        except:
            n = 8
        n = max(1, min(n, 20))
        self.complexity_var.set(f"Climbing Stairs: {n} stairs")

        dp = [0] * (n + 1)
        dp[0] = 1
        if n >= 1:
            dp[1] = 1

        def draw_state(curr=-1):
            self.canvas.delete("all")
            done = (curr is None)
            active = n if done else curr

            # Title
            self.canvas.create_text(400, 22,
                                    text=f"Climbing Stairs  —  {n} steps",
                                    fill="white", font=("Helvetica Neue", 14, "bold"))
            self.canvas.create_text(400, 45,
                                    text="Ways(n) = Ways(n-1) + Ways(n-2)",
                                    fill=TEXT_COLOR, font=("Consolas", 11))

            # ── DP value boxes (top area) ──
            box = 42
            gap = 6
            cols = min(n + 1, 10)
            total_w = cols * (box + gap) - gap
            start_x = (800 - total_w) // 2
            start_y = 70

            for i in range(n + 1):
                col = i % 10
                row = i // 10
                x = start_x + col * (box + gap)
                y = start_y + row * (box + 22)

                if done or i < active:
                    fill = SUCCESS_COLOR
                elif i == active:
                    fill = HIGHLIGHT_COLOR
                else:
                    fill = CARD_BG

                self.canvas.create_rectangle(x, y, x + box, y + box,
                                             fill=fill, outline=BORDER_COLOR, width=1)
                self.canvas.create_text(x + box // 2, y + box // 2 - 2,
                                        text=str(dp[i]), fill="white",
                                        font=("Consolas", 10, "bold"))
                self.canvas.create_text(x + box // 2, y + box + 9,
                                        text=f"w({i})", fill=TEXT_COLOR,
                                        font=("Arial", 7))

            # ── Clean staircase (bottom area) ──
            stair_base_y = 420
            step_h = 16
            step_w = max(28, min(48, 520 // (n + 1)))
            stair_start_x = 80

            for i in range(n + 1):
                x = stair_start_x + i * step_w
                y = stair_base_y - (i + 1) * step_h
                w = step_w * (n + 1 - i)   # longer steps at bottom look better? 
                # Actually keep uniform width for clarity
                w = step_w + 8

                if done or i < active:
                    fill = SUCCESS_COLOR
                elif i == active:
                    fill = HIGHLIGHT_COLOR
                else:
                    fill = "#2d3250"

                self.canvas.create_rectangle(x, y, x + w, y + step_h - 1,
                                             fill=fill, outline=BORDER_COLOR)
                self.canvas.create_text(x + w // 2, y + step_h // 2,
                                        text=str(i), fill="white",
                                        font=("Arial", 8, "bold"))

            # Current formula highlight
            if not done and active >= 2:
                self.canvas.create_text(400, 455,
                                        text=f"w({active}) = w({active-1}) + w({active-2}) = {dp[active-1]} + {dp[active-2]} = {dp[active]}",
                                        fill=HIGHLIGHT_COLOR, font=("Consolas", 12, "bold"))
            elif done:
                self.canvas.create_text(400, 455,
                                        text=f"Total ways to climb {n} stairs = {dp[n]}",
                                        fill=SUCCESS_COLOR, font=("Consolas", 13, "bold"))

            self.root.update()

        draw_state(0)
        self.check_sim_state()
        for i in range(2, n + 1):
            dp[i] = dp[i - 1] + dp[i - 2]
            draw_state(i)
            self.check_sim_state()

        draw_state(None)
        self.complexity_var.set(f"Climbing Stairs: {dp[n]} ways to climb {n} stairs")


if __name__ == "__main__":
    root = tk.Tk()

    def load_app():
        UltimateSimulator(root)

    auth = AuthManager(root, load_app)
    root.mainloop()