import pygame

class Cell:
    def __init__(self, row, col, size):
        self.row = row
        self.col = col
        self.size = size
        self.x = int(col * size + size/2)
        self.y = int(row * size + size/2)
        self.walls = {'top': True, 'right': True, 'bottom': True, 'left': True}
        self.finalized = False
        self.is_start = False
        self.is_end = False
        self.processing = False

    def draw(self, surface, wall_color=(255, 255, 255), fill_color=(30, 144, 255)):
        half = self.size // 2
        x1, y1 = self.x - half, self.y - half  # top-left
        x2, y2 = self.x + half, self.y + half  # bottom-right

        # Fill if visited
        # Priority: Start > End > Visited
        if self.processing:
            pygame.draw.rect(surface, (255, 140, 0), (x1, y1, self.size, self.size)) # Orange
        elif self.is_start:
            pygame.draw.rect(surface, (0, 100, 0), (x1, y1, self.size, self.size))  # Green
        elif self.is_end:
            pygame.draw.rect(surface, (205, 153, 0), (x1, y1, self.size, self.size))  # Yellow
        elif self.finalized:
            pygame.draw.rect(surface, fill_color, (x1, y1, self.size, self.size))

        # Draw walls
        if self.walls['top']:
            pygame.draw.line(surface, wall_color, (x1, y1), (x2, y1), 2)
        if self.walls['right']:
            pygame.draw.line(surface, wall_color, (x2, y1), (x2, y2), 2)
        if self.walls['bottom']:
            pygame.draw.line(surface, wall_color, (x2, y2), (x1, y2), 2)
        if self.walls['left']:
            pygame.draw.line(surface, wall_color, (x1, y2), (x1, y1), 2)

    def set_as_start(self):
        self.is_start = True

    def set_as_end(self):
        self.is_end = True
