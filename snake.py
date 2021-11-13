import numpy
import pygame
from pygame import display


from model import *
from graphics import *
from constans import *


class Game_field:
    def __init__(self, x):
        self.score = 0
        self.snake = Snake(FIELD_SIZE_W // 2, FIELD_SIZE_H // 2, self)
        self.fruit = Fruit(*self.snake.get_pos())
        self.screen = pygame.Surface((WIDTH, HEIGHT - BAR_HEIGHT))
        self.interf = pygame.Surface((WIDTH, BAR_HEIGHT))
        self.x = x

    def update(self):
        self.snake.move(self.fruit.get_pos())
        self.screen.fill((0, 0, 0))
        self.screen.blit(draw_field(
            self.screen, *self.snake.get_pos(), 
            self.fruit.get_pos(), self.snake.get_step()
            ), (0, 0))
        self.interf.fill((90, 90, 90))
        self.interf.blit(draw_interface(self.interf, self.score), (0, 0))

    def new_fruit(self):
        self.fruit = Fruit(*self.snake.get_pos())

    def snake_down(self):
        self.snake.down()

    def snake_up(self):
        self.snake.up()

    def snake_left(self):
        self.snake.left()

    def snake_right(self):
        self.snake.right()


class Game:
    def __init__(self):
        self.clock = pygame.time.Clock()
        self.display = pygame.display.set_mode((WIDTH, HEIGHT))
        self.GAME_RUNNING = True

    def start_menu(self):
        self.menu = True
        menu_buttons = []
        menu_buttons.append(Button("Player only", 200, 300, 200, 50))
        menu_buttons.append(Button("AI only", 200, 400, 200, 50))
        menu_buttons.append(Button("AI VS Player", 200, 500, 200, 50))
        menu_buttons.append(Button("EXIT", 200, 600, 200, 50))
        while self.menu:
            x, y = pygame.mouse.get_pos()
            self.clock.tick(FPS)
            self.display.fill((0, 0, 0))
            click = self.keys_menu()
            for i in range(len(menu_buttons)):
                if menu_buttons[i].check_pressed(x, y) and click:
                    print(0)
                    self.menu = False
                    if i == 0:
                        self.mainloop(["gamer"])
                    if i == 1:
                        self.mainloop(["AI"])
                    if i == 2:
                        self.mainloop(["AI", "gamer"])
                    if i == 3:
                        self.GAME_RUNNING = False   
            draw_start_menu(menu_buttons)
            pygame.display.flip()

    def mainloop(self, fields):
        self.gamer = None
        self.game_fields = []
        pygame.display.quit()
        self.display = pygame.display.set_mode((len(fields) * WIDTH, HEIGHT))
        for i in range(len(fields)):
            game_field = Game_field(i * WIDTH)
            self.game_fields.append(game_field)
            if fields[i] == "gamer":
                self.gamer = game_field
        while self.GAME_RUNNING:
            self.clock.tick(FPS)
            self.display.fill((0, 0, 0))
            self.keys_loop()
            for field in self.game_fields:
                field.update()
                self.display.blit(field.screen, (field.x, BAR_HEIGHT))
                self.display.blit(field.interf, (field.x, 0))
            pygame.display.flip()

    def keys_loop(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.GAME_RUNNING = False 
                self.menu = False
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
                                self.GAME_RUNNING = False 
                                pause = False
                if self.gamer != None:
                    if event.key == pygame.K_UP:
                        self.gamer.snake_up()
                    if event.key == pygame.K_DOWN:
                        self.gamer.snake_down()
                    if event.key == pygame.K_LEFT:
                        self.gamer.snake_left()                        
                    if event.key == pygame.K_RIGHT:
                        self.gamer.snake_right()

    def keys_menu(self):
        click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.GAME_RUNNING = False 
                self.menu = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
        return click


def main():
    Game().start_menu()

if __name__ == "__main__":
    pygame.init()
    main()
    pygame.quit()