import numpy
import pygame
from pygame import display


from model import *
from graphics import *
from constans import *

class Player(Snake):
    pass

class Game():
    def __init__(self):
        self.WIDTH = WIDTH
        self.HEIGHT = HEIGHT
        self.clock = pygame.time.Clock()
        self.display = pygame.display.set_mode((WIDTH, HEIGHT))
        self.mainloop()
        #self.start_menu()

    def start_menu(self):
        pass

    def mainloop(self):
        cells_1 = []
        snake1 = Snake(12, 12)
        while GAME_RUNNING:
            self.clock.tick(FPS)
            self.display.fill((0, 0, 0))
            self.keys_loop()
            draw_field()
            draw_interface()
            pygame.display.flip()

    def keys_loop(self):
        pass



def main():
    Game()

if __name__ == "__main__":
    pygame.init()
    main()
    pygame.quit()