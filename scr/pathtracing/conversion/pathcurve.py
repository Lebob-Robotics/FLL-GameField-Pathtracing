import math

from pathtracing.conversion.arc import Arc

class Path:
    def __init__(self, *points: tuple[int, int]):
        self.points = points
        self.arcs = self.find_segments()
        
    def get_arc(self, id: int):
        return self.arcs[id]
    
    def find_segments(self):
        arcs: list[list[tuple[float, float]]] = []
        index, arc_index, last_direction = 0, 0, 0
        while index <= len(self.points):
            point = self.points[index]
            next = self.points[index + 1]
            if Path.has_changed_direction(last_direction, point, next):
                last_direction = Path.direction(point, next)
                arcs[arc_index].append(point)
                
            if len(arcs[arc_index]) == 3:
                arc_index += 1
            index += 1
        return [Arc(*arc) for arc in arcs]
    
    @staticmethod
    def direction(p1: tuple[float, float], p2: tuple[float, float]):
        return math.atan2(p2[1] - p1[1],  p2[0] - p1[0])
    
    @staticmethod
    def has_changed_direction(last_dir: float, p1: tuple[float, float], p2: tuple[float, float]):
        if Path.direction(p1, p2) != last_dir:
            return True
        return False