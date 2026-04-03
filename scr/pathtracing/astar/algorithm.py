from queue import PriorityQueue

from pathtracing.astar.node import Node
from pathtracing.astar.grid import Grid

class Algorithm:
    def __init__(self, grid: Grid, started: bool = False):
        self.grid: Grid = grid
        self.started: bool = started
        self.found_path: bool = False
        
        self.grid.update_nodes()
        self.grid.start_node.g = 0
        self.grid.start_node.update_fscore()

        self.search_index = 0
        self.open_set: PriorityQueue[tuple[float, int, Node]] = PriorityQueue()
        self.open_set.put((0, self.search_index, self.grid.start_node))
        self.closed_set = set([self.grid.start_node])
        
    def step(self):
        f_score, index, node = self.open_set.get()
        if node != self.grid.start_node and node != self.grid.endNode:
            node.set_flag(Node.Flags.CLOSED)

        if node == self.grid.endNode:
            self.started = False
            self.found_path = True

        for pos, weight in node.neighbours:
            neighbour: Node = self.grid.get_item_by_array(pos)
            if neighbour.isFlag(Node.Flags.BARRIER):
                continue
            
            gScore = node.g + weight
            if gScore < neighbour.g:
                neighbour.g = node.g + weight
                neighbour.update_fscore()

                if neighbour not in self.closed_set:
                    self.search_index += 1
                    self.open_set.put((neighbour.f, self.search_index, neighbour))
                    self.closed_set.add(neighbour)
                    neighbour.set_flag(Node.Flags.OPEN) if neighbour != self.grid.endNode else neighbour.set_flag(Node.Flags.DESTINATION)
                    
        if self.open_set.qsize() == 0:
            self.started = False
            self.found_path = False
