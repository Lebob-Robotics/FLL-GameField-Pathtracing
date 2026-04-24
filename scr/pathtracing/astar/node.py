from pygame import sprite
from math import inf
from enum import Enum

class Node(sprite.Sprite):
    class Flags(Enum):
        EMPTY = 'pink'
        UNCHECKED = 'white'
        CLOSED = 'red'
        OPEN = 'green'
        BARRIER = 'black'
        ORIGIN = 'orange'
        DESTINATION = 'turquoise3'
        PATH = 'purple'
        
    neighhour_nodes: tuple = ((-1.0, -1.0, 2.0), (-1.0, 0.0, 1.0), (-1.0, 1.0, 2.0),
                             (0.0, -1.0, 1.0)                   , (0.0, 1.0, 1.0),
                             (1.0, -1.0, 2.0),  (1.0, 0.0, 1.0) , (1.0, 1.0, 2.0))
    
    def __init__(self, x: int, y: int, length: float, width: float = 0, flag = Flags.EMPTY):
        self.x: int = x
        self.y: int = y
        self.length: float = length
        self.width: float = width if width else length
        self.flag = flag
        
        self.predeccessor: None | Node = None
        self.neighbours: list[tuple[Node, float]] = [(self, 0)]
        self.weight: float = 0
        self.f: float = inf
        self.g: float = inf
        self.h: float = inf
    
    def set_flag(self, flag: Flags):
        self.flag = flag
        
    def get_flag(self):
        return self.flag
    
    def is_flag(self, flag: Flags):
        return self.flag == flag
    
    @staticmethod
    def heuristic(this, other):
        return abs(this.x - other.x) ** 2 + abs(this.y - other.y) ** 2
    
    def set_heuristic(self, other):
        self.h = Node.heuristic(self, other)
        
    def find_neighbours(self, grid):
        self.neighbours = []
        for x, y, weight in Node.neighhour_nodes:
            if not (self.x + x >= 0 and self.x + x < grid.length):
                continue
            if not (self.y + y >= 0 and self.y + y < grid.height):
                continue
            
            neighbour = grid.get_item_by_array((self.x + x, self.y + y))
            self.neighbours.append((neighbour, weight + neighbour.weight))
    
    def update_fscore(self):
        self.f = self.g + self.h
        
    def get_pos(self):
        return self.x, self.y