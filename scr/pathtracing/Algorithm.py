from queue import PriorityQueue

from pathtracing.Node import Node
from pathtracing.Grid import Grid

class Algorithm:
    def __init__(self, grid: Grid, started: bool = False):
        self.grid: Grid = grid
        self.started: bool = started
        self.foundPath: bool = False
        
        self.grid.updateNodes()
        self.grid.startNode.g = 0
        self.grid.startNode.updateFScore()

        self.searchIndex = 0
        self.openSet: PriorityQueue[tuple[float, int, Node]] = PriorityQueue()
        self.openSet.put((0, self.searchIndex, self.grid.startNode))
        self.closedSet = set([self.grid.startNode])
        
    def step(self):
        f_score, index, node = self.openSet.get()
        if node != self.grid.startNode and node != self.grid.endNode:
            node.setFlag(Node.Flags.CLOSED)

        if node == self.grid.endNode:
            self.started = False
            self.foundPath = True

        for pos, weight in node.neighbours:
            neighbour: Node = self.grid.getItemByArray(pos)
            if neighbour.isFlag(Node.Flags.BARRIER):
                continue
            
            gScore = node.g + weight
            if gScore < neighbour.g:
                neighbour.g = node.g + weight
                neighbour.updateFScore()

                if neighbour not in self.closedSet:
                    self.searchIndex += 1
                    self.openSet.put((neighbour.f, self.searchIndex, neighbour))
                    self.closedSet.add(neighbour)
                    neighbour.setFlag(Node.Flags.OPEN) if neighbour != self.grid.endNode else neighbour.setFlag(Node.Flags.DESTINATION)
                    
        if self.openSet.qsize() == 0:
            self.started = False
            self.foundPath = False
