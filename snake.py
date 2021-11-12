import numpy
import pygame


from model import *
from graphics import *
from constans import *



class Game():
    def __init__(self):
        self.WIDTH = WIDTH
        self.HEIGHT = HEIGHT
        self.clock = pygame.time.Clock()
        self.display = pygame.display.set_mode((WIDTH, HEIGHT))
        self.start_menu()

    def start_menu(self):
        pass

    def mainloop(self):
        pass




def main():
    Game()

if __name__ == "__main__":
    pygame.init()
    main()
    pygame.quit()