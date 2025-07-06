# imports:
import pygame
from wall import Wall
from character import Character
import characters.default_character as dc


#consts:
COLOR_BG = "sienna4"
COLOR_WALL = "violetred4"
WALL_SIZE = 20
DISPLAY_SIZE = (1280, 720)  # only change for testing
FPS = 60

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
        self.walls.append(Wall(COLOR_WALL, pygame.math.Vector2(50, 20), WALL_SIZE))


    def game_loop(self):
        running = True
        direction = pygame.math.Vector2(0, 0)
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

            # update physics:d
            self.character.update(300, direction, dt)
            # check collisions with screen edge:
            hitbox = self.character.get_hitbox()
            # x-axis:
            if hitbox.left < 0:
                print("out of screen left")
                self.character.set_position(0, hitbox.top)
            elif hitbox.right > DISPLAY_SIZE[0]:
                self.character.set_position(DISPLAY_SIZE[0]-dc.width, hitbox.top)
                print("out of screen right")
            # y-axis:
            if hitbox.top < 0:
                print("out of screen top")
                self.character.set_position(hitbox.left, 0)
            elif hitbox.bottom > DISPLAY_SIZE[1]:
                self.character.set_position(hitbox.left, DISPLAY_SIZE[1]-dc.height)
                print("out of screen bottom")
            # check other collisions:
            if hitbox.colliderect(self.walls[0].get_hitbox()):
                print("collision with wall")
            # Update stuff on screen
            # wipe screen by filling it with the background color:
            self.screen.fill(COLOR_BG)
            self.walls[0].draw(self.screen)
            self.character.draw(self.screen)

            # update the display
            pygame.display.flip()
        # if game endet:
        pygame.quit()

if __name__ == "__main__":
    main = Main()
    main.game_loop()
