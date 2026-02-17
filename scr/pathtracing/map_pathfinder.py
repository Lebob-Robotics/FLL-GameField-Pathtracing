from scr.pathtracing.pathfinding.grid import Grid
from scr.pathtracing.pathfinding.pathfinder import PathTracer

class MapPathTracer(PathTracer):
    def __init__(self, grid: Grid):
        super().__init__(grid)
        
    def run(self):
        pass
        