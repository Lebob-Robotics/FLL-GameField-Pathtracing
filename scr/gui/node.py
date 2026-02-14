import pygame

flags = {
    'unchecked': 'white',
    'checking': 'blue',
    'open': 'green',
    'closed': 'red',
    'barrier': 'black',
    'origin': 'orange',
    'destination': 'aquamarine4',
    'path': 'purple'
}

class Node:
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col

        self.width = width // total_rows
        self.total_rows = total_rows

        # positioning on 2D plane
        self.x = col * self.width
        self.y = row * self.width

        # node state
        self.colour = flags['unchecked']
        self.flag = 'unchecked'

        # algorithm related
        self.neighbours = [] # 2D list of adjacent nodes with their respective weights
        self.g = float('inf')
        self.h = float('inf')
        self.f = self.g + self.h

    # state management
    def is_state(self, state):
        return self.flag == state

    def set_state(self, state):
        self.flag = state
        self.colour = flags[state]

    def reset_state(self):
        self.set_state('unchecked')

    def draw(self, surf):
        pygame.draw.rect(surf, self.colour, (self.x, self.y, self.width, self.width))

    def update_neighbours(self, grid):
        self.neighbours = []
        for neighbour in grid.adjacent_neighbours:
            col, row = self.col + neighbour[0], self.row + neighbour[1]
            if grid.within_bounds(col, row) and not grid[col][row].is_state('barrier'):
                self.neighbours.append([grid[col][row], 1]) # where second value is weight

        for neighbour in grid.diagonal_neighbours:
            col, row = self.col + neighbour[0], self.row + neighbour[1]
            if grid.within_bounds(col, row) and not grid[col][row].is_state('barrier'):
                self.neighbours.append([grid[col][row], grid.diagonal_weight])