import random

def remove_walls(a, b):
    dx = a.col - b.col
    dy = a.row - b.row

    if dx == 1:
        a.walls['left'] = False
        b.walls['right'] = False
    elif dx == -1:
        a.walls['right'] = False
        b.walls['left'] = False
    if dy == 1:
        a.walls['top'] = False
        b.walls['bottom'] = False
    elif dy == -1:
        a.walls['bottom'] = False
        b.walls['top'] = False

class MazeGeneratorDFS:
    def __init__(self, grid, rows, cols, xs, ys, xe, ye):
        self.grid = grid
        self.rows = rows
        self.cols = cols
        self.start = grid[xs][ys]
        self.end = grid[xe][ye]
        self.current = self.start
        self.stack = []

    def get_neighbors(self, cell):
        neighbors = []
        r, c = cell.row, cell.col
        dirs = [(-1, 0), (0, 1), (1, 0), (0, -1)]
        # top, right, bottom, left

        for dr, dc in dirs:
            nr, nc = r + dr, c + dc
            if 0 <= nr < self.rows and 0 <= nc < self.cols:
                neighbor = self.grid[nr][nc]
                if not neighbor.finalized:
                    neighbors.append(neighbor)
        return neighbors

    def step(self):
        self.current.finalized = True
        neighbors = self.get_neighbors(self.current)

        if neighbors:
            next_cell = random.choice(neighbors)
            self.stack.append(self.current)
            self.current.processing = True
            remove_walls(self.current, next_cell)
            self.current = next_cell
            return True
        elif self.stack:
            popped = self.stack.pop()
            popped.processing = False
            self.current = popped
            return True
        else:
            return False

class MazeGeneratorPrims:
    def __init__(self, grid, rows, cols, xs, ys, xe, ye):
        self.grid = grid
        self.rows = rows
        self.cols = cols
        self.start = grid[xs][ys]
        self.end = grid[xe][ye]
        self.frontier = []
        self.current = self.start

        self.start.finalized = True
        self.add_frontier(self.start)

    def add_frontier(self, cell):
        r, c = cell.row, cell.col
        directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if 0 <= nr < self.rows and 0 <= nc < self.cols:
                neighbor = self.grid[nr][nc]
                if not neighbor.finalized and neighbor not in self.frontier:
                    neighbor.processing = True
                    self.frontier.append(neighbor)

    def get_finalized_neighbors(self, cell):
        r, c = cell.row, cell.col
        neighbors = []
        directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if 0 <= nr < self.rows and 0 <= nc < self.cols:
                neighbor = self.grid[nr][nc]
                if neighbor.finalized:
                    neighbors.append(neighbor)
        return neighbors

    def step(self):
        if not self.frontier:
            return False

        cell = random.choice(self.frontier)
        self.current = cell
        finalized_neighbors = self.get_finalized_neighbors(cell)

        if finalized_neighbors:
            neighbor = random.choice(finalized_neighbors)
            remove_walls(cell, neighbor)
            cell.finalized = True
            self.add_frontier(cell)

        cell.processing = False
        self.frontier.remove(cell)
        return True

class MazeGeneratorHuntAndKill:
    def __init__(self, grid, rows, cols, xs, ys, xe, ye):
        self.grid = grid
        self.rows = rows
        self.cols = cols
        self.start = grid[xs][ys]
        self.end = grid[xe][ye]
        self.current = self.start
        self.mode = 'kill'

    def get_neighbors(self, cell):
        neighbors = []
        r, c = cell.row, cell.col
        directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]  # top, right, bottom, left
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if 0 <= nr < self.rows and 0 <= nc < self.cols:
                neighbor = self.grid[nr][nc]
                if not neighbor.finalized:
                    neighbors.append(neighbor)
        return neighbors


    def get_finalized_neighbors(self, cell):
        neighbors = []
        r, c = cell.row, cell.col
        directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]  # top, right, bottom, left
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if 0 <= nr < self.rows and 0 <= nc < self.cols:
                neighbor = self.grid[nr][nc]
                if neighbor.finalized:
                    neighbors.append(neighbor)
        return neighbors

    def step(self):
        self.current.finalized = True
        if self.mode == 'kill':
            neighbors = self.get_neighbors(self.current)
            self.current.processing = True
            if neighbors:
                next_cell = random.choice(neighbors)
                remove_walls(self.current, next_cell)
                self.current = next_cell
                return True
            else:
                self.mode = 'hunt'
                return True

        elif self.mode == 'hunt':
            for r in range(self.rows):
                for c in range(self.cols):
                    cell = self.grid[r][c]
                    cell.processing = False
                    if not cell.finalized:
                        finalized_neighbors = self.get_finalized_neighbors(cell)
                        if finalized_neighbors:
                            neighbor = random.choice(finalized_neighbors)
                            remove_walls(cell, neighbor)
                            cell.finalized = True
                            self.current = cell
                            self.mode = 'kill'
                            return True
            return False
        return False

