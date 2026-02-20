import pygame

from Node import Node

class Grid(pygame.sprite.Group):
    def __init__(self, length: int, height: int, windowSurface: pygame.Surface, screenBuffer: int = 20):
        self.height: int = height
        self.length: int = length
        
        self.windowSurface: pygame.Surface = windowSurface
        self.screenBuffer: int = screenBuffer
        self.nodeSize: tuple[float, float] = ((self.windowSurface.get_width() - self.screenBuffer) / length, 
                                              (self.windowSurface.get_height()- self.screenBuffer) / height)
        
        self.nodes = [[Node(x, y, self.nodeSize[0], self.nodeSize[1], flag = Node.Flags.UNCHECKED) 
                       for y in range(height)] for x in range(length)]
        
        self.startNode: Node = self[0][0]
        self.endNode: Node = self[length - 1][height - 1]
        
    def draw(self, surface: pygame.Surface):
        self.startNode.setFlag(Node.Flags.ORIGIN)
        self.endNode.setFlag(Node.Flags.DESTINATION)
        
        surface.fill('white')
        for row in self.nodes:
            for node in row:
                rect = pygame.rect.Rect(
                    node.x * self.nodeSize[0] + self.screenBuffer // 2, 
                    node.y * self.nodeSize[1] + self.screenBuffer // 2, 
                    self.nodeSize[0], self.nodeSize[1])
                pygame.draw.rect(surface, node.getFlag().value, rect)
                
        for row in range(len(self.nodes)):
            for column in range(row):
                pygame.draw.line(surface, "grey", (row * self.nodeSize[0] + self.screenBuffer // 2,  
                                                   self.screenBuffer // 2), 
                                 (row * self.nodeSize[0] + self.screenBuffer // 2, 
                                  self.height * self.nodeSize[1] + self.screenBuffer // 2))
                
        for column in range(len(self.nodes[0])):
            for row in range(column):
                pygame.draw.line(surface, "grey", (self.screenBuffer // 2, 
                                                   column * self.nodeSize[1] + self.screenBuffer // 2), 
                                 (self.length * self.nodeSize[0] + self.screenBuffer // 2, 
                                  column * self.nodeSize[1] + self.screenBuffer // 2))
                
    def getMouseNode(self, position: tuple[int, int]):
        x = int((position[0] - self.screenBuffer // 2) // self.nodeSize[0])
        y = int((position[1] - self.screenBuffer // 2) // self.nodeSize[1])
        return self[x][y]
    
    def updateNodes(self):
        for row in self.nodes:
            for node in row:
                node.findNeighbours((self.length, self.height))
                node.setHeuristic(self.endNode)
    
    def __getitem__(self, key):
        return self.nodes[key]
    
    def getItemByArray(self, key: tuple[int, int]):
        return self[int(key[0])][int(key[1])]