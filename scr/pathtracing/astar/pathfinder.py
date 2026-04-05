import pygame

from pathtracing.astar.grid import Grid
from pathtracing.astar.node import Node
from pathtracing.astar.algorithm import Algorithm

class PathFinder:
    def __init__(self, grid: Grid, window):
        self.grid = grid
        self.window: pygame.Surface = window
        
        self.debugFont = pygame.font.SysFont('arial', 20)
        self.algorithm: Algorithm = Algorithm(self.grid)
        
    def step(self):  
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not self.algorithm.started:
                    self.algorithm = Algorithm(self.grid, True)
                
        if self.algorithm.started:
            self.algorithm.step()
        else:
            self.edit_grid()
        
        self.window.fill('white')
        self.grid.draw(self.window)
        self.draw_path()
        
        self.debug(1, self.grid.getMouseNode(pygame.mouse.get_pos()).get_pos())
            
    def edit_grid(self):
        if any(pygame.mouse.get_pressed()):
            mouse_pos = pygame.mouse.get_pos()
            node: Node = self.grid.getMouseNode(mouse_pos)
            if pygame.mouse.get_pressed()[0]:  # left click
                mod_keys = pygame.key.get_mods()
                if mod_keys == pygame.KMOD_NONE:
                    node.set_flag(Node.Flags.BARRIER)
                elif mod_keys == pygame.KMOD_LSHIFT:
                    self.grid.start_node.set_flag(Node.Flags.UNCHECKED)
                    self.grid.start_node = node
                elif mod_keys == pygame.KMOD_RSHIFT:
                    self.grid.end_node.set_flag(Node.Flags.UNCHECKED)
                    self.grid.end_node = node
            
            elif pygame.mouse.get_pressed()[2]:  # right click
                node.set_flag(Node.Flags.UNCHECKED)
                
    def draw_path(self):
        for i in range(len(self.algorithm.path) - 1):
            pygame.draw.line(self.window, "purple", 
                             self.grid.convert_coords(self.algorithm.path[i]), 
                             self.grid.convert_coords(self.algorithm.path[i + 1]),
                             width = 3)
                
    def debug(self, line: int, heading: str, *args, x_pos: int = 10, line_height: int = 20):
        self.window.blit(self.debugFont.render(f"{heading}: {', '.join(map(str,args))}", True, 'red'), (x_pos, line * line_height))
        
if __name__ == "__main__":
    pygame.init()
    window = pygame.display.set_mode((1000, 800))
    pygame.display.set_caption("Pathfinder")
    
    pathFinder = PathFinder(Grid(50, 40, window.size, background_colour= 'white'), window)
    while True:
        pathFinder.step()
        pygame.display.update()