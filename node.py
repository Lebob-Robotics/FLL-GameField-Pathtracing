import pygame

flags = {
    'open': 'white',
    'closed': 'red',
    'barrier': 'black',
    'origin': 'orange',
    'destination': 'aquamarine4'
}

class Node:
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col

        self.width = width // total_rows
        self.total_rows = total_rows

        # positioning on 2D plane
        self.x = row * self.width
        self.y = col * self.width

        # node state
        self.colour = flags['open']
        self.flag = 'open'

        # algorithm related
        self.neighbours = []
        self.g_score = float('inf')
        self.h_score = float('inf')
        self.f_score = self.g_score + self.h_score

    # state management
    def is_state(self, state):
        return self.flag == state

    def set_state(self, state):
        self.flag = state
        self.colour = flags[state]

    def reset_state(self):
        self.set_state('open')

    def draw(self, surf):
        pygame.draw.rect(surf, self.colour, (self.x, self.y, self.width, self.width))

    def update_neighbours(self, grid):
        self.neighbours = []
        if self.row > 0 and not grid[self.row - 1][self.col].is_state('barrier'): # check up
            self.neighbours.append(grid[self.row - 1][self.col])
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_state('barrier'): # check down
            self.neighbours.append(grid[self.row + 1][self.col])
        if self.col > 0 and not grid[self.row][self.col - 1].is_state('barrier'): # check left
            self.neighbours.append(grid[self.row][self.col - 1])
        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_state('barrier'): # check right
            self.neighbours.append(grid[self.row][self.col + 1])

    # comparing nodes
    def __lt__(self, other):
        return False