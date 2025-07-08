# imports:
import pygame
from pygame.math import Vector2
from wall import Wall
from character import Character
import characters.default_character as dc


#consts:
COLOR_BG = "sienna4"
COLOR_WALL = "black"#"violetred4"
WALL_SIZE = 70
DISPLAY_SIZE = (1280, 720)  # only change for testing
FPS = 60


# consts for developing:
SPEED = 300

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
        self.walls.append(Wall(COLOR_WALL, Vector2(600, 350), WALL_SIZE))
        self.wall_hitboxes = [i.get_hitbox() for i in self.walls]

    def screen_collisions_x(self, hitbox):
        if hitbox.left < 0:
            print("out of screen left")
            self.character.set_position(0, hitbox.top)
        elif hitbox.right > DISPLAY_SIZE[0]:
            self.character.set_position(DISPLAY_SIZE[0]-dc.width, hitbox.top)
            print("out of screen right")

    def screen_collisions_y(self, hitbox):
        if hitbox.top < 0:
            print("out of screen top")
            self.character.set_position(hitbox.left, 0)
        elif hitbox.bottom > DISPLAY_SIZE[1]:
            self.character.set_position(hitbox.left, DISPLAY_SIZE[1]-dc.height)
            print("out of screen bottom")

    def wall_collisions_x(self, hitbox, direction):
        coll = hitbox.collidelist(self.wall_hitboxes)
        if coll >=0:
            coll_hitbox = self.wall_hitboxes[coll]
            if direction.x < 0:
                self.character.set_position(coll_hitbox.right, hitbox.y)
            elif direction.x > 0:
                self.character.set_position(coll_hitbox.left - dc.width, hitbox.y)


    def wall_collisions_y(self, hitbox, direction):
        coll = hitbox.collidelist(self.wall_hitboxes)
        if coll >=0:
            coll_hitbox = self.wall_hitboxes[coll]
            if direction.y < 0:
                self.character.set_position(hitbox.x, coll_hitbox.bottom)
            elif direction.y > 0:
                self.character.set_position(hitbox.x, coll_hitbox.top -dc.width)

    def game_loop(self):
        running = True
        direction = Vector2(0, 0)
        while running:
            dt = self.clock.tick(FPS) / 1000
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
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
            self.character.update_physics(SPEED, direction)
            # check collisions on x-axis
            self.character.update_hitbox_x(dt)
            hitbox = self.character.get_hitbox()
            self.screen_collisions_x(hitbox)
            self.wall_collisions_x(hitbox, direction)
            # check collisions on y-axis
            self.character.update_hitbox_y(dt)
            hitbox = self.character.get_hitbox()
            self.screen_collisions_y(hitbox)
            self.wall_collisions_y(hitbox, direction)
            # update the actual character to the position of the hitbox
            self.character.update_body(hitbox)
            # Update stuff on screen
            # wipe screen by filling it with the background color:
            self.screen.fill(COLOR_BG)
            self.walls[0].draw(self.screen)  # draw walls
            self.character.draw(self.screen)  # draw character
            # update the display
            pygame.display.flip()
        # if game endet:
        pygame.quit()

if __name__ == "__main__":
    main = Main()
    main.game_loop()
