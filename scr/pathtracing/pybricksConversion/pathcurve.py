class Path:
    def __init__(self, *points: tuple[int, int]):
        self.points = points
        
    def get_arc(self, id: int):
        return