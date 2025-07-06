from pygame.math import Vector2
from pygame.draw import rect, circle
from pygame import Rect

class Character():

    def __init__(self, color:str, width:int, height:int):
        self.color: str = color
        self.height: int = height
        self.width: int = width
        # init movement variables
        self.direction = (0, 0)
        self.speed: int = 0
        self.acceleration: Vector2 = Vector2(0, 0)
        self.body = Rect(0,0, width, height)

##############
## physics: ##
##############

    def set_position(self, position_x, position_y):
        self.body.update(position_x, position_y, self.width, self.height)

    def update(self, speed: int, direction: Vector2, dt:int):
        self.speed = speed
        self.direction = direction
        self.body.center += self.speed*self.direction*dt

    def get_hitbox(self):
        return self.body

##############
## drawing: ##
##############

    def draw(self, surface):
        rect(surface, self.color, self.body)
