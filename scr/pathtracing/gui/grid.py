import pygame
import math

from scr.pathtracing.gui.node import Node

class Grid:
    def __init__(self, rows, cols, width):
        # list comprehension to create grid
        self.grid = [[Node(row, col, width, rows) for row in range(rows)] for col in range(cols)]

        # store dimensions
        self.width = width # window width
        self.space = width // rows # space between nodes
        self.rows = rows
        self.cols = cols

        # list of valid neighbours for each node with their relative positions
        self.adjacent_neighbours = ((-1, 0), (0, 1), (1, 0), (0, -1))
        self.diagonal_neighbours = ((-1, -1), (-1, 1), (1, 1), (1, -1))
        self.diagonal_weight = math.sqrt(2) # weight for diagonal movement

    def draw(self, surf):
        surf.fill('white')
        for col in self:
            for node in col:
                node.draw(surf)

        # draw grid lines
        for i in range(self.rows):
            pygame.draw.line(surf, 'grey', (0, i * self.space), (self.width, i * self.space))
            for j in range(self.cols):
                pygame.draw.line(surf, 'grey', (j * self.space, 0), (j * self.space, self.width))

    def get_mouse_node(self, pos):
        row = pos[1] // self.space
        col = pos[0] // self.space
        return self[col][row]

    # check if position is within grid bounds
    def within_bounds(self, col, row):
        return 0 <= row < self.rows and 0 <= col < self.cols

    def update_neighbours(self):
        for col in self:
            for node in col:
                node.update_neighbours(self)

    def update_heuristics(self, end):
        for col in self:
            for node in col:
                node.h = self.heuristic(node, end)

    def __getitem__(self, key):
        return self.grid[key]

    @staticmethod
    def heuristic(node1, node2):
        return math.dist((node1.col, node1.row), (node2.col, node2.row))