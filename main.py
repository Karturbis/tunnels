# imports:
import pygame


#consts:
COLOR_BG = "sienna4"
FPS = 60
DISPLAY_SIZE = (1280, 720)  # only change for testing

class Main():


    def __init__(self):
        # pygame setup
        pygame.init()
        self.screen = pygame.display.set_mode(DISPLAY_SIZE)
        self.clock = pygame.time.Clock()

    def game_loop(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False



            # Update stuff on screen
            # wipe screen by filling it with the background color:
            self.screen.fill(COLOR_BG)

            # update the display
            pygame.display.flip()

            self.clock.tick(FPS)  # limits the FPS
        # if game endet:
        pygame.quit()

if __name__ == "__main__":
    main = Main()
    main.game_loop()