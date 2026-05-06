from pathlib import Path

import pygame

import pathtracing.gui as gui
from pathtracing.gamefieldpathfinder import GameFieldPathfinder

SCR_DIR = Path(__file__).resolve().parent.parent

class Main:
    def __init__(self):
        pygame.init()
        self.pathfinder: GameFieldPathfinder = GameFieldPathfinder("unearthed")

        gui.FileUtility.absolute_path = str(SCR_DIR)
        self.guiIcons: dict[str, pygame.Surface] = gui.FileUtility.import_folder_dict("assets", "gui")
        self.guiGroup: pygame.sprite.Group = pygame.sprite.Group()

        if "saveIcon" in self.guiIcons:
            self.saveButton: gui.Button = gui.Button((60, 60), (100, 100), 'white',
                                                     icon=self.guiIcons["saveIcon"],
                                                     groups=[self.guiGroup])
    
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