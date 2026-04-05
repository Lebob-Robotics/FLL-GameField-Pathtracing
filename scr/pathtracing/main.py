import pygame

import pathtracing.gui as gui
from pathtracing.gamefieldpathfinder import GameFieldPathfinder

class Main:
    def __init__(self):
        pygame.init()
        self.pathfinder: GameFieldPathfinder = GameFieldPathfinder("unearthed")
        
        self.guiIcons: dict[str, pygame.Surface] = gui.FileUtility.import_folder_dict("scr", "assets", "gui")
        self.guiGroup: pygame.sprite.Group = pygame.sprite.Group()
        
        self.saveButton: gui.Button = gui.Button((60, 60), (100, 100), 'white', 
                                                 icon = self.guiIcons["saveIcon"], 
                                                 groups = [self.guiGroup])
    
        self.window: pygame.Surface = pygame.display.get_surface() # type: ignore
    
    def run(self):
        while True:
            self.pathfinder.step()
            
            self.guiGroup.update()
            self.guiGroup.draw(self.window)
            pygame.display.update()
    
if __name__ == '__main__':
    program = Main()
    program.run()