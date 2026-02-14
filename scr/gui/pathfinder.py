import pygame

from queue import PriorityQueue

from scr.gui.grid import Grid

class Main:
    def __init__(self, win_width):
        pygame.init()

        # initialise window
        self.window = pygame.display.set_mode((win_width, win_width))
        pygame.display.set_caption("Game Field")

        # timing and clock
        self.clock = pygame.time.Clock()
        self.tick_rate = 0

        # debug
        self.font = pygame.font.SysFont('arial', 20)

        # initialise grid
        self.width = win_width
        self.grid = Grid(50, 50, self.width)

        # algorithm related
        self.set_index = 0
        self.open_set = PriorityQueue()
        self.open_set_hash = set() # set to keep track of contents of open set
        self.closed_set = set()
        self.traced_path = {}

        self.path_found = False

        # significant nodes
        self.start = None
        self.end = None

        # run loop
        self.started = False
        self.running = True

    def debug(self, y, heading, *args):
        self.window.blit(self.font.render(heading + ': ' + ', '.join(map(str,args)), True, 'red'), (10, y * 20))

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
                elif node.flag == 'unchecked':
                    node.set_state('barrier')

            elif pygame.mouse.get_pressed()[2]:  # right click
                node.reset_state()
                if node == self.start:
                    self.start = None
                elif node == self.end:
                    self.end = None

    # a* algorithm
    def initiate_search(self):
        self.started = True
        self.grid.update_neighbours()
        self.grid.update_heuristics(self.end)

        self.set_index = 0
        self.open_set = PriorityQueue()
        self.open_set.put((0, self.set_index, self.start)) # item in queue in format (f-score, index, node)
        self.open_set_hash = {self.start}
        self.traced_path = {}

        self.start.g = 0
        self.start.f = self.start.g + self.start.h

    def algorithm(self):
        f_score, index, node = self.open_set.get()
        self.open_set_hash.remove(node)
        self.closed_set.add(node)
        if node != self.start and node != self.end:
            node.set_state('closed')

        if node == self.end:
            self.started = False
            self.path_found = True

        for neighbour, weight in node.neighbours: # iterate through neighbours
            if neighbour in self.closed_set:
                continue

            g_score = node.g + weight # temporarily assign a g_score to neighbour
            if g_score < neighbour.g: # check if new path is shorter
                neighbour.g = node.g + weight # update g_score
                neighbour.f = neighbour.g + neighbour.h
                self.traced_path[neighbour] = node # update path

                if neighbour not in self.open_set_hash: # if neighbour not in open set
                    self.set_index += 1
                    self.open_set.put((neighbour.f, self.set_index, neighbour))
                    self.open_set_hash.add(neighbour)
                    neighbour.set_state('open') if neighbour != self.end else neighbour.set_state('destination')

    def reconstruct_path(self):
        node = self.end
        while node in self.traced_path:
            node = self.traced_path[node]
            node.set_state('path') if node != self.start else node.set_state('origin')

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif self.started:
                    continue
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE and self.start and self.end:
                        self.initiate_search()
                    elif event.key == pygame.K_e and not self.started:
                        self.grid = Grid(50, 50, self.width)
                        self.start = None
                        self.end = None

            if not self.started: # edit grid while algorithm is not running
                self.edit_grid()
            elif not self.open_set.empty(): # run algorithm while open set is not empty
                self.algorithm()
            else: # case where path is not found
                self.path_found = False
                self.started = False

            if self.path_found:
                self.reconstruct_path()

            # visually display algorithm
            self.grid.draw(self.window)
            if self.start:
                self.debug(1, 'Start', self.start.col, self.start.row)
            if self.end:
                self.debug(2, 'End', self.end.col, self.end.row)

            self.debug(3, 'Frame Rate', self.slider.value)

            self.slider.update()
            self.slider.draw(self.window)

            pygame.display.flip()

            if self.started:
                self.clock.tick(self.tick_rate)
            else:
                self.clock.tick(60)

        pygame.quit()

if __name__ == "__main__":
    main = Main(win_width = 800)
    main.run()

