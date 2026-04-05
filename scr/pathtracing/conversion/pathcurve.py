import math

from pathtracing.conversion.arc import Arc
from pathtracing.conversion.line import Line

class PathCurve:
    def __init__(self, *points: tuple[float, float], end_pos: tuple[float, float], jaggedness: float = 1, max_length: float = 5):
        self.points = tuple(reversed(points))
        self.jaggedness = jaggedness
        self.max_length = max_length
        self.end_pos = end_pos
        
        self.path: list[Line | Arc] = []
        self.path = self.find_arcs()

    def find_arcs(self):
        path: list[Line | Arc] = []
        arc_points: list[tuple[float, float]] = []
        last_direction = 999
        
        index = 0
        point, next = self.points[index], self.points[index + 1]
        while True:
            point = self.points[index]
            next = self.points[index + 1]
            index += 1
            
            if PathCurve.has_changed_direction(last_direction, point, next):
                last_direction = PathCurve.direction(point, next)
                arc_points.append(point)
                
            jagged = False
            if len(arc_points) == 3:
                jagged = abs(math.dist(arc_points[0], arc_points[1]) - 
                             math.dist(arc_points[1], arc_points[2])) > self.jaggedness
                
            if len(arc_points) <= 1:
                continue
            exceeds_length: bool = math.dist(arc_points[-1], arc_points[-2]) > self.max_length
                
            if jagged or exceeds_length:
                path = self.arc_points_to_line(path, arc_points)
                
            if len(arc_points) == 3 or exceeds_length:
                if not (jagged or exceeds_length):
                    path.append(Arc(*arc_points))
                arc_points = [arc_points[-1]]
                
            if next == self.end_pos:
                arc_points.append(next)
                break
                
        path = self.arc_points_to_line(path, arc_points)
        return path
    
    @staticmethod
    def arc_points_to_line(path, points: list[tuple[float, float]]):
        for i in range(len(points) - 1):
            path.append(Line(points[i], points[i + 1]))
        return path
    
    @staticmethod
    def direction(p1: tuple[float, float], p2: tuple[float, float]):
        return math.atan2(p2[1] - p1[1],  p2[0] - p1[0])
    
    @staticmethod
    def has_changed_direction(last_dir: float, p1: tuple[float, float], p2: tuple[float, float]):
        if PathCurve.direction(p1, p2) != last_dir:
            return True
        return False
    
    def __getitem__(self, key):
        return self.path[key]