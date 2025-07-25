import random
from operator import truediv


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

class MazeGeneratorSidewinder:
    def __init__(self, grid, rows, cols, xs, ys, xe, ye):
        self.grid = grid
        self.rows = rows
        self.cols = cols
        self.start = grid[xs][ys]
        self.end = grid[xe][ye]
        self.current = self.start
        self.current.finalized = True

        self.atrow = 0
        self.atcol = 0
        self.run = []

    def step(self):
        if self.atrow == 0:
            if self.atcol < self.cols - 1:
                current = self.grid[0][self.atcol]
                right = self.grid[0][self.atcol + 1]
                right.finalized = True
                remove_walls(current, right)
                self.atcol += 1
                self.current = right
                return True
            elif self.atcol == self.cols - 1:
                self.atrow += 1
                self.atcol = 0
                self.current = self.grid[self.atrow][self.atcol]
                self.current.processing = True
                self.run.append(self.current)
                return True
        else:
            if self.atcol < self.cols - 1:
                ch = random.choice([0, 1])
                if ch == 0:
                    self.atcol += 1
                    next_cell = self.grid[self.atrow][self.atcol]
                    remove_walls(self.current, next_cell)
                    next_cell.processing = True
                    self.run.append(next_cell)
                    self.current = self.grid[self.atrow][self.atcol]
                    return True
                else:
                    temp = random.choice(self.run)
                    up_cell = self.grid[temp.row-1][temp.col]
                    remove_walls(temp, up_cell)
                    for cell in self.run:
                        cell.processing = False
                        cell.finalized = True
                    self.run.clear()
                    self.atcol += 1
                    self.current = self.grid[self.atrow][self.atcol]
                    self.current.processing = True
                    self.run.append(self.current)
                    return True
            elif self.atcol == self.cols - 1:
                temp = random.choice(self.run)
                up_cell = self.grid[temp.row-1][temp.col]
                remove_walls(temp, up_cell)
                for cell in self.run:
                    cell.processing = False
                    cell.finalized = True
                self.run.clear()
                self.atcol = 0
                self.atrow += 1
                if self.atrow == self.rows:
                    return False
                self.current = self.grid[self.atrow][self.atcol]
                self.current.processing = True
                self.run.append(self.current)
                return True
        return False

class MazeGeneratorKruskal:
    def __init__(self, grid, rows, cols, xs, ys, xe, ye):
        self.grid = grid
        self.rows = rows
        self.cols = cols
        self.start = grid[xs][ys]
        self.end = grid[xe][ye]
        self.current = self.start

        self.regions = [[r * cols + c for c in range(cols)] for r in range(rows)]
        self.edges = []

        for r in range(rows):
            for c in range(cols):
                if r + 1 < rows:
                    self.edges.append(((r, c), (r + 1, c)))
                if c + 1 < cols:
                    self.edges.append(((r, c), (r, c + 1)))

        random.shuffle(self.edges)
        self.index = 0

    def merge_regions(self, old_id, new_id):
        for r in range(self.rows):
            for c in range(self.cols):
                if self.regions[r][c] == old_id:
                    self.regions[r][c] = new_id

    def step(self):
        if self.index >= len(self.edges):
            return False

        (r1, c1), (r2, c2) = self.edges[self.index]
        self.index += 1

        reg1 = self.regions[r1][c1]
        self.current = self.grid[r1][c1]
        reg2 = self.regions[r2][c2]

        if reg1 != reg2:
            self.grid[r1][c1].finalized = True
            self.grid[r2][c2].finalized = True
            remove_walls(self.grid[r1][c1], self.grid[r2][c2])
            self.merge_regions(reg2, reg1)

        return True

class MazeGeneratorGrowingTree:
    def __init__(self, grid, rows, cols, xs, ys, xe, ye):
        self.grid = grid
        self.rows = rows
        self.cols = cols
        self.start = grid[xs][ys]
        self.end = grid[xe][ye]
        self.current = self.start
        self.count = 0

        self.active = [self.start]
        self.start.processing = True
        self.max_grow = 10  # how many neighbors to consider before fallback

    def get_unvisited_neighbors(self, cell):
        neighbors = []
        r, c = cell.row, cell.col
        directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if 0 <= nr < self.rows and 0 <= nc < self.cols:
                neighbor = self.grid[nr][nc]
                if not neighbor.finalized and not neighbor.processing:
                    neighbors.append(neighbor)
        return neighbors

    def step(self):
        if not self.active:
            return False
        if self.count < self.max_grow:
            neighbors = self.get_unvisited_neighbors(self.current)
            if neighbors:
                next_cell = random.choice(neighbors)
                remove_walls(self.current, next_cell)
                next_cell.processing = True
                self.active.append(next_cell)
                self.current = next_cell
                self.count += 1
                return True
            else:
                # dead end, remove from active list
                if self.current in self.active:
                    self.active.remove(self.current)
                    self.current.processing = False
                    self.current.finalized = True
                self.count = self.max_grow
                return True
        else:
            # Fallback: pick another active cell
            if self.active:
                # modify this logic to change how the maze is generated
                self.current = random.choice(self.active)
                self.count = 0
                return True
            return False

class MazeGeneratorWilson:
    def __init__(self, grid, rows, cols, xs, ys, xe, ye):
        self.grid = grid
        self.rows = rows
        self.cols = cols
        self.start = grid[xs][ys]
        self.end = grid[xe][ye]
        self.current = self.start
        self.not_maze = [cell for row in grid for cell in row]
        self.path = []

        #set first cell of maze
        first = random.choice(self.not_maze)
        first.finalized = True
        self.not_maze.remove(first)

        #set new cell to begin random walk
        self.current = random.choice(self.not_maze)
        self.prev = self.current
        self.current.processing = True
        self.path.append(self.current)

    def get_neighbors(self, cell, prev_cell):
        neighbors = []
        r, c = cell.row, cell.col
        directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]  # top, right, bottom, left
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if 0 <= nr < self.rows and 0 <= nc < self.cols:
                neighbor = self.grid[nr][nc]

                # Uncomment below line to skip the immediate backtrack:
                if neighbor == prev_cell: continue

                neighbors.append(neighbor)
        return neighbors

    def step(self):
        if not self.not_maze:
            return False
        neighbors = self.get_neighbors(self.current, self.prev)
        next_cell = random.choice(neighbors)
        if next_cell.finalized:
            remove_walls(self.current, next_cell)
            while len(self.path) > 1:
                latter = self.path.pop()
                former = self.path[-1]
                remove_walls(latter, former)
                latter.processing = False
                latter.finalized = True
                if latter in self.not_maze:
                    self.not_maze.remove(latter)
            # Finalize the last remaining cell
            last = self.path.pop()
            last.processing = False
            last.finalized = True
            self.not_maze.remove(last)

            if not self.not_maze:
                return False
            self.current = random.choice(self.not_maze)
            self.prev = self.current
            self.current.processing = True
            self.path.append(self.current)
            return True
        elif next_cell.processing:
            while next_cell != self.path[-1]:
                self.path[-1].processing = False
                self.path.pop()
            self.current = next_cell
            self.prev = self.current
            return True
        else:
            self.prev = self.current
            self.current = next_cell
            self.path.append(self.current)
            self.current.processing = True
            return True

class MazeGeneratorAldousBroder:
    def __init__(self, grid, rows, cols, xs, ys, xe, ye):
        self.grid = grid
        self.rows = rows
        self.cols = cols
        self.start = grid[xs][ys]
        self.end = grid[xe][ye]
        self.total_cells = self.rows * self.cols

        self.current = self.start
        self.current.finalized = True
        self.visited_count = 1

    def get_neighbors(self, cell):
        r, c = cell.row, cell.col
        directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]  # N, E, S, W
        neighbors = []
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if 0 <= nr < self.rows and 0 <= nc < self.cols:
                neighbors.append(self.grid[nr][nc])
        return neighbors

    def step(self):
        if self.visited_count >= self.total_cells:
            return False

        neighbors = self.get_neighbors(self.current)
        next_cell = random.choice(neighbors)

        if not next_cell.finalized:
            remove_walls(self.current, next_cell)
            next_cell.finalized = True
            self.visited_count += 1

        self.current = next_cell
        return True



