# Maze Generator Visualizer (WIP)

A **visual maze generation tool** using `pygame` in Python, **with multiple algorithms**:  
Each algorithm runs step-by-step and visualizes the maze construction live with animated updates.

---

## File Structure

```
.
├── main.py                # Main entry point; handles pygame window and maze generation loop
├── cell.py                # Defines individual maze cells (walls, colors, draw logic)
├── grid.py                # Utility to create the grid of cells
├── mazemakers.py          # Contains all maze generation algorithms and shared logic
└── README.md              # You are here
```

---

## How to Run

### Prerequisites:
- Python 3.9
- `pygame` library

Install pygame if not already installed:
```bash
pip install pygame
```

###  To Run the Visualizer:
```bash
python main.py
```

---

## Algorithms Implemented

### 1. **Depth-First Search (DFS) Maze Generator**
- Carves out a path by diving deep and backtracking.
- Stack-based approach.
- Visualization:
  - Orange cells: Currently being processed.
  - Blue fill: Finalized path.

---

### 2. **Prim's Algorithm**
- Randomly selects frontier cells and connects to an adjacent visited cell.
- Ensures uniform spread.
- Visualization:
  - Orange cells: Frontier set (border of the current maze).
  - Blue fill: Finalized path.

---

### 3. **Hunt-and-Kill Algorithm**
- Alternates between random walks ("kill mode") and scanning unvisited cells ("hunt mode").
- Quicker and easy to implement.
- Visualization:
  - Orange cells: Path during random walk.
  - Blue cells: Cells scanned during hunt.

---

### 4. **Binary tree Algorithm**
- Iterates through the entire grid.
- Is the simplest in logic, carves a path randomly north or west - that's it.
- Visualization:
  - Blue fill: Finalized path.

---

### 5. **Origin Shifter Algorithm**
- Initializes a "perfect" maze with a fully linked "tree".
- Each step shifts the “origin” by rewiring paths using directional arrows.
- If a wall exists, it removes the new wall and restores the old one.
- Visualization:
  - Blue fill: Modified cell.
  - Black fill: Unmodified cell.

---

### 6. **Sidewinder Algorithm**
- Connects entire first row.
- Processes each row, either by creating a "run" set by removing walls to the east, or by creating a connection of this "run" set to the upper row by a north passage.
- Visualization:
  - Blue fill: Finalized cell.
  - Orange fill: Cells in current "run" set.

---

### 7. **Kruskals Algorithm**
- Treats each cell as its own disjoint set.
- Processes random walls; removes them only if they connect disjoint sets.
- Ensures no cycles while creating a fully connected maze.
- Visualization:
  - Blue fill: Finalized cell.
  - Orange fill: Currently merged set.

---

### 8. **Growing Tree Algorithm**
- Starts with one cell and grows a path by choosing neighbors.
- Behavior depends on selection strategy (e.g., newest, random), backtracks via this strategy to select a new growing point when exceeding set length or when it has no valid neighbors.
- Visualization:
  - Blue fill: Finalized cell.
  - Orange fill: Actively growing cells.

---

### 9. **Wilsons Algorithm**
- Begins by selecting one random cell and marking it as part of the maze.
- Repeatedly performs a loop-erased random walk (a random walk that removes any loops it creates as it goes) from a random unvisited cell until it connects to the maze.
- On reaching the maze, the path is finalized.
- Can toggle backtrack prevention for random walk to increase generation speed
- Visualization:
  - Blue fill: Finalized cell.
  - Orange fill: Active walk path.

---

## Cell Color Codes

| Color         | Meaning                          |
|---------------|----------------------------------|
| 🟩 Green       | Start cell                        |
| 🟨 Yellow      | End cell                          |
| 🟦 Blue        | Finalized (visited) cell          |
| 🟧 Orange      | Cell currently being processed    |
| ⬛ Black       | Wall / Undiscovered               |
| ⬜ White lines | Maze cell walls                   |

---

## Customization

You can change the maze generation algorithm by modifying this line in `main.py`:

```python
generator = side_gen(maze_grid, ROWS, COLS, 0, 0, ROWS-1, COLS-1)
```

Available options:
```python
dfs_gen, hak_gen, prims_gen, btree_gen, ori_gen, side_gen, krus_gen, grow_gen, wil_gen
```

Just replace as required

---

## Configuration

You can tweak parameters like resolution and cell size at the top of `main.py`:

```python
WIDTH, HEIGHT = 800, 800
CELL_SIZE = 20
FPS = 60
```

---

