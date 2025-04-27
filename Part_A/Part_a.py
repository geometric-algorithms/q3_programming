import matplotlib.pyplot as plt
import matplotlib.patches as patches

class RangeTreeNode:
    def __init__(self, points):
        # Points sorted by x-coordinate
        self.points = sorted(points, key=lambda p: p[0])
        self.left = None
        self.right = None
        self.x_mid = None
        self.y_sorted = sorted(points, key=lambda p: p[1])  # For 1D y-queries

        if len(points) == 1:
            return  # Leaf node

        mid = len(self.points) // 2
        self.x_mid = self.points[mid][0]

        left_points = self.points[:mid]
        right_points = self.points[mid:]

        self.left = RangeTreeNode(left_points)
        self.right = RangeTreeNode(right_points)


class RangeTree2D:
    def __init__(self, points):
        if points:
            self.root = RangeTreeNode(points)
        else:
            self.root = None

    def query(self, x1, x2, y1, y2):
        return self._query_recursive(self.root, x1, x2, y1, y2)

    def _query_recursive(self, node, x1, x2, y1, y2):
        if not node:
            return []

        result = []

        min_x = node.points[0][0]
        max_x = node.points[-1][0]

        # Case 1: Entire node's x-range is within query range
        if x1 <= min_x and max_x <= x2:
            # Use binary search to get y-range
            ys = [p[1] for p in node.y_sorted]
            l = self._lower_bound(ys, y1)
            r = self._upper_bound(ys, y2)
            return node.y_sorted[l:r]

        # Case 2: Need to search children
        if node.left and x1 <= node.x_mid:
            result += self._query_recursive(node.left, x1, x2, y1, y2)
        if node.right and x2 >= node.x_mid:
            result += self._query_recursive(node.right, x1, x2, y1, y2)

        return result

    # Binary search helpers
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
    

def read_points_from_file(filename):
    points = []
    with open(filename, 'r') as file:
        for line in file:
            x, y = map(int, line.strip().split())
            points.append((x, y))
    return points


def visualize_range_query(points, query_rect, result_points):
    """
    Visualizes:
    - All input points
    - The query rectangle
    - The matched result points
    """
    x1, x2, y1, y2 = query_rect

    fig, ax = plt.subplots(figsize=(8, 6))
    ax.set_title("2D Range Tree Query Visualization")

    # Plot all points
    all_x = [p[0] for p in points]
    all_y = [p[1] for p in points]
    ax.scatter(all_x, all_y, color='gray', label='All Points')

    # Plot query rectangle
    rect = patches.Rectangle((x1, y1), x2 - x1, y2 - y1,
                             linewidth=2, edgecolor='blue', facecolor='none', linestyle='--')
    ax.add_patch(rect)

    # Plot result points
    res_x = [p[0] for p in result_points]
    res_y = [p[1] for p in result_points]
    ax.scatter(res_x, res_y, color='red', label='Query Results', zorder=5)

    # Annotate points
    for p in result_points:
        ax.annotate(f'{p}', (p[0] + 0.2, p[1] + 0.2), fontsize=9, color='red')

    ax.set_xlim(min(all_x) - 1, max(all_x) + 2)
    ax.set_ylim(min(all_y) - 1, max(all_y) + 2)
    ax.legend()
    ax.grid(True)
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.show()


if __name__ == "__main__":
    n = int(input("Enter number of points: "))
    points = []
    print("Enter x and y separated by space and points seperated by line: ")
    for _ in range(n):
        x, y = map(int, input().split())
        points.append((x, y))

    tree = RangeTree2D(points)

    queries = []
    n = int(input("Enter number of queries: "))
    print("Enter query as four integers and line seperated: ")
    for _ in range(n):
        x1, x2, y1, y2 = map(int, input().split())
        queries.append((x1, x2, y1, y2))

    for x1, x2, y1, y2 in queries:
        query_rect = (x1, x2, y1, y2)
        result = tree.query(x1, x2, y1, y2)
        print(f"Query x:[{x1},{x2}], y:[{y1},{y2}] → {result}")
        visualize_range_query(points, query_rect, result)
