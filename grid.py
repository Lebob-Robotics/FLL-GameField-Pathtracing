import pygame
from node import Node

class Grid:
    def __init__(self, rows, cols, width):
        # list comprehension to create grid
        self.grid = [[Node(j, i, width, rows) for j in range(cols)] for i in range(rows)]

        self.width = width
        self.rows = rows
        self.cols = cols
        self.space = self.width // self.rows

    def draw(self, surf):
        surf.fill('white')

        for row in self:
            for node in row:
                node.draw(surf)

        for i in range(self.rows):
            pygame.draw.line(surf, 'grey', (0, i * self.space), (self.width, i * self.space))
            for j in range(self.cols):
                pygame.draw.line(surf, 'black', (j * self.space, 0), (j * self.space, self.width))

    def get_mouse_node(self, pos):
        row = pos[1] // self.space
        col = pos[0] // self.space
        return self[row][col]

    def update(self):
        for row in self:
            for node in row:
                node.update_neighbours(self)

    def __getitem__(self, key):
        return self.grid[key]