import pygame

from pathtracing.Grid import Grid
from pathtracing.Node import Node
from pathtracing.Algorithm import Algorithm

class PathFinder:
    def __init__(self, grid: Grid, window):
        self.grid = grid
        self.window: pygame.Surface = window
        
        self.debugFont = pygame.font.SysFont('arial', 20)
        self.algorithm: Algorithm = Algorithm(self.grid)
        
    def run(self):  
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE and not self.algorithm.started:
                        self.algorithm = Algorithm(self.grid, True)
                    
            if self.algorithm.started:
                self.algorithm.step()
            else:
                self.editGrid()
            
            self.grid.draw(self.window)
            
            pygame.display.update()
            
    def editGrid(self):
        if any(pygame.mouse.get_pressed()):
            mousePos = pygame.mouse.get_pos()
            node: Node = self.grid.getMouseNode(mousePos)
            if pygame.mouse.get_pressed()[0]:  # left click
                modKeys = pygame.key.get_mods()
                if modKeys == pygame.KMOD_NONE:
                    node.setFlag(Node.Flags.BARRIER)
                elif modKeys == pygame.KMOD_LSHIFT:
                    self.grid.startNode.setFlag(Node.Flags.UNCHECKED)
                    self.grid.startNode = node
                elif modKeys == pygame.KMOD_RSHIFT:
                    self.grid.endNode.setFlag(Node.Flags.UNCHECKED)
                    self.grid.endNode = node
            
            elif pygame.mouse.get_pressed()[2]:  # right click
                node.setFlag(Node.Flags.UNCHECKED)
                
    def debug(self, line: int, heading: str, *args, xPos: int = 10, lineHeight: int = 20):
        self.window.blit(self.debugFont.render(f"{heading}: {', '.join(map(str,args))}", True, 'red'), (xPos, line * lineHeight))
        
if __name__ == "__main__":
    pygame.init()
    window = pygame.display.set_mode((1000, 800))
    pygame.display.set_caption("Pathfinder")
    
    pathFinder = PathFinder(Grid(50, 40, window), window)
    pathFinder.run()