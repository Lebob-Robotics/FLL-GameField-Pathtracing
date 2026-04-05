import math

from pathtracing.conversion.arc import Arc

class PathCurve:
    def __init__(self, *points: tuple[float, float]):
        self.points = tuple(reversed(points))
        self.arcs = self.find_arcs()
        
    def get_arc(self, id: int):
        return self.arcs[id]
    
    def find_arcs(self):
        arcs: list[list[tuple[float, float]]] = [[]]
        last_direction = 999
        
        for index in range(len(self.points) - 1):
            point = self.points[index]
            next = self.points[index + 1]
            if PathCurve.has_changed_direction(last_direction, point, next):
                last_direction = PathCurve.direction(point, next)
                arcs[-1].append(point) 
                
            if len(arcs[-1]) == 3:
                arcs.append([])
                
        arcs.pop()
        print([Arc(*arc) for arc in arcs])
        return [Arc(*arc) for arc in arcs]
    
    @staticmethod
    def direction(p1: tuple[float, float], p2: tuple[float, float]):
        return math.atan2(p2[1] - p1[1],  p2[0] - p1[0])
    
    @staticmethod
    def has_changed_direction(last_dir: float, p1: tuple[float, float], p2: tuple[float, float]):
        if PathCurve.direction(p1, p2) != last_dir:
            return True
        return False