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
        
    neighbourNodes: tuple = ((-1.0, -1.0, 2.0), (-1.0, 0.0, 1.0), (-1.0, 1.0, 2.0),
                             (0.0, -1.0, 1.0)                   , (0.0, 1.0, 1.0),
                             (1.0, -1.0, 2.0),  (1.0, 0.0, 1.0) , (1.0, 1.0, 2.0))
    
    def __init__(self, x: int, y: int, length: float, width: float = 0, flag = Flags.EMPTY):
        self.x: int = x
        self.y: int = y
        self.length: float = length
        self.width: float = width if width else length
        self.flag = flag
        
        self.successor: None | Node = None
        self.neighbours: list[tuple[tuple[int, int], float]] = [((0, 0), 0)]
        self.f: float = inf
        self.g: float = inf
        self.h: float = inf
    
    def setFlag(self, flag: Flags):
        self.flag = flag
        
    def getFlag(self):
        return self.flag
    
    def isFlag(self, flag: Flags):
        return self.flag == flag
    
    def setHeuristic(self, other):
        self.h = abs(self.x - other.x) ** 2 + abs(self.y - other.y) ** 2
        
    def findNeighbours(self, gridSize: tuple[int, int]):
        self.neighbours = []
        for x, y, weight in Node.neighbourNodes:
            if not (self.x + x >= 0 and self.x + x < gridSize[0]):
                continue
            if not (self.y + y >= 0 and self.y + y < gridSize[1]):
                continue
            
            self.neighbours.append(((self.x + x, self.y + y), weight))
    
    def updateFScore(self):
        self.f = self.g + self.h