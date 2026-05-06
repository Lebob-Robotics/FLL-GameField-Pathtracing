import pygame

from pathtracing.astar.node import Node

class Grid(pygame.sprite.Group):
    def __init__(self, length: int, height: int, windowSize: tuple[int, int], screenBuffer: int = 20, background: pygame.surface.Surface | None = None, background_colour: str = "white", node_transparency: int = 255):
        self.height: int = height
        self.length: int = length
            
        self.screenBuffer: int = screenBuffer
        self.gridSurface: pygame.Surface = pygame.Surface([point - self.screenBuffer for point in windowSize], pygame.SRCALPHA)
        self.node_size: tuple[float, float] = ((self.gridSurface.get_width()) / length, 
                                              (self.gridSurface.get_height()) / height)
        
        self.nodeAlpha: int = node_transparency
        self.background: pygame.Surface = pygame.Surface(self.gridSurface.size)
        self.backgroundColour = background_colour
        self.background.fill(self.backgroundColour)
        if background:
            self.background = pygame.transform.scale(background, self.background.size)
        
        self.nodes = [[Node(x, y, self.node_size[0], self.node_size[1], flag = Node.Flags.UNCHECKED) 
                       for y in range(height)] for x in range(length)]
        
        self.start_node: Node = self[0][0]
        self.end_node: Node = self[length - 1][height - 1]
        
    def draw(self, surface: pygame.Surface):
        self.start_node.set_flag(Node.Flags.ORIGIN)
        self.end_node.set_flag(Node.Flags.DESTINATION)
    
        self.gridSurface.blit(self.background)
        for row in self.nodes:
            for node in row:
                rect = pygame.rect.Rect(
                    node.x * self.node_size[0], 
                    node.y * self.node_size[1],
                    self.node_size[0], self.node_size[1])
                colour = pygame.Color(node.getFlag().value)
                node = pygame.Surface(self.node_size, pygame.SRCALPHA)
                node.fill(colour)
                node.set_alpha(self.nodeAlpha)
                self.gridSurface.blit(node, rect)
                
        for row in range(len(self.nodes)):
            for column in range(row):
                pygame.draw.line(self.gridSurface, "grey", 
                                 (row * self.node_size[0], 0), 
                                 (row * self.node_size[0], 
                                  self.height * self.node_size[1]))
                
        for column in range(len(self.nodes[0])):
            for row in range(column):
                pygame.draw.line(self.gridSurface, "grey", 
                                 (0, column * self.node_size[1]), 
                                 (self.length * self.node_size[0], 
                                  column * self.node_size[1]))
                
        surface.blit(self.gridSurface, (self.screenBuffer // 2, self.screenBuffer // 2))
        
    def convert_coords(self, coords: tuple[float, float]):
        return [coords[point] * self.node_size[point] + 
                self.screenBuffer // 2 + 
                self.node_size[point] // 2 
                for point in range(len(coords))]
                
    def getMouseNode(self, position: tuple[int, int]):
        x = int((position[0] - self.screenBuffer // 2) // self.node_size[0])
        y = int((position[1] - self.screenBuffer // 2) // self.node_size[1])
        return self[x][y]
    
    def update_nodes(self):
        for row in self.nodes:
            for node in row:
                node.findNeighbours((self.length, self.height))
                node.setHeuristic(self.end_node)

    def reset_pathfinding(self):
        """Clear OPEN/CLOSED/PATH flags and reset f/g/h scores. Preserves BARRIER."""
        from math import inf
        for row in self.nodes:
            for node in row:
                if node.isFlag(Node.Flags.BARRIER):
                    continue
                node.set_flag(Node.Flags.UNCHECKED)
                node.predeccessor = None
                node.f = node.g = node.h = inf

    def clear_barriers(self):
        for row in self.nodes:
            for node in row:
                if node.isFlag(Node.Flags.BARRIER):
                    node.set_flag(Node.Flags.UNCHECKED)

    def add_barrier_disc(self, cx: int, cy: int, radius: int):
        """Mark every node within `radius` cells of (cx, cy) as BARRIER."""
        for x in range(max(0, cx - radius), min(self.length, cx + radius + 1)):
            for y in range(max(0, cy - radius), min(self.height, cy + radius + 1)):
                if (x - cx) ** 2 + (y - cy) ** 2 <= radius ** 2:
                    self[x][y].set_flag(Node.Flags.BARRIER)

    def set_start(self, x: int, y: int):
        self.start_node.set_flag(Node.Flags.UNCHECKED)
        self.start_node = self[x][y]

    def set_end(self, x: int, y: int):
        self.end_node.set_flag(Node.Flags.UNCHECKED)
        self.end_node = self[x][y]
    
    def __getitem__(self, key):
        return self.nodes[key]
    
    def get_item_by_array(self, key: tuple[int, int]):
        return self[int(key[0])][int(key[1])]