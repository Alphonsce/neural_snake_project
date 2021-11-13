from AI_constans import *
import numpy as np
import pygame
from enum import Enum
from collections import namedtuple
import random


class Fruit:
    def __init__(self, snakepose, snakehead):
        not_founded = True
        while not_founded:
            not_founded = False
            self.pos = (random.randint(0, FIELD_SIZE_W - 1), random.randint(0, FIELD_SIZE_H - 1))
            for item in snakepose:
                if snakepose == self.pos:
                    not_founded = True
            if snakehead == self.pos:
                not_founded = True
    
    def get_pos(self):
        return self.pos

class Snake:
    def __init__(self, x, y, gamefield):
        self.tail = [(x-1, y), (x-2, y)]
        self.head = (x, y)
        self.speed = (1, 0)
        self.new_speed = (1, 0)
        self.alive = True
        self.step = 0
        self.gamefield = gamefield

    def move(self, fruit):
        """ Отвечает за перемещение змеи
        fruit - положение фрукта на поле
        """
        if self.alive:
            self.step += 1
        if self.step >= FRAMES_PER_STEP:
            self.step = 0
            x, y = self.head 
            Vx, Vy = self.speed
            if not(0 <= (x + Vx) < FIELD_SIZE_W and 0 <= (y + Vy) < FIELD_SIZE_H):
                self.speed = (0, 0)
                self.alive = False
            else:
                for part in self.tail[1:]:
                    if part == (x + Vx, y + Vy):
                        self.speed = (0, 0)
                        self.alive = False
                if self.alive:
                    if fruit != (x + Vx, y + Vy):
                        self.tail.pop(0)
                    else:
                        self.gamefield.new_fruit()
                    self.tail.append(self.head)
                    self.head = (x + Vx, y + Vy)
                    if self.new_speed != (-Vx, -Vy):
                        self.speed = self.new_speed
                
    def up(self):
        self.new_speed = (0, -1)

    def down(self):
        self.new_speed = (0, 1)

    def left(self):
        self.new_speed = (-1, 0)
            
    def right(self):
        self.new_speed = (1, 0)

    def get_pos(self):
        """ Возвращает положения частей хвоста и головы"""
        return (self.tail, self.head)

    def get_step(self):
        return self.step


def draw_field(surf, snake_tail, snake_head, fruit, step):
    """ Функция рисует поле.
    Первоначльно она должна нарисовать темное поле
    Исходя из массива надо нарисовать квадратики в клеточках: 
    surf - Поле на котором надо нарисовать.
    cells - массив чисел. Соответствия устанавливаются с помощью 
    класса Cell в модуле constans
    Фрукт - красный (занимает 80% ширины и высоты клетки)
    Змея - зеленая (занимает 80% ширины и высоты клетки)
    Голова - Зеленая (занимает 100% ширины и высоты клетки)
    Также для каждой части змеи надо сделать соединение между двумя клеточками -
    Салатовая, например(занимает 80% ширины или высоты клетки)
    """
    (x_0, y_0) = fruit
    x_0 *= CELL_SIDE
    y_0 *= CELL_SIDE
    pygame.draw.rect(surf, RED, (x_0, y_0, CELL_SIDE, CELL_SIDE))
    k = 0.5 * (1 - WIDTH_OF_TAIL)
    (x_0, y_0) = snake_head
    (x, y) = snake_tail[-1]
    x_0 += step / FRAMES_PER_STEP * (x_0 - x)
    y_0 += step / FRAMES_PER_STEP * (y_0 - y)
    pygame.draw.rect(surf, BLUE, (int(x_0 * CELL_SIDE), int(y_0 * CELL_SIDE), CELL_SIDE, CELL_SIDE))
    for i in range(len(snake_tail) - 1):
        (x, y) = snake_tail[-i - 1]
        pygame.draw.rect(surf, SNAKE_COLORS[i % len(SNAKE_COLORS)], (
            int((min(x, x_0) + k) * CELL_SIDE),
            int((min(y, y_0) + k) * CELL_SIDE),
            int(CELL_SIDE * (1 + abs(x - x_0) - 2 * k)),
            int(CELL_SIDE * (1 + abs(y - y_0) - 2 * k))
            ))

        (x_0, y_0) = (x, y)
    (x, y) = snake_tail[0]
    x += step / FRAMES_PER_STEP * (x_0 - x)
    y += step / FRAMES_PER_STEP * (y_0 - y)
    pygame.draw.rect(surf, SNAKE_COLORS[i % len(SNAKE_COLORS)], (
        int((min(x, x_0) + k) * CELL_SIDE),
        int((min(y, y_0) + k) * CELL_SIDE),
        int(CELL_SIDE * (1 + abs(x - x_0) - 2 * k)),
        int(CELL_SIDE * (1 + abs(y - y_0) - 2 * k))
        ))
    return surf

def draw_interface(surf, score):
    """ Полоса в верху экрана, на которой выводится счет"""
    pass #FIXME
    return surf

def draw_text(text, size, x, y, colour, surf):
    """ Функция располагает текст на заданном холсте
    ОПОРНОЙ ТОЧКОЙ ЯВЛЯЕТСЯ СЕРЕДИНА ВЕРХА ТЕКСТА
    text: строка, вывод которой предполагается
    size: размер шрифта в пикселях
    x, y: положение опорной точки текста
    colour: цвет текста
    surf: холст, на который пишется
    """
    font = pygame.font.SysFont(TEXT_FONT, size)
    text_surface = font.render(text, True, colour)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)


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
        self.interf.fill((0, 0, 0))
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
        self.display = pygame.display.set_mode((2 * WIDTH, HEIGHT))
        self.GAME_RUNNING = True

    def start_menu(self):
        self.mainloop(["gamer"])

    def mainloop(self, fields):
        self.gamer = None
        self.game_fields = []
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


def main():
    Game().start_menu()

if __name__ == "__main__":
    pygame.init()
    main()
    pygame.quit()