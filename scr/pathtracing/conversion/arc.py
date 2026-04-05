import pygame
import math

from pathtracing.astar.grid import Grid
from pathtracing.conversion.line import Line

class Arc:
    def __init__(self, p1, p2, p3):
        self.start: tuple[float, float] = p1
        self.midpoint: tuple[float, float] = p2
        self.end: tuple[float, float] = p3
        self.centre: tuple[float, float] = (0, 0)
        
        self.radius: float = self.calculate_radius()
        self.angle: float = self.calculate_angle()
        
    def calculate_radius(self):
        l1 = Line(self.start, self.midpoint).get_perpendicular_bisector()
        l2 = Line(self.midpoint, self.end).get_perpendicular_bisector()
        self.centre = Line.line_intersection(l1, l2)
        return sum((math.dist(self.start, self.centre), math.dist(self.end, self.centre))) / 2

    def calculate_angle(self):
        return math.acos((2 * self.radius**2 - math.dist(self.start, self.end)**2) / (4 * self.radius**2))
    
    def draw(self, surface, grid: Grid):
        pygame.draw.circle(surface, "blue", grid.convert_coords(self.centre), self.radius * grid.node_size[0], 5)
    
    