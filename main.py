# imports:
import math
import pygame
from pygame.math import Vector2
from wall import Wall
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
WALLNUMBER = 300
SIGHT_RADIUS = 200

class Main():

    def __init__(self):
        # pygame setup
        pygame.init()
        self.screen = pygame.display.set_mode(DISPLAY_SIZE)
        self.clock = pygame.time.Clock()
        # character setup:
        self.character = Character(dc.color, dc.width, dc.height)
        # general setup:
        self.scale = 5
        self.walls = []
        for i in range(WALLNUMBER):
            self.walls.append(Wall("black", Vector2(random.randint(0, DISPLAY_SIZE[0]), random.randint(0, DISPLAY_SIZE[1])), WALL_SIZE))
        self.wall_hitboxes = [i.get_hitbox() for i in self.walls]

    def game_loop(self):
        running = True
        direction = Vector2(0, 0)
        debug_draw_lines: bool = False
        debug_draw_polygons: bool = False
        while running:
            dt = self.clock.tick(FPS) / 1000
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        debug_draw_lines = True
                    elif event.key == pygame.K_e:
                        debug_draw_lines = False
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
            walls_in_sight = [
                wall for wall in self.walls
                    if math.hypot(
                        abs(wall.get_position()[0] -self.character.get_position()[0]),
                        abs(wall.get_position()[1]-self.character.get_position()[1])) < SIGHT_RADIUS
                ]
            wall_hitboxes_in_sight = [i.get_hitbox() for i in walls_in_sight]
            self.character.accelerate(direction.clamp_magnitude(1), 10000)
            self.character.update(direction, self.wall_hitboxes, FRICTION_COEFFICIENT, dt, DISPLAY_SIZE)
            # wipe screen by filling it with the background color:
            self.screen.fill(COLOR_BG)
            for wall in walls_in_sight:
                wall.draw(self.screen)
            self.character.draw(self.screen, wall_hitboxes_in_sight, debug_draw_lines, debug_draw_polygons)  # draw character
            # update the display
            pygame.display.flip()
        # if game endet:
        pygame.quit()

if __name__ == "__main__":
    main = Main()
    main.game_loop()
