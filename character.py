from numpy import sign
from pygame.math import Vector2
from pygame import draw
from pygame import FRect

class Character():

    def __init__(self, color:str, width:int, height:int, position: Vector2):
        self.color: str = color
        self.height: int = height
        self.width: int = width
        # init movement variables
        self.direction = (0, 0)
        self.speed: int = 0
        self.velocity: Vector2 = Vector2(0, 0)
        self.acceleration: Vector2 = Vector2(0, 0)
        self.body = FRect(position, (width, height))
        self.hitbox = self.body

##############
## physics: ##
##############

    # updating:

    def _get_hitbox(self):
        return self.body

    def _update_physics(self, direction: Vector2, friction_coefficient: float, dt):
        if self.velocity.magnitude_squared() < 25:
            self.velocity = Vector2(0, 0)
        self.acceleration -= self.velocity * self.velocity.magnitude() * friction_coefficient
        self.velocity += self.acceleration * dt

    def _update_hitbox_x(self, dt:int):
        self.hitbox.center += Vector2(self.velocity.x *dt, 0)

    def _update_hitbox_y(self, dt:int):
        self.hitbox.center += Vector2(0, self.velocity.y *dt)

    def _update_body(self, hitbox: FRect=None):
        if hitbox:
            self.hitbox = hitbox
        self.body = self.hitbox

    def _screen_collisions_x(self, display_size):
        if self.hitbox.left < 0:
            self.set_position(0, self.hitbox.top)
        elif self.hitbox.right > display_size[0]:
            self.set_position(display_size[0]-self.width, self.hitbox.top)

    def _screen_collisions_y(self, display_size):
        if self.hitbox.top < 0:
            self.set_position(self.hitbox.left, 0)
        elif self.hitbox.bottom > display_size[1]:
            self.set_position(self.hitbox.left, display_size[1]-self.height)

    def _wall_collisions_x(self, wall_hitboxes):
        coll = self.hitbox.collidelist(wall_hitboxes)
        if coll >=0:
            coll_hitbox = wall_hitboxes[coll]
            if self.velocity.x < 0:
                self.set_position(coll_hitbox.right, self.hitbox.y)
            elif self.velocity.x > 0:
                self.set_position(coll_hitbox.left - self.width, self.hitbox.y)
            self.velocity.x = 0

    def _wall_collisions_y(self, wall_hitboxes):
        coll = self.hitbox.collidelist(wall_hitboxes)
        if coll >=0:
            coll_hitbox = wall_hitboxes[coll]
            if self.velocity.y < 0:
                self.set_position(self.hitbox.x, coll_hitbox.bottom)
            elif self.velocity.y > 0:
                self.set_position(self.hitbox.x, coll_hitbox.top -self.width)
            self.velocity.y = 0

    def update(self, direction, wall_hitboxes, friction_coefficient, dt, display_size):
        self._update_physics(direction, friction_coefficient, dt)
        self._update_hitbox_x(dt)
        self._screen_collisions_x(display_size)
        self._wall_collisions_x(wall_hitboxes)
        self._update_hitbox_y(dt)
        self._screen_collisions_y(display_size)
        self._wall_collisions_y(wall_hitboxes)
        self._update_body()

    # from outside changeable physics:

    def set_position(self, position_x, position_y):
        self.body.update(position_x, position_y, self.width, self.height)

    def get_position(self):
        return self.hitbox.center

    def accelerate(self, direction: Vector2, acceleration: float):
        self.acceleration = acceleration*direction

##############
## drawing: ##
##############

    def _draw_body(self, surface):
        draw.rect(surface, self.color, self.body)

    def draw(self, surface, wall_hitboxes, draw_lines:bool, draw_polygons:bool):
        self._draw_body(surface)
        lines = self._create_lines(surface, wall_hitboxes)
        if draw_lines:
            self._draw_lines_of_sight(surface, lines)
        if draw_polygons:
            self._draw_shadow_polygon(surface, lines)

    def _draw_lines_of_sight(self, surface, lines):
        for i in lines:
            for j in i:
                for k in j:
                    draw.line(surface, "black" ,k[0], k[1])

    def _draw_shadow_polygon(self, surface, lines):
        for wall_lines in lines:
            for direction_lines in wall_lines:
                try:
                    p0 = direction_lines[0][0]
                    p1 = direction_lines[0][1]
                    p2 = direction_lines[-1][0]
                    p3 = direction_lines[-1][1]
                    draw.polygon(surface, "black", [p0, p2, p3, p1])
                except Exception:
                    pass

    # lines of sight
    def _create_lines(self, surface, wall_hitboxes) -> list:
        position = self.hitbox.center
        width = surface.width
        height = surface.height
        lines = []
        for wall in wall_hitboxes:
            wall_lines: list = [[],[],[],[]]
            for i in range(width):
                cl_top = wall.clipline(position, (i, 0))
                cl_bot = wall.clipline(position, (i, height))
                if cl_top:
                    wall_lines[0].append(tuple((cl_top[1], (i, 0))))
                if cl_bot:
                    wall_lines[1].append(tuple((cl_bot[1], (i, height))))
            for i in range(height):
                cl_left = wall.clipline(position, (0, i))
                cl_right = wall.clipline(position, (width, i))
                if cl_left:
                    wall_lines[2].append(tuple((cl_left[1], (0, i))))
                if cl_right:
                    wall_lines[3].append(tuple((cl_right[1], (width, i))))
            lines.append(wall_lines)
        return lines


