import pygame

from Node import Node

class Grid(pygame.sprite.Group):
    def __init__(self, length: int, height: int, windowSurface: pygame.Surface):
        self.height: int = height
        self.length: int = length
        
        self.windowSurface: pygame.Surface = windowSurface
        self.nodeSize: tuple[float, float] = (self.windowSurface.get_width() / length, self.windowSurface.get_height() / height)
        
        self.nodes = [[Node(x, y, self.nodeSize[0], self.nodeSize[1], flag = Node.Flags.UNCHECKED) for y in range(height)] for x in range(length)]
        
    def draw(self, surface: pygame.Surface):
        surface.fill('white')
        for row in self.nodes:
            for node in row:
                rect = pygame.rect.Rect(
                    node.x * self.nodeSize[0], node.y * self.nodeSize[1], 
                    self.nodeSize[0], self.nodeSize[1])
                pygame.draw.rect(surface, node.getFlag().value, rect)
                
        for row in range(len(self.nodes)):
            for column in range(row):
                pygame.draw.line(surface, "grey", (row * self.nodeSize[0], 0), (row * self.nodeSize[0], self.height * self.nodeSize[1]))
                
        for column in range(len(self.nodes[0])):
            for row in range(column):
                pygame.draw.line(surface, "grey", (0, column * self.nodeSize[1]), (self.length * self.nodeSize[0], column * self.nodeSize[1]))
                
    def get_mouse_node(self, pos):
        x = int(pos[0] // self.nodeSize[0])
        y = int(pos[1] // self.nodeSize[1])
        return self[x][y]
        
    def __getitem__(self, key):
        return self.nodes[key]