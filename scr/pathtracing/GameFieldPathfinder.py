from pathlib import Path
import pygame

from pathtracing.Pathfinder import PathFinder
from pathtracing.Grid import Grid

class GameFieldPathfinder(PathFinder):
    def __init__(self, mapName: str):
        WINDOW_WIDTH: int = 1500
        GRID_SIZE: int = 100
        
        pygame.init()
        gameMap = pygame.image.load(Path("scr", "assets", "gamefields", f"{mapName}-gamefield.jpeg"))
        window = pygame.display.set_mode(pygame.transform.scale_by(gameMap, WINDOW_WIDTH / gameMap.width).size)
        pygame.display.set_caption(f"{mapName.capitalize()} Gamefield Pathfinding")
    
        grid = Grid(GRID_SIZE, round((window.get_height() / window.get_width()) * 100), window.size, 
                    background = gameMap, 
                    nodeAlpha = 100)
        super().__init__(grid, window)
        
        
if __name__ == "__main__":
    pathfinder = GameFieldPathfinder("unearthed")
    pathfinder.run()