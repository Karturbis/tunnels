from pygame.math import Vector2
from pygame.draw import rect as draw_rect
from pygame import Rect

class Wall():

    def __init__(self, color:str, position: Vector2, size: int):
        self.color = color
        self.position = position
        self.size = size
        self.body = Rect(position, (size, size))

    def draw(self, surface):
        draw_rect(surface, self.color, self.body)

    def get_hitbox(self):
        return self.body
