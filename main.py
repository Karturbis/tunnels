# imports:
import math
import pygame
from pygame.math import Vector2
from walls import Walls
from character import Character
import characters.default_character as dc
import random

#consts:
COLOR_BG = "sienna4"
COLOR_WALL = "black"#"violetred4"
WALL_SIZE = 20
DISPLAY_SIZE = (1280, 720)  # only change for testing
FPS = 60


# consts for developing:
FRICTION_COEFFICIENT = 0.1
SEED = random.randint(0, 12000)
#SEED = 8094
print(f"Seed: {SEED}")
random.seed(SEED)
WALL_PROBABILITY = 3  # in percent
SIGHT_RADIUS = 200
CHARACTER_START_POSITION = Vector2(DISPLAY_SIZE[0]//2, DISPLAY_SIZE[1]//2)

class Main():

    def __init__(self):
        # pygame setup
        pygame.init()
        self.screen = pygame.display.set_mode(DISPLAY_SIZE)
        self.clock = pygame.time.Clock()
        # character setup:
        self.character = Character(dc.color, dc.width, dc.height, CHARACTER_START_POSITION)
        # general setup:
        self.scale = 5
        self.walls_obj = Walls("black", WALL_SIZE, self.screen, WALL_PROBABILITY, SEED)
        self.wall_hitboxes = self.walls_obj.get_walls()

    def game_loop(self):
        running = True
        direction = Vector2(0, 0)
        debug_draw_lines: bool = False
        debug_draw_polygons: bool = False
        debug_line_of_sight: bool = True
        while running:
            dt = self.clock.tick(FPS) / 1000
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        debug_draw_lines = not debug_draw_lines
                    elif event.key == pygame.K_e:
                        debug_line_of_sight = not debug_line_of_sight
                    if event.key == pygame.K_q:
                        debug_draw_polygons = not debug_draw_polygons
                keys = pygame.key.get_pressed()
                # movement:
                if keys[pygame.K_w] and keys[pygame.K_s]:
                    direction.y = 0
                elif keys[pygame.K_w]:
                    direction.y = -1
                elif keys[pygame.K_s]:
                    direction.y = 1
                else:
                    direction.y = 0
                if keys[pygame.K_a] and keys[pygame.K_d]:
                    direction.x = 0
                elif keys[pygame.K_a]:
                    direction.x = -1
                elif keys[pygame.K_d]:
                    direction.x = 1
                else:
                    direction.x = 0

            # update physics:
            if debug_line_of_sight:
                wall_hitboxes_in_sight = [
                    wall for wall in self.wall_hitboxes
                        if math.hypot(
                            abs(wall.center[0] -self.character.get_position()[0]),
                            abs(wall.center[1]-self.character.get_position()[1])) < SIGHT_RADIUS
                    ]
            else:
                wall_hitboxes_in_sight = self.wall_hitboxes
            self.character.accelerate(direction.clamp_magnitude(1), 10000)
            self.character.update(direction, self.wall_hitboxes, FRICTION_COEFFICIENT, dt, DISPLAY_SIZE)
            # wipe screen by filling it with the background color:
            self.screen.fill(COLOR_BG)
            for wall in wall_hitboxes_in_sight:
                self.walls_obj.draw(self.screen, wall)
            self.character.draw(self.screen, wall_hitboxes_in_sight, debug_draw_lines, debug_draw_polygons)  # draw character
            # update the display
            pygame.display.flip()
        # if game endet:
        pygame.quit()

if __name__ == "__main__":
    main = Main()
    main.game_loop()
