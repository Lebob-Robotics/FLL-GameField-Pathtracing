from pathlib import Path
import pygame

from pathtracing.astar.pathfinder import PathFinder
from pathtracing.astar.grid import Grid
from pathtracing.conversion.pathcurve import PathCurve

class GameFieldPathfinder(PathFinder):
    def __init__(self, mapName: str):
        WINDOW_WIDTH: int = 1500
        GRID_SIZE: int = 70
        
        gameMap = pygame.image.load(Path("scr", "assets", "gamefields", f"{mapName}-gamefield.jpeg"))
        window = pygame.display.set_mode(pygame.transform.scale_by(gameMap, WINDOW_WIDTH / gameMap.width).size)
        pygame.display.set_caption(f"{mapName.capitalize()} Gamefield Pathfinding")
    
        grid = Grid(GRID_SIZE, round((window.get_height() / window.get_width()) * GRID_SIZE), window.size, 
                    background = gameMap, 
                    node_transparency = 100)
        super().__init__(grid, window)
        self.path_curve: PathCurve = PathCurve(end_pos= self.grid.end_node.get_pos())
        self.path_calculated: bool = False
        
    def step(self):
        super().step()
        
        if self.algorithm.found_path and not self.path_calculated:
            self.path_calculated = True
            self.convert_path()
        self.draw_path()
        
    def convert_path(self):
        self.path_curve = PathCurve(*self.algorithm.path, end_pos= self.grid.end_node.get_pos(), 
                                    jaggedness= 3, max_length= 5)
        
    def draw_path(self):
        for section in self.path_curve.path:
            section.draw(self.window, self.grid)
            
        
if __name__ == "__main__":
    pygame.init()
    pathfinder = GameFieldPathfinder("unearthed")
    while True:
        pathfinder.step()
        pygame.display.update()