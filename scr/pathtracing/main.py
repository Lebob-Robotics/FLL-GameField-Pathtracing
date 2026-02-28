import pygame

import pathtracing.gui as gui
from pathtracing.gamefieldpathfinder import GameFieldPathfinder

class Main:
    def __init__(self):
        pygame.init()
        self.pathfinder: GameFieldPathfinder = GameFieldPathfinder("unearthed")
        
        self.guiIcons: dict[str, pygame.Surface] = gui.FileUtility.import_folder_dict("scr", "assets", "gui")
        self.guiGroup: pygame.sprite.Group = pygame.sprite.Group()
        
        self.saveButton: gui.Button = gui.Button((30, 30), 'grey', 
                                                 icon = self.guiIcons["saveIcon"], 
                                                 groups = [self.guiGroup])
        
if __name__ == '__main__':
    program = Main()