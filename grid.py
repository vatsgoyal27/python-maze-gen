from cell import Cell

def create_grid(rows, cols, cell_size):
    grid = []
    for row in range(rows):
        row_cells = []
        for col in range(cols):
            cell = Cell(row, col, cell_size)
            row_cells.append(cell)
        grid.append(row_cells)
    # print(grid)
    return grid

