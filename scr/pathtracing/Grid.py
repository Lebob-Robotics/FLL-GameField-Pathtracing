import pygame

from Node import Node

class Grid(pygame.sprite.Group):
    def __init__(self, length: int, height: int, windowSize: tuple[int, int], screenBuffer: int = 20, background: pygame.surface.Surface | None = None, backgroundColour: str = "white", nodeAlpha: int = 255):
        self.height: int = height
        self.length: int = length
            
        self.screenBuffer: int = screenBuffer
        self.gridSurface: pygame.Surface = pygame.Surface([point - self.screenBuffer for point in windowSize], pygame.SRCALPHA)
        self.nodeSize: tuple[float, float] = ((self.gridSurface.get_width()) / length, 
                                              (self.gridSurface.get_height()) / height)
        
        self.nodeAlpha: int = nodeAlpha
        self.background: pygame.Surface = pygame.Surface(self.gridSurface.size)
        self.backgroundColour = backgroundColour
        self.background.fill(self.backgroundColour)
        if background:
            self.background = pygame.transform.scale(background, self.background.size)
        
        self.nodes = [[Node(x, y, self.nodeSize[0], self.nodeSize[1], flag = Node.Flags.UNCHECKED) 
                       for y in range(height)] for x in range(length)]
        
        self.startNode: Node = self[0][0]
        self.endNode: Node = self[length - 1][height - 1]
        
    def draw(self, surface: pygame.Surface):
        self.startNode.setFlag(Node.Flags.ORIGIN)
        self.endNode.setFlag(Node.Flags.DESTINATION)
    
        self.gridSurface.blit(self.background)
        for row in self.nodes:
            for node in row:
                rect = pygame.rect.Rect(
                    node.x * self.nodeSize[0], 
                    node.y * self.nodeSize[1],
                    self.nodeSize[0], self.nodeSize[1])
                colour = pygame.Color(node.getFlag().value)
                node = pygame.Surface(self.nodeSize, pygame.SRCALPHA)
                node.fill(colour)
                node.set_alpha(self.nodeAlpha)
                self.gridSurface.blit(node, rect)
                
        for row in range(len(self.nodes)):
            for column in range(row):
                pygame.draw.line(self.gridSurface, "grey", 
                                 (row * self.nodeSize[0], 0), 
                                 (row * self.nodeSize[0], 
                                  self.height * self.nodeSize[1]))
                
        for column in range(len(self.nodes[0])):
            for row in range(column):
                pygame.draw.line(self.gridSurface, "grey", 
                                 (0, column * self.nodeSize[1]), 
                                 (self.length * self.nodeSize[0], 
                                  column * self.nodeSize[1]))
                
        surface.blit(self.gridSurface, (self.screenBuffer // 2, self.screenBuffer // 2))
                
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