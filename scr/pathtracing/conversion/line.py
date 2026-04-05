import pygame

class Line:
    VERTICAL_GRADIENT = 999999
    
    def __init__(self, p1: tuple[float, float], p2: tuple[float, float]):
        self.p1 = p1
        self.p2 = p2
        
        self.m = -((p1[1] - p2[1]) / (p1[0] - p2[0])) if (p1[0] - p2[0]) != 0 else -self.VERTICAL_GRADIENT
        self.y_int = p1[1] + (p1[0] * self.m)
        
    @property
    def y_intercept(self):
        return self.y_int
    
    @property
    def gradient(self):
        return self.m
        
    def get_perpendicular_bisector(self):
        midpoint = ((self.p2[0] + self.p1[0]) / 2), ((self.p2[1] + self.p1[1]) / 2)
        print(midpoint)
        gradient = 1 / self.m if self.m != 0 else self.VERTICAL_GRADIENT
        return Line(midpoint, (midpoint[0] + 1, midpoint[1] + gradient))
    
    @staticmethod
    def line_intersection(l1, l2):
        x1, y1, c1 = l1.gradient, -1, -l1.y_intercept
        x2, y2, c2 = l2.gradient, -1, -l2.y_intercept
        
        x = (y1*c2 - y2*c1) / (x1*y2 - x2*y1)
        y = (c1*x2 - c2*x1) / (x1*y2 - x2*y1)
        return (x, -y)
        