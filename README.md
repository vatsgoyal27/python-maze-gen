# Maze Generator Visualizer (WIP)

A **visual maze generation tool** using `pygame` in Python, featuring **different algorithms**:  
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
generator = hak_gen(maze_grid, ROWS, COLS, 0, 0, ROWS-1, COLS-1)
```

Available options:
```python
dfs_gen, hak_gen, prims_gen
```

Just replace `hak_gen` as required

---

## Configuration

You can tweak parameters like resolution and cell size at the top of `main.py`:

```python
WIDTH, HEIGHT = 800, 800
CELL_SIZE = 20
FPS = 60
```

---

