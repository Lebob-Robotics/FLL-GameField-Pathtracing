class Path:
    def __init__(self, *points: tuple[int, int]):
        self.points = points
        
    def getSegment(self, segment: int):
        return