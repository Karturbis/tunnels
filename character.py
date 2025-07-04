from pygame.math import Vector2

class Character():

    def __init__(self, shape:str, color:str, length:int=0, width:int=0, radius:int=0):
        self.color: str = color
        if shape == "circle":
            self.radius: int = radius
        elif shape == "rect":
            self.length: int = length
            self.width: int = width
        self.shape: str = shape
        # init movement variables
        self.position: Vector2 = Vector2(0, 0)
        self.velocity: Vector2 = Vector2(0, 0)
        self.acceleration: Vector2 = Vector2(0, 0)

    def update_movement(self):
        self.velocity += self.acceleration
        self.position += self.velocity






##############
## drawing: ##
##############

    def draw_circle(self):
        pass

    def draw_rect(self):
        pass

    def draw(self):
        if self.shape == "circle":
            self.draw_circle()
        elif self.shape == "rect":
            self.draw_rect()
