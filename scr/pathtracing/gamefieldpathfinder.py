from pathlib import Path
import pygame

from pathtracing.astar.algorithm import Algorithm
from pathtracing.astar.grid import Grid
from pathtracing.astar.node import Node
from pathtracing.astar.pathfinder import PathFinder
from pathtracing.conversion.pathcurve import PathCurve
from pathtracing.missions import (
    HOME_POS,
    MISSION_LANDMARK_RADIUS,
    MISSIONS_BY_FIELD,
    ROBOT_RADIUS,
)


# Inflated obstacle radius matches generate_robot so GUI preview = robot code.
OBSTACLE_RADIUS = ROBOT_RADIUS + MISSION_LANDMARK_RADIUS
EDGE_BUFFER = max(1, ROBOT_RADIUS - 4)


class GameFieldPathfinder(PathFinder):
    def __init__(self, mapName: str):
        WINDOW_WIDTH: int = 1500
        GRID_SIZE: int = 70

        asset_path = Path(__file__).resolve().parent.parent / "assets" / "gamefields" / f"{mapName}-gamefield.jpeg"
        gameMap = pygame.image.load(asset_path)
        window = pygame.display.set_mode(pygame.transform.scale_by(gameMap, WINDOW_WIDTH / gameMap.width).size)
        pygame.display.set_caption(f"{mapName.capitalize()} Gamefield Pathfinding")

        grid = Grid(GRID_SIZE, round((window.get_height() / window.get_width()) * GRID_SIZE), window.size,
                    background=gameMap,
                    node_transparency=100)
        super().__init__(grid, window)

        self.field_name = mapName
        self.missions = MISSIONS_BY_FIELD.get(mapName, [])
        self.mission_index = 0

        self.path_curve: PathCurve = PathCurve(end_pos=self.grid.end_node.get_pos())
        self.path_calculated: bool = False

        self._setup_for_current_mission()

    def _apply_obstacles(self, target_index: int):
        self.grid.clear_barriers()
        for x in range(self.grid.length):
            for y in range(EDGE_BUFFER):
                self.grid[x][y].set_flag(Node.Flags.BARRIER)
                self.grid[x][self.grid.height - 1 - y].set_flag(Node.Flags.BARRIER)
        for y in range(self.grid.height):
            for x in range(EDGE_BUFFER):
                self.grid[x][y].set_flag(Node.Flags.BARRIER)
                self.grid[self.grid.length - 1 - x][y].set_flag(Node.Flags.BARRIER)
        for i, (_mid, _name, pos) in enumerate(self.missions):
            if i == target_index:
                continue
            self.grid.add_barrier_disc(pos[0], pos[1], OBSTACLE_RADIUS)

    def _setup_for_current_mission(self):
        if not self.missions:
            return
        self.grid.reset_pathfinding()
        self._apply_obstacles(self.mission_index)
        self.grid.set_start(*HOME_POS)
        target = self.missions[self.mission_index][2]
        self.grid.set_end(*target)
        self.grid[HOME_POS[0]][HOME_POS[1]].set_flag(Node.Flags.UNCHECKED)
        self.grid[target[0]][target[1]].set_flag(Node.Flags.UNCHECKED)

        self.algorithm = Algorithm(self.grid, started=True)
        self.path_calculated = False
        self.path_curve = PathCurve(end_pos=self.grid.end_node.get_pos())

    def _advance_mission(self):
        if not self.missions:
            return
        self.mission_index = (self.mission_index + 1) % len(self.missions)
        self._setup_for_current_mission()

    def step(self):
        for event in pygame.event.get(pygame.KEYDOWN):
            if event.key == pygame.K_n:
                self._advance_mission()

        super().step()

        if self.algorithm.found_path and not self.path_calculated:
            self.path_calculated = True
            self.convert_path()

        self.draw_path()
        self._draw_mission_label()

    def convert_path(self):
        if not self.algorithm.path:
            return
        self.path_curve = PathCurve(*self.algorithm.path,
                                    end_pos=self.grid.end_node.get_pos(),
                                    jaggedness=3, max_length=5)

    def draw_path(self):
        for section in self.path_curve.path:
            section.draw(self.window, self.grid)

    def _draw_mission_label(self):
        if not self.missions:
            return
        mid, name, _ = self.missions[self.mission_index]
        self.debug(2, f"mission {self.mission_index + 1}/{len(self.missions)}", f"{mid} {name}")
        self.debug(3, "press N for next mission", "")


if __name__ == "__main__":
    pygame.init()
    pathfinder = GameFieldPathfinder("unearthed")
    while True:
        pathfinder.step()
        pygame.display.update()
