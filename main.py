import pygame
import grid
from mazemakers import MazeGeneratorDFS as dfs_gen, MazeGeneratorPrims as prims_gen, MazeGeneratorHuntAndKill as hak_gen, MazeGeneratorBinaryTree as btree_gen

WIDTH, HEIGHT = 800, 800
CELL_SIZE = 20
ROWS, COLS = WIDTH // CELL_SIZE, HEIGHT // CELL_SIZE
FPS = 60

pygame.init()
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Maze Generator')
clock = pygame.time.Clock()

maze_grid = grid.create_grid(ROWS, COLS, CELL_SIZE)
generator = btree_gen(maze_grid, ROWS, COLS, 0, 0, ROWS-1, COLS-1)

running = True
making_maze = True
while running:
    clock.tick(FPS)
    WIN.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Draw each iteration of the grid
    for row in maze_grid:
        for cell in row:
            cell.draw(WIN)

    if making_maze:
        pygame.draw.rect(WIN, (200, 0, 0), (generator.current.x - CELL_SIZE // 2, generator.current.y - CELL_SIZE // 2, CELL_SIZE, CELL_SIZE))
        making_maze = generator.step()
        # draw each update
        if not making_maze:
            generator.start.set_as_start()
            generator.end.set_as_end()
    else:

        # Maze is done; wait for quit event
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
    pygame.display.flip()

pygame.quit()

