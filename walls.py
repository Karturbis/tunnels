import random
from pygame.math import Vector2
from pygame.draw import rect as draw_rect
from pygame import FRect

class Walls():

    def __init__(self, color:str, wall_size: int, surface, probability, seed):
        random.seed(seed)
        self.color = color
        self.wall_size = wall_size
        self.walls = self._make_walls(surface, probability)

    def _make_walls(self, surface, probability) -> list:
        wall_number_x = surface.width//self.wall_size
        wall_number_y = surface.height//self.wall_size
        walls = []
        for x in range(wall_number_x):
            for y in range(wall_number_y):
                p = random.randint(1, 100)
                if p <= probability:
                    walls.append(FRect(x*self.wall_size, y*self.wall_size, self.wall_size, self.wall_size))
        return walls

    def draw(self, surface, wall):
        draw_rect(surface, self.color, wall)

    def get_walls(self):
        return self.walls
