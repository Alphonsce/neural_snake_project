import numpy
import pygame
from pygame import display


from model import *
from graphics import *
from constans import *


class Game_field():
    def __init__(self):
        self.snake = Snake(FIELD_SIZE_W // 2, FIELD_SIZE_H // 2)
        self.fruit = Fruit(*self.snake.get_pos())
        self.screen = pygame.Surface((WIDTH / 2, HEIGHT - BAR_HEIGHT))
        self.interf = pygame.Surface((WIDTH / 2, BAR_HEIGHT))

    def update(self):
        self.snake.move(self.fruit.get_pos())

    def new_fruit(self):
        self.fruit = Fruit(*self.snake.get_pos())



class Game():
    def __init__(self):
        self.clock = pygame.time.Clock()
        self.display = pygame.display.set_mode((WIDTH, HEIGHT))
        self.mainloop()
        self.GAME_RUNNING = True
        #self.start_menu()

    def start_menu(self):
        pass

    def mainloop(self):
        self.game_fields = []
        self.game_fields.append(Game_field())
        while self.GAME_RUNNING:
            self.clock.tick(FPS)
            self.display.fill((0, 0, 0))
            self.keys_loop()
            self.display.blit(draw_field(self.screen, ), (0, BAR_HEIGHT))
            self.display.blit(draw_interface(self.interf, ), (0, 0))
            pygame.display.flip()

    def keys_loop(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.GAME_RUNNUNG = False 
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    pause = True
                    while pause:
                        self.clock.tick(FPS)
                        for eventpause in pygame.event.get():
                            if eventpause.type == pygame.KEYDOWN:
                                if eventpause.key == pygame.K_p:
                                    pause = False
                            if eventpause.type == pygame.QUIT:
                                self.GAME_RUNNUNG = False 
                                pause = False
                if event.key == pygame.K_UP:
                    pass



def main():
    Game()

if __name__ == "__main__":
    pygame.init()
    main()
    pygame.quit()