from pygame import sprite

from enum import Enum

class Node(sprite.Sprite):
    class Flags(Enum):
        EMPTY = 'pink'
        UNCHECKED = 'white'
        CHECKED = 'red'
        OPEN = 'green'
        BARRIER = 'black'
        ORIGIN = 'orange'
        DESTINATION = 'turqoise'
        PATH = 'purple'
    
    def __init__(self, x: int, y: int, length: float, width: float = 0, flag = Flags.EMPTY):
        self.x: int = x
        self.y: int = y
        self.length: float = length
        self.width: float = width if width else length
        self.flag = flag
        
    def setFlag(self, flag: Flags):
        self.flag = flag
        
    def getFlag(self):
        return self.flag
    
    def isFlag(self, flag: Flags):
        return self.flag == flag