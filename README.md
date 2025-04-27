# 2D Range Tree Visualizer (Static and Dynamic)

## Concept

This project implements two types of 2D Range Trees:
- **Static 2D Range Tree**: A pre-built tree structure allowing fast orthogonal range queries on a static set of points. No insertions or deletions are allowed after construction.
- **Dynamic 2D Range Tree**: A segment-tree-based structure that supports dynamic point insertions, deletions, and live range queries.

Both structures aim to optimize 2D rectangular range queries, where the goal is to retrieve all points lying inside a given query rectangle.

---

## Time Complexities

### Static 2D Range Tree
- **Build Time:** $O(n \log n)$
- **Query Time:** $O(\log^2 n + k)$, where $k$ = number of points reported
- **Space Complexity:** $O(n \log n)$

### Dynamic 2D Range Tree
- **Insertion Time:** $O(\log x_{max} \times \log n)$
- **Deletion Time:** $O(\log x_{max} \times \log n)$
- **Query Time:** $O(\log x_{max} \times \log n + k)$
- **Space Complexity:** $O(n \log x_{max})$

---

## Data Structures Used

- **Static Range Tree**
  - Binary tree based on x-coordinates.
  - Each node maintains a list sorted by y-coordinates.
  
- **Dynamic Range Tree**
  - Segment tree structure over x-axis ranges.
  - Each node stores:
    - Sorted list of y-values.
    - List of points inside the range.
  - Manual binary search is used for efficient insertions, deletions, and queries.

---

## How to Run

1. Ensure you have `python3` installed on your system.

2. Open your terminal.

3. Give execute permission to the `test.sh` file (if not already):

```bash
chmod +x test.sh
./test.sh


