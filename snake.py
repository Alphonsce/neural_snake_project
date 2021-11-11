import pygame
import numpy

from graphics import *
import model

def main():
    draw_screen(pygame, display, 2)
    screen.blit(display, (20, 40))
    pygame.display.flip()

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((300, 400))
    display = pygame.Surface((800, 800))
    main()
    x = 0
    while x < 10000000:
        x+=1
    pygame.quit()