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
        self.velocity: Vector2 = Vector2(0, 0)
        self.acceleration: Vector2 = Vector2(0, 0)
        self.body = Rect(0,0, width, height)
        self.hitbox = self.body

##############
## physics: ##
##############

    def set_position(self, position_x, position_y):
        self.body.update(position_x, position_y, self.width, self.height)

    def update_physics(self, speed: int, direction: Vector2):
        self.speed = speed
        self.direction = direction
        self.velocity = speed*direction
        if self.velocity.magnitude_squared() > 0:  # using magnitude sqaured bc. its more efficient
            self.velocity.clamp_magnitude_ip(speed)

    def update_hitbox_x(self, dt:int):
        self.hitbox.center += Vector2(self.velocity.x*dt, 0)

    def update_hitbox_y(self, dt:int):
        self.hitbox.center += Vector2(0, self.velocity.y*dt)

    def update_body(self, hitbox: Rect=None):
        if hitbox:
            self.hitbox = hitbox
        self.body = self.hitbox

    def get_hitbox(self):
        return self.body

##############
## drawing: ##
##############

    def draw(self, surface):
        rect(surface, self.color, self.body)
