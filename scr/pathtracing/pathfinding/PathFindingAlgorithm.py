import pygame

from pathtracing.pathfinding.Grid import Grid
from pathtracing.pathfinding.Node import Node

class PathFinder:
    def __init__(self, grid: Grid, window):
        self.grid = grid
        self.window = window
        
        self.debugFont = pygame.font.SysFont('arial', 20)
        
    def run(self):  
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    
            self.edit_grid()
            
            self.grid.draw(self.window)
            self.debug(1, "node", self.grid.get_mouse_node(pygame.mouse.get_pos()).x, self.grid.get_mouse_node(pygame.mouse.get_pos()).y)
            
            pygame.display.update()
            
    def edit_grid(self):
        mouse_pos = pygame.mouse.get_pos()
        if any(mouse_pos):
            node: Node = self.grid.get_mouse_node(mouse_pos)
            if pygame.mouse.get_pressed()[0]:  # left click
                node.setFlag(Node.Flags.BARRIER)
            elif pygame.mouse.get_pressed()[2]:  # right click
                node.setFlag(Node.Flags.UNCHECKED)
                
    def debug(self, y, heading, *args):
        self.window.blit(self.debugFont.render(heading + ': ' + ', '.join(map(str,args)), True, 'red'), (10, y * 20))
        
if __name__ == "__main__":
    pygame.init()
    window = pygame.display.set_mode((1000, 800))
    pygame.display.set_caption("Pathfinder")
    
    pathFinder = PathFinder(Grid(200, 160, window), window)
    pathFinder.run()