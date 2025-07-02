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

def add_walls(a, b):
    dx = a.col - b.col
    dy = a.row - b.row

    if dx == 1:
        a.walls['left'] = True
        b.walls['right'] = True
    elif dx == -1:
        a.walls['right'] = True
        b.walls['left'] = True
    if dy == 1:
        a.walls['top'] = True
        b.walls['bottom'] = True
    elif dy == -1:
        a.walls['bottom'] = True
        b.walls['top'] = True

def check_wall(a, b):
    dx = a.col - b.col
    dy = a.row - b.row

    if dx == 1:
        return a.walls['left'] and b.walls['right']
    elif dx == -1:
        return a.walls['right'] and b.walls['left']
    elif dy == 1:
        return a.walls['top'] and b.walls['bottom']
    elif dy == -1:
        return a.walls['bottom'] and b.walls['top']
    else:
        raise ValueError("Cells are not adjacent.")


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

class MazeGeneratorBinaryTree:
    def __init__(self, grid, rows, cols, xs, ys, xe, ye):
        self.grid = grid
        self.rows = rows
        self.cols = cols
        self.start = grid[xs][ys]
        self.end = grid[xe][ye]
        self.current = grid[0][0]
        self.done = False

    def step(self):
        if self.done:
            return False

        self.current.finalized = True
        r, c = self.current.row, self.current.col

        neighbors = []
        if r > 0:
            neighbors.append(self.grid[r - 1][c])  # north
        if c < self.cols - 1:
            neighbors.append(self.grid[r][c + 1])  # east

        if neighbors:
            neighbor = random.choice(neighbors)
            remove_walls(self.current, neighbor)
            neighbor.finalized = True

        # Move to next cell in row-major order
        if c < self.cols - 1:
            self.current = self.grid[r][c + 1]
        elif r < self.rows - 1:
            self.current = self.grid[r + 1][0]
        else:
            self.done = True
            return False

        return True

class MazeGeneratorOriginShift:
    def __init__(self, grid, rows, cols, xs, ys, xe, ye):
        self.grid = grid
        self.rows = rows
        self.cols = cols
        self.start = grid[xs][ys]
        self.end = grid[xe][ye]
        self.current = self.start
        self.point_mat = [["" for _ in range(len(self.grid[0]))] for _ in range(len(self.grid))]

        # initialize a "perfect maze", create the "tree"
        for col in range(self.cols):
            for row in range(self.rows - 1):
                current = self.grid[row][col]
                below = self.grid[row + 1][col]
                self.arrow(current, below)
                remove_walls(current, below)

        for c in range(self.cols - 1, 0, -1):
            current = self.grid[self.rows - 1][c]
            left = self.grid[self.rows - 1][c - 1]
            self.arrow(current, left)
            remove_walls(current, left)
        self.current = self.grid[self.rows - 1][0]

    def arrow(self, a, b):
        if a.row == b.row and a.col == b.col:
            self.point_mat[a.row][a.col] = ""
            return

        dr = b.row - a.row
        dc = b.col - a.col

        if dr == -1:
            self.point_mat[a.row][a.col] = "up"
        elif dr == 1:
            self.point_mat[a.row][a.col] = "down"
        elif dc == -1:
            self.point_mat[a.row][a.col] = "left"
        elif dc == 1:
            self.point_mat[a.row][a.col] = "right"

    def get_neighbors(self, cell):
        neighbors = []
        r, c = cell.row, cell.col
        directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]  # top, right, bottom, left
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if 0 <= nr < self.rows and 0 <= nc < self.cols:
                neighbor = self.grid[nr][nc]
                neighbors.append(neighbor)
        return neighbors

    def add_wall_from_arrow(self, cell):
        direction = self.point_mat[cell.row][cell.col]

        if direction == "up" and cell.row > 0:
            neighbor = self.grid[cell.row - 1][cell.col]
            add_walls(cell, neighbor)

        elif direction == "down" and cell.row < self.rows - 1:
            neighbor = self.grid[cell.row + 1][cell.col]
            add_walls(cell, neighbor)

        elif direction == "left" and cell.col > 0:
            neighbor = self.grid[cell.row][cell.col - 1]
            add_walls(cell, neighbor)

        elif direction == "right" and cell.col < self.cols - 1:
            neighbor = self.grid[cell.row][cell.col + 1]
            add_walls(cell, neighbor)

    def step(self):
        neighbors = self.get_neighbors(self.current)
        unvisited = [n for n in neighbors if not n.finalized]
        visited = [n for n in neighbors if n.finalized]
        candidates = unvisited if unvisited else visited
        next_cell = random.choice(candidates)

        check_wall(self.current, next_cell)
        if check_wall(self.current, next_cell):
            # build a new bridge
            remove_walls(self.current, next_cell)
            self.arrow(self.current, next_cell)
            # delete an old one
            self.add_wall_from_arrow(next_cell)
            self.arrow(next_cell, next_cell)
            self.current = next_cell
        else:
            # replace a bridge in the opposite direction
            self.arrow(self.current, next_cell)
            self.arrow(next_cell, next_cell)
            self.current = next_cell
        self.current.finalized = True
        return True


