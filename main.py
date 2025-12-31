import pygame

import math
from queue import PriorityQueue

from grid import Grid

class Main:
    def __init__(self, width):
        pygame.init()
        self.window = pygame.display.set_mode((width, width))
        pygame.display.set_caption("A* Pathfinding")

        self.font = pygame.font.SysFont('arial', 20)

        self.width = width
        self.grid = Grid(50, 50, self.width)

        self.open_set = PriorityQueue()
        self.open_set_hash = {}
        self.traced_path = {}

        self.start = None
        self.end = None
        self.is_started = False

        self.running = True

    def debug(self, y, *args):
        self.window.blit(self.font.render(', '.join(map(str,args)), True, 'red'), (10, y * 20))

    @staticmethod
    def heuristic(node1, node2):
        return math.dist((node1.col, node1.row), (node2.col, node2.row))

    def edit_grid(self):
        mouse_pos = pygame.mouse.get_pos()
        if any(mouse_pos):
            node = self.grid.get_mouse_node(mouse_pos)
            if pygame.mouse.get_pressed()[0]:  # left click
                if not self.start and node != self.end:
                    self.start = node
                    self.start.set_state('origin')
                elif not self.end and node != self.start:
                    self.end = node
                    self.end.set_state('destination')
                elif node.flag == 'open':
                    node.set_state('barrier')

            elif pygame.mouse.get_pressed()[2]:  # right click
                node.reset_state()
                if node == self.start:
                    self.start = None
                elif node == self.end:
                    self.end = None

    # a* algorithm
    def initiate_search(self):
        self.is_started = True
        self.grid.update()

        self.open_set = PriorityQueue()
        self.open_set.put((0, self.start)) # item in queue in format (f-score, node)
        self.open_set_hash[self.start] = self.start
        self.traced_path = {}

        # equivalent to just being: f-score = heuristic
        self.start.g_score = 0
        self.start.h_score = self.heuristic(self.start, self.end)
        self.start.f_score = self.start.g_score + self.start.h_score

    def algorithm(self):
        q = self.open_set.get()
        for adjacent in q.neighbours:
            if adjacent == self.end:
                break # end search
            else:
                adjacent.h_score = self.heuristic(adjacent, self.end)
                adjacent.g_score = q.g_score + adjacent.


    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif self.is_started:
                    continue
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.initiate_search()

            if self.is_started and self.open_set.empty():
                self.is_started = False

            if not self.is_started:
                self.edit_grid()
            else:
                self.algorithm()

            self.grid.draw(self.window)
            if self.start:
                self.debug(1, self.start.x, self.start.y)
            if self.end:
                self.debug(2, self.end.x, self.end.y)

            pygame.display.flip()

        pygame.quit()

if __name__ == "__main__":
    main = Main(800)
    main.run()

