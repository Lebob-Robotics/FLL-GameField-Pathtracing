import pathtracing.gui
from pathtracing.gamefieldpathfinder import GameFieldPathfinder

class Main:
    def __init__(self):
        self.pathfinder: GameFieldPathfinder = GameFieldPathfinder("rebuilt")
        
        