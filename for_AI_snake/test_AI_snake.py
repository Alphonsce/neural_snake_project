from AI_constans import *
import numpy as np
import pygame
from enum import Enum
from collections import namedtuple
import random
from human_snake import draw_field

# вместо is_collision я могу использовать game_field.snake.alive
# [straight, right, left]
# внутри AI_Game я сделаю другой метод, который будет из action делать direction и потом просто вызывать move(direction)

class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4

class Fruit:
    def __init__(self, snakepose, snakehead):
        not_founded = True
        while not_founded:
            not_founded = False
            self.pos = (random.randint(0, FIELD_SIZE_W - 1), random.randint(0, FIELD_SIZE_H - 1))
            for item in snakepose:
                if item == self.pos:
                    not_founded = True
            if snakehead == self.pos:
                not_founded = True
                

class Snake:
    def __init__(self, x, y, gamefield):
        self.tail = [(x - 1, y), (x - 2, y)]
        self.head = (x, y)
        self.speed = (1, 0)
        self.alive = True
        self.step = 0
        self.gamefield = gamefield
        self.speed_from_direction = {
            Direction.RIGHT: (1, 0),
            Direction.DOWN: (0, 1),
            Direction.LEFT: (-1, 0),
            Direction.UP: (0, -1)
            }
        self.direction = Direction.RIGHT
        self.new_direction = Direction.RIGHT

    def move(self, fruit_coords, direction):
        """ Отвечает за перемещение змеи
        fruit_coords - положение фрукта на поле

        Суть теперь в том, чтобы здесь делать движиние по direction,
        который мы получаем из action при помощи метода в классе AI_Game
        """
        direction = self.direction # временно!

        if self.alive:
            self.step += 1
        if self.step >= FRAMES_PER_STEP:
            self.step = 0
            x, y = self.head 
            Vx, Vy = self.speed_from_direction[direction]
            if not(0 <= (x + Vx) < FIELD_SIZE_W and 0 <= (y + Vy) < FIELD_SIZE_H):
                self.speed = (0, 0)
                self.alive = False
            else:
                for part in self.tail[1:]:
                    if part == (x + Vx, y + Vy):
                        self.speed = (0, 0)
                        self.alive = False
                if self.alive:
                    if fruit_coords != (x + Vx, y + Vy):
                        self.tail.pop(0)
                    else:
                        self.gamefield.new_fruit()
                    self.tail.append(self.head)
                    self.head = (x + Vx, y + Vy)

    def get_pos(self):
        """ Возвращает положения частей хвоста и головы"""
        return (self.tail, self.head)

    def get_step(self):
        return self.step


class AI_Game:
    def __init__(self):
        self.clock = pygame.time.Clock()
        self.display = pygame.display.set_mode((WIDTH, HEIGHT))
        # field init:
        self.reset()

    def reset(self):
        '''здесь находятся все параметры для инициализации игры заново'''
        self.frame_number = 0
        self.score = 0
        self.snake = Snake(FIELD_SIZE_W // 2, FIELD_SIZE_H // 2, self)
        self.fruit = Fruit(*self.snake.get_pos())
        self.screen = pygame.Surface((WIDTH, HEIGHT - BAR_HEIGHT))


    def update_drawing(self):
        self.screen.fill((0, 0, 0))
        self.screen.blit(draw_field(
            self.screen, *self.snake.get_pos(), 
            self.fruit.pos, self.snake.get_step()
            ), (0, 0))

    def direction_from_action(self, action):
        '''в конце будет return direction
        потом self.snake.move(direction_from_action(action))
        
        '''
        pass

    def new_fruit(self):
        self.fruit = Fruit(*self.snake.get_pos())
        self.score += 1

    def snake_down(self):
        self.snake.direction = Direction.DOWN

    def snake_up(self):
        self.snake.direction = Direction.UP

    def snake_left(self):
        self.snake.direction = Direction.LEFT

    def snake_right(self):
        self.snake.direction = Direction.RIGHT

    def mainloop_step(self, action=[1, 0, 0]):
        '''Теперь предсказанный action передается сюда,
        затем он передается в move, а потом исходя из action, 
        смотрится direction и выбирается скорость и змейка смещается
        '''
        #print(self.snake.direction)
        self.frame_number += 1

        self.clock.tick(FPS)
        self.display.fill((0, 0, 0))
        self.update_drawing()
        self.snake.move(self.fruit.pos, action)
        self.display.blit(self.screen, (0, BAR_HEIGHT))
        pygame.display.flip()
        for event in pygame.event.get():
            self.frame_number += 1
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            # для теста:
            # if event.type == pygame.KEYDOWN:
            #     if event.key == pygame.K_UP:
            #         self.snake_up()
            #     if event.key == pygame.K_DOWN:
            #         self.snake_down()
            #     if event.key == pygame.K_LEFT:
            #         self.snake_left()                        
            #     if event.key == pygame.K_RIGHT:
            #         self.snake_right()

def main():
    aigame = AI_Game()
    while True:
        aigame.mainloop_step()

        if not aigame.snake.alive:
            print(aigame.score)
            #aigame.reset()
            break


if __name__ == "__main__":
    pygame.init()
    main()
