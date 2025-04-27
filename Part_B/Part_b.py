import tkinter as tk
import tkinter.messagebox
from tkinter import filedialog
import os
import ast

# Paste your DynamicRangeTree2D implementation here before running this code
class SegmentTreeNode:
    def __init__(self, x_range):
        self.x_range = x_range  # (low, high)
        self.left = None
        self.right = None
        self.ys = []  # Sorted list of y-values for points in this x-range
        self.points = []  # Full (x, y) points stored here

class DynamicRangeTree2D:
    def __init__(self, min_x=0, max_x=10000):
        self.root = self.build_tree(min_x, max_x)

    def build_tree(self, l, r):
        node = SegmentTreeNode((l, r))
        if l == r:
            return node
        mid = (l + r) // 2
        node.left = self.build_tree(l, mid)
        node.right = self.build_tree(mid + 1, r)
        return node

    def _insert(self, node, x, y):
        if not node:
            return
        if node.x_range[0] <= x <= node.x_range[1]:
            node.points.append((x, y))
            self._insert_sorted(node.ys, y)
            if node.left:
                self._insert(node.left, x, y)
            if node.right:
                self._insert(node.right, x, y)

    def insert(self, x, y):
        self._insert(self.root, x, y)

    def _delete(self, node, x, y):
        if not node:
            return
        if node.x_range[0] <= x <= node.x_range[1]:
            if (x, y) in node.points:
                node.points.remove((x, y))
            self._remove_sorted(node.ys, y)
            if node.left:
                self._delete(node.left, x, y)
            if node.right:
                self._delete(node.right, x, y)

    def delete(self, x, y):
        self._delete(self.root, x, y)

    def _query(self, node, x1, x2, y1, y2, result):
        if not node or node.x_range[1] < x1 or node.x_range[0] > x2:
            return
        if x1 <= node.x_range[0] and node.x_range[1] <= x2:
            # node is fully within x-range, search its ys list
            for y in self._range_query_sorted(node.ys, y1, y2):
                for px, py in node.points:
                    if py == y and x1 <= px <= x2 and y1 <= py <= y2:
                        result.append((px, py))
            return
        self._query(node.left, x1, x2, y1, y2, result)
        self._query(node.right, x1, x2, y1, y2, result)

    def query(self, x1, x2, y1, y2):
        result = []
        self._query(self.root, x1, x2, y1, y2, result)
        return result

    # --- Helper functions for sorted insert/remove/query ---
    def _insert_sorted(self, arr, val):
        # Binary insert
        l, r = 0, len(arr)
        while l < r:
            m = (l + r) // 2
            if arr[m] < val:
                l = m + 1
            else:
                r = m
        arr.insert(l, val)

    def _remove_sorted(self, arr, val):
        # Binary remove
        l, r = 0, len(arr)
        while l < r:
            m = (l + r) // 2
            if arr[m] < val:
                l = m + 1
            else:
                r = m
        if l < len(arr) and arr[l] == val:
            arr.pop(l)

    def _range_query_sorted(self, arr, low, high):
        # Returns list of y-values in [low, high]
        l = self._lower_bound(arr, low)
        r = self._upper_bound(arr, high)
        return arr[l:r]

    def _lower_bound(self, arr, val):
        l, r = 0, len(arr)
        while l < r:
            m = (l + r) // 2
            if arr[m] < val:
                l = m + 1
            else:
                r = m
        return l

    def _upper_bound(self, arr, val):
        l, r = 0, len(arr)
        while l < r:
            m = (l + r) // 2
            if arr[m] <= val:
                l = m + 1
            else:
                r = m
        return l

# Helper class for visualization with enhanced features
class RangeTreeVisualizer:
    def __init__(self, master):
        self.master = master
        self.master.title("Dynamic 2D Range Tree Visualizer")

        self.canvas_width = 600
        self.canvas_height = 600
        self.scale = 10
        self.margin = 30

        self.tree = DynamicRangeTree2D(min_x=0, max_x=100)
        self.points = []

        self.canvas = tk.Canvas(master, width=self.canvas_width, height=self.canvas_height, bg='white')
        self.canvas.bind("<Button-1>", self.on_left_click)
        self.canvas.bind("<Button-3>", self.on_right_click)
        self.canvas.pack()

        self.controls = tk.Frame(master)
        self.controls.pack()

        for label in ['x1', 'x2', 'y1', 'y2']:
            tk.Label(self.controls, text=label + ":").pack(side=tk.LEFT)
            setattr(self, f"{label}_entry", tk.Entry(self.controls, width=5))
            getattr(self, f"{label}_entry").pack(side=tk.LEFT)

        tk.Button(self.controls, text="Query", command=self.run_query).pack(side=tk.LEFT)
        tk.Button(self.controls, text="Clear", command=self.clear_all).pack(side=tk.LEFT)
        tk.Button(self.controls, text="Save", command=self.save_points).pack(side=tk.LEFT)
        tk.Button(self.controls, text="Load", command=self.load_points).pack(side=tk.LEFT)
        tk.Button(self.controls, text="Export Query", command=self.export_query_results).pack(side=tk.LEFT)

        # 🔹 Load initial points from file if it exists
        try:
            loaded_pts = []
            n = int(input("Enter the number of points: "))
            print("Enter point as 'x y': ")
            for _ in range(n):
                x_str, y_str = input().strip().split()
                x, y = int(x_str), int(y_str)
                loaded_pts.append((x, y))
                self.tree.insert(x, y)      # Insert into your data structure
                self.points.append((x, y))  # Keep track of the points

            self.status_text = f"Loaded {len(loaded_pts)} points from user input."

        except Exception as e:
            self.status_text = f"Failed to load points: {e}"

        self.redraw()

        self.status = tk.Label(master, text=self.status_text, anchor="w")
        self.status.pack(fill="x")

        self.draw_axes()

    def coord_to_canvas(self, x, y):
        return self.margin + x * self.scale, self.canvas_height - (self.margin + y * self.scale)

    def draw_point(self, x, y, color="black", size=4):
        cx, cy = self.coord_to_canvas(x, y)
        self.canvas.create_oval(cx - size, cy - size, cx + size, cy + size, fill=color)

    def draw_rectangle(self, x1, x2, y1, y2, color="blue"):
        cx1, cy1 = self.coord_to_canvas(x1, y1)
        cx2, cy2 = self.coord_to_canvas(x2, y2)
        self.canvas.create_rectangle(cx1, cy1, cx2, cy2, outline=color, dash=(4, 2), width=2)

    def draw_axes(self):
        self.canvas.delete("axes")
        # Draw X and Y axes with ticks
        for i in range(0, 101, 10):
            x, y = self.coord_to_canvas(i, 0)
            self.canvas.create_line(x, self.canvas_height - self.margin - 3,
                                    x, self.canvas_height - self.margin + 3, tags="axes")
            self.canvas.create_text(x, self.canvas_height - self.margin + 10,
                                    text=str(i), tags="axes", font=("Arial", 7))

            x, y = self.coord_to_canvas(0, i)
            self.canvas.create_line(self.margin - 3, y, self.margin + 3, y, tags="axes")
            self.canvas.create_text(self.margin - 15, y, text=str(i), tags="axes", font=("Arial", 7))

        self.canvas.create_line(self.margin, self.margin,
                                self.margin, self.canvas_height - self.margin, tags="axes")
        self.canvas.create_line(self.margin, self.canvas_height - self.margin,
                                self.canvas_width - self.margin, self.canvas_height - self.margin, tags="axes")

    def on_left_click(self, event):
        x = int((event.x - self.margin) / self.scale)
        y = int((self.canvas_height - event.y - self.margin) / self.scale)

        if not (0 <= x <= 100 and 0 <= y <= 100):
            self.status.config(text="Click inside drawing area.")
            return

        if (x, y) not in self.points:
            self.tree.insert(x, y)
            self.points.append((x, y))
            self.status.config(text=f"Point ({x}, {y}) inserted.")

        # If in query mode, check and highlight if in rectangle
        if getattr(self, "query_mode", False):
            x1, x2, y1, y2 = self.last_query
            if x1 <= x <= x2 and y1 <= y <= y2:
                if (x, y) not in self.last_result:
                    self.last_result.append((x, y))
            self.redraw(highlights=self.last_result, rect=(x1, x2, y1, y2))
        else:
            self.redraw()

    def on_right_click(self, event):
        x = int((event.x - self.margin) / self.scale)
        y = int((self.canvas_height - event.y - self.margin) / self.scale)

        if (x, y) not in self.points:
            self.status.config(text=f"No point at ({x}, {y}) to delete.")
            return

        self.tree.delete(x, y)
        self.points.remove((x, y))
        self.status.config(text=f"Point ({x}, {y}) deleted.")

        if getattr(self, "query_mode", False):
            if (x, y) in self.last_result:
                self.last_result.remove((x, y))
            x1, x2, y1, y2 = self.last_query
            self.redraw(highlights=self.last_result, rect=(x1, x2, y1, y2))
        else:
            self.redraw()

    def redraw(self, highlights=None, rect=None):
        self.canvas.delete("all")
        self.draw_axes()
        for pt in self.points:
            self.draw_point(*pt)
        if highlights:
            for pt in highlights:
                self.draw_point(*pt, color="red", size=5)
        if rect:
            self.draw_rectangle(*rect)

    def run_query(self):
        try:
            x1 = int(self.x1_entry.get())
            x2 = int(self.x2_entry.get())
            y1 = int(self.y1_entry.get())
            y2 = int(self.y2_entry.get())
            if x1 > x2 or y1 > y2:
                raise ValueError("x1 > x2 or y1 > y2")
            self.last_query = (x1, x2, y1, y2)
            result = self.tree.query(x1, x2, y1, y2)
            self.last_result = result
            self.redraw(highlights=result, rect=(x1, x2, y1, y2))
            self.query_mode = True  # Enter query mode
            self.status.config(text=f"{len(result)} point(s) in range.")
        except Exception as e:
            tkinter.messagebox.showerror("Query Error", str(e))

    def clear_all(self):
        self.canvas.delete("all")
        self.points.clear()
        self.tree = DynamicRangeTree2D(min_x=0, max_x=100)
        self.draw_axes()
        self.query_mode = False
        self.status.config(text="Canvas cleared.")

    def save_points(self):
        path = filedialog.asksaveasfilename(defaultextension=".txt")
        if path:
            with open(path, "w") as f:
                f.write(str(self.points))
            self.status.config(text=f"Points saved to {os.path.basename(path)}.")

    def load_points(self):
        path = filedialog.askopenfilename()
        if path:
            with open(path, "r") as f:
                data = f.read()
            try:
                pts = ast.literal_eval(data)
                self.clear_all()
                for x, y in pts:
                    self.tree.insert(x, y)
                    self.points.append((x, y))
                self.redraw()
                self.status.config(text=f"Loaded {len(pts)} point(s) from {os.path.basename(path)}.")
            except:
                tkinter.messagebox.showerror("Load Error", "Invalid point file.")

    def export_query_results(self):
        if hasattr(self, "last_result"):
            path = filedialog.asksaveasfilename(defaultextension=".txt")
            if path:
                with open(path, "w") as f:
                    for pt in self.last_result:
                        f.write(f"{pt}\n")
                self.status.config(text=f"Query results exported to {os.path.basename(path)}.")
        else:
            tkinter.messagebox.showinfo("No Query", "No query results to export yet.")

# Launch the GUI
if __name__ == "__main__":
    root = tk.Tk()
    app = RangeTreeVisualizer(root)
    root.mainloop()
