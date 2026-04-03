import math
from pathtracing.astar.line import Line

class Arc:
    def __init__(self, p1: tuple[int, int], p2: tuple[int, int], p3: tuple[int, int]):
        self.start = p1
        self.midpoint = p2
        self.end = p3
        
        self.radius: float = self.calculate_radius()
        self.angle: float = self.calculate_angle()
        
    def calculate_radius(self):
        l1 = Line(self.start, self.midpoint).get_perpendicular_bisector()
        l2 = Line(self.midpoint, self.end).get_perpendicular_bisector()
        centre = Line.line_intersection(l1, l2)
        return math.dist(self.start, centre)

    def calculate_angle(self):
        return math.acos((2 * self.radius**2 - math.dist(self.start, self.end)**2) / (2 * self.radius**2))
    
    